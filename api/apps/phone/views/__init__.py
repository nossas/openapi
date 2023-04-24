from rest_framework import status
from rest_framework.response import Response

from apps.actionnetwork.views import ActionCreateApiView
from apps.actionnetwork.serializers import ActionSerializerMixin

from ..models import PhonePressure
from ..conf import settings
from .utils import create_twilio_call


class PhonePressureSerializer(ActionSerializerMixin):
    class Meta(ActionSerializerMixin.Meta):
        model = PhonePressure


class PhonePressureCreateAPIView(ActionCreateApiView):
    serializer_class = PhonePressureSerializer

    def post_create(self, instance, request, headers):
        call = create_twilio_call(
            call_from=instance.person.phone_numbers.first().number,
            call_to=instance.targets.first().phone_number,
            endpoint=settings.TWILIO_WEBHOOK_URL
        )

        return Response(
            {"action_id": instance.id, "url": call["url"]},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )