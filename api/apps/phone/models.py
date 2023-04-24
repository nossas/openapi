from django.db import models

from apps.actionnetwork.models import OutreachInterface


class Call(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('queued', 'Queued'),
        ('initiated', 'Initiated'),
        ('ringing', 'Ringing'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    sid = models.CharField(verbose_name="call sid", max_length=100, blank=True, null=True)
    status = models.CharField(verbose_name="call status", max_length=50, choices=STATUS_CHOICES)
    from_number = models.CharField(verbose_name="from", max_length=25)
    to_number = models.CharField(verbose_name="to", max_length=25)


class TargetPhonePressure(models.Model):
    name = models.CharField(verbose_name="name", max_length=100)
    phone_number = models.CharField(verbose_name="phone number", max_length=25)

    def __str__(self):
        return f"{self.name} <{self.phone_number}>"


class PhonePressure(OutreachInterface):
    targets = models.ManyToManyField(TargetPhonePressure)