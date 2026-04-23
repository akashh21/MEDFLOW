from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doc', views.doc, name='doc'),
    path('formm', views.formm, name='formm'),
    path('sugar', views.sugar, name='sugar'),
    path('patient-management', views.patient_management, name='patient_management'),
    path('delete/<int:id>/', views.delete_patient, name='delete_patient'),
    path('delete-doctor/<int:id>/', views.delete_doctor, name='delete_doctor'),
]