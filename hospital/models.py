from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name




class Patient(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    mobile_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message='Phone number must be 10 digits')]
    )
    email = models.EmailField(unique=True)
    patient_id = models.CharField(max_length=10, unique=True)  # Unique Patient ID

    def __str__(self):
        return self.name 


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message='Phone number must be 10 digits')]
    )
    email = models.EmailField()
    image = models.ImageField(upload_to='doctor_images/', null=True, blank=True)

    def __str__(self):
        return self.name



class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  
    token_number = models.IntegerField(unique=True, null=True, blank=True)  
    date = models.DateTimeField(default=timezone.now, editable=False)
    consulted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Automatically generate a token number before saving
        if not self.token_number:
            # You can implement your own logic for generating token numbers
            # For simplicity, let's assume a sequential numbering
            last_appointment = Appointment.objects.filter(department=self.department).order_by('-token_number').first()
            if last_appointment:
                self.token_number = last_appointment.token_number + 1
            else:
                self.token_number = 1
        super(Appointment, self).save(*args, **kwargs)



class Consultation(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=255,null=True)  
    consumption_time = models.CharField(max_length=50,null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,)
    illness_reason = models.TextField()
    date = models.DateTimeField(default=timezone.now, editable=False)
    
    def __str__(self):
        return f"{self.date} - {self.patient.name} -  {self.doctor.name} - {self.illness_reason} - Medicine: {self.medicine_name}, Consumption Time: {self.consumption_time}"
    
    def save(self, *args, **kwargs):
        # Set the appointment based on patient and doctor
        if not self.appointment:
            self.appointment = Appointment.objects.filter(
                patient=self.patient, doctor=self.doctor, consulted=True
            ).first()
        super(Consultation, self).save(*args, **kwargs)


# models.py
class Reassignment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    current_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='current_doctor')
    new_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='new_doctor')
    reason = models.TextField()
    consultations = models.ManyToManyField(Consultation, blank=True)

    def __str__(self):
        return f'Reassignment Request for {self.patient.name}'


class Pharmacy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=254, null=True)  # Add the missing email field
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message='Phone number must be 10 digits')]
    )
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.consultation} - {self.patient.name} - {self.doctor.name} - {self.submission_time}"


