import secrets

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View

from employees.models import EmployeeProfile

from .forms import LoginForm, SignUpForm
from .models import EmailVerificationToken

User = get_user_model()


def _send_verification_email(request, user):
    token = secrets.token_urlsafe(32)
    EmailVerificationToken.objects.update_or_create(
        user=user, defaults={'token': token}
    )
    verify_url = request.build_absolute_uri(
        reverse('accounts:verify_email', kwargs={'token': token})
    )
    send_mail(
        subject='Verify your Dayflow HRMS account',
        message=(
            f'Hi {user.first_name or user.username},\n\n'
            f'Please verify your email by visiting the link below:\n{verify_url}\n\n'
            'If you did not create this account, you can ignore this email.'
        ),
        from_email=None,
        recipient_list=[user.email],
        fail_silently=True,
    )


class SignUpView(View):
    template_name = 'registration/signup.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            EmployeeProfile.objects.get_or_create(user=user)
            _send_verification_email(request, user)
            messages.success(
                request,
                'Account created successfully! Please check your email '
                '(printed to server console in this demo) to verify your address, then sign in.'
            )
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form})


class EmailOrUsernameLoginView(LoginView):
    """Sign-in view (FR 3.1.2). Accepts either username or email."""

    template_name = 'registration/login.html'
    authentication_form = LoginForm

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().get_full_name() or form.get_user().username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Incorrect credentials. Please check your email/username and password.')
        return super().form_invalid(form)


def logout_view(request):
    auth_logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


def verify_email(request, token):
    token_obj = get_object_or_404(EmailVerificationToken, token=token)
    user = token_obj.user
    user.is_email_verified = True
    user.save(update_fields=['is_email_verified'])
    token_obj.delete()
    messages.success(request, 'Your email has been verified. You can now sign in.')
    return redirect('accounts:login')
