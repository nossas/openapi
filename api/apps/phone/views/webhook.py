# from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response


from twilio.twiml.voice_response import VoiceResponse

# from bonde.openapi.actions.views import ActionCreateApiView, ActionSerializerMixin

from ..models import Call


@csrf_exempt
def fowarding(request, call_id):
    call = Call.objects.get(pk=call_id)
    twilio_call = request.POST

    voice_response = VoiceResponse()
    dial = voice_response.dial(caller_id=twilio_call["Caller"])

    url_tracking = (
        f"{reverse('call_tracking', kwargs={'call_id': call.id}, request=request)}"
    )

    dial.number(
        phone_number=call.to_number,
        status_callback=url_tracking,
        status_callback_method="POST",
        status_callback_event="initiated ringing answered completed",
    )

    return HttpResponse(str(voice_response), content_type="application/xml")


@api_view(["POST"])
def tracking(request, call_id):
    call = Call.objects.get(pk=call_id)
    twilio_call = request.data

    call.sid = twilio_call["CallSid"]
    call.status = twilio_call["CallStatus"]
    call.save()

    return Response(
        {
            "sid": call.sid,
            "status": call.status,
            "url": reverse("call_status", kwargs={"call_id": call.id}, request=request),
        }
    )


@api_view(["GET"])
def check_status(request, call_id):
    call = Call.objects.get(pk=call_id)
    return Response(
        {
            "sid": call.sid,
            "status": call.status,
            "url": reverse("call_status", kwargs={"call_id": call.id}, request=request),
        }
    )
