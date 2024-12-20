from django.db import models
from django.contrib.auth.models import User
import random
import string
from datetime import datetime, timedelta, time


class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    year_of_study = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    
    # Add the username field
    username = models.CharField(max_length=20,  blank=True)

    def save(self, *args, **kwargs):
        # Set the username to student_id if it's not already set
        if not self.username:
            self.username = self.student_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"


class Hostel(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=150)
    total_rooms = models.PositiveIntegerField()
    warden = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)  # Gender of the students allowed to stay in this hostel

    def __str__(self):
        return f" Hostel :  {self.name} for  {self.gender}"


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple', 'Triple'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField(default=4)  # Default to 4 beds
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE)

    def __str__(self):
        return f"Room {self.room_number} in {self.hostel.name}"

    def available_beds(self):
        """Return the number of available beds in the room."""
        return self.beds.filter(is_occupied=False).count()

    def is_full(self):
        """Check if all beds in the room are occupied."""
        return self.available_beds() == 0


class Bed(models.Model):
    bed_number = models.PositiveIntegerField()
    room = models.ForeignKey(Room, related_name='beds', on_delete=models.CASCADE)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Bed {self.bed_number} in {self.room.room_number}"



class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(null=True, blank=True)

    receipt_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.student.student_id} - {self.amount_paid} KES"


class Complaint(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    complaint_text = models.TextField()
    date_filed = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"Complaint by {self.student.student_id} - {self.status}"


class Staff(models.Model):
    ROLE_CHOICES = [
        ('Warden', 'Warden'),
        ('Caretaker', 'Caretaker'),
        ('Cleaner', 'Cleaner'),
        ('Security', 'Security'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.role}"


class BedAllocation(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.student.student_id} - Bed {self.bed_number} in {self.room.room_number}"


class Visitor(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    date_of_visit = models.DateField(auto_now_add=True)
    check_in_time = models.TimeField(default=time(12, 0))  # Default time set to 12:00 PM
    check_out_time = models.TimeField(blank=True, null=True)
    purpose = models.TextField()

    def save(self, *args, **kwargs):
        # Automatically set checkout time to be no later than 10:00 PM
        if not self.check_out_time:
            max_checkout_time = time(22, 0)  # 10:00 PM
            check_in_datetime = datetime.combine(self.date_of_visit, self.check_in_time)
            auto_checkout_time = check_in_datetime + timedelta(hours=2)  # Default stay duration of 2 hours
            if auto_checkout_time.time() > max_checkout_time:
                self.check_out_time = max_checkout_time
            else:
                self.check_out_time = auto_checkout_time.time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} visiting {self.student.student_id}"



class MaintenanceRequest(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    issue_description = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])

    def __str__(self):
        return f"{self.room.room_number} - {self.status}"


class BedBooking(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bed_bookings")
    hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE, related_name="bed_bookings")
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name="bed_bookings")
    bed = models.ForeignKey('Bed', on_delete=models.CASCADE, related_name="bed_bookings")
    date_booked = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    registration_number = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)  # Optional field
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    booking_id = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def generate_booking_id(self):
        """
        Generates a unique 10-character alphanumeric booking ID.
        """
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def save(self, *args, **kwargs):
        # Automatically generate a unique booking_id if not set
        if not self.booking_id:
            self.booking_id = self.generate_booking_id()
        
        # Ensure the bed is marked as occupied
        if not self.bed.is_occupied:
            self.bed.is_occupied = True
            self.bed.save()

        # Call the parent save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bed {self.bed.bed_number} in Room {self.room.room_number}, Hostel {self.hostel.name} booked by {self.student.username}"
