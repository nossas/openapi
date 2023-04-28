from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

from .signals import post_action_record_email_message


class EmailConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.email"
    label = "email"
    
    def ready(self):
        """
        Responsável por conectar os signals aos modelos de todas as aplicações.
        Único local da aplicação que esses disparos devem ser utilizados
        """
        from apps.phone.models import PhonePressure

        post_save.connect(post_action_record_email_message, sender=PhonePressure)