from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .forms import PatientForm,ReceptionSignupForm, ReceptionLoginForm,AppointmentForm,DepartmentForm,DoctorSignUpForm,ConsultationForm,ReassignmentForm,PharmacySignupForm,DoctorChangePasswordForm,ReceptionChangePasswordForm,PharmacyChangePasswordForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import uuid
from .models import Patient, Appointment,Department,Doctor,Consultation,Pharmacy
from django.contrib.auth import logout
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.template.loader import render_to_string
import random
import string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def home(request):
    return render(request, 'index.html')

def reception_base(request):
    return render(request, 'reception/reception_base.html')

def generate_random_password():
    return ''.join(random.choices(string.digits, k=6))
def send_password_email(email, password, user_type):
    if user_type == 'PHARMACY':
        subject = 'Welcome to CoveCare Pharmacy'
    elif user_type == 'DOCTOR':
        subject = 'Welcome Doctor'
    elif user_type == 'RECEPTION':
        subject = 'Welcome Receptionist'
    else:
        subject = 'Your Account Details'  # Default subject

    message = f'Hi, your password is {password}. Please keep it secure.'
    from_email = 'aiswaryaajithprojects@gmail.com'
    send_mail(subject, message, from_email, [email])

def pharmacy_signup(request):
    if request.method == 'POST':
        form = PharmacySignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = generate_random_password()
            user.set_password(password)
            user.save()
            my_pharmacy_group, created = Group.objects.get_or_create(name='PHARMACY')
            my_pharmacy_group.user_set.add(user)
            send_password_email(user.email, password, user_type='PHARMACY')
            messages.success(request, 'Welcome to CoveCare Pharmacy! Your account has been created successfully.')
            login(request, user)
            return redirect('pharmacy_login')
    else:
        form = PharmacySignupForm()
    return render(request, 'pharmacy/pharmacy_signup.html', {'form': form})

def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            password = generate_random_password()
            user.set_password(password)
            user.save()
            my_doctor_group, created = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group.user_set.add(user)
            send_password_email(user.email, password, user_type='DOCTOR')
            doctor = Doctor.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                department=form.cleaned_data['department'],
                phone_number=form.cleaned_data['phone_number'],
                email=user.email,
                image=form.cleaned_data['image'],
            )
            login(request, user)
            print(doctor.name, doctor.user.username, doctor.department, doctor.phone_number, doctor.email)
            return render(request, 'doctor/doctor_login.html', {'doctor': doctor})
    else:
        form = DoctorSignUpForm()
    return render(request, 'doctor/doctor_signup.html', {'form': form})

def reception_signup(request):
    if request.method == 'POST':
        form = ReceptionSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            password = generate_random_password()
            user.set_password(password)
            user.save()
            my_reception_group, created = Group.objects.get_or_create(name='RECEPTION')
            my_reception_group.user_set.add(user)
            send_password_email(user.email, password, user_type='RECEPTION')
            login(request, user)
            
            return redirect('reception_login')
    else:
        form = ReceptionSignupForm()
    return render(request, 'reception/reception_signup.html', {'form': form})


def reception_login(request):
    if request.method == 'POST':
        form = ReceptionLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('reception_home')
    else:
        form = ReceptionLoginForm()
    return render(request, 'reception/reception_login.html', {'form': form})



def is_reception(user):
    return user.groups.filter(name='RECEPTION').exists()


@login_required(login_url='reception_login')
@user_passes_test(is_reception)
def reception_home(request):
    return render(request, 'reception/reception_home.html', {})


def generate_unique_patient_id():
    return str(uuid.uuid4())[:10]
def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)

            patient.patient_id = generate_unique_patient_id()
            patient.save()

            subject = 'Hospital Registration Confirmation'
            message = f'Thank you for registering at our hospital. Your Patient ID is: {patient.patient_id}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [patient.email]
            send_mail(subject, message, from_email, recipient_list)

            return render(request, 'reception/appointment_form.html', {'patient': patient})
    else:
        form = PatientForm()
    return render(request, 'reception/register_patient.html', {'form': form})



@login_required(login_url='reception_login')
@user_passes_test(is_reception)
def generate_token(request):
    return str(uuid.uuid4().int)[:6]
def appointment_form(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.token_number = generate_token(request)
            appointment.save()

            send_token_email(patient.email, appointment.token_number )
            return redirect('appointment_booking', patient_id=patient.patient_id)
    else:
        form = AppointmentForm()

    selected_department_id = request.POST.get('department') 

    if selected_department_id is not None:
        form.set_doctor_choices(selected_department_id)

    return render(request, 'reception/appointment_form.html', {'form': form, 'patient': patient})
def send_token_email(email, token):
    subject = 'Your Appointment Token'
    message = f'Your appointment token is: {token}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

@login_required(login_url='reception_login')
@user_passes_test(is_reception)
def manual_appointment_booking(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        patient = get_object_or_404(Patient, patient_id=patient_id)
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.token_number = generate_token(request) 
            appointment.save()
            send_token_email(patient.email, appointment.token_number)
            return redirect('appointment_booking', patient_id=patient.patient_id)
    else:
        form = AppointmentForm()

        selected_department_id = request.POST.get('department') 

        if selected_department_id is not None:
            form.set_doctor_choices(selected_department_id)
    return render(request, 'reception/manual_appointment_booking.html', {'form': form})


def get_doctors(request):
    department_id = request.GET.get('department_id')
    doctors = Doctor.objects.filter(department_id=department_id)
    doctor_choices = [{'value': doctor.id, 'label': doctor.name} for doctor in doctors]
    return render(request, 'reception/get_doctors.html', {'doctors': doctor_choices})


@login_required(login_url='reception_login')
@user_passes_test(is_reception)
def appointment_booking(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    appointment = Appointment.objects.filter(patient=patient).latest('id')

    return render(request, 'reception/appointment_booking.html', {'patient': patient, 'appointment': appointment})



@login_required(login_url='reception_login')
@user_passes_test(is_reception)
def search_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        if patient_id:
            # If a patient ID is provided, attempt to retrieve the patient from the database.
            patient = get_object_or_404(Patient, patient_id=patient_id)
            appointments = Appointment.objects.filter(patient=patient)
            # Retrieve the appointments associated with the patient.

            return render(request, 'reception/patient_details.html', {'patient': patient, 'appointments': appointments})
            # Render a template showing patient details and consulting history.

    return render(request, 'reception/search_patient.html')
    # If the request method is not POST or if patient ID is not provided, render the search form.





@login_required(login_url='reception_login')
@user_passes_test(is_reception)
def reception_change_password_view(request):
    if request.method == 'POST':
        form = ReceptionChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            update_session_auth_hash(request, user)  
            return redirect('reception_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ReceptionChangePasswordForm(request.user)
    return render(request, 'reception/reception_change_password.html', {'form': form})



@login_required(login_url='reception_login')
@user_passes_test(is_reception)
def patient_details(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    appointments = Appointment.objects.filter(patient=patient)

    return render(request, 'reception/patient_details.html', {'patient': patient, 'appointments': appointments})


@login_required(login_url='reception_login')
@user_passes_test(is_reception)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'reception/department_list.html', {'departments': departments})



@login_required(login_url='reception_login')
@user_passes_test(is_reception)
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'reception/add_department.html', {'form': form})



@login_required(login_url='reception_login')
@user_passes_test(is_reception)
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'reception/edit_department.html', {'form': form, 'department': department})



@login_required(login_url='reception_login')
@user_passes_test(is_reception)
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        department.delete()
        return redirect('department_list')
    return render(request, 'reception/delete_department.html', {'department': department})


def reception_logout(request):
    logout(request)
    return redirect('home') 


# views.py  doctor
def doctor_base(request):
    return render(request, 'doctor/doctor_base.html')



def doctor_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('doctor_home') 
    else:
        form = AuthenticationForm()
    return render(request, 'doctor/doctor_login.html', {'form': form})


def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()


@login_required(login_url='doctor_login')
@user_passes_test(is_doctor)
def doctor_home(request):
    return render(request, 'doctor/doctor_home.html', {'user': request.user})



def doctor_logout(request):
    logout(request)
    return redirect('doctor_login')


def doctor_appointment_list(request):
    doctor_appointments = Appointment.objects.filter(doctor=request.user.doctor) 
    return render(request, 'doctor/doctor_appointment_list.html', {'doctor_appointments': doctor_appointments})

@login_required(login_url='doctor_login')
@user_passes_test(is_doctor)
def doctor_change_password_view(request):
    if request.method == 'POST':
        form = DoctorChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            update_session_auth_hash(request, user)  
            return redirect('doctor_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = DoctorChangePasswordForm(request.user)
    return render(request, 'doctor/doctor_change_password.html', {'form': form})


@login_required(login_url='doctor_login')
@user_passes_test(is_doctor)
def doctor_search_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        if patient_id:
            patient = get_object_or_404(Patient, patient_id=patient_id)
            consultation_history = Consultation.objects.filter(patient=patient)
            return render(request, 'doctor/doctor_patient_details.html', {'patient': patient,'consultation_history': consultation_history})
    return render(request, 'doctor/doctor_search_patient.html')


def doctor_patient_details(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    consultation_history = Consultation.objects.filter(patient=patient)
    context = {
        'patient': patient,
        'consultation_history': consultation_history,
    }
    return render(request, 'doctor/doctor_patient_details.html', context)




def consultation_page(request, appointment_token, patient_id):
    appointment = get_object_or_404(Appointment, token_number=appointment_token, patient__patient_id=patient_id)
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            print("Form is valid. Proceeding...")
            consultation = form.save(commit=False)
            consultation.appointment = appointment
            consultation.doctor = request.user.doctor  
            consultation.patient = appointment.patient  
            consultation.save()
            appointment.consulted = True
            appointment.save()
            print("Consultation saved successfully.")
            return redirect('doctor_appointment_list')
        else:
            print("Form is not valid.")
            print(form.errors)
    else:
        form = ConsultationForm()
    form.fields['patient'].initial = appointment.patient
    form.fields['doctor'].initial = request.user.doctor

    return render(request, 'doctor/consultation.html', {'form': form, 'appointment': appointment})


def reassign_patient(request):
    if request.method == 'POST':
        form = ReassignmentForm(request.POST, current_doctor=request.user.doctor)
        if form.is_valid():
            reassignment = form.save()
            return redirect('doctor_home')      
    else:
        form = ReassignmentForm(current_doctor=request.user.doctor)
    patient_id = request.GET.get('patient_id')
    if patient_id:
        consultations = Consultation.objects.filter(patient_id=patient_id)
    else:
        consultations = []
    context = {'form': form, 'consultations': consultations}
    return render(request, 'doctor/reassign_patient.html', context)


def is_pharmacy(user):
    return user.groups.filter(name='PHARMACY').exists()


def pharmacy_base(request):
    return render(request, 'pharmacy/pharmacy_base.html')



def pharmacy_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pharmacy_home')  # Adjust to your actual pharmacy dashboard URL
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'pharmacy/pharmacy_login.html', {'form': form})


def pharmacy_logout(request):
    logout(request)
    return redirect('pharmacy_login')


@login_required(login_url='pharmacy_login')
@user_passes_test(is_pharmacy)
def pharmacy_home(request):
    return render(request, 'pharmacy/pharmacy_home.html')


def recently_submitted_consultations(request):
    recently_submitted_consultations = Consultation.objects.all().order_by('-date')[:10]
    return render(request, 'pharmacy/recently_submitted_consultations.html', {
        'recently_submitted_consultations': recently_submitted_consultations
    })



@login_required(login_url='pharmacy_login')
@user_passes_test(is_pharmacy)
def pharmacy_search_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        if patient_id:
            patient = get_object_or_404(Patient, patient_id=patient_id)
            consultation_history = Consultation.objects.filter(patient=patient)
            return render(request, 'pharmacy/pharmacy_patient_details.html', {'patient': patient,'consultation_history': consultation_history})
    return render(request, 'pharmacy/pharmacy_search_patient.html')


def pharmacy_patient_details(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    consultation_history = Consultation.objects.filter(patient=patient)
    context = {
        'patient': patient,
        'consultation_history': consultation_history,
    }
    return render(request, 'pharmacy/pharmacy_patient_details.html', context)



def patient_consultation_history(request, patient_id):
    consultation_history = Consultation.objects.filter(patient__patient_id=patient_id).order_by('-date')

    return render(request, 'pharmacy/patient_consultation_history.html', {
        'consultation_history': consultation_history
    })


@login_required(login_url='pharmacy_login')
@user_passes_test(is_pharmacy)
def pharmacy_change_password_view(request):
    if request.method == 'POST':
        form = PharmacyChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            update_session_auth_hash(request, user)  
            return redirect('pharmacy_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PharmacyChangePasswordForm(request.user)
    return render(request, 'pharmacy/pharmacy_change_password.html', {'form': form})