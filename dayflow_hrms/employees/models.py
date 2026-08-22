from django.conf import settings
from django.db import models


def profile_picture_path(instance, filename):
    return f'profile_pics/{instance.user.employee_id}/{filename}'


def document_path(instance, filename):
    return f'documents/{instance.profile.user.employee_id}/{filename}'


class EmployeeProfile(models.Model):
    """Extended profile data on top of the auth User (FR 3.3)."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    # Personal details
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to=profile_picture_path, null=True, blank=True)

    # Job details
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    employment_status = models.CharField(
        max_length=20,
        choices=[('ACTIVE', 'Active'), ('ON_LEAVE', 'On Leave'), ('INACTIVE', 'Inactive')],
        default='ACTIVE',
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='direct_reports',
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile: {self.user}'


class EmployeeDocument(models.Model):
    """Uploaded documents belonging to an employee's profile (FR 3.3.1)."""

    profile = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=150)
    file = models.FileField(upload_to=document_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.profile.user.employee_id})'
