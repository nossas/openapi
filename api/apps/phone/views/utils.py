from django.urls import reverse

from twilio.rest import Client

from ..conf import settings
from ..models import Call


client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def create_twilio_call(call_from, call_to, endpoint):
    """
    Create and register a Twilio call
    """

    call = Call.objects.create(
        status="created", from_number=call_from, to_number=call_to
    )

    url_fowarding = (
        f"{endpoint}{reverse('call_fowarding', kwargs={'call_id': call.id})}"
    )

    url_tracking = f"{endpoint}{reverse('call_tracking', kwargs={'call_id': call.id})}"

    twilio_call = client.calls.create(
        url=url_fowarding,
        to=call_from,
        from_=settings.TWILIO_PHONE_NUMBER,
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
        "url": f"{endpoint}{reverse('call_status', kwargs={'call_id': call.id})}",
    }
