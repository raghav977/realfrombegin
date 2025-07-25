# 🏢 School Management System – Django + DRF + Google OAuth2

A comprehensive school management system backend built with **Django 5**, **Django REST Framework**, and **Google OAuth2** login. It features modular apps, multi-role login (Principal, Staff, Teacher, Student), JWT authentication, and a clean RESTful API architecture.

---

## 🚀 Features

* ✅ Google OAuth2 login for principals
* ✅ Custom roles: Principal, Staff, Teacher, Student
* ✅ Role-based login and permissions
* ✅ JWT Authentication (`rest_framework_simplejwt`)
* ✅ Modular architecture for apps like school, section, class, subject, result, and attendance
* ✅ Multi-database setup with router
* ✅ CORS-enabled for frontend integration
* ✅ Environment variable handling with `.env`
* ✅ Clean & production-friendly project structure

---

## 📦 Tech Stack

* **Python 3.11+**
* **Django 5.2+**
* **Django REST Framework**
* **Simple JWT**
* **social-auth-app-django**
* **django-role-permissions**
* **MySQL**
* **CORS Headers**

---

## 🛠️ Setup Instructions

### 🔀 1. Clone the repository

```bash
git clone https://github.com/raghav977/realfrombegin.git
cd realfrombegin
```

---

### 📦 2. Set up virtual environment

```bash
python -m venv venv
venv\Scripts\activate     # On Windows
# OR
source venv/bin/activate  # On macOS/Linux
```

---



---

### 📓 4. Create `.env` in the root folder

```env
# core Django settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Google OAuth2 credentials
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Database (used in settings.py directly)
DB_USER=root
DB_PASSWORD=Root@123
DB_NAME=digitalpathsala
DB_HOST=localhost
DB_PORT=3306
```

✅ `.env` is already included in `.gitignore` for safety.

---

### 📇 5. MySQL Configuration

Create  databases manually in MySQL:

```sql
CREATE DATABASE digitalpathsala;

```

Ensure your `.env` or `settings.py` matches the credentials.

---

### ⚙️ 6. Apply migrations

```bash
python manage.py migrate
```

---

### 👤 7. Create a superuser

```bash
python manage.py createsuperuser
```

---

### ▶️ 8. Run the server

```bash
python manage.py runserver
```

Access at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧱 Project Structure

```
realfrombegin/
├── accounts/            # Custom user model & auth
├── attendance/          # Attendance tracking
├── assignments/         # Assignment handling
├── classes/             # Class & section management
├── core/                # Project settings
├── dashboard/           # Overview/dashboard data
├── exam/                # Exam scheduling
├── result/              # Results and grading 
├── school/              # Multi-tenant DB logic
├── subjects/            # Subject management
├── manage.py
└── .env                 # Environment variables
```

---

## 🔐 Authentication

### 1. Google OAuth (Principal)

* Redirects to Google OAuth login
* Automatically creates principal if new

### 2. JWT Auth (Other Roles)

* Login with credentials → Get access & refresh tokens
* Add `Authorization: Bearer <access_token>` in API headers

---

## 🧪 Sample API Endpoints

| Role      | Endpoint              |
| --------- | --------------------- |
| Principal | `/api/auth/google/`   |
| Staff     | `/accounts/staff/login/`   |
| Teacher   | `/accounts/teacher/login/` |
| Student   | `/accounts/student/login/` |
many more check on core urls.py and then corresponding urls of the apps
and still on the progress..  |

---

## ⚙️ Environment Setup (Auto-Loaded)

In `core/settings.py`, we use:

```python
import environ
env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
GOOGLE_CLIENT_ID = env('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = env('GOOGLE_CLIENT_SECRET')
```

Install with:

```bash
pip install django-environ
```

---

## 🌐 CORS Setup

```python
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
```

> ✅ Change to specific domains for production!

---

## ✅ Role Permissions

Using `django-role-permissions`, roles and permissions are defined in `accounts/roles.py`:

```python
from rolepermissions.roles import AbstractUserRole

class Principal(AbstractUserRole):
    available_permissions = {
        'view_school': True,
        'add_teacher': True,
    }

class Teacher(AbstractUserRole):
    available_permissions = {
        'upload_result': True,
    }
```

---



## 🐄 Running Tests

```bash
python manage.py test
```

---

## 🔐 Security Tips

* ❌ Never commit your `.env` file
* ✅ Use GitHub secrets scanning & protection
* ✅ Rotate OAuth and DB credentials regularly

---

## 📖 License

This project is licensed under the MIT License.

---

## 👨‍💻 Maintainer

**Raghav** – [GitHub](https://github.com/raghav977)

Feel free to fork, contribute, and make it better! 🚀
