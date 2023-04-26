from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.actionnetwork.admin import ActionRecordAdmin

from .models import (
    # TargetPhoneGroup,
    PhonePressure,
    # TargetPhonePressure,
    # TargetPhoneGroupCampaign
)


# class TargetPhoneGroupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'group__name')
#     filter_horizontal = ('targets', )

#     @admin.display(ordering="group__name", description=_("comunidade"))
#     def group__name(self, obj):
#         return obj.group.name

# admin.site.register(TargetPhoneGroup, TargetPhoneGroupAdmin)


# class TargetPhoneGroupCampaignAdmin(admin.ModelAdmin):
#     list_display = ('target_group__name', 'campaign__name')

#     @admin.display(ordering="target_group__name", description=_("grupo de alvos"))
#     def target_group__name(self, obj):
#         return obj.target_group.name

#     @admin.display(ordering="campaign__name", description=_("campanha"))
#     def campaign__name(self, obj):
#         return obj.campaign.title

# admin.site.register(TargetPhoneGroupCampaign, TargetPhoneGroupCampaignAdmin)


# admin.site.register(TargetPhonePressure)
admin.site.register(PhonePressure, ActionRecordAdmin)