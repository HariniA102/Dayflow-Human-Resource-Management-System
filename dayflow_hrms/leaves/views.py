from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import admin_required
from attendance.models import Attendance

from .forms import LeaveRequestForm, LeaveReviewForm
from .models import LeaveRequest


@login_required
def apply_leave(request):
    """FR 3.5.1: Employee applies for leave."""
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            messages.success(request, 'Your leave request has been submitted and is pending approval.')
            return redirect('leaves:my_leaves')
    else:
        form = LeaveRequestForm()
    return render(request, 'leaves/apply_leave.html', {'form': form})


@login_required
def my_leaves(request):
    leaves = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'leaves/my_leaves.html', {'leaves': leaves})


@admin_required
def all_leaves(request):
    """FR 3.5.2: Admin can view all leave requests, filterable by status."""
    status = request.GET.get('status', '')
    leaves = LeaveRequest.objects.select_related('employee')
    if status:
        leaves = leaves.filter(status=status)
    return render(request, 'leaves/all_leaves.html', {
        'leaves': leaves,
        'status': status,
        'status_choices': LeaveRequest.Status.choices,
    })


@admin_required
def review_leave(request, leave_id):
    """FR 3.5.2: Admin approves/rejects a leave request with comments."""
    leave = get_object_or_404(LeaveRequest, pk=leave_id)
    if request.method == 'POST':
        form = LeaveReviewForm(request.POST, instance=leave)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.reviewed_by = request.user
            leave.reviewed_at = timezone.now()
            leave.save()

            # Changes reflect immediately in employee attendance records.
            if leave.status == LeaveRequest.Status.APPROVED:
                current = leave.start_date
                while current <= leave.end_date:
                    Attendance.objects.update_or_create(
                        employee=leave.employee, date=current,
                        defaults={'status': Attendance.Status.LEAVE},
                    )
                    current += timezone.timedelta(days=1)

            messages.success(request, f'Leave request has been {leave.get_status_display().lower()}.')
            return redirect('leaves:all_leaves')
    else:
        form = LeaveReviewForm(instance=leave)
    return render(request, 'leaves/review_leave.html', {'form': form, 'leave': leave})
