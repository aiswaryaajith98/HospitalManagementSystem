from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient,Appointment,Department,Doctor,Consultation,Reassignment,Pharmacy
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.exceptions import MultipleObjectsReturned
import random
import string
from django.contrib.auth.forms import PasswordChangeForm


class ReceptionSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100, required=True)
    phonenumber = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2','name','phonenumber']

    def __init__(self, *args, **kwargs):
        super(ReceptionSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    



class ReceptionLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'address', 'mobile_number', 'email']



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['department', 'doctor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        departments = Department.objects.all()
        department_choices = [(department.id, department.name) for department in departments]
        self.fields['department'].choices = department_choices

    def set_doctor_choices(self, department_id):
        doctors = Doctor.objects.filter(department_id=department_id)
        doctor_choices = [(doctor.id, doctor.name) for doctor in doctors]
        self.fields['doctor'].choices = doctor_choices

     
        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']


class DoctorSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=15)
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label='Department',
        widget=forms.Select(attrs={'class': 'form-control'}),  
    )
    phone_number = forms.CharField(max_length=10)
    email = forms.EmailField()
    image = forms.ImageField(required=False, label='Profile Image')

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude password field
        self.fields.pop('password')



class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['patient', 'doctor', 'illness_reason', 'medicine_name', 'consumption_time']

    def __init__(self, *args, **kwargs):
        appointment = kwargs.pop('appointment', None)

        super().__init__(*args, **kwargs)
  
        if appointment:
            self.fields['patient'].initial = appointment.patient
            self.fields['doctor'].initial = appointment.doctor

        self.fields['patient'].widget.attrs['class'] = 'readonly-field'
        self.fields['doctor'].widget.attrs['class'] = 'readonly-field'




class ReassignmentForm(forms.ModelForm):
    class Meta:
        model = Reassignment
        fields = ['patient', 'current_doctor', 'new_doctor', 'reason', 'consultations']

    def __init__(self, *args, **kwargs):
        current_doctor = kwargs.pop('current_doctor', None)
        super().__init__(*args, **kwargs)

        # 1. Fetch the patient queryset based on the current doctor
        if current_doctor:
            self.fields['patient'].queryset = Patient.objects.filter(
                consultation__doctor=current_doctor,
                consultation__appointment__isnull=False
            ).distinct()

        # 2. Fetch the current login doctor
        if current_doctor:
            self.fields['current_doctor'].queryset = Doctor.objects.filter(id=current_doctor.id)

        # 3. Fetch the current login doctor's department
        current_department = current_doctor.department if current_doctor else None

        # Exclude doctors from the current department
        if current_department:
            self.fields['new_doctor'].queryset = Doctor.objects.exclude(department=current_department)


class PharmacySignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=100, label='Pharmacy Name')
    phone_number = forms.CharField(max_length=10, label='Phone Number')
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields.pop('password')


class DoctorChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize form labels if needed
        self.fields['old_password'].label = "Old Password"
        self.fields['new_password1'].label = "New Password"
        self.fields['new_password2'].label = "Confirm New Password"

        # Add password validation
        self.fields['new_password1'].widget.attrs['pattern'] = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        self.fields['new_password1'].widget.attrs['title'] = "Must contain at least 8 characters, including at least one letter, one number, and one special character."

        
class PharmacyChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize form labels if needed
        self.fields['old_password'].label = "Old Password"
        self.fields['new_password1'].label = "New Password"
        self.fields['new_password2'].label = "Confirm New Password"

        # Add password validation
        self.fields['new_password1'].widget.attrs['pattern'] = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        self.fields['new_password1'].widget.attrs['title'] = "Must contain at least 8 characters, including at least one letter, one number, and one special character."


class ReceptionChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize form labels if needed
        self.fields['old_password'].label = "Old Password"
        self.fields['new_password1'].label = "New Password"
        self.fields['new_password2'].label = "Confirm New Password"

        # Add password validation
        self.fields['new_password1'].widget.attrs['pattern'] = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        self.fields['new_password1'].widget.attrs['title'] = "Must contain at least 8 characters, including at least one letter, one number, and one special character."