from django.contrib import admin

from .models import EmployeeDocument, EmployeeProfile


class EmployeeDocumentInline(admin.TabularInline):
    model = EmployeeDocument
    extra = 0


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'designation', 'employment_status', 'date_of_joining')
    list_filter = ('department', 'employment_status')
    search_fields = ('user__username', 'user__employee_id', 'user__email')
    inlines = [EmployeeDocumentInline]


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'uploaded_at')
