from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Doctor, Appointment


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields': ('phone',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {'fields': ('phone',)}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['doctor_name', 'specialization', 'qualification', 'experience', 'consultation_fee', 'availability']
    search_fields = ['doctor_name', 'specialization']
    list_filter = ['specialization']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'created_at']
    list_filter = ['status', 'appointment_date']
    search_fields = ['patient__username', 'doctor__doctor_name']
