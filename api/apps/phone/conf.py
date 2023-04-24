from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from appconf import AppConf


class ZendeskConf(AppConf):
    ACCOUNT_SID = None
    AUTH_TOKEN = None
    PHONE_NUMBER = None

    class Meta:
        prefix = 'twilio'

