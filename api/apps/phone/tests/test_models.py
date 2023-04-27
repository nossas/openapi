import pytest
import requests_mock

import requests

from model_bakery import baker

from apps.actionnetwork.models import ActionGroup, Campaign, Person, Tag
from apps.actionnetwork.models.campaigns import ActionRecordManager
from apps.phone.models import PhonePressure


@pytest.fixture
def campaign(db, requests_mock):
    action_group = baker.make(ActionGroup)
    tags = baker.make(Tag, action_group=action_group, _quantity=3)
    campaign = baker.make(
        Campaign,
        resource_name="form",
        an_response_json={"_links": {"self": {"href": "http://localhost"}}},
        tags=tags,
        action_group=action_group,
        make_m2m=True
    )

    requests_mock.post("http://localhost/outreaches", status_code=200, json={})

    return campaign


def test_create_person_postal_address(db, campaign):
    objects = ActionRecordManager()
    objects.model = PhonePressure

    expected_value = {
        "address_lines": "Rua X",
        "locality": "Rio de Janeiro",
        "region": "RJ",
        "postal_code": "123456789",
        "country": "BR",
    }

    kwargs = {
        "given_name": "Test",
        "phone_number": "+5521999998888",
        "postal_address": expected_value,
    }

    instance = objects.create(campaign=campaign, **kwargs)

    postal_address = instance.person.postal_addresses.first()

    assert postal_address.address_lines == expected_value["address_lines"]
    assert postal_address.locality == expected_value["locality"]
    assert postal_address.region == expected_value["region"]
    assert postal_address.postal_code == expected_value["postal_code"]
    assert postal_address.country == expected_value["country"]


def test_create_person_phone_and_email(db, campaign):
    objects = ActionRecordManager()
    objects.model = PhonePressure

    email = "test@domain.local"
    phone = "+5521999998888"

    kwargs = {
        "given_name": "Test",
        "phone_number": phone,
        "email_address": email
    }

    instance = objects.create(campaign=campaign, **kwargs)

    person1 = Person.objects.filter(email_addresses__address=email).first()
    person2 = Person.objects.filter(phone_numbers__number=phone).first()

    assert instance.person == person1
    assert instance.person == person2


def test_add_person_tags_when_campaign_relationship(db, campaign):
    objects = ActionRecordManager()
    objects.model = PhonePressure

    kwargs = {
        "given_name": "Test",
        "email_address": "test@domain.local"
    }

    instance = objects.create(campaign=campaign, **kwargs)

    assert list(instance.person.tags.all()) == list(campaign.tags.all())


def test_add_request_tags_when_campaign_relationship(db, campaign, mocker):
    objects = ActionRecordManager()
    objects.model = PhonePressure

    kwargs = {
        "given_name": "Test",
        "email_address": "test@domain.local"
    }
    spy = mocker.spy(ActionRecordManager, "request_action_network_api")

    instance = objects.create(campaign=campaign, **kwargs)

    spy.assert_called_once_with(
        objects,
        person=instance.person,
        campaign=instance.campaign,
        add_tags=[x.label for x in instance.campaign.tags.all()]
    )