# from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.actionnetwork.models import Target, OutreachInterface


class PhonePressure(OutreachInterface):
    targets = models.ManyToManyField(Target)

    class Meta:
        verbose_name = _("Pressão")
        verbose_name_plural = _("Pressões")


class Call(models.Model):
    STATUS_CHOICES = (
        ("created", "Created"),
        ("queued", "Queued"),
        ("initiated", "Initiated"),
        ("ringing", "Ringing"),
        ("in-progress", "In Progress"),
        ("completed", "Completed"),
    )

    sid = models.CharField(
        verbose_name="call sid", max_length=100, blank=True, null=True
    )
    status = models.CharField(
        verbose_name="call status", max_length=50, choices=STATUS_CHOICES
    )
    from_number = models.CharField(verbose_name="from", max_length=25)
    to_number = models.CharField(verbose_name="to", max_length=25)

    phone_pressure = models.ForeignKey(PhonePressure, on_delete=models.CASCADE)
