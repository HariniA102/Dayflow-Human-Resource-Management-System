from django.urls import path

from . import views

app_name = 'payroll'

urlpatterns = [
    path('', views.my_payroll, name='my_payroll'),
    path('overview/', views.payroll_overview, name='payroll_overview'),
    path('<int:user_id>/edit/', views.edit_salary, name='edit_salary'),
    path('<int:user_id>/generate/', views.generate_payslip, name='generate_payslip'),
]
