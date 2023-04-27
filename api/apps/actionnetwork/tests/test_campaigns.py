import pytest
import requests_mock

from model_bakery import baker

from apps.actionnetwork.models import Campaign, Person, ActionGroup
from apps.actionnetwork.models.campaigns import ActionRecordManager, SubmissionInterface
from apps.actionnetwork.exceptions import InvalidRequestAPIException


def test_save_response_json_when_create_campaign(db):
    action_group = baker.make(ActionGroup)
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
        assert m.last_request.headers["OSDI-API-Token"] == action_group.an_secret_key

        assert campaign.an_response_json["title"] == campaign.title


def test_not_create_campaign_and_raise_exception(db):
    action_group = baker.make(ActionGroup)
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
        Campaign, an_response_json={"_links": {"self": {"href": expected_value}}}
    )

    assert campaign.get_endpoint() == expected_value


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
