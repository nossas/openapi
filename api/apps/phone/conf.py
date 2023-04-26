from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from appconf import AppConf


class PhoneConf(AppConf):
    # ACCOUNT_SID = None
    # AUTH_TOKEN = None
    # PHONE_NUMBER = None
    WEBHOOK_URL = None

    class Meta:
        prefix = 'twilio'

