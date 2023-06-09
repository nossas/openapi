import requests
import json

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from ..exceptions import (
    InvalidRequestAPIException,
    InvalidInstanceModelException,
    FieldException,
)

from .peoples import Person, EmailAddress, PhoneNumber, PostalAddress
from .details import ActionGroup, TargetGroup, Tag


class CampaignManager(models.Manager):
    def create(self, **kwargs):
        title = kwargs.get("title")
        resource_name = kwargs.get("resource_name")
        action_group = kwargs.get("action_group")

        # Request for Action Network API
        response = requests.post(
            f"https://actionnetwork.org/api/v2/{resource_name}/",
            data={"title": title, "origin_system": "Bonde"},
            headers={"OSDI-API-Token": action_group.an_secret_key},
        )

        if response.status_code == 200:
            # Save on database Campaign model with response
            return super(CampaignManager, self).create(
                title=title,
                resource_name=resource_name,
                action_group=action_group,
                an_response_json=response.json(),
            )

        raise InvalidRequestAPIException(response.text)


class CampaignOptions(models.TextChoices):
    SUBMISSIONS = "forms", _("Formulário")
    DONATIONS = "fundraising_pages", _("Doação")
    SIGNATURES = "petitions", _("Petição")
    OUTREACHES = "advocacy_campaigns", _("Pressão")


class Campaign(models.Model):
    title = models.CharField(verbose_name=_("nome da campanha"), max_length=200)

    resource_name = models.CharField(
        verbose_name=_("tipo de campanha"),
        max_length=50,
        choices=CampaignOptions.choices,
    )

    an_response_json = models.JSONField(verbose_name=_("resposta da action network"))

    action_group = models.ForeignKey(ActionGroup, on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag, blank=True)

    # Used only advocacy campaigns
    target_groups = models.ManyToManyField(TargetGroup, blank=True)

    objects = CampaignManager()

    class Meta:
        verbose_name = _("campanha")
        verbose_name_plural = _("campanhas")

    def __str__(self):
        return self.title

    def get_endpoint(self):
        return self.an_response_json["_links"]["self"]["href"]


class EmailTemplateOptions(models.TextChoices):
    POST_ACTION = "post_action", _("Pós ação")


class EmailTemplate(models.Model):
    email_type = models.CharField(
        verbose_name=_("tipo de email"),
        max_length=30,
        default=EmailTemplateOptions.POST_ACTION,
        choices=EmailTemplateOptions.choices,
    )
    from_name = models.CharField(verbose_name=_("nome do remetente"), max_length=20)
    from_email = models.EmailField(verbose_name=_("email do remetente"))
    subject = models.CharField(verbose_name=_("assunto"), max_length=40)
    content = models.TextField(verbose_name="conteúdo")

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)


class ActionRecordManager(models.Manager):
    def create(self, campaign, **kwargs):
        # Raise Incorrect Action Model
        if (
            self.model.__name__ == "Donation"
            and campaign.resource_name != "fundraising_pages"
        ):
            raise InvalidInstanceModelException(
                "Donation model request fundraising_pages campaign"
            )

        if self.model.__name__ == "Submission" and campaign.resource_name != "form":
            raise InvalidInstanceModelException(
                "Submission model request forms campaign"
            )

        if self.model.__name__ == "Signature" and campaign.resource_name != "petitions":
            raise InvalidInstanceModelException(
                "Signature model request petitions campaign"
            )

        if (
            self.model.__name__ == "Outreach"
            and campaign.resource_name != "advocacy_campaigns"
        ):
            raise InvalidInstanceModelException(
                "Outreach model request advocacy campaign"
            )

        # Instance of person
        person = kwargs.pop("person", None)

        # Fields to create or get person instance
        given_name = kwargs.pop("given_name", None)
        family_name = kwargs.pop("family_name", None)
        email_address = kwargs.pop("email_address", None)
        phone_number = kwargs.pop("phone_number", None)

        if not person and not email_address and not phone_number:
            raise FieldException("person or email_address or phone_number is required")

        elif not person and (email_address or phone_number):
            person = Person.objects.filter(
                Q(email_addresses__address=email_address)
                | Q(phone_numbers__number=phone_number)
            ).first()

        if not person:
            person = Person.objects.create(
                given_name=given_name, family_name=family_name
            )

            if email_address:
                EmailAddress.objects.create(address=email_address, person=person)

            if phone_number:
                PhoneNumber.objects.create(number=phone_number, person=person)

            postal_address = kwargs.pop("postal_address", None)
            if postal_address:
                PostalAddress.objects.create(**postal_address, person=person)
        else:
            if not person.email_addresses.filter(address=email_address).exists():
                EmailAddress.objects.create(address=email_address, person=person)

            if not person.phone_numbers.filter(number=phone_number).exists():
                PhoneNumber.objects.create(number=phone_number, person=person)

            postal_address = kwargs.pop("postal_address", None)
            if postal_address:
                PostalAddress.objects.create(**postal_address, person=person)

        if campaign.tags.exists():
            person.tags.set(campaign.tags.all())

        # TODO: Mudar forma alterar implementação a partir dos tipos de ação
        if self.__get_resource_name() == "donations":
            amount = kwargs.get("amount")
            created_date = kwargs.get("created_date")

            if not amount:
                raise FieldException("amount is required")

            if not created_date:
                raise FieldException("created_date is required")

            response = self.request_action_network_api(
                person=person,
                campaign=campaign,
                add_tags=[x.label for x in campaign.tags.all()],
                # remove_tags=remove_tags,
                # Params only used to donations
                recipients=[dict(display_name=campaign.title, amount=float(amount))],
                created_date=created_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
        else:
            response = self.request_action_network_api(
                person=person,
                campaign=campaign,
                add_tags=[x.label for x in campaign.tags.all()],
                # remove_tags=remove_tags,
            )

        # Call super create method for instance
        action = super(ActionRecordManager, self).create(
            person=person,
            campaign=campaign,
            an_response_json=response.json(),
            **kwargs,
        )

        return action

    def __get_resource_name(self):
        if issubclass(self.model, SubmissionInterface):
            return "submissions"
        elif issubclass(self.model, SignatureInterface):
            return "signatures"
        elif issubclass(self.model, DonationInterface):
            return "donations"
        elif issubclass(self.model, OutreachInterface):
            return "outreaches"
        else:
            raise InvalidInstanceModelException(
                f"{self.model.__name__} should be implement an interface"
            )

    def request_action_network_api(
        self, person, campaign, add_tags=[], remove_tags=[], **kwargs
    ):
        resource_name = self.__get_resource_name()
        endpoint = f"{campaign.get_endpoint()}/{resource_name}"

        payload = {
            "person": {
                "family_name": person.family_name,
                "given_name": person.given_name,
            },
            "add_tags": add_tags,
            "remove_tags": remove_tags,
        }

        email_addesses = person.email_addresses.all()
        if len(email_addesses) > 0:
            payload["person"]["email_addresses"] = list(
                map(lambda x: dict(address=x.address), email_addesses)
            )

        postal_addresses = person.postal_addresses.all()
        if len(postal_addresses) > 0:
            payload["person"]["postal_addresses"] = list(
                map(
                    lambda x: dict(postal_code=x.postal_code),
                    postal_addresses,
                )
            )

        phone_numbers = person.phone_numbers.all()
        if len(phone_numbers) > 0:
            payload["person"]["phone_numbers"] = list(
                map(lambda x: dict(number=x.number), phone_numbers)
            )

        custom_fields = person.custom_fields.all()
        if len(custom_fields) > 0:
            payload["person"]["custom_fields"] = {
                item.name: item.value for item in person.custom_fields.all()
            }

        payload.update(kwargs)

        response = requests.post(
            endpoint,
            data=json.dumps(payload),
            headers={
                "Content-Type": "application/json",
                "OSDI-API-Token": campaign.action_group.an_secret_key,
            },
        )

        if response.status_code == 200:
            return response

        raise InvalidRequestAPIException(response.text)


class ActionRecord(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    created_date = models.DateTimeField(
        verbose_name=_("data de criação"), default=timezone.now
    )

    # add_tags = ArrayField(models.CharField(verbose_name="Add tags", max_length=30))

    # remove_tags = ArrayField(models.CharField(verbose_name="Remove tags", max_length=30))

    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, verbose_name=_("campanha")
    )

    an_response_json = models.JSONField(verbose_name=_("resposta da action network"))

    class Meta:
        abstract = True

    objects = ActionRecordManager()

    def uuid(self):
        uuid_text = self.an_response_json["identifiers"][0]
        return uuid_text.replace("action_network:", "")


class SubmissionInterface(ActionRecord):
    class Meta:
        abstract = True


class SignatureInterface(ActionRecord):
    class Meta:
        abstract = True


class DonationInterface(ActionRecord):
    amount = models.DecimalField(
        verbose_name=_("valor"), decimal_places=2, max_digits=10
    )

    class Meta:
        abstract = True


class OutreachInterface(ActionRecord):
    class Meta:
        abstract = True
