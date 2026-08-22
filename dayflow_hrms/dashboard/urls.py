from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_redirect, name='redirect'),
    path('employee/', views.employee_dashboard, name='employee_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]
