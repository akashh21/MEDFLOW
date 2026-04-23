from django.contrib import admin
from app.models import Doctor,patient
admin.site.register(patient)
admin.site.register(Doctor)

# Register your models here.