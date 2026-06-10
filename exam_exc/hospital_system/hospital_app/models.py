from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    SPECIALITY_CHOICE = [
        ("cardiologist", "CARDIOLOGIST"),
        ("dermatologist", "DERMATOLOGIST"),
        ("neurologist","NEUROLOGIST")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=101)
    specialty = models.CharField(max_length=51, choices=SPECIALITY_CHOICE)
    image = models.ImageField(upload_to="doctors/",  null=True, blank=True)
    institution = models.CharField(max_length=101)
    completed_appointments = models.PositiveIntegerField(default=0)
    email = models.EmailField()
    phone = models.CharField(max_length=101)

    def __str__(self):
        return self.full_name


class Patient(models.Model):
    GENDER_CHOICES = [
        ("male", "MALE"),
        ("female","FEMALE")
    ]
    full_name = models.CharField(max_length=101)
    birth_date = models.DateField()
    gender = models.CharField(max_length=51, choices=GENDER_CHOICES)
    email = models.EmailField()
    institution = models.CharField(max_length=101)

    def __str__(self):
        return self.full_name

class Appointment(models.Model):
    TYPE_CHOICES = [
        ("cardiology", "CARDIOLOGY"),
        ("dermatology", "DERMATOLOGY"),
        ("neurology", "NEUROLOGY")
    ]

    STATUS_CHOICES = [
        ("scheduled", "SCHEDULED"),
        ("in_progress", "IN PROGRESS"),
        ("completed", "COMPLETED")
    ]

    appointment_type = models.CharField(max_length=51, choices=TYPE_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=51, choices=STATUS_CHOICES, default="scheduled")
    datetime = models.DateTimeField()
    note = models.TextField(blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    responsible_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='responsible_appointments')

    def __str__(self):
        return f"{self.appointment_type} on {self.datetime.strftime('%Y-%m-%d %H:%M')}"


class AppointmentAssignment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        unique_together =('appointment', 'doctor')


    def __str__(self):
        return f"{self.doctor.full_name} assisting {self.appointment}"


