from django.db import migrations


def load_sample_doctors(apps, schema_editor):
    Doctor = apps.get_model('booking', 'Doctor')

    sample_doctors = [
        {
            'doctor_name': 'Dr. Aarti Sharma',
            'specialization': 'Cardiologist',
            'qualification': 'MBBS, MD (Cardiology)',
            'experience': '12 years',
            'consultation_fee': '1200.00',
            'availability': 'Mon, Wed, Fri - 10AM to 3PM',
            'description': 'Specialist in cardiac care and preventive cardiology.',
        },
        {
            'doctor_name': 'Dr. Karan Mehta',
            'specialization': 'Cardiologist',
            'qualification': 'MBBS, DM (Cardiology)',
            'experience': '15 years',
            'consultation_fee': '1500.00',
            'availability': 'Tue, Thu - 11AM to 4PM',
            'description': 'Experienced in heart disease management and care plans.',
        },
        {
            'doctor_name': 'Dr. Nisha Kapoor',
            'specialization': 'Dermatologist',
            'qualification': 'MBBS, MD (Dermatology)',
            'experience': '10 years',
            'consultation_fee': '900.00',
            'availability': 'Mon, Thu - 10AM to 2PM',
            'description': 'Expert in skincare and dermatological treatments.',
        },
        {
            'doctor_name': 'Dr. Rahul Gupta',
            'specialization': 'Dermatologist',
            'qualification': 'MBBS, DDV',
            'experience': '11 years',
            'consultation_fee': '950.00',
            'availability': 'Wed, Fri - 12PM to 5PM',
            'description': 'Focuses on acne, pigmentation, and clinical dermatology.',
        },
        {
            'doctor_name': 'Dr. Priya Nair',
            'specialization': 'Neurologist',
            'qualification': 'MBBS, DM (Neurology)',
            'experience': '13 years',
            'consultation_fee': '1400.00',
            'availability': 'Tue, Sat - 10AM to 2PM',
            'description': 'Neuro specialist for headache and nerve disorders.',
        },
        {
            'doctor_name': 'Dr. Anil Verma',
            'specialization': 'Neurologist',
            'qualification': 'MBBS, MD (Neurology)',
            'experience': '14 years',
            'consultation_fee': '1450.00',
            'availability': 'Mon, Fri - 2PM to 6PM',
            'description': 'Experienced in stroke care and neurological rehabilitation.',
        },
        {
            'doctor_name': 'Dr. Meenakshi Rao',
            'specialization': 'Orthopedic',
            'qualification': 'MBBS, MS (Orthopedics)',
            'experience': '10 years',
            'consultation_fee': '1100.00',
            'availability': 'Mon, Wed, Sat - 11AM to 3PM',
            'description': 'Orthopedic surgeon specializing in joint and bone health.',
        },
        {
            'doctor_name': 'Dr. Vikram Singh',
            'specialization': 'Orthopedic',
            'qualification': 'MBBS, DNB (Orthopedics)',
            'experience': '12 years',
            'consultation_fee': '1150.00',
            'availability': 'Tue, Thu - 1PM to 5PM',
            'description': 'Focuses on sports injuries and fracture care.',
        },
        {
            'doctor_name': 'Dr. Sneha Patel',
            'specialization': 'Dentist',
            'qualification': 'BDS, MDS (Conservative Dentistry)',
            'experience': '9 years',
            'consultation_fee': '700.00',
            'availability': 'Mon, Wed, Fri - 9AM to 1PM',
            'description': 'Dental care expert for smiles and oral health.',
        },
        {
            'doctor_name': 'Dr. Arjun Desai',
            'specialization': 'Dentist',
            'qualification': 'BDS, MDS (Orthodontics)',
            'experience': '11 years',
            'consultation_fee': '850.00',
            'availability': 'Tue, Thu - 11AM to 4PM',
            'description': 'Specialist in braces, crowns, and dental rehabilitation.',
        },
        {
            'doctor_name': 'Dr. Kavya Iyer',
            'specialization': 'Pediatrician',
            'qualification': 'MBBS, MD (Pediatrics)',
            'experience': '8 years',
            'consultation_fee': '900.00',
            'availability': 'Mon, Wed, Fri - 10AM to 2PM',
            'description': 'Child health specialist for infants and teens.',
        },
        {
            'doctor_name': 'Dr. Sameer Joshi',
            'specialization': 'Pediatrician',
            'qualification': 'MBBS, DCH',
            'experience': '10 years',
            'consultation_fee': '950.00',
            'availability': 'Tue, Thu - 1PM to 5PM',
            'description': 'Experienced pediatrician for preventive care and immunizations.',
        },
        {
            'doctor_name': 'Dr. Ritu Malhotra',
            'specialization': 'General Physician',
            'qualification': 'MBBS, MD (General Medicine)',
            'experience': '15 years',
            'consultation_fee': '800.00',
            'availability': 'Mon to Fri - 9AM to 1PM',
            'description': 'General physician for comprehensive medical care.',
        },
        {
            'doctor_name': 'Dr. Sunil Chawla',
            'specialization': 'General Physician',
            'qualification': 'MBBS',
            'experience': '13 years',
            'consultation_fee': '750.00',
            'availability': 'Tue to Sat - 2PM to 6PM',
            'description': 'General health expert for routine and follow-up consultations.',
        },
    ]

    for doctor_data in sample_doctors:
        Doctor.objects.update_or_create(
            doctor_name=doctor_data['doctor_name'],
            specialization=doctor_data['specialization'],
            defaults={
                'qualification': doctor_data['qualification'],
                'experience': doctor_data['experience'],
                'consultation_fee': doctor_data['consultation_fee'],
                'availability': doctor_data['availability'],
                'description': doctor_data['description'],
            },
        )


def unload_sample_doctors(apps, schema_editor):
    Doctor = apps.get_model('booking', 'Doctor')
    sample_names = [
        'Dr. Aarti Sharma', 'Dr. Karan Mehta',
        'Dr. Nisha Kapoor', 'Dr. Rahul Gupta',
        'Dr. Priya Nair', 'Dr. Anil Verma',
        'Dr. Meenakshi Rao', 'Dr. Vikram Singh',
        'Dr. Sneha Patel', 'Dr. Arjun Desai',
        'Dr. Kavya Iyer', 'Dr. Sameer Joshi',
        'Dr. Ritu Malhotra', 'Dr. Sunil Chawla',
    ]
    Doctor.objects.filter(doctor_name__in=sample_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_sample_doctors, reverse_code=unload_sample_doctors),
    ]
