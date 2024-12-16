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

def complaint_list(request):
    complaints = Complaint.objects.all()
    return render(request, 'complaints/list.html', {'complaints': complaints})
