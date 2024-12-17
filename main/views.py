from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import CustomRegistrationForm, CustomLoginForm

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
            student_id = form.cleaned_data['student_id']
            password = form.cleaned_data['password']
            user = authenticate(request, username=student_id, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid student ID or password")
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
def student_register(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/register.html', {'form': form})

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