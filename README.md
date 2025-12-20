# Gate Pass Backend System

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2%2B-092E20.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django_REST_Framework-3.16-a30000.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive backend solution designed for educational institutions to digitize and automate the student leave request and gate pass issuance process. Built with modern Django practices, this system handles multi-level approval workflows, real-time notifications, and secure role-based access control.

---

## 🚀 Key Features

### 🔐 Authentication & Roles
* **JWT Authentication**: Secure stateless authentication using `djangorestframework-simplejwt`.
* **Role-Based Access Control (RBAC)**: Distinct permissions for **Students**, **Department HODs**, **Hostel Wardens**, and **Admins**.
* **Custom User Models**: Extended user profiles handling specific attributes for students (parents' contact, room numbers) and staff.

### 📝 Leave Management Workflow
* **Digital Leave Requests**: Students can apply for leave with dates and reasons.
* **Multi-Stage Approval**:
    1.  **HOD Approval**: Academic clearance from the department.
    2.  **Warden/Admin Approval**: Residential clearance.
* **Status Tracking**: Real-time tracking of application status (Pending, Approved, Rejected).

### 🎟️ Gate Pass Generation
* **Automated Issuance**: System automatically generates a `GatePass` entry upon final approval.
* **Unique Security Codes**: Each pass includes a unique tracking code for security verification at the gate.

### 🔔 Notifications
* **Background Services**: Dedicated `notifications` app to handle alerts.
* **Status Updates**: Users are notified immediately when their leave status changes.

---

## 🛠️ Technical Stack

| Component | Technology |
| :--- | :--- |
| **Framework** | Django 5.2 |
| **API** | Django REST Framework (DRF) 3.16 |
| **Database** | PostgreSQL (via `psycopg3`) |
| **Server** | Uvicorn (ASGI) / Gunicorn (WSGI) |
| **Package Manager** | [uv](https://github.com/astral-sh/uv) |
| **Documentation** | OpenAPI 3.0 via `drf-spectacular` |

---

## 📂 Project Architecture

```text
├── api/                 # Global API configurations
├── apps/                # Modular Django Apps
│   ├── core/            # Shared logic (Hostel/Department models)
│   ├── leave/           # Leave Request & Gate Pass business logic
│   ├── notifications/   # Background notification services
│   └── users/           # Custom User, Student, and Staff models
├── config/              # Project settings (ASGI/WSGI)
└── staticfiles/         # Static assets for Admin panel
``` 
## ⚙️ Installation & Setup

This project uses **uv** for fast and reliable dependency management.

### Prerequisites
* Python 3.14+
* PostgreSQL
* `uv` installed

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/gate-pass-backend.git](https://github.com/yourusername/gate-pass-backend.git)
cd gate-pass-backend
``` 
## 2. Environment Configuration

```bash 
Create a .env file in the root directory:
DEBUG=True
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgres://user:password@localhost:5432/gate_pass_db
ALLOWED_HOSTS=127.0.0.1,localhost
```
## 3. Install Dependencies
```bash 
uv sync
```
Markdown

## ⚙️ Installation & Setup

This project uses **uv** for fast and reliable dependency management.

### Prerequisites
* Python 3.14+
* PostgreSQL
* `uv` installed

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/gate-pass-backend.git](https://github.com/yourusername/gate-pass-backend.git)
cd gate-pass-backend

2. Environment Configuration

Create a .env file in the root directory:
Code snippet
```bash 
# Django core
SECRET_KEY=some-secret-key
DEBUG=True

# Hosts
ALLOWED_HOSTS=
CSRF_TRUSTED_ORIGINS=
CORS_ALLOWED_ORIGINS=

# JWT timing (minutes)
ACCESS_TOKEN_LIFETIME=60
REFRESH_TOKEN_LIFETIME=7

DB_NAME=your database name 
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
EMAIL_APP_PASSWORD=

```

## 3. Install Dependencies
```bash 
uv sync
```


## 4. Database Setup

Apply migrations to set up the schema:
```bash
uv run manage.py migrate
```
## Create a superuser for dashboard access:
```bash 
uv run manage.py createsuperuser
```
## 5. Run the Server

For development 
```bash
uv run python manage.py runserver 
```
## 📖 API Documentation

The project includes auto-generated, interactive API documentation.
```test 
    Swagger UI: http://127.0.0.1:8000/api/docs/

    Redoc: http://127.0.0.1:8000/api/schema/redoc/

    OpenAPI Schema: http://127.0.0.1:8000/api/schema/
```
## 🤝 Contributing

    Fork the repository.

    Create a feature branch (git checkout -b feature/AmazingFeature).

    Commit your changes (git commit -m 'Add some AmazingFeature').

    Push to the branch (git push origin feature/AmazingFeature).

    Open a Pull Request.
