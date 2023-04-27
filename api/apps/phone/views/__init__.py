from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from apps.actionnetwork.models import IntegrationOptions
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

    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)

        if not request.openapi_group.integration_set.filter(name=IntegrationOptions.TWILIO).exists():
            raise APIException(
                detail=f"Required setup a {IntegrationOptions.TWILIO} integration.",
                code=500
            )

    def post_create(self, instance, request, headers):
        call = create_twilio_call(
            # TODO: torna melhor a forma de escolher os numeros
            call_from=instance.person.phone_numbers.first().number,
            call_to=instance.targets.first().phone_number,
            endpoint=settings.TWILIO_WEBHOOK_URL,
            action_record=instance
        )

        response = Response(
            {"action_id": instance.id, "status": call["status"], "url": call["url"]},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

        return response
