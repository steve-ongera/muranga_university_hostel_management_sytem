from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class StudentRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    student_id = forms.CharField(max_length=20)
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        student_id = cleaned_data.get('student_id')

        # Check if the student exists in the Student database
        try:
            student = Student.objects.get(
                first_name=first_name,
                last_name=last_name,
                student_id=student_id
            )
            self.cleaned_data['student'] = student
        except Student.DoesNotExist:
            raise forms.ValidationError("No matching student found in the database.")
        
        return cleaned_data


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'



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
        fields = '__all__'
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


from django import forms
from .models import BedBooking, Bed

class BedBookingForm(forms.ModelForm):
    class Meta:
        model = BedBooking
        fields = ['hostel', 'room', 'bed']  # Include the necessary fields
        widgets = {
            'room': forms.HiddenInput(),
            'bed': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)

        # Set room and bed as readonly if needed
        self.fields['hostel'].widget.attrs['readonly'] = True
