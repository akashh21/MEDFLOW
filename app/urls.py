from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/patient/', views.register_patient_view, name='register_patient'),
    path('register/doctor/', views.register_doctor_view, name='register_doctor'),
    path('doc', views.doc, name='doc'),
    path('formm', views.formm, name='formm'),
    path('sugar', views.sugar, name='sugar'),
    path('patient-management', views.patient_management, name='patient_management'),
    path('delete/<int:id>/', views.delete_patient, name='delete_patient'),
    path('delete-doctor/<int:id>/', views.delete_doctor, name='delete_doctor'),
    path('toggle-leave/', views.toggle_leave, name='toggle_leave'),
    path('update-status/<int:id>/<str:status>/', views.update_appointment_status, name='update_status'),
]