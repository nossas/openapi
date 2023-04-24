from rest_framework import authentication, exceptions

from .models import UsersGroup


class UsersGroupAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_token = request.headers.get('OpenAPI-Token')

        if auth_token and request.method == 'POST':
            request.openapi_group = UsersGroup.objects.get(token=auth_token)
            return (None, None)
        elif request.method != 'POST':
            raise exceptions.AuthenticationFailed('POST only permitted used OpenAPIToken')
