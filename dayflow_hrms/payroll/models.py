from django.conf import settings
from django.db import models


class SalaryStructure(models.Model):
    """Current salary structure for an employee (FR 3.6)."""

    employee = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='salary_structure')
    basic = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hra = models.DecimalField('HRA', max_digits=12, decimal_places=2, default=0)
    conveyance_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    provident_fund = models.DecimalField('Provident Fund Deduction', max_digits=12, decimal_places=2, default=0)
    tax_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Salary structure: {self.employee.employee_id}'

    @property
    def gross_salary(self):
        return self.basic + self.hra + self.conveyance_allowance + self.other_allowances

    @property
    def total_deductions(self):
        return self.provident_fund + self.tax_deduction + self.other_deductions

    @property
    def net_salary(self):
        return self.gross_salary - self.total_deductions


class PayrollRun(models.Model):
    """A monthly payroll / salary-slip record for an employee."""

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payslips')
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    generated_on = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='payrolls_generated',
    )

    class Meta:
        unique_together = ('employee', 'month', 'year')
        ordering = ['-year', '-month']

    def __str__(self):
        return f'{self.employee.employee_id} payslip {self.month}/{self.year}'
