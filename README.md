# University Learning Management System (LMS)

A comprehensive, role-based Learning Management System built with **Django 5.0** and **PostgreSQL**. This platform facilitates academic management by organizing departments, programs, courses, and user interactions (assignments, grading, polling, and notifications).

### 🎥 Live Demo
*GitHub Markdown does not support direct video embeds.*  
**[👉 Click here to watch the Live Demo Video on LinkedIn](https://www.linkedin.com/embed/feed/update/urn:li:ugcPost:7359905851928625152?collapsed=1)**

## 🚀 Features

*   **Role-Based Access Control:** Custom user model supporting `Admin`, `Teacher`, `Student`, and `Department Manager` roles.
*   **Department & Program Management:** Organize academics logically with dedicated departments and program structures.
*   **Course Management:** Teachers can create lectures, upload study materials (PDFs, Videos), and manage assignments.
*   **Enrollment System:** Students can enroll in courses, which require admin/teacher approval before granting access.
*   **Assignments & Grading:** Students can submit text or files for assignments. Teachers can review submissions, assign marks, and provide feedback.
*   **Communication:** Built-in apps for global notifications and polls/surveys.

## 🛠️ Technology Stack

*   **Backend:** Python 3.x, Django 5.0.6
*   **Database:** PostgreSQL (`psycopg2`)
*   **Environment Setup:** `python-dotenv` for securely managing secrets.
*   **Frontend:** Server-Side Rendered Django Templates (HTML, CSS, JS)

## 📁 Project Structure

```
university-lms-django/
│
├── accounts/       # Custom user models, authentication, and role logic
├── courses/        # Course, Lecture, Assignment, Submission, and Grading models
├── departments/    # Department and Program models
├── notifications/  # System-wide alert and notification logic
├── polls/          # Voting, surveying, and feedback logic
├── results/        # Examination and final result management
├── static/         # Global static files (CSS, JS, Images)
├── templates/      # Global HTML templates (base.html, etc.)
└── lms_project/    # Core project settings and configurations
```

## ⚙️ Local Installation & Setup

Follow these steps to run the project locally on your machine.

### 1. Prerequisites
*   Python 3.10+ installed
*   PostgreSQL installed and running
*   Git installed

### 2. Database Configuration
Create a PostgreSQL database for the project. Open your `psql` terminal or pgAdmin and run:
```sql
CREATE DATABASE lms_db;
CREATE USER postgres WITH PASSWORD 'your_secure_password';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE lms_db TO postgres;
```

### 3. Clone & Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/codedbyasim/university-lms-django.git
cd university-lms-django

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup Environment Variables
The project uses environment variables to keep sensitive data like passwords and secret keys secure.
1. Create a `.env` file in the root directory (or rename `.env.example` to `.env`).
2. Add your database credentials and Django secret key to it:
```env
SECRET_KEY=your-secret-key-goes-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=lms_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Run Migrations
Apply the database schemas:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Admin)
Create an admin account to access the Django backend:
```bash
python manage.py createsuperuser
```

### 8. Run the Server
Start the development server:
```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/`. You will be redirected to the login page. Admin dashboard is available at `http://127.0.0.1:8000/admin/`.

## 🤝 Contributing
For any additional changes, please ensure that you create a new app using `python manage.py startapp <app_name>` and register it in `lms_project/settings.py` under `INSTALLED_APPS`.
