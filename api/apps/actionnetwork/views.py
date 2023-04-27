from django.utils.timezone import now

from rest_framework import authentication, status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, CreateAPIView, ListAPIView, RetrieveAPIView

from apps.auth2.authentication import OpenAPIAuthentication
from apps.auth2.permissions import OpenAPIAuthenticated

from .models import Campaign
from .serializers import CampaignSerializer


class OpenAPIAuthMixin(object):
    authentication_classes = [
        OpenAPIAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [
        OpenAPIAuthenticated,
    ]


class ActionCreateApiView(OpenAPIAuthMixin, CreateAPIView):
    def validate(self, request):
        self.kwargs.update(
            {
                "campaign": get_object_or_404(
                    Campaign,
                    pk=self.kwargs.get("campaign_id"),
                    action_group=request.openapi_group,
                )
            }
        )

    def post_create(self, instance, request, headers):
        return Response(
            {"action_id": instance.id}, status=status.HTTP_201_CREATED, headers=headers
        )

    def create(self, request, *args, **kwargs):
        self.validate(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save(campaign=self.kwargs.get("campaign"))

        # TODO: padronizar resposta de ação
        headers = self.get_success_headers(request.data)

        return self.post_create(instance, request, headers)


class CampaignAPIListView(ListAPIView):
    """
    Documentando esse endpoint API
    """

    serializer_class = CampaignSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self, *args, **kwargs):
        queryset = Campaign.objects
        if not self.request.user.is_superuser:
            return queryset.filter(action_group__users__in=[self.request.user])

        return queryset.all()



class CampaignAPIDetailView(OpenAPIAuthMixin, RetrieveAPIView):
    """"""
    serializer_class = CampaignSerializer
    queryset = Campaign.objects