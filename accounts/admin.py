from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from . import models
# Register your models here.

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['first_name', 'last_name',]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'),{'fields':('first_name','last_name','department',)}),
        (
            _('Permissions'),
            {'fields':('is_active', 'is_staff', 'is_lecturer','is_superuser')}
        ),
        (_('Important dates'), {'fields':('last_login', )})

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'department','password1', 'password2')
        }),
    )
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Department)