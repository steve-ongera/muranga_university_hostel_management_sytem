from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

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