from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import admin_required

from .forms import SalaryStructureForm
from .models import PayrollRun, SalaryStructure

User = get_user_model()


@login_required
def my_payroll(request):
    """FR 3.6.1: Payroll data is read-only for employees."""
    structure, _ = SalaryStructure.objects.get_or_create(employee=request.user)
    payslips = PayrollRun.objects.filter(employee=request.user)
    return render(request, 'payroll/my_payroll.html', {
        'structure': structure,
        'payslips': payslips,
    })


@admin_required
def payroll_overview(request):
    """FR 3.6.2: Admin can view payroll of all employees."""
    employees = User.objects.filter(role=User.Role.EMPLOYEE).select_related('salary_structure')
    # Ensure every employee has a salary structure to display.
    for emp in employees:
        SalaryStructure.objects.get_or_create(employee=emp)
    employees = User.objects.filter(role=User.Role.EMPLOYEE).select_related('salary_structure')
    return render(request, 'payroll/payroll_overview.html', {'employees': employees})


@admin_required
def edit_salary(request, user_id):
    """FR 3.6.2: Admin can update salary structure to ensure payroll accuracy."""
    employee = get_object_or_404(User, pk=user_id)
    structure, _ = SalaryStructure.objects.get_or_create(employee=employee)
    if request.method == 'POST':
        form = SalaryStructureForm(request.POST, instance=structure)
        if form.is_valid():
            form.save()
            messages.success(request, f'Salary structure updated for {employee.get_full_name() or employee.username}.')
            return redirect('payroll:payroll_overview')
    else:
        form = SalaryStructureForm(instance=structure)
    return render(request, 'payroll/edit_salary.html', {'form': form, 'employee': employee, 'structure': structure})


@admin_required
def generate_payslip(request, user_id):
    """Generates (or regenerates) the current month's payslip from the salary structure."""
    employee = get_object_or_404(User, pk=user_id)
    structure, _ = SalaryStructure.objects.get_or_create(employee=employee)
    today = timezone.localdate()
    payslip, created = PayrollRun.objects.update_or_create(
        employee=employee, month=today.month, year=today.year,
        defaults={
            'gross_salary': structure.gross_salary,
            'total_deductions': structure.total_deductions,
            'net_salary': structure.net_salary,
            'generated_by': request.user,
        },
    )
    verb = 'generated' if created else 'regenerated'
    messages.success(request, f'Payslip {verb} for {employee.get_full_name() or employee.username} ({today.month}/{today.year}).')
    return redirect('payroll:payroll_overview')
