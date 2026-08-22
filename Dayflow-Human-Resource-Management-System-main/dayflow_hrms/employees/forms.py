from django import forms
from django.contrib.auth import get_user_model

from accounts.mixins import BootstrapFormMixin

from .models import EmployeeDocument, EmployeeProfile

User = get_user_model()


class EmployeeSelfEditForm(BootstrapFormMixin, forms.ModelForm):
    """FR 3.3.2: Employees can edit limited fields only."""

    class Meta:
        model = EmployeeProfile
        fields = ['phone', 'address', 'profile_picture']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class AdminEmployeeEditForm(BootstrapFormMixin, forms.ModelForm):
    """FR 3.3.2: Admin can edit all employee details."""

    class Meta:
        model = EmployeeProfile
        fields = [
            'phone', 'address', 'date_of_birth', 'profile_picture',
            'department', 'designation', 'date_of_joining',
            'employment_status', 'manager',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manager'].queryset = User.objects.filter(role=User.Role.ADMIN)


class AdminUserEditForm(BootstrapFormMixin, forms.ModelForm):
    """Lets an Admin edit the core account fields of an employee."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role', 'is_active']


class DocumentUploadForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = EmployeeDocument
        fields = ['title', 'file']
