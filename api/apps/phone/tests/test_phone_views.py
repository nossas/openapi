import pytest
import requests_mock

from rest_framework.test import APIClient
from model_bakery import baker

from apps.actionnetwork.models import (
    ActionGroup,
    Campaign,
    TargetGroup,
    Person,
    PhoneNumber,
    Integration,
    Target
)


client = APIClient()


def test_create_phone_view_twilio_not_setup(db):
    action_group = baker.make(ActionGroup)
    target_group = baker.make(TargetGroup, make_m2m=True)
    campaign = baker.make(
        Campaign,
        action_group=action_group,
        resource_name="advocacy_campaigns",
        target_groups=[target_group],
        make_m2m=True,
    )

    email = "test@domain.local"
    phone = "+5521999998888"
    payload = {
        "person": {"given_name": "Test", "phone_number": phone, "email_address": email},
        "targets": [1],
    }

    response = client.post(
        f"/api/campaigns/{campaign.id}/phone/",
        data=payload,
        headers={"OpenAPI-Token": action_group.openapi_token},
        format="json",
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "Required setup a twilio integration."}


@pytest.fixture
def prepare_campaign(db, requests_mock):
    action_group = baker.make(ActionGroup)
    baker.make(Integration, action_group=action_group, config={
        "AUTH_TOKEN": "x",
        "ACCOUNT_SID": "x",
        "PHONE_NUMBER": "+55999998888"
    })

    target = baker.make(Target, phone_number="+5591999998888")
    target_group = baker.make(TargetGroup, make_m2m=True, targets=[target])
    campaign = baker.make(
        Campaign,
        action_group=action_group,
        resource_name="advocacy_campaigns",
        target_groups=[target_group],
        make_m2m=True,
        an_response_json={"_links": {"self": {"href": "http://localhost"}}},
    )

    requests_mock.post("http://localhost/outreaches", status_code=200, json={})
    requests_mock.post("https://api.twilio.com/2010-04-01/Accounts/x/Calls.json", status_code=200, json={
        "status": "queued",
        "sid": "asdad"
    })

    def f():
      return campaign

    return f

def test_create_view_person_phone_and_email(db, prepare_campaign):
    campaign = prepare_campaign()
    
    email = "test@domain.local"
    phone = "+5521999998888"
    payload = {
        "person": {"given_name": "Test", "phone_number": phone, "email_address": email},
        "targets": [campaign.target_groups.first().targets.first().id],
    }

    client.post(
        f"/api/campaigns/{campaign.id}/phone/",
        data=payload,
        headers={"OpenAPI-Token": campaign.action_group.openapi_token},
        format="json",
    )

    person1 = Person.objects.filter(email_addresses__address=email).first()
    person2 = Person.objects.filter(phone_numbers__number=phone).first()

    assert person1 == person2


def test_create_view_person_exists_phone_and_email(db, prepare_campaign):
    campaign = prepare_campaign()
    phone = "+5521999998888"

    person_obj = baker.make(Person)
    baker.make(PhoneNumber, number=phone, person=person_obj)

    email = "test2@domain.local"
    payload = {
        "person": {"given_name": "Test", "phone_number": phone, "email_address": email},
        "targets": [1],
    }

    client.post(
        f"/api/campaigns/{campaign.id}/phone/",
        data=payload,
        headers={"OpenAPI-Token": campaign.action_group.openapi_token},
        format="json",
    )

    person1 = Person.objects.filter(email_addresses__address=email).first()
    person2 = Person.objects.filter(phone_numbers__number=phone).first()

    assert person1 == person2


def test_create_view_person_exists_phone_and_email_with_postal_address(db, prepare_campaign):
    campaign = prepare_campaign()
    phone = "+5521999998888"

    person_obj = baker.make(Person)
    baker.make(PhoneNumber, number=phone, person=person_obj)

    email = "test2@domain.local"
    payload = {
        "person": {
            "given_name": "Test",
            "phone_number": phone,
            "email_address": email,
            "postal_address": {
                "locality": "Belo Horizonte",
                "region": "MG"
            }

        },
        "targets": [1],
    }

    client.post(
        f"/api/campaigns/{campaign.id}/phone/",
        data=payload,
        headers={"OpenAPI-Token": campaign.action_group.openapi_token},
        format="json",
    )

    postal_address = Person.objects.filter(phone_numbers__number=phone).first().postal_addresses.first()

    assert postal_address.locality == "Belo Horizonte"
    assert postal_address.region == "MG"