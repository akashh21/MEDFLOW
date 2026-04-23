from django.shortcuts import render,redirect
from django.http import HttpResponse
from app.models import Doctor,patient



def home(request):
    return render(request, 'home.html')

def doc(request):
    if request.method=='POST':
        n=request.POST['doctor_name']
        s=request.POST['specialization']
        data=Doctor(doctor_name=n,specialization=s)
        data.save()
        return render(request,'index.html',{'key':Doctor.objects.all()})
    return render(request,'index.html')

import pickle

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

def formm(request):
    if request.method == 'POST':
        n = request.POST['patient_name']
        a = int(request.POST['age'])
        dd = request.POST['appointment_date']
        d = request.POST['doctor_name']
        if a<10:
            return HttpResponse("inavlid Age")
        else:
            doc_obj = Doctor.objects.get(id=d)

            patient.objects.create(patient_name=n, age=a,appointment_date=dd, doctor=doc_obj)

    return render(request, 'form.html', {'key': patient.objects.all(),'Doctor': Doctor.objects.all()})


def patient_management(request):
    doctors = Doctor.objects.all()
    doctor_id = request.GET.get('doctor')

    if doctor_id:
        data = patient.objects.filter(doctor_id=doctor_id)
    else:
        data = patient.objects.all()

    return render(request, 'patient_management.html', {
        'data': data,
        'doctors': doctors
    })


def delete_patient(request, id):
    patient.objects.get(id=id).delete()
    return redirect('patient_management')

def delete_doctor(request, id):
    Doctor.objects.get(id=id).delete()
    return redirect('doc')