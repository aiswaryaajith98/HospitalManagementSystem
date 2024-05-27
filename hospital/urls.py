from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    
    path('reception_base', views.reception_base, name='reception_base'),
    path('reception_home', views.reception_home, name='reception_home'),

    path('reception_signup/', views.reception_signup, name='reception_signup'),
    path('reception_login/', views.reception_login, name='reception_login'),


    path('register_patient/', views.register_patient, name='register_patient'),
    path('appointment_form/<str:patient_id>/', views.appointment_form, name='appointment_form'),
    path('manual_appointment_booking/', views.manual_appointment_booking, name='manual_appointment_booking'),
    path('appointment_booking/<str:patient_id>/', views.appointment_booking, name='appointment_booking'),
    path('get_doctors/', views.get_doctors, name='get_doctors'),


    path('search_patient/', views.search_patient, name='search_patient'),
    path('patient_details/<str:patient_id>/', views.patient_details, name='patient_details'),


    path('department_list/', views.department_list, name='department_list'),
    path('add_department/', views.add_department, name='add_department'),
    path('edit_department/<int:department_id>/', views.edit_department, name='edit_department'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),

    path('reception_logout/', views.reception_logout, name='reception_logout'),

    path('reception_change_password/', views.reception_change_password_view, name='reception_change_password'),
    

    #doctor urls.py

    path('doctor_base/', views.doctor_base, name='doctor_base'),
    path('doctor_signup/', views.doctor_signup, name='doctor_signup'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('doctor_home/', views.doctor_home, name='doctor_home'),
    path('doctor_logout/', views.doctor_logout, name='doctor_logout'),

    path('doctor_change_password/', views.doctor_change_password_view, name='doctor_change_password'),

    path('doctor_appointment_list/', views.doctor_appointment_list, name='doctor_appointment_list'),
    path('doctor_search_patient/', views.doctor_search_patient, name='doctor_search_patient'),
    path('doctor_patient_details/<int:patient_id>/', views.doctor_patient_details, name='doctor_patient_details'),

    path('consultation/<int:appointment_token>/<str:patient_id>/', views.consultation_page, name='consultation_page'),
    path('reassign_patient/', views.reassign_patient, name='reassign_patient'),
    
    
    #pharmacy

    path('pharmacy_base/', views.pharmacy_base, name='pharmacy_base'),
    path('pharmacy_signup/', views.pharmacy_signup, name='pharmacy_signup'),
    path('pharmacy_login/', views.pharmacy_login, name='pharmacy_login'),
    path('pharmacy_home/', views.pharmacy_home, name='pharmacy_home'),
    path('recently-submitted-consultations/', views.recently_submitted_consultations, name='recently_submitted_consultations'),
    path('pharmacy_logout/', views.pharmacy_logout, name='pharmacy_logout'),


    path('pharmacy_search_patient/', views.pharmacy_search_patient, name='pharmacy_search_patient'),
    path('pharmacy_patient_details/<int:patient_id>/', views.pharmacy_patient_details, name='pharmacy_patient_details'),
    path('patient-consultation-history/<str:patient_id>/', views.patient_consultation_history, name='patient_consultation_history'),

    path('pharmacy_change_password/', views.pharmacy_change_password_view, name='pharmacy_change_password'),
]   