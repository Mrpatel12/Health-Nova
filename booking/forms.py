from datetime import date
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput
from .models import CustomUser, Appointment, Doctor


class UserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=120, required=True, label='Full Name')
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True, label='Phone Number')

    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'autocomplete': 'new-password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with this email already exists.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone.isdigit():
            raise ValidationError('Phone number must contain only digits.')
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name', '').strip()
        name_parts = full_name.split(' ', 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username_or_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')
        if username_or_email and password:
            user = authenticate(
                username=username_or_email,
                password=password,
            )
            if user is None:
                try:
                    user_obj = CustomUser.objects.get(email__iexact=username_or_email)
                    user = authenticate(username=user_obj.username, password=password)
                except CustomUser.DoesNotExist:
                    user = None
            if user is None:
                raise ValidationError('Invalid credentials. Please try again.')
            cleaned_data['user'] = user
        return cleaned_data


class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    appointment_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'symptoms', 'contact_number']

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)
        self.doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['contact_number'].widget.attrs.update({'placeholder': 'Enter your contact number'})
        self.fields['symptoms'].widget.attrs.update({'rows': 4})

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        if appointment_date < date.today():
            raise ValidationError('Please select a future date for the appointment.')
        return appointment_date

    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number', '').strip()
        if not contact.isdigit():
            raise ValidationError('Contact number must contain digits only.')
        return contact

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        if self.patient and self.doctor and appointment_date and appointment_time:
            exists = Appointment.objects.filter(
                patient=self.patient,
                doctor=self.doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
            ).exists()
            if exists:
                raise ValidationError('You already have an appointment booked with this doctor for the selected slot.')
        return cleaned_data


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    subject = forms.CharField(max_length=180)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'rows': 5})


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This email is already in use.')
        return email


class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'is_staff', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This email is already in use.')
        return email


class AdminDoctorEditForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['doctor_name', 'specialization', 'qualification', 'experience', 'consultation_fee', 'availability', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control', 'rows': 4})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class AdminAppointmentEditForm(forms.ModelForm):
    appointment_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    appointment_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'symptoms', 'contact_number', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

