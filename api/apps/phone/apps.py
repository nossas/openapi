from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PhoneConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.phone"
    label = "phone"