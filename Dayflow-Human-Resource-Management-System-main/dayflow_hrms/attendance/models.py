from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime

class Attendance(models.Model):
    """Daily attendance record (FR 3.4)."""

    class Status(models.TextChoices):
        PRESENT = 'PRESENT', 'Present'
        ABSENT = 'ABSENT', 'Absent'
        HALF_DAY = 'HALF_DAY', 'Half-day'
        LEAVE = 'LEAVE', 'Leave'

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    date = models.DateField(default=timezone.localdate)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PRESENT
    )
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']

    def __str__(self):
        # Use username or email instead of employee_id (unless you added that field yourself)
        return f'{self.employee.username} - {self.date} - {self.get_status_display()}'

    @property
    def hours_worked(self):
        """Calculate hours worked in decimal hours if both check-in and check-out exist."""
        if self.check_in and self.check_out:
            # Convert TimeField values to datetime objects for subtraction
            check_in_dt = datetime.combine(self.date, self.check_in)
            check_out_dt = datetime.combine(self.date, self.check_out)
            delta = check_out_dt - check_in_dt
            return round(delta.total_seconds() / 3600, 2)
        return None
