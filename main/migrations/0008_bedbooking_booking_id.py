# Generated by Django 5.1.2 on 2024-12-20 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_bedbooking_amount_bedbooking_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bedbooking',
            name='booking_id',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
