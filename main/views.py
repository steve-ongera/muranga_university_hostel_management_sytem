from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Room, Complaint, FeePayment, MaintenanceRequest
from .forms import StudentForm, ComplaintForm, FeePaymentForm, MaintenanceForm

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
