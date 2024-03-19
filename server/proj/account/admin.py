from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm
)

from account.forms import UserChangeForm, UserCreationForm
from account.models import Profile, SiteInfo, FormMessage


@admin.register(Profile)
class ProfileAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ('email', 'client_id', 'phone', 'is_active', 'is_staff', 'notify')
    list_filter = ('is_active', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'client_id')}),
        ('Персональная информация', {'fields': ('phone', 'notify')}),
        ('Доступы', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'client_id'),
        }),
    )
    readonly_fields = ('date_joined', 'last_login')
    search_fields = ('email',)
    ordering = ('email',)


admin.site.unregister(Group)


@admin.register(FormMessage)
class FormMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'person', 'phone')


@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request) -> bool:
        if self.model.objects.count() >= 1:
            return False
        return True
