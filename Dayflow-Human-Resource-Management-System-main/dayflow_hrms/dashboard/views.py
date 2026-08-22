from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from accounts.decorators import admin_required
from attendance.models import Attendance
from leaves.models import LeaveRequest

User = get_user_model()


@login_required
def dashboard_redirect(request):
    """Sends the user to the right dashboard based on their role."""
    if request.user.is_admin_role:
        return redirect('dashboard:admin_dashboard')
    return redirect('dashboard:employee_dashboard')


@login_required
def employee_dashboard(request):
    """FR 3.2.1: Employee dashboard with quick-access cards and recent activity."""
    today = timezone.localdate()
    today_attendance = Attendance.objects.filter(employee=request.user, date=today).first()
    recent_leaves = LeaveRequest.objects.filter(employee=request.user)[:5]
    pending_leaves_count = LeaveRequest.objects.filter(
        employee=request.user, status=LeaveRequest.Status.PENDING
    ).count()
    recent_attendance = Attendance.objects.filter(employee=request.user).order_by('-date')[:7]

    return render(request, 'dashboard/employee_dashboard.html', {
        'today_attendance': today_attendance,
        'recent_leaves': recent_leaves,
        'pending_leaves_count': pending_leaves_count,
        'recent_attendance': recent_attendance,
    })


@admin_required
def admin_dashboard(request):
    """FR 3.2.2: Admin/HR dashboard - employee list, attendance, leave approvals.
    Also covers section 5's analytics & reports dashboard bullet point."""
    today = timezone.localdate()

    total_employees = User.objects.filter(role=User.Role.EMPLOYEE).count()
    present_today = Attendance.objects.filter(date=today, status=Attendance.Status.PRESENT).count()
    absent_today = Attendance.objects.filter(date=today, status=Attendance.Status.ABSENT).count()
    on_leave_today = Attendance.objects.filter(date=today, status=Attendance.Status.LEAVE).count()

    pending_leaves = LeaveRequest.objects.filter(status=LeaveRequest.Status.PENDING).select_related('employee')
    recent_employees = User.objects.filter(role=User.Role.EMPLOYEE).order_by('-date_joined')[:5]

    return render(request, 'dashboard/admin_dashboard.html', {
        'total_employees': total_employees,
        'present_today': present_today,
        'absent_today': absent_today,
        'on_leave_today': on_leave_today,
        'pending_leaves': pending_leaves,
        'pending_leaves_count': pending_leaves.count(),
        'recent_employees': recent_employees,
        'today': today,
    })
