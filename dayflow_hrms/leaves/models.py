from django.conf import settings
from django.db import models


class LeaveRequest(models.Model):
    """Leave / time-off request (FR 3.5)."""

    class LeaveType(models.TextChoices):
        PAID = 'PAID', 'Paid Leave'
        SICK = 'SICK', 'Sick Leave'
        UNPAID = 'UNPAID', 'Unpaid Leave'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=10, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    remarks = models.TextField(blank=True)

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    admin_comment = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviewed_leave_requests',
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    applied_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_on']

    def __str__(self):
        return f'{self.employee.employee_id}: {self.leave_type} ({self.start_date} to {self.end_date})'

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1
