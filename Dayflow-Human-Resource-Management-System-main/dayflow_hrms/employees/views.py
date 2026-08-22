from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required

from .forms import (
    AdminEmployeeEditForm, AdminUserEditForm, DocumentUploadForm, EmployeeSelfEditForm,
)
from .models import EmployeeProfile

User = get_user_model()


@login_required
def my_profile(request):
    """FR 3.3.1: employees view their own profile."""
    profile, _ = EmployeeProfile.objects.get_or_create(user=request.user)
    return render(request, 'employees/profile_detail.html', {
        'profile': profile,
        'is_own_profile': True,
    })


@login_required
def edit_my_profile(request):
    """FR 3.3.2: employees edit limited fields (address, phone, picture)."""
    profile, _ = EmployeeProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = EmployeeSelfEditForm(request.POST, request.FILES, instance=profile)
        doc_form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if request.FILES.get('file') and doc_form.is_valid():
                doc = doc_form.save(commit=False)
                doc.profile = profile
                doc.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('employees:my_profile')
    else:
        form = EmployeeSelfEditForm(instance=profile)
        doc_form = DocumentUploadForm()
    return render(request, 'employees/profile_edit.html', {
        'form': form, 'doc_form': doc_form, 'profile': profile,
    })


@admin_required
def employee_list(request):
    """FR 3.2.2: Admin/HR dashboard - employee list."""
    query = request.GET.get('q', '').strip()
    employees = User.objects.filter(role=User.Role.EMPLOYEE).select_related('profile')
    if query:
        employees = employees.filter(
            username__icontains=query
        ) | employees.filter(
            first_name__icontains=query
        ) | employees.filter(
            employee_id__icontains=query
        )
    return render(request, 'employees/employee_list.html', {
        'employees': employees.distinct().order_by('first_name', 'last_name'),
        'query': query,
    })


@admin_required
def employee_detail(request, user_id):
    """FR 3.2.2: Admin can view / switch between employee profiles."""
    employee = get_object_or_404(User, pk=user_id)
    profile, _ = EmployeeProfile.objects.get_or_create(user=employee)
    return render(request, 'employees/profile_detail.html', {
        'profile': profile,
        'is_own_profile': False,
    })


@admin_required
def employee_edit(request, user_id):
    """FR 3.3.2: Admin can edit all employee details."""
    employee = get_object_or_404(User, pk=user_id)
    profile, _ = EmployeeProfile.objects.get_or_create(user=employee)
    if request.method == 'POST':
        user_form = AdminUserEditForm(request.POST, instance=employee)
        profile_form = AdminEmployeeEditForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'{employee.get_full_name() or employee.username}\u2019s record was updated.')
            return redirect('employees:employee_detail', user_id=employee.id)
    else:
        user_form = AdminUserEditForm(instance=employee)
        profile_form = AdminEmployeeEditForm(instance=profile)
    return render(request, 'employees/profile_admin_edit.html', {
        'user_form': user_form, 'profile_form': profile_form, 'employee': employee,
    })
