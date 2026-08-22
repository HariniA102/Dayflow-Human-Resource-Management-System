from django.urls import path

from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.my_profile, name='my_profile'),
    path('edit/', views.edit_my_profile, name='edit_my_profile'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<int:user_id>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:user_id>/edit/', views.employee_edit, name='employee_edit'),
]
