from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from appconf import AppConf


class ZendeskConf(AppConf):
    GROUPMODEL = None

    class Meta:
        prefix = "actionnetwork"

    def configure_groupmodel(self, value):
        if not value:
            raise ImproperlyConfigured(
                "Requested setting ACTIONNETWORK_GROUPMODEL, but settings are not configured"
            )
        return value
