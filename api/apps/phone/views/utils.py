from django.urls import reverse

from twilio.rest import Client
from apps.actionnetwork.models import IntegrationOptions

from ..models import Call


def create_twilio_call(call_from, call_to, endpoint, action_record):
    """
    Create and register a Twilio call
    """
    twilio_config = action_record.campaign.action_group.integration_set.filter(
        name=IntegrationOptions.TWILIO
    ).first()

    client = Client(twilio_config.get("ACCOUNT_SID"), twilio_config.get("AUTH_TOKEN"))

    call = Call.objects.create(
        status="created",
        from_number=call_from,
        to_number=call_to,
        phone_pressure=action_record,
    )

    url_fowarding = (
        f"{endpoint}{reverse('call_fowarding', kwargs={'call_id': call.id})}"
    )

    url_tracking = f"{endpoint}{reverse('call_tracking', kwargs={'call_id': call.id})}"

    twilio_call = client.calls.create(
        url=url_fowarding,
        to=call_from,
        from_=twilio_config.get("PHONE_NUMBER"),
        method="POST",
        # Callback configuration
        status_callback=url_tracking,
        status_callback_method="POST",
        status_callback_event=["initiated", "ringing", "answered", "completed"],
    )

    call.sid = twilio_call.sid
    call.status = twilio_call.status
    call.save()

    return {
        "sid": call.sid,
        "status": call.status,
        "url": reverse("call_status", kwargs={"call_id": call.id}),
    }
