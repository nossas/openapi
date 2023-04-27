from typing import Any, Optional
from django.contrib import admin
from django.db.models.fields.related import RelatedField
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import (
    ActionGroup,
    Campaign,
    CampaignOptions,
    Person,
    EmailAddress,
    PhoneNumber,
    PostalAddress,
    CustomField,
    Target,
    TargetGroup,
    Tag,
    Integration
)


class ReadOnlyMixin(object):
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    readonly_fields = ('address', )
    extra = 0


class PhoneNumberInline(ReadOnlyMixin, admin.TabularInline):
    model = PhoneNumber
    readonly_fields = ("number",)
    extra = 0


class PostalAddressInline(ReadOnlyMixin, admin.StackedInline):
    model = PostalAddress
    extra = 0


class CustomFieldInline(admin.TabularInline):
    model = CustomField
    extra = 0


class PersonAdmin(admin.ModelAdmin):
    list_display = ("email_address", "full_name")
    inlines = [
        EmailAddressInline,
        PhoneNumberInline,
        PostalAddressInline,
        CustomFieldInline,
    ]
    search_fields = (
        "given_name",
        "email_addresses__address",
    )

    @admin.display(ordering="given_name", description="Person name")
    def full_name(self, obj):
        return obj.given_name + " " + obj.family_name

    @admin.display(ordering="email_addresses__address", description="Email")
    def email_address(self, obj):
        return obj.email_addresses.first()


class CampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "resource_name")
    fields = ("title", "action_group", "resource_name")
    readonly_fields = ("an_response_json",)
    
    filter_horizontal = ("tags", )

    def get_fields(self, request, obj=None):
        if obj and obj.resource_name == CampaignOptions.OUTREACHES:
            return self.fields + ('tags', 'target_groups', )
        elif obj:
            return self.fields + ('tags', )

        return super(CampaignAdmin, self).get_fields(request, obj)

    def get_form(self, request, obj, change, **kwargs):
        form = super(CampaignAdmin, self).get_form(request, obj, change, **kwargs)

        if obj and 'tags' in form.base_fields:
            form.base_fields['tags'].queryset = Tag.objects.filter(action_group=obj.action_group)

        return form

    def save_model(self, request, obj, form, change):
        if not change:
            return Campaign.objects.create(**form.cleaned_data)
        return super().save_model(request, obj, form, change)


class ActionRecordAdmin(admin.ModelAdmin):
    list_display = (
        "action__uuid",
        "person__full_name",
        "person__uuid",
        "campaign__title",
    )
    readonly_fields = ("an_response_json",)

    @admin.display(ordering="person__given_name", description="Person name")
    def person__full_name(self, obj):
        if obj.person.family_name:
            return obj.person.given_name + " " + obj.person.family_name

        return obj.person.given_name

    @admin.display(ordering="campaign__title", description="Campaign title")
    def campaign__title(self, obj):
        return obj.campaign.title

    @admin.display(description="Person UUID")
    def person__uuid(self, obj):
        # return obj.api_response_json["_links"]["osdi:person"].split("/")[-1]
        return "asdijaid"

    @admin.display(description="Action UUID")
    def action__uuid(self, obj):
        return obj.uuid()

    # def has_add_permission(self, request, obj=None):
    #     return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            return self.model.objects.create(**form.cleaned_data)

        return super().save_model(request, obj, form, change)


class DonationActionAdmin(ActionRecordAdmin):
    list_display = ActionRecordAdmin.list_display + (
        "amount",
        "created_date",
    )


# Register your models here.
# admin.site.register(ActionGroup)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Person, PersonAdmin)

# admin.site.register(Donation, DonationActionAdmin)
# admin.site.register(Submission, ActionAdmin)
# admin.site.register(Signature, ActionAdmin)

class IntegrationInline(admin.StackedInline):
    model = Integration
    extra = 0


class ActionGroupAdmin(admin.ModelAdmin):
    fields = ("name", "an_secret_key", "openapi_token", "users")
    readonly_fields = ("openapi_token", )
    inlines = [IntegrationInline, ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user

        return super().save_model(request, obj, form, change)

admin.site.register(ActionGroup, ActionGroupAdmin)


admin.site.register(Tag)
admin.site.register(Target)
admin.site.register(TargetGroup)