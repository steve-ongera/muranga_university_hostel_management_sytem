from django import forms
from .models import *
# forms.py



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
