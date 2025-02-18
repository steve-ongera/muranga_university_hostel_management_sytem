from django.urls import path
from . import views

urlpatterns = [
    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_profile, name='student_profile'),
    path('students/create/', views.create_student, name='create_student'),
    path('students/detail/<int:student_id>/', views.student_detail, name='student_detail'),
    path('students/update/<int:student_id>/', views.update_student, name='update_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/update_profile/', views.update_profile, name='update_profile'),

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
    #students mentenance urls
    path('submit-maintenance-request/', views.submit_maintenance_request, name='submit_maintenance_request'),
    path('maintenance-requests/', views.maintenance_request_list, name='maintenance_request_list'),
    
    #visitors urls 
    path('visitors/', views.visitor_list, name='visitor_list'),
    path('visitors/create/', views.create_visitor, name='create_visitor'),
    path('visitors/detail/<int:visitor_id>/', views.visitor_detail, name='visitor_detail'),
    path('visitors/update/<int:visitor_id>/', views.update_visitor, name='update_visitor'),
    path('visitors/delete/<int:visitor_id>/', views.delete_visitor, name='delete_visitor'),
    path('visitor-check-in/', views.visitor_check_in, name='visitor_check_in'),
    #bed alocation urls
    path('bed_allocations/', views.bed_allocation_list, name='bed_allocation_list'),
    path('bed_allocations/create/', views.create_bed_allocation, name='create_bed_allocation'),
    path('bed_allocations/detail/<int:allocation_id>/', views.bed_allocation_detail, name='bed_allocation_detail'),
    path('bed_allocations/update/<int:allocation_id>/', views.update_bed_allocation, name='update_bed_allocation'),
    path('bed_allocations/delete/<int:allocation_id>/', views.delete_bed_allocation, name='delete_bed_allocation'),
    #staff
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/create/', views.create_staff, name='create_staff'),
    path('staff/detail/<int:staff_id>/', views.staff_detail, name='staff_detail'),
    path('staff/update/<int:staff_id>/', views.update_staff, name='update_staff'),
    path('staff/delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    #hostel
    path('hostels/', views.hostel_list, name='hostel_list'),
    path('hostels/create/', views.create_hostel, name='create_hostel'),
    path('hostels/detail/<int:hostel_id>/', views.hostel_detail, name='hostel_detail'),
    path('hostels/update/<int:hostel_id>/', views.update_hostel, name='update_hostel'),
    path('hostels/delete/<int:hostel_id>/', views.delete_hostel, name='delete_hostel'),
    #auth
    
    path('', views.login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('admin_dashboard/', views.dashboard, name='admin_dashboard'),
    path('student_register/', views.student_register, name='student_register'),
    # URL for listing all hostels

    path('bookings_hostels/', views.bookings_hostel_list, name='hostel_list'),
    path('bookings_hostels/<int:hostel_id>/rooms/', views.bookings_room_list, name='room_list'),
    path('bookings_rooms/<int:room_id>/beds/', views.bookings_bed_list, name='bed_list'),
    path('bookings_beds/<int:bed_id>/book/', views.bookings_book_bed, name='book_bed'),
    path('book-bed/', views.book_bed, name='book_bed'),  # Without bed preselected
    path('book-bed/<int:bed_id>/', views.book_bed, name='book_bed_with_id'),  # With bed preselected
    path('booking-success/', views.booking_success, name='booking_success'),
    #search 
    path('search-booking/', views.search_booking_view, name='search_booking'),
    path('search-student/', views.search_student_view, name='search_student'),
    
]
