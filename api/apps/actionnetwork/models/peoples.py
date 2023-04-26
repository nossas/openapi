from django.db import models
from django.utils.translation import gettext_lazy as _

from .details import Tag


class Person(models.Model):
    given_name = models.CharField(verbose_name=_("nome"), max_length=80)

    family_name = models.CharField(
        verbose_name=_("sobrenome"), max_length=120, null=True, blank=True
    )

    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = _("pessoa")
        verbose_name_plural = _("pessoas")

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f"{self.given_name} {self.family_name}"


class EmailAddress(models.Model):
    address = models.EmailField(verbose_name=_("endereço de email"), unique=True)

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="email_addresses",
        verbose_name=_("pessoa"),
    )

    def __str__(self):
        return self.address


class PhoneNumber(models.Model):
    number = models.CharField(
        verbose_name=_("número de telefone"), max_length=15, unique=True
    )

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="phone_numbers",
        verbose_name=_("pessoa"),
    )

    def __str__(self):
        return self.number


class PostalAddress(models.Model):
    address_lines = models.CharField(
        verbose_name=_("endereço"), max_length=200, blank=True
    )

    locality = models.CharField(verbose_name=_("cidade"), max_length=80, blank=True)

    region = models.CharField(verbose_name=_("estado"), max_length=100, blank=True)

    postal_code = models.CharField(verbose_name=_("cep"), max_length=30, blank=True)

    country = models.CharField(verbose_name=_("país"), max_length=30, blank=True)

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="postal_addresses",
        verbose_name=_("pessoa"),
    )


class CustomField(models.Model):
    name = models.CharField(verbose_name=_("nome do campo"), max_length=50)

    value = models.CharField(verbose_name=_("valor do campo"), max_length=150)

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="custom_fields",
        verbose_name=_("pessoa"),
    )
