from django.contrib import admin

from apps.actionnetwork.admin import ActionAdmin

from .models import TargetPhonePressure, PhonePressure


admin.site.register(TargetPhonePressure)

admin.site.register(PhonePressure, ActionAdmin)