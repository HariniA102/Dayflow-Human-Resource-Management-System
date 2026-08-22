from django.contrib import admin

from .models import PayrollRun, SalaryStructure


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ('employee', 'basic', 'hra', 'net_salary')
    search_fields = ('employee__username', 'employee__employee_id')


@admin.register(PayrollRun)
class PayrollRunAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'year', 'net_salary', 'generated_on')
    list_filter = ('month', 'year')
