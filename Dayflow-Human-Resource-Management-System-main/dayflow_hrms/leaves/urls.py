from django.urls import path

from . import views

app_name = 'leaves'

urlpatterns = [
    path('apply/', views.apply_leave, name='apply_leave'),
    path('mine/', views.my_leaves, name='my_leaves'),
    path('all/', views.all_leaves, name='all_leaves'),
    path('<int:leave_id>/review/', views.review_leave, name='review_leave'),
]
