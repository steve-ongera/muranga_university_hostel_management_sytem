from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# forms.py


class CustomRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'profile_picture']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        return cleaned_data

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  # Adjust the fields as necessary

# Student Form
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'room', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

# Complaint Form
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['student', 'complaint_text', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'complaint_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

# Fee Payment Form
class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        exclude = ['date_paid']



# Maintenance Request Form
class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['room', 'issue_description', 'priority', 'status']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'issue_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['room', 'issue_description', 'status', 'priority']


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['name', 'phone_number', 'student', 'date_of_visit', 'purpose']        


class BedAllocationForm(forms.ModelForm):
    class Meta:
        model = BedAllocation
        fields = ['student', 'room', 'bed_number']


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'email', 'phone_number', 'role', 'hostel']


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'location', 'total_rooms', 'warden']