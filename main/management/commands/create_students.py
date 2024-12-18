import random
from faker import Faker
from django.core.management.base import BaseCommand
from main.models import Student, Room  # Replace 'your_app' with your app name

class Command(BaseCommand):
    help = 'Create 1000 students with a different list of Kenyan names'

    def handle(self, *args, **kwargs):
        fake = Faker()
        gender_choices = ['Male', 'Female']
        courses = [
            'Accounting', 'Agriculture', 'Architecture', 'Biotechnology', 
            'Economics', 'Software Engineering', 'Statistics', 'Journalism'
        ]

        # New list of male names
        kenyan_first_names_male = [
            'Elias', 'Isaac', 'Geoffrey', 'Oscar', 'Abel', 'Harrison', 'Stephen', 'Cliff', 'Rodney', 'Frank',
            'Julius', 'Elvis', 'Duncan', 'Cyrus', 'Benson', 'Timothy', 'Leonard', 'Wilfred', 'Morris', 'Edgar',
            'Boniface', 'Fred', 'Wilson', 'Oliver', 'Peter', 'Raphael', 'Lawrence', 'Phillip', 'Simon', 'Eddie',
            'Jonah', 'Evans', 'Amos', 'Victor', 'Ian', 'Noah', 'Sylvester', 'Gideon', 'Richard', 'Francis',
            'Patrick', 'Kenneth', 'Antony', 'Collins', 'Newton', 'Jeremiah', 'Laban', 'Samson', 'Gilbert', 'Enock'
        ]
        
        # New list of female names
        kenyan_first_names_female = [
            'Aisha', 'Betty', 'Caroline', 'Cynthia', 'Doreen', 'Edna', 'Evelyn', 'Florence', 'Gloria', 'Janet',
            'Joan', 'Josephine', 'Joy', 'Lilian', 'Maureen', 'Mercy', 'Millicent', 'Phoebe', 'Priscilla', 'Rachel',
            'Regina', 'Rose', 'Selina', 'Sophia', 'Stella', 'Susan', 'Terry', 'Tracy', 'Violet', 'Vivian',
            'Winnie', 'Angela', 'Deborah', 'Lucy', 'Irene', 'Felicity', 'Daisy', 'Clare', 'Hilda', 'Zawadi',
            'Fatuma', 'Halima', 'Saida', 'Zena', 'Rukia', 'Kadzo', 'Mariam', 'Leila', 'Shani', 'Sofia'
        ]

        # New list of last names
        kenyan_last_names = [
            'Odongo', 'Kiplagat', 'Langat', 'Kibet', 'Cheruiyot', 'Chepkwony', 'Rotich', 'Koech', 'Wekesa', 'Simiyu',
            'Mutua', 'Musyoka', 'Kitheka', 'Mwanzia', 'Kimani', 'Kamotho', 'Gikonyo', 'Wambugu', 'Muthee', 'Njenga',
            'Nyaga', 'Karimi', 'Muthoni', 'Kanyiri', 'Nduta', 'Wairimu', 'Mulei', 'Kilonzo', 'Makau', 'Kivuva',
            'Mutugi', 'Thiong’o', 'Ngugi', 'Kiarie', 'Muiruri', 'Nyongesa', 'Ogola', 'Amollo', 'Okoth', 'Okumu',
            'Wandera', 'Owuor', 'Mabonga', 'Abuya', 'Ouma', 'Otuma', 'Oduor', 'Kariuki', 'Mwangi', 'Gitonga'
        ]
        
        rooms = list(Room.objects.all())  # Fetch available rooms
        students = []

        for _ in range(1000):
            gender = random.choice(gender_choices)
            if gender == 'Male':
                first_name = random.choice(kenyan_first_names_male)
            else:
                first_name = random.choice(kenyan_first_names_female)
            last_name = random.choice(kenyan_last_names)
            student_id = fake.unique.random_number(digits=8, fix_len=True)
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"
            phone_number = f"+2547{random.randint(0, 9)}{random.randint(100000, 999999)}"
            course = random.choice(courses)
            year_of_study = random.randint(1, 4)
            room = random.choice(rooms) if rooms else None
            
            students.append(Student(
                student_id=student_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                course=course,
                year_of_study=year_of_study,
                gender=gender,
                room=room,
            ))

        # Bulk create students
        Student.objects.bulk_create(students)
        self.stdout.write(self.style.SUCCESS('Successfully created another 1000 students.'))
