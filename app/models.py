from django.db import models

class Doctor(models.Model):
    doctor_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.doctor_name} - {self.specialization}"


class patient(models.Model):
    patient_name = models.CharField(max_length=50)
    age = models.IntegerField()
    appointment_date = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient_name} ({self.age})"