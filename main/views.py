from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomRegistrationForm, CustomLoginForm
from django.contrib.auth.decorators import login_required


from django.contrib import messages

#student registration into the system 

def student_register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            student_id = student.student_id  # Use the student_id as the username
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # Check if a user with this student_id already exists
            if User.objects.filter(username=student_id).exists():
                messages.error(request, "A user with this student ID already exists.")
            else:
                # Create a new user account with the student_id as the username
                user = User.objects.create_user(
                    username=student_id,  # Set username as student_id
                    password=password,
                    first_name=student.first_name,
                    last_name=student.last_name,
                    email=email
                )
                
                messages.success(request, "Account created successfully. You are now logged in.")
                
                # Redirect to the login page or dashboard
                return redirect('login')  # Replace 'login' with your actual login URL name
    else:
        form = StudentRegistrationForm()

    return render(request, 'auth/student_register.html', {'form': form})

@login_required
def student_dashboard(request):
    # Get the currently logged-in user
    user = request.user
    
    try:
        # Fetch student data based on the logged-in user
        student = Student.objects.get(student_id=user.username)  # Assuming username is student_id
        
        context = {
            'student': student,
            'user': user,
        }
        return render(request, 'student_dashboard.html', context)
    except Student.DoesNotExist:
        messages.error(request, "Student information not found.")
        return redirect('login')  # Redirect to home or any other page
    

def update_profile(request):
    user = request.user
    try:
        student = Student.objects.get(student_id=user.username)
    except Student.DoesNotExist:
        messages.error(request, "Student information not found.")
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('student_dashboard')
    else:
        form = StudentProfileUpdateForm(instance=student)

    return render(request, 'students/update_profile.html', {'form': form})


# Registration View
def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Create a user to log in with student_id
            user = User.objects.create_user(username=student_id, email=email, password=password)
            user.save()
            form.save()
            return redirect('login')
    else:
        form = CustomRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

# Login View
def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)  # This logs in the user

                # Redirect based on whether the user is a staff member (admin) or not (student)
                if user.is_staff:  # Check if the user has admin privileges (staff status)
                    return redirect('admin_dashboard')  # Replace 'admin_dashboard' with the actual URL name for the admin dashboard
                else:
                    return redirect('student_dashboard')  # Replace 'student_dashboard' with the actual URL name for the student dashboard

            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = CustomLoginForm()

    return render(request, 'auth/login.html', {'form': form})

# Dashboard View
def dashboard(request):
    # Dashboard Statistics
    total_users = User.objects.count()
    total_students = Student.objects.count()
    total_hostels = Hostel.objects.count()
    total_rooms = Room.objects.count()
    total_beds = BedAllocation.objects.count()
    total_fee_payments = FeePayment.objects.count()

    # Complaints and Maintenance Summary
    recent_complaints = Complaint.objects.order_by('-date_filed')[:5]  # Latest 5 complaints
    pending_maintenance = MaintenanceRequest.objects.filter(status="Pending").order_by('-date_reported')[:5]

    # Context to pass to the template
    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_hostels': total_hostels,
        'total_rooms': total_rooms,
        'total_beds': total_beds,
        'total_fee_payments': total_fee_payments,
        'recent_complaints': recent_complaints,
        'pending_maintenance': pending_maintenance,
    }
    return render(request, 'dashboard.html', context)


# Logout View
def custom_logout(request):
    logout(request)
    return redirect('login')

# Student views


def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})

# Create Student
def create_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/create.html', {'form': form})

# List all Students
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})

# Detail View for Student
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'students/detail.html', {'student': student})

# Update Student
def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/update.html', {'form': form, 'student': student})

# Delete Student
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    return render(request, 'students/confirm_delete.html', {'student': student})

def student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/profile.html', {'student': student})

# Room views
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/list.html', {'rooms': rooms})

# Room Detail View
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)  # Fetch the room by its ID
    return render(request, 'rooms/detail.html', {'room': room})


# Create Room View
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()  # Save the room to the database
            return redirect('room_list')  # Redirect to the room list view after creation
    else:
        form = RoomForm()  # Create an empty form for GET requests
    return render(request, 'rooms/create.html', {'form': form})


# Update Room View
def update_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)  # Get the room by ID
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)  # Prepopulate the form with room data
        if form.is_valid():
            form.save()  # Save the updated room to the database
            return redirect('room_list')  # Redirect to the room list view after updating
    else:
        form = RoomForm(instance=room)  # Prepopulate the form with room data for GET requests
    return render(request, 'rooms/update.html', {'form': form, 'room': room})


# Delete Room View
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        room.delete()  # Delete the room
        return redirect('room_list')  # Redirect to the room list after deletion
    return render(request, 'rooms/delete_confirm.html', {'room': room})


# Complaint views
def file_complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/file.html', {'form': form})

# Complaint List (Read all complaints)
def complaint_list(request):
    complaints = Complaint.objects.all()
    return render(request, 'complaints/list.html', {'complaints': complaints})

# Complaint Detail View (Read single complaint)
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    return render(request, 'complaints/detail.html', {'complaint': complaint})

# Update Complaint
def update_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == "POST":
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, 'complaints/update.html', {'form': form, 'complaint': complaint})

# Delete Complaint
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == "POST":
        complaint.delete()
        return redirect('complaint_list')
    return render(request, 'complaints/confirm_delete.html', {'complaint': complaint})

# Create a Maintenance Request
def file_maintenance_request(request):
    if request.method == "POST":
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceRequestForm()
    return render(request, 'maintenance/file.html', {'form': form})

# List all Maintenance Requests
def maintenance_list(request):
    requests = MaintenanceRequest.objects.all()
    return render(request, 'maintenance/list.html', {'requests': requests})

# Detail View for a Maintenance Request
def maintenance_detail(request, request_id):
    maintenance = get_object_or_404(MaintenanceRequest, id=request_id)
    return render(request, 'maintenance/detail.html', {'maintenance': maintenance})

# Update a Maintenance Request
def update_maintenance_request(request, request_id):
    maintenance = get_object_or_404(MaintenanceRequest, id=request_id)
    if request.method == "POST":
        form = MaintenanceRequestForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceRequestForm(instance=maintenance)
    return render(request, 'maintenance/update.html', {'form': form, 'maintenance': maintenance})

# Delete a Maintenance Request
def delete_maintenance_request(request, request_id):
    maintenance = get_object_or_404(MaintenanceRequest, id=request_id)
    if request.method == "POST":
        maintenance.delete()
        return redirect('maintenance_list')
    return render(request, 'maintenance/confirm_delete.html', {'maintenance': maintenance})


# Create a Visitor
def create_visitor(request):
    if request.method == "POST":
        form = VisitorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visitor_list')
    else:
        form = VisitorForm()
    return render(request, 'visitors/create.html', {'form': form})

# List all Visitors
def visitor_list(request):
    visitors = Visitor.objects.all()
    return render(request, 'visitors/list.html', {'visitors': visitors})

# Detail View for a Visitor
def visitor_detail(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    return render(request, 'visitors/detail.html', {'visitor': visitor})

# Update a Visitor
def update_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if request.method == "POST":
        form = VisitorForm(request.POST, instance=visitor)
        if form.is_valid():
            form.save()
            return redirect('visitor_list')
    else:
        form = VisitorForm(instance=visitor)
    return render(request, 'visitors/update.html', {'form': form, 'visitor': visitor})

# Delete a Visitor
def delete_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if request.method == "POST":
        visitor.delete()
        return redirect('visitor_list')
    return render(request, 'visitors/confirm_delete.html', {'visitor': visitor})


# Create a Bed Allocation
def create_bed_allocation(request):
    if request.method == "POST":
        form = BedAllocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bed_allocation_list')
    else:
        form = BedAllocationForm()
    return render(request, 'bed_allocations/create.html', {'form': form})

# List all Bed Allocations
def bed_allocation_list(request):
    bed_allocations = BedAllocation.objects.all()
    return render(request, 'bed_allocations/list.html', {'bed_allocations': bed_allocations})

# Detail View for a Bed Allocation
def bed_allocation_detail(request, allocation_id):
    allocation = get_object_or_404(BedAllocation, id=allocation_id)
    return render(request, 'bed_allocations/detail.html', {'allocation': allocation})

# Update a Bed Allocation
def update_bed_allocation(request, allocation_id):
    allocation = get_object_or_404(BedAllocation, id=allocation_id)
    if request.method == "POST":
        form = BedAllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            form.save()
            return redirect('bed_allocation_list')
    else:
        form = BedAllocationForm(instance=allocation)
    return render(request, 'bed_allocations/update.html', {'form': form, 'allocation': allocation})

# Delete a Bed Allocation
def delete_bed_allocation(request, allocation_id):
    allocation = get_object_or_404(BedAllocation, id=allocation_id)
    if request.method == "POST":
        allocation.delete()
        return redirect('bed_allocation_list')
    return render(request, 'bed_allocations/confirm_delete.html', {'allocation': allocation})



# Create Staff
def create_staff(request):
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'staff/create.html', {'form': form})

# List all Staff
def staff_list(request):
    staff_members = Staff.objects.all()
    return render(request, 'staff/list.html', {'staff_members': staff_members})

# Detail View for Staff
def staff_detail(request, staff_id):
    staff_member = get_object_or_404(Staff, id=staff_id)
    return render(request, 'staff/detail.html', {'staff_member': staff_member})

# Update Staff
def update_staff(request, staff_id):
    staff_member = get_object_or_404(Staff, id=staff_id)
    if request.method == "POST":
        form = StaffForm(request.POST, instance=staff_member)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm(instance=staff_member)
    return render(request, 'staff/update.html', {'form': form, 'staff_member': staff_member})

# Delete Staff
def delete_staff(request, staff_id):
    staff_member = get_object_or_404(Staff, id=staff_id)
    if request.method == "POST":
        staff_member.delete()
        return redirect('staff_list')
    return render(request, 'staff/confirm_delete.html', {'staff_member': staff_member})


# Create Hostel
def create_hostel(request):
    if request.method == "POST":
        form = HostelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hostel_list')
    else:
        form = HostelForm()
    return render(request, 'hostels/create.html', {'form': form})

# List all Hostels
def hostel_list(request):
    hostels = Hostel.objects.all()
    return render(request, 'hostels/list.html', {'hostels': hostels})

# Detail View for Hostel
def hostel_detail(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    return render(request, 'hostels/detail.html', {'hostel': hostel})

# Update Hostel
def update_hostel(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    if request.method == "POST":
        form = HostelForm(request.POST, instance=hostel)
        if form.is_valid():
            form.save()
            return redirect('hostel_list')
    else:
        form = HostelForm(instance=hostel)
    return render(request, 'hostels/update.html', {'form': form, 'hostel': hostel})

# Delete Hostel
def delete_hostel(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    if request.method == "POST":
        hostel.delete()
        return redirect('hostel_list')
    return render(request, 'hostels/confirm_delete.html', {'hostel': hostel})


# View to list all hostels
def bookings_hostel_list(request):
    hostels = Hostel.objects.all()
    
    # Get the number of rooms for each hostel
    for hostel in hostels:
        hostel.room_count = hostel.room_set.count()  # Count rooms in each hostel
    
    return render(request, 'bookings/hostel_list.html', {'hostels': hostels})


# View to see rooms in a selected hostel
def bookings_room_list(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    rooms = Room.objects.filter(hostel=hostel)

    # Calculate the total number of vacant beds across all rooms in the hostel
    total_vacant_beds = Bed.objects.filter(room__hostel=hostel, is_occupied=False).count()
    
    # Calculate vacant beds for each room
    for room in rooms:
        vacant_beds = Bed.objects.filter(room=room, is_occupied=False).count()
        room.vacant_beds = vacant_beds  # Attach the count of vacant beds to the room object

    return render(request, 'bookings/room_list.html', {'hostel': hostel, 'rooms': rooms , 'total_vacant_beds': total_vacant_beds})



# View to see available beds in a selected room
def bookings_bed_list(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    beds = Bed.objects.filter(room=room, is_occupied=False)
    return render(request, 'bookings/bed_list.html', {'room': room, 'beds': beds})


def bookings_book_bed(request, bed_id):
    bed = get_object_or_404(Bed, id=bed_id)
    context = {
        'bed': bed,
    }
    return render(request, 'bookings/view_bed.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Bed
from .forms import BedBookingForm
from .utils import send_bed_booking_receipt_email

def book_bed(request, bed_id):
    # Fetch the selected bed
    bed = get_object_or_404(Bed, id=bed_id, is_occupied=False)

    if request.method == 'POST':
        form = BedBookingForm(request.POST, student=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user  # Link the booking to the student
            booking.bed = bed  # Set the bed
            booking.room = bed.room  # Set the room
            booking.save()

            # Mark the bed as occupied
            bed.is_occupied = True
            bed.save()

            # Send email with receipt PDF
            send_bed_booking_receipt_email(booking)

            return redirect('booking_success')
    else:
        form = BedBookingForm(
            initial={
                'hostel': bed.room.hostel,
                'room': bed.room,
                'bed': bed,
            },
            student=request.user
        )

    return render(request, 'bookings/book_bed.html', {'form': form, 'bed': bed})




def booking_success(request):
    return render(request, 'bookings/booking_success.html')