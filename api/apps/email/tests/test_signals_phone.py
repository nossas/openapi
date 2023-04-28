import pytest
import requests_mock
from model_bakery import baker

from apps.actionnetwork.models import (
    ActionGroup,
    Campaign,
    Integration,
    IntegrationOptions,
    EmailTemplate,
    EmailTemplateOptions,
)
from apps.phone.models import PhonePressure


@pytest.fixture
def campaign(db, requests_mock):
    action_group = baker.make(ActionGroup)
    action_group.integration_set.set(
        [
            baker.make(
                Integration,
                name=IntegrationOptions.SENDGRID,
                config={"API_KEY": "test-api-key"},
            )
        ]
    )
    campaign = baker.make(
        Campaign,
        resource_name="form",
        an_response_json={"_links": {"self": {"href": "http://localhost"}}},
        # tags=tags,
        action_group=action_group,
        make_m2m=True,
    )

    baker.make(
        EmailTemplate, campaign=campaign, email_type=EmailTemplateOptions.POST_ACTION
    )

    requests_mock.post("http://localhost/outreaches", status_code=200, json={})

    return campaign


@pytest.fixture
def spy_mail_client(mocker):
    from apps.email.clients import SendGridEmailClient

    mocker.patch("python_http_client.Client")

    return mocker.spy(SendGridEmailClient, "send_mail")


def test_call_post_email_message_phone_create(db, campaign, spy_mail_client):
    PhonePressure.objects.create(
        campaign=campaign, given_name="Test", email_address="test@domain.local"
    )

    assert spy_mail_client.call_count == 1


def test_call_post_email_message_only_when_phone_create(db, campaign, spy_mail_client):
    instance = PhonePressure.objects.create(
        campaign=campaign, given_name="Test", email_address="test@domain.local"
    )

    campaign2 = baker.make(Campaign)
    instance.campaign = campaign2
    instance.save()

    assert spy_mail_client.call_count == 1


def test_call_post_email_message_only_action_group_sendgrid_integration(
    db, campaign, spy_mail_client
):
    campaign.action_group.integration_set.all().delete()

    PhonePressure.objects.create(
        campaign=campaign, given_name="Test", email_address="test@domain.local"
    )

    assert spy_mail_client.call_count == 0


# def test_send_mail_with_campaign_settings(db, campaign, spy_mail_client):
#     person_email_address = "test@domain.local"
#     email_template_mock = campaign.emailtemplate_set.filter(
#         email_type=EmailTemplateOptions.POST_ACTION
#     ).first()

#     PhonePressure.objects.create(
#         campaign=campaign, given_name="Test", email_address=person_email_address
#     )

#     assert spy_mail_client.assert_called_once_with(
#         to_email=person_email_address,
#         from_email=f"{email_template_mock.from_name} <{email_template_mock.from_email}>",
#         subject=email_template_mock.subject,
#         content=email_template_mock.content,
#     )
