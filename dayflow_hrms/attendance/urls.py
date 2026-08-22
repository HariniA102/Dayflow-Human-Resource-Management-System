from django.urls import path

from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.my_attendance, name='my_attendance'),
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/', views.check_out, name='check_out'),
    path('all/', views.all_attendance, name='all_attendance'),
    path('mark/<int:employee_id>/', views.mark_attendance, name='mark_attendance'),
]
