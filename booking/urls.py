from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('appointments/history/', views.appointment_history, name='appointment_history'),
    path('profile/', views.profile_view, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('portal-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('portal-admin/appointment/edit/<int:appointment_id>/', views.admin_appointment_edit, name='admin_appointment_edit'),
    path('portal-admin/appointment/delete/<int:appointment_id>/', views.admin_appointment_delete, name='admin_appointment_delete'),
    path('portal-admin/user/edit/<int:user_id>/', views.admin_user_edit, name='admin_user_edit'),
    path('portal-admin/user/delete/<int:user_id>/', views.admin_user_delete, name='admin_user_delete'),
    path('portal-admin/doctor/edit/<int:doctor_id>/', views.admin_doctor_edit, name='admin_doctor_edit'),
    path('doctor/action/<int:appointment_id>/<str:action>/', views.doctor_action, name='doctor_action'),
]
