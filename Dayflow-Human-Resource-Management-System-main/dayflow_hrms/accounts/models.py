from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for Dayflow HRMS.

    Adds an Employee ID, a role (Admin/HR vs Employee) and an
    email-verification flag on top of Django's built-in auth fields.
    """

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin / HR Officer'
        EMPLOYEE = 'EMPLOYEE', 'Employee'

    employee_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.EMPLOYEE)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'employee_id']

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.employee_id})'

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN


class EmailVerificationToken(models.Model):
    """A single-use token emailed to a user to confirm their address."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_token')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Verification token for {self.user.username}'
