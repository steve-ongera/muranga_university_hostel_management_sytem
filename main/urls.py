from django.urls import path
from . import views

urlpatterns = [
    # Student URLs
    path('students/register/', views.student_register, name='student_register'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_profile, name='student_profile'),

    # Room URLs
    path('rooms/', views.room_list, name='room_list'),

    # Complaint URLs
    path('complaints/file/', views.file_complaint, name='file_complaint'),
    path('complaints/', views.complaint_list, name='complaint_list'),
]
