from datetime import date, datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import (
    AppointmentForm, ContactForm, LoginForm, ProfileUpdateForm, UserRegistrationForm,
    AdminUserEditForm, AdminDoctorEditForm, AdminAppointmentEditForm
)
from .models import Appointment, CustomUser, Doctor, SPECIALIZATION_CHOICES


def home(request):
    featured_doctors = Doctor.objects.all()[:6]
    context = {
        'featured_doctors': featured_doctors,
    }
    return render(request, 'booking/home.html', context)


def about(request):
    return render(request, 'booking/about.html')


def services(request):
    return render(request, 'booking/services.html')


def doctors(request):
    doctors = Doctor.objects.all()
    search = request.GET.get('search', '').strip()
    specialization = request.GET.get('specialization', '').strip()
    date_value = request.GET.get('date', '').strip()
    time_value = request.GET.get('time', '').strip()

    if search:
        doctors = doctors.filter(doctor_name__icontains=search)
    if specialization:
        doctors = doctors.filter(specialization__iexact=specialization)
    if date_value:
        try:
            selected_date = datetime.strptime(date_value, '%Y-%m-%d').date()
            if selected_date < date.today():
                messages.error(request, 'Please choose today or a future date.')
            else:
                weekday = selected_date.strftime('%a')
                doctors = doctors.filter(availability__icontains=weekday)
        except ValueError:
            messages.error(request, 'Please select a valid date.')

    if time_value:
        try:
            datetime.strptime(time_value, '%H:%M')
        except ValueError:
            messages.error(request, 'Please select a valid time.')

    context = {
        'doctors': doctors,
        'search': search,
        'specialization': specialization,
        'date_value': date_value,
        'time_value': time_value,
        'specializations': [choice[0] for choice in SPECIALIZATION_CHOICES],
    }
    return render(request, 'booking/doctors.html', context)


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    context = {'doctor': doctor}
    return render(request, 'booking/doctor_detail.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. You are now logged in.')
            login(request, user)
            return redirect('patient_dashboard')
        messages.error(request, 'Please correct the highlighted fields to register successfully.')
    else:
        form = UserRegistrationForm()
    return render(request, 'booking/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('patient_dashboard')
        messages.error(request, 'Login failed. Check your credentials and try again.')
    else:
        form = LoginForm()
    return render(request, 'booking/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def _is_doctor(user):
    return hasattr(user, 'doctor_profile') and user.doctor_profile is not None


def _is_admin(user):
    return user.is_superuser


@login_required
def patient_dashboard(request):
    appointments = Appointment.objects.filter(patient=request.user)
    total = appointments.count()
    upcoming = appointments.filter(appointment_date__gte=date.today(), status__in=['Pending', 'Approved']).count()
    completed = appointments.filter(status='Completed').count()
    cancelled = appointments.filter(status='Cancelled').count()
    context = {
        'appointments': appointments,
        'total': total,
        'upcoming': upcoming,
        'completed': completed,
        'cancelled': cancelled,
    }
    return render(request, 'booking/patient_dashboard.html', context)


@login_required
def doctor_dashboard(request):
    if not _is_doctor(request.user):
        messages.warning(request, 'Doctor dashboard is restricted to doctor accounts.')
        return redirect('home')
    doctor = request.user.doctor_profile
    appointments = Appointment.objects.filter(doctor=doctor)
    pending = appointments.filter(status='Pending').count()
    approved = appointments.filter(status='Approved').count()
    completed = appointments.filter(status='Completed').count()
    cancelled = appointments.filter(status='Cancelled').count()

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'pending': pending,
        'approved': approved,
        'completed': completed,
        'cancelled': cancelled,
    }
    return render(request, 'booking/doctor_dashboard.html', context)


@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, patient=request.user, doctor=doctor)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            appointment.status = 'Pending'
            appointment.save()
            messages.success(request, 'Appointment booked successfully. The doctor will review your request.')
            return redirect('appointment_history')
        messages.error(request, 'There was an issue booking the appointment. Please correct the form.')
    else:
        form = AppointmentForm(patient=request.user, doctor=doctor)
    return render(request, 'booking/book_appointment.html', {'doctor': doctor, 'form': form})


@login_required
def appointment_history(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'booking/appointment_history.html', {'appointments': appointments})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        messages.error(request, 'Please fix the errors in the form.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'booking/profile.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Thank you for contacting us. We will respond soon.')
            return redirect('contact')
        messages.error(request, 'Please correct the contact form.')
    else:
        form = ContactForm()
    return render(request, 'booking/contact.html', {'form': form})


@login_required
def admin_dashboard(request):
    if not _is_admin(request.user):
        messages.warning(request, 'Admin dashboard is available only to administrators.')
        return redirect('home')
    
    appointments = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')
    users = CustomUser.objects.all().order_by('username')
    doctors = Doctor.objects.all().order_by('doctor_name')
    
    user_count = users.count()
    doctor_count = doctors.count()
    appointment_count = appointments.count()
    pending = appointments.filter(status='Pending').count()
    approved = appointments.filter(status='Approved').count()
    completed = appointments.filter(status='Completed').count()
    cancelled = appointments.filter(status='Cancelled').count()
    
    return render(request, 'booking/admin_dashboard.html', {
        'user_count': user_count,
        'doctor_count': doctor_count,
        'appointment_count': appointment_count,
        'pending': pending,
        'approved': approved,
        'completed': completed,
        'cancelled': cancelled,
        'appointments': appointments,
        'users': users,
        'doctors': doctors,
    })


@login_required
def admin_appointment_edit(request, appointment_id):
    if not _is_admin(request.user):
        messages.error(request, 'Unauthorized access.')
        return redirect('home')
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        form = AdminAppointmentEditForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated/postponed successfully.')
            return redirect('admin_dashboard')
        messages.error(request, 'Error updating appointment.')
    else:
        form = AdminAppointmentEditForm(instance=appointment)
    return render(request, 'booking/admin_appointment_edit.html', {'form': form, 'appointment': appointment})


@login_required
def admin_appointment_delete(request, appointment_id):
    if not _is_admin(request.user):
        messages.error(request, 'Unauthorized access.')
        return redirect('home')
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.delete()
    messages.success(request, 'Appointment deleted successfully.')
    return redirect('admin_dashboard')


@login_required
def admin_user_edit(request, user_id):
    if not _is_admin(request.user):
        messages.error(request, 'Unauthorized access.')
        return redirect('home')
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} updated successfully.')
            return redirect('admin_dashboard')
        messages.error(request, 'Error updating user.')
    else:
        form = AdminUserEditForm(instance=user)
    return render(request, 'booking/admin_user_edit.html', {'form': form, 'edit_user': user})


@login_required
def admin_user_delete(request, user_id):
    if not _is_admin(request.user):
        messages.error(request, 'Unauthorized access.')
        return redirect('home')
    user = get_object_or_404(CustomUser, pk=user_id)
    if user == request.user:
        messages.error(request, 'You cannot delete yourself!')
        return redirect('admin_dashboard')
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('admin_dashboard')


@login_required
def admin_doctor_edit(request, doctor_id):
    if not _is_admin(request.user):
        messages.error(request, 'Unauthorized access.')
        return redirect('home')
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    if request.method == 'POST':
        form = AdminDoctorEditForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Doctor profile for {doctor.doctor_name} updated successfully.')
            return redirect('admin_dashboard')
        messages.error(request, 'Error updating doctor profile.')
    else:
        form = AdminDoctorEditForm(instance=doctor)
    return render(request, 'booking/admin_doctor_edit.html', {'form': form, 'doctor': doctor})



@login_required
def doctor_action(request, appointment_id, action):
    if not _is_doctor(request.user):
        messages.error(request, 'Unauthorized action.')
        return redirect('home')
    doctor = request.user.doctor_profile
    appointment = get_object_or_404(Appointment, pk=appointment_id, doctor=doctor)
    if action == 'approve':
        appointment.status = 'Approved'
        messages.success(request, 'Appointment approved successfully.')
    elif action == 'reject':
        appointment.status = 'Cancelled'
        messages.success(request, 'Appointment rejected successfully.')
    elif action == 'complete':
        appointment.status = 'Completed'
        messages.success(request, 'Appointment marked completed.')
    else:
        messages.error(request, 'Invalid action requested.')
        return redirect('doctor_dashboard')
    appointment.save()
    return redirect('doctor_dashboard')


def custom_404(request, exception):
    return render(request, 'booking/404.html', status=404)
