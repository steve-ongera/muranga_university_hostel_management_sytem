from django.urls import path
from . import views

urlpatterns = [
    # Student URLs
    path('students/register/', views.student_register, name='student_register'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_profile, name='student_profile'),

    # Room URLs
    path('rooms/', views.room_list, name='room_list'),
    path('create/', views.create_room, name='create_room'),
    path('update/<int:room_id>/', views.update_room, name='update_room'),
    path('delete/<int:room_id>/', views.delete_room, name='delete_room'),
    path('detail/<int:room_id>/', views.room_detail, name='room_detail'),  # Add this URL for the detail view

    # Complaint URLs
    path('complaints/file/', views.file_complaint, name='file_complaint'),
    path('complaints/', views.complaint_list, name='complaint_list'),
]
