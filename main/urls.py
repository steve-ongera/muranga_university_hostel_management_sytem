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
    path('complaints/detail/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('complaints/update/<int:complaint_id>/', views.update_complaint, name='update_complaint'),
    path('complaints/delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    # maintenance urls
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/file/', views.file_maintenance_request, name='file_maintenance_request'),
    path('maintenance/detail/<int:request_id>/', views.maintenance_detail, name='maintenance_detail'),
    path('maintenance/update/<int:request_id>/', views.update_maintenance_request, name='update_maintenance_request'),
    path('maintenance/delete/<int:request_id>/', views.delete_maintenance_request, name='delete_maintenance_request'),
    #visitors
    path('visitors/', views.visitor_list, name='visitor_list'),
    path('visitors/create/', views.create_visitor, name='create_visitor'),
    path('visitors/detail/<int:visitor_id>/', views.visitor_detail, name='visitor_detail'),
    path('visitors/update/<int:visitor_id>/', views.update_visitor, name='update_visitor'),
    path('visitors/delete/<int:visitor_id>/', views.delete_visitor, name='delete_visitor'),
    
]
