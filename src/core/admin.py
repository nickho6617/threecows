from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class EventInline(admin.TabularInline):
    model = models.LifeEvent


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


class BovidAdmin(admin.ModelAdmin):
    inlines = [
        EventInline,
    ]
    list_display = (
            'type_of_bovid',
            'date_of_birth',
            'breed',
            'name',
            'price'
    )


class LifeEventAdmin(admin.ModelAdmin):
    list_display = (
            'event_type',
            'notes',
            'event_date',
            'bovid',
            'user'
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Bovid, BovidAdmin)
admin.site.register(models.LifeEvent, LifeEventAdmin)
