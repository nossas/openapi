# from django import forms
from django.contrib import admin
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import UsersGroup, User

# class UserAdmin(BaseUserAdmin):
#     list_display = ('email', 'first_name', 'is_active', 'is_staff', 'is_superuser')
#     ordering = ('email', )

class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class UsersGroupAdmin(admin.ModelAdmin):
    fields = ('name', 'api_secret_key', 'token')
    readonly_fields = ('token', )


admin.site.register(UsersGroup, UsersGroupAdmin)
admin.site.register(User, UserAdmin)