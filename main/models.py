from django.db import models

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

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

class Hostel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=150)
    total_rooms = models.PositiveIntegerField()
    warden = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple', 'Triple'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    current_occupants = models.PositiveIntegerField(default=0)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE)

    def __str__(self):
        return f"Room {self.room_number} in {self.hostel.name}"

    def is_full(self):
        return self.current_occupants >= self.capacity



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
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_of_visit = models.DateField()
    purpose = models.TextField()

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
