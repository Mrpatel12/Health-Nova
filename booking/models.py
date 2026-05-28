from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

PHONE_VALIDATOR = RegexValidator(r'^\d{10,15}$', 'Enter a valid phone number with digits only.')

SPECIALIZATION_CHOICES = [
    ('Cardiologist', 'Cardiologist'),
    ('Dermatologist', 'Dermatologist'),
    ('Neurologist', 'Neurologist'),
    ('Orthopedic', 'Orthopedic'),
    ('Dentist', 'Dentist'),
    ('Pediatrician', 'Pediatrician'),
    ('General Physician', 'General Physician'),
]

APPOINTMENT_STATUS = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
]


def doctor_image_upload_path(instance, filename):
    return f'doctors/{instance.doctor_name.replace(" ", "_")}/{filename}'


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, validators=[PHONE_VALIDATOR])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='doctor_profile')
    doctor_name = models.CharField(max_length=120)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    qualification = models.CharField(max_length=120)
    experience = models.CharField(max_length=50)
    consultation_fee = models.DecimalField(max_digits=7, decimal_places=2)
    availability = models.CharField(max_length=120, blank=True)
    profile_image = models.ImageField(upload_to=doctor_image_upload_path, blank=True, null=True)
    description = models.TextField(blank=True)

    @property
    def default_image_url(self):
        default_images = {
            'Dr. Aarti Sharma': 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?q=80&w=900&auto=format&fit=crop',
            'Dr. Karan Mehta': 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?q=80&w=900&auto=format&fit=crop',
            'Dr. Nisha Kapoor': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=900&auto=format&fit=crop',
            'Dr. Rahul Gupta': 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?q=80&w=900&auto=format&fit=crop',
            'Dr. Priya Nair': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=900&auto=format&fit=crop',
            'Dr. Anil Verma': 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?q=80&w=900&auto=format&fit=crop',
            'Dr. Meenakshi Rao': 'https://images.unsplash.com/photo-1550831107-1553da8c8464?q=80&w=900&auto=format&fit=crop',
            'Dr. Vikram Singh': 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?q=80&w=900&auto=format&fit=crop',
            'Dr. Sneha Patel': 'https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=900&auto=format&fit=crop',
            'Dr. Arjun Desai': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=900&auto=format&fit=crop',
            'Dr. Kavya Iyer': 'https://images.unsplash.com/photo-1527613426441-4da17471b66d?q=80&w=900&auto=format&fit=crop',
            'Dr. Sameer Joshi': 'https://images.unsplash.com/photo-1614608682850-e0d6ed316d47?q=80&w=900&auto=format&fit=crop',
            'Dr. Ritu Malhotra': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=900&auto=format&fit=crop',
            'Dr. Sunil Chawla': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=900&auto=format&fit=crop',
        }
        return default_images.get(self.doctor_name, 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?q=80&w=900&auto=format&fit=crop')

    def __str__(self):
        return f'{self.doctor_name} ({self.specialization})'


class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    symptoms = models.TextField(blank=True)
    contact_number = models.CharField(max_length=15, validators=[PHONE_VALIDATOR])
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('patient', 'doctor', 'appointment_date', 'appointment_time')
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f'{self.patient.username} – {self.doctor.doctor_name} on {self.appointment_date} {self.appointment_time}'
