# Hospital Management & Diabetes Prediction System

A Django-based web application that serves as a unified platform for hospital management and predictive healthcare. It enables administrators or hospital staff to manage doctors and patients, while also offering an integrated machine learning feature to predict diabetes based on patient health metrics.

## Features

- **Doctor Management:** Add new doctors and specify their specialization. View and delete existing doctor profiles.
- **Patient Management:** Register new patients, assign them to available doctors, and record appointment dates. View a comprehensive list of patients or filter them by their assigned doctor.
- **Diabetes Prediction:** A dedicated module that utilizes a pre-trained machine learning model (`diabetes_model.pkl`) to predict the likelihood of diabetes. It takes multiple health factors (pregnancies, glucose, blood pressure, skin thickness, insulin, BMI, diabetes pedigree function, age) and outputs a diagnostic prediction.

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite3 (default)
- **Machine Learning:** `pickle` for loading the pre-trained diabetes prediction model (typically requires `scikit-learn` depending on how the model was trained).
- **Frontend:** HTML/CSS (Django Templates)

## Project Structure

- `app/` - The main application containing models, views, and URL routing for the project's logic.
  - `models.py` - Defines the `Doctor` and `patient` models.
  - `views.py` - Contains the logic for the application, including doctor/patient management and the ML model integration.
  - `urls.py` - Handles application-level routing.
- `hostpital/` - The main project configuration directory.
- `template/` - Contains all HTML templates for the frontend (`home.html`, `index.html`, `form.html`, `patient_management.html`, `predicthome.html`).
- `static/` - Stores static assets like CSS, JavaScript, and images.
- `media/` - Directory for user-uploaded media files.
- `diabetes_model.pkl` - The serialized ML model used for diabetes prediction.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Django 4.x/5.x (or compatible version)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd hostpital
   ```

2. **Install dependencies:**
   Make sure Django and standard ML libraries are installed (required for the pickle model to load correctly).
   ```bash
   pip install django scikit-learn numpy pandas
   ```

3. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000/`.

## Endpoints

- `/` - Home page
- `/doc` - Add/View Doctors
- `/formm` - Add a new Patient
- `/patient-management` - View and manage patients
- `/sugar` - Diabetes prediction form
- `/delete/<int:id>/` - Delete a patient
- `/delete-doctor/<int:id>/` - Delete a doctor
