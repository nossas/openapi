from rest_framework import status
from rest_framework.response import Response

from apps.actionnetwork.views import ActionCreateApiView
from apps.actionnetwork.serializers import ActionSerializerMixin

from ..models import PhonePressure
from .utils import create_twilio_call


ENDPOINT = "https://cede-2804-14d-c882-9ace-c345-e37f-35e1-a3f6.ngrok-free.app"


class PhonePressureSerializer(ActionSerializerMixin):
    class Meta(ActionSerializerMixin.Meta):
        model = PhonePressure


class PhonePressureCreateAPIView(ActionCreateApiView):
    serializer_class = PhonePressureSerializer

    def post_create(self, instance, request, headers):
        call = create_twilio_call(
            call_from=instance.person.phone_numbers.first().number,
            call_to=instance.targets.first().phone_number,
            endpoint=ENDPOINT
        )

        return Response(
            {"action_id": instance.id, "url": call["url"]},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )