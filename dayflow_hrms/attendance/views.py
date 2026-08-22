from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import admin_required

from .models import Attendance

User = get_user_model()


@login_required
def my_attendance(request):
    """FR 3.4.2: Employees can view only their own attendance."""
    records = Attendance.objects.filter(employee=request.user).order_by('-date')[:60]
    today = timezone.localdate()
    today_record = Attendance.objects.filter(employee=request.user, date=today).first()
    return render(request, 'attendance/my_attendance.html', {
        'records': records,
        'today_record': today_record,
    })


@login_required
def check_in(request):
    """FR 3.4.1: check-in for employee."""
    today = timezone.localdate()
    record, created = Attendance.objects.get_or_create(
        employee=request.user, date=today,
        defaults={'status': Attendance.Status.PRESENT},
    )
    if record.check_in:
        messages.warning(request, 'You have already checked in today.')
    else:
        record.check_in = timezone.localtime().time()
        record.status = Attendance.Status.PRESENT
        record.save()
        messages.success(request, f'Checked in at {record.check_in.strftime("%I:%M %p")}.')
    return redirect('attendance:my_attendance')


@login_required
def check_out(request):
    """FR 3.4.1: check-out for employee."""
    today = timezone.localdate()
    record = Attendance.objects.filter(employee=request.user, date=today).first()
    if not record or not record.check_in:
        messages.error(request, 'You need to check in before checking out.')
    elif record.check_out:
        messages.warning(request, 'You have already checked out today.')
    else:
        record.check_out = timezone.localtime().time()
        record.save()
        messages.success(request, f'Checked out at {record.check_out.strftime("%I:%M %p")}.')
    return redirect('attendance:my_attendance')


@admin_required
def all_attendance(request):
    """FR 3.4.2 & 3.2.2: Admin/HR can view attendance of all employees."""
    date_filter = request.GET.get('date') or str(timezone.localdate())
    employee_filter = request.GET.get('employee')

    records = Attendance.objects.select_related('employee').filter(date=date_filter)
    if employee_filter:
        records = records.filter(employee_id=employee_filter)

    employees = User.objects.filter(role=User.Role.EMPLOYEE).order_by('first_name')

    return render(request, 'attendance/all_attendance.html', {
        'records': records.order_by('employee__first_name'),
        'date_filter': date_filter,
        'employee_filter': employee_filter,
        'employees': employees,
    })


@admin_required
def mark_attendance(request, employee_id):
    """Allows Admin/HR to set/correct an employee's status for a date."""
    employee = get_object_or_404(User, pk=employee_id)
    date = request.GET.get('date') or str(timezone.localdate())

    if request.method == 'POST':
        status = request.POST.get('status')
        record, _ = Attendance.objects.get_or_create(employee=employee, date=request.POST.get('date', date))
        record.status = status
        record.notes = request.POST.get('notes', '')
        record.save()
        messages.success(request, f'Attendance updated for {employee.get_full_name() or employee.username}.')
        return redirect('attendance:all_attendance')

    record = Attendance.objects.filter(employee=employee, date=date).first()
    return render(request, 'attendance/mark_attendance.html', {
        'employee': employee, 'date': date, 'record': record,
        'status_choices': Attendance.Status.choices,
    })
