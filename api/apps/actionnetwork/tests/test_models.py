import pytest

import requests_mock
from model_bakery import baker
from django.conf import settings

from apps.actionnetwork.models import (
    Campaign,
    Person,
    ActionRecordModel,
    ActionRecordManager,
)
from apps.actionnetwork.exceptions import InvalidRequestAPIException


def test_save_response_json_when_create_campaign(db):
    action_group = baker.make(settings.ACTIONNETWORK_GROUPMODEL)
    params = {
        "title": "Campaign #1",
        "action_group": action_group,
        "resource_name": "forms",
    }

    with requests_mock.mock() as m:
        m.post(
            f"https://actionnetwork.org/api/v2/{params['resource_name']}/",
            status_code=200,
            json={"title": params["title"]},
        )

        campaign = Campaign.objects.create(**params)

        assert m.called is True
        assert m.last_request.headers["OSDI-API-Token"] == action_group.api_secret_key

        assert campaign.api_response_json["title"] == campaign.title


def test_not_create_campaign_and_raise_exception(db):
    action_group = baker.make(settings.ACTIONNETWORK_GROUPMODEL)
    params = {
        "title": "Campaign #1",
        "action_group": action_group,
        "resource_name": "forms",
    }

    with requests_mock.mock() as m:
        m.post(
            f"https://actionnetwork.org/api/v2/{params['resource_name']}/",
            status_code=500,
            json={"title": params["title"]},
        )

        with pytest.raises(InvalidRequestAPIException):
            Campaign.objects.create(**params)


def test_campaign_get_endpoint(db):
    expected_value = "http://"
    campaign = baker.make(
        Campaign, api_response_json={"_links": {"self": {"href": expected_value}}}
    )

    assert campaign.get_endpoint() == expected_value


def test_campaign_get_url_type(db):
    expected_value = "forms"
    campaign = baker.make(Campaign, resource_name=expected_value)
    assert campaign.get_url_type() == expected_value

    expected_value = "donations"
    campaign.resource_name = "fundraising_pages"
    assert campaign.get_url_type() == expected_value

    expected_value = "email_pressures"
    campaign.resource_name = "petitions"
    assert campaign.get_url_type() == expected_value


def test_campaign_str(db):
    campaign = baker.make(Campaign)

    assert str(campaign) == campaign.title


def test_person_str(db):
    kwargs = dict(given_name="Test", family_name="Test")
    person = baker.make(Person, **kwargs)

    assert (
        str(person)
        == person.full_name()
        == f"{kwargs['given_name']} {kwargs['family_name']}"
    )


# def test_action_record_model_objects(db):

#     class Inherit(ActionRecordModel):
#         pass

#     assert isinstance(Inherit.objects, ActionRecordManager)


# def test_action_record_model_uuid(db):

#     class Inherit(ActionRecordModel):
#         pass

#     expected_value = "1234-5678"
#     action = baker.make(Inherit, api_response_json={
#         "identifiers": [
#             f"action_network:{expected_value}"
#         ]
#     })

#     assert action.uuid() == expected_value
