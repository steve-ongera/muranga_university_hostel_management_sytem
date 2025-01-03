# Generated by Django 5.1.2 on 2024-12-18 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_student_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='current_occupants',
        ),
        migrations.AlterField(
            model_name='room',
            name='capacity',
            field=models.PositiveIntegerField(default=4),
        ),
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bed_number', models.PositiveIntegerField()),
                ('is_occupied', models.BooleanField(default=False)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beds', to='main.room')),
            ],
        ),
    ]
