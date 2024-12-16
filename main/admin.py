from django.contrib import admin
from .models import Student, Room, Hostel, FeePayment, Complaint, Staff, BedAllocation, Visitor, MaintenanceRequest

admin.site.register(Student)
admin.site.register(Room)
admin.site.register(Hostel)
admin.site.register(FeePayment)
admin.site.register(Complaint)
admin.site.register(Staff)
admin.site.register(BedAllocation)
admin.site.register(Visitor)
admin.site.register(MaintenanceRequest)
