# Generated by Django 5.1.2 on 2024-12-16 19:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('location', models.CharField(max_length=150)),
                ('total_rooms', models.PositiveIntegerField()),
                ('warden', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=10, unique=True)),
                ('capacity', models.PositiveIntegerField()),
                ('current_occupants', models.PositiveIntegerField(default=0)),
                ('room_type', models.CharField(choices=[('Single', 'Single'), ('Double', 'Double'), ('Triple', 'Triple')], max_length=10)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.hostel')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_description', models.TextField()),
                ('date_reported', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=20)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.room')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('role', models.CharField(choices=[('Warden', 'Warden'), ('Caretaker', 'Caretaker'), ('Cleaner', 'Cleaner'), ('Security', 'Security')], max_length=20)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.hostel')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('course', models.CharField(max_length=100)),
                ('year_of_study', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('date_registered', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.room')),
            ],
        ),
        migrations.CreateModel(
            name='FeePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_paid', models.DateField(blank=True, null=True)),
                ('receipt_number', models.CharField(max_length=50, unique=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student')),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint_text', models.TextField()),
                ('date_filed', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student')),
            ],
        ),
        migrations.CreateModel(
            name='BedAllocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bed_number', models.PositiveIntegerField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.room')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.student')),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('date_of_visit', models.DateField()),
                ('purpose', models.TextField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student')),
            ],
        ),
    ]
