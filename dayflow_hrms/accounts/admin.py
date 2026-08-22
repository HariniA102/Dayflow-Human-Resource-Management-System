from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import EmailVerificationToken, User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'employee_id', 'email', 'role', 'is_email_verified', 'is_active')
    list_filter = ('role', 'is_email_verified', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Dayflow HRMS', {'fields': ('employee_id', 'role', 'is_email_verified')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Dayflow HRMS', {'fields': ('employee_id', 'email', 'role')}),
    )
    search_fields = ('username', 'employee_id', 'email', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)
admin.site.register(EmailVerificationToken)
