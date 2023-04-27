import uuid

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ActionGroup(models.Model):
    name = models.CharField(verbose_name=_("nome do grupo"), max_length=150)

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("mobilizadores"), blank=True
    )

    # Access Action Network API
    an_secret_key = models.CharField(
        verbose_name=_("chave secreta da API"),
        help_text=_("chave secreta do seu grupo na API da Action Network"),
        max_length=200,
    )
    # Used on autenticate OpenAPI
    openapi_token = models.CharField(
        verbose_name=_("token de autenticação"),
        help_text=_("Usado para fazer autenticação dos recursos na OpenAPI"),
        max_length=85,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("criado por"),
        on_delete=models.CASCADE,
        related_name="action_group",
    )

    class Meta:
        verbose_name = _("comunidade")
        verbose_name_plural = _("comunidades")

    def __str__(self):
        return self.name


class IntegrationOptions(models.TextChoices):
    TWILIO = "twilio", "Twilio"

class Integration(models.Model):
    name = models.CharField(verbose_name=_("nome da integração"), max_length=100, choices=IntegrationOptions.choices)
    config = models.JSONField(verbose_name=_("configuração"))
    action_group = models.ForeignKey(ActionGroup, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("integração")
        verbose_name_plural = _("integrações")
    

    def get(self, config_name, default_value=None):
        if config_name in self.config:
            return self.config[config_name]
        
        return default_value


class Target(models.Model):
    name = models.CharField(verbose_name=_("nome"), max_length=100)
    email_address = models.CharField(
        verbose_name=_("endereço de email"), max_length=100, null=True, blank=True
    )
    phone_number = models.CharField(
        verbose_name=_("telefone"), max_length=25, null=True, blank=True
    )

    action_group = models.ForeignKey(ActionGroup, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("alvo")
        verbose_name_plural = _("alvos")
    
    def __str__(self):
        return self.name


class TargetGroup(models.Model):
    name = models.CharField(verbose_name=_("nome do grupo"), max_length=30)
    targets = models.ManyToManyField(Target, verbose_name=_("alvos"))

    class Meta:
        verbose_name = _("grupo de alvos")
        verbose_name_plural = _("grupos de alvos")
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    slug = models.SlugField(verbose_name=_("slug"), max_length=110)
    label = models.CharField(verbose_name=_("nome"), max_length=100)

    action_group = models.ForeignKey(ActionGroup, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")
        unique_together = ('slug', 'action_group')

    def __str__(self):
        return self.label