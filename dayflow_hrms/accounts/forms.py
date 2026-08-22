from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .mixins import BootstrapFormMixin
from .models import User


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    """Sign-up form covering FR 3.1.1: Employee ID, Email, Password, Role."""

    employee_id = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=False)
    role = forms.ChoiceField(choices=User.Role.choices, required=True)

    class Meta:
        model = User
        fields = (
            'employee_id', 'username', 'first_name', 'last_name',
            'email', 'role', 'password1', 'password2',
        )

    def clean_employee_id(self):
        employee_id = self.cleaned_data['employee_id']
        if User.objects.filter(employee_id=employee_id).exists():
            raise forms.ValidationError('An account with this Employee ID already exists.')
        return employee_id

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.employee_id = self.cleaned_data['employee_id']
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.is_active = True
        user.is_email_verified = False
        if commit:
            user.save()
        return user


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    """Sign-in form (FR 3.1.2). Uses username, but the login view also
    accepts an email address for convenience."""

    username = forms.CharField(label='Email or Username')
