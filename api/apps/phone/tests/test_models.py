import pytest
import requests_mock

from model_bakery import baker

from apps.actionnetwork.models import Campaign
from apps.actionnetwork.models.campaigns import ActionRecordManager
from apps.phone.models import PhonePressure


def test_create_person_postal_address(db, requests_mock):
    campaign = baker.make(
        Campaign,
        resource_name="form",
        an_response_json={"_links": {"self": {"href": "http://localhost"}}},
    )

    requests_mock.post("http://localhost/outreaches", status_code=200, json={})

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