from rest_framework import authentication, exceptions

from apps.actionnetwork.models import ActionGroup


class OpenAPIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_token = request.headers.get('OpenAPI-Token')

        if auth_token:
            request.openapi_group = ActionGroup.objects.get(openapi_token=auth_token)
            return (None, None)
        
        raise exceptions.AuthenticationFailed(f'{request.method} only permitted used with OpenAPI-Token headers')
