from django.core.management.base import BaseCommand
from django.db import transaction
from main.models import Room, Bed

class Command(BaseCommand):
    help = 'Populate 4 beds for each room'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            rooms = Room.objects.all()
            beds_created = 0

            for room in rooms:
                if room.beds.exists():
                    self.stdout.write(f"Beds already exist for Room {room.room_number}. Skipping.")
                    continue

                for bed_number in range(1, 5):
                    Bed.objects.create(
                        bed_number=bed_number,
                        room=room,
                        is_occupied=False
                    )
                    beds_created += 1

                self.stdout.write(f"Created 4 beds for Room {room.room_number}.")

            self.stdout.write(f"Total beds created: {beds_created}")
