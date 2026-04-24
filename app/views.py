from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Doctor, patient, UserProfile
import pickle

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            # Redirect to patient management or home based on role
            if hasattr(user, 'userprofile') and user.userprofile.is_doctor:
                return redirect('patient_management')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('home')

def register_patient_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        e = request.POST.get('email')
        if User.objects.filter(username=u).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=u, password=p, email=e)
            UserProfile.objects.create(user=user, is_patient=True)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    return render(request, 'register.html', {'role': 'Patient'})

def register_doctor_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        e = request.POST.get('email')
        n = request.POST.get('doctor_name')
        s = request.POST.get('specialization')
        
        if User.objects.filter(username=u).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=u, password=p, email=e)
            UserProfile.objects.create(user=user, is_doctor=True)
            Doctor.objects.create(user=user, doctor_name=n, specialization=s)
            login(request, user)
            messages.success(request, 'Doctor account created successfully!')
            return redirect('patient_management')
    return render(request, 'register.html', {'role': 'Doctor'})

def doc(request):
    if request.method=='POST':
        n=request.POST.get('doctor_name')
        s=request.POST.get('specialization')
        data=Doctor(doctor_name=n,specialization=s)
        data.save()
        return render(request,'index.html',{'key':Doctor.objects.all()})
    return render(request,'index.html')

@login_required
def sugar(request):
    if request.method == 'POST':
        try:
            pregnancies = int(request.POST['pregnancies'])
            glucose = int(request.POST['glucose'])
            blood_pressure = int(request.POST['blood_pressure'])
            skin_thickness = int(request.POST['skin_thickness'])
            insulin = int(request.POST['insulin'])
            bmi = float(request.POST['bmi'])
            diabetes_pedigree_function = float(request.POST['diabetes_pedigree_function'])
            age = int(request.POST['age'])

            model = pickle.load(open('diabetes_model.pkl', 'rb'))
            prediction = model.predict([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]])

            if prediction[0] == 1:
                result = "The person has sugar (diabetes)."
            else:
                result = "The person does not have sugar (diabetes)."
        except ValueError:
            result = "Error: Please enter valid numerical values for all fields."
        except Exception as e:
            result = f"Error in prediction: {str(e)}"

        return render(request, 'predicthome.html', {'result': result})

    return render(request, 'predicthome.html')

@login_required
def formm(request):
    if request.method == 'POST':
        n = request.POST.get('patient_name')
        a = int(request.POST.get('age'))
        dd = request.POST.get('appointment_date')
        d_id = request.POST.get('doctor_name')
        if a < 10:
            messages.error(request, "Invalid Age. Must be at least 10.")
        else:
            doc_obj = Doctor.objects.get(id=d_id)
            if doc_obj.is_on_leave:
                messages.error(request, 'This doctor is currently on leave.')
            else:
                patient.objects.create(user=request.user, patient_name=n, age=a, appointment_date=dd, doctor=doc_obj)
                messages.success(request, 'Appointment booked successfully! Status is Pending.')
                return redirect('patient_management')

    return render(request, 'form.html', {'key': patient.objects.filter(user=request.user), 'Doctor': Doctor.objects.all()})

@login_required
def patient_management(request):
    # If user is a doctor, show their appointments
    if hasattr(request.user, 'userprofile') and request.user.userprofile.is_doctor:
        try:
            doc_obj = Doctor.objects.get(user=request.user)
            data = patient.objects.filter(doctor=doc_obj)
        except Doctor.DoesNotExist:
            data = []
        return render(request, 'patient_management.html', {'data': data, 'is_doctor': True})
    
    # If user is a patient, show their booked appointments
    data = patient.objects.filter(user=request.user)
    return render(request, 'patient_management.html', {'data': data, 'is_doctor': False})

@login_required
def delete_patient(request, id):
    try:
        p = patient.objects.get(id=id)
        # Check permissions: only the doctor or the patient themselves can delete
        if (hasattr(request.user, 'userprofile') and request.user.userprofile.is_doctor and p.doctor.user == request.user) or p.user == request.user:
            p.delete()
            messages.success(request, 'Appointment deleted.')
        else:
            messages.error(request, 'Permission denied.')
    except patient.DoesNotExist:
        messages.error(request, 'Appointment not found.')
    return redirect('patient_management')

def delete_doctor(request, id):
    Doctor.objects.get(id=id).delete()
    return redirect('doc')

@login_required
def toggle_leave(request):
    if hasattr(request.user, 'userprofile') and request.user.userprofile.is_doctor:
        try:
            doc_obj = Doctor.objects.get(user=request.user)
            doc_obj.is_on_leave = not doc_obj.is_on_leave
            doc_obj.save()
            if doc_obj.is_on_leave:
                messages.success(request, 'You are now marked as ON LEAVE.')
            else:
                messages.success(request, 'You are now marked as AVAILABLE.')
        except Doctor.DoesNotExist:
            messages.error(request, 'Doctor profile not found.')
    return redirect('patient_management')

@login_required
def update_appointment_status(request, id, status):
    if hasattr(request.user, 'userprofile') and request.user.userprofile.is_doctor:
        try:
            p = patient.objects.get(id=id)
            if p.doctor.user == request.user:
                if status in ['Approved', 'Cancelled']:
                    p.status = status
                    p.save()
                    messages.success(request, f'Appointment {status} successfully.')
                else:
                    messages.error(request, 'Invalid status.')
            else:
                messages.error(request, 'Permission denied.')
        except patient.DoesNotExist:
            messages.error(request, 'Appointment not found.')
    return redirect('patient_management')