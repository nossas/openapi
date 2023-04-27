import pytest
import json

from rest_framework.test import APIClient
from model_bakery import baker

from apps.actionnetwork.models import ActionGroup, Campaign, TargetGroup
from apps.actionnetwork.serializers import CampaignSerializer


client = APIClient()


def test_campaigns_details_targets(db):
    action_group = baker.make(ActionGroup)
    target_group = baker.make(TargetGroup, make_m2m=True)
    campaign = baker.make(
        Campaign,
        action_group=action_group,
        resource_name="advocacy_campaigns",
        target_groups=[target_group],
        make_m2m=True,
    )
    # campaign.target_groups.set(target_group)

    response = client.get(
        f"/api/campaigns/{campaign.id}/",
        headers={"OpenAPI-Token": action_group.openapi_token},
    )

    result = response.json()
    serializer = CampaignSerializer(campaign)

    assert result == serializer.data
