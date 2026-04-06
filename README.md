# 💰 Finance Dashboard Backend API

> A Django REST Framework backend for a Finance Dashboard with JWT authentication, role-based access control (RBAC), and analytics APIs.

![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![Django](https://img.shields.io/badge/django-5.0-green.svg)

---

## 🎯 Overview

This project is a **production-ready backend API** for a Finance Dashboard system that:

- Manages **users and roles**
- Stores **financial records**
- Provides **analytics and dashboard insights**
- Implements **secure authentication and authorization**

The system supports **three roles with different permissions**.

| Role | Access |
|-----|-----|
| **Admin** | Full access (CRUD records + manage users) |
| **Analyst** | View all records + analytics |
| **Viewer** | View only own records |

---

## 🚀 Live Demo

| Service | URL |
|------|------|
| **API Base URL** | https://finance-backend-2m27.onrender.com/api/ |
| **Swagger Documentation** | https://finance-backend-2m27.onrender.com/api/docs |


---

## ✨ Features

### 👥 User Management
- Role-based access control (RBAC)
- Three user roles:
  - Viewer
  - Analyst
  - Admin

### 💰 Financial Records
- Create, read, update, delete financial records
- Filtering by:
  - date
  - category
  - amount
  - type (income/expense)

### 📊 Dashboard Analytics
APIs provide insights including:

- Total income
- Total expenses
- Net balance
- Category-wise spending
- Monthly / weekly trends
- Recent transactions

### 🔐 Security
- JWT authentication
- Token refresh support
- Permission-based access control

### 🛡️ Robust API Design
- Input validation
- Structured error responses
- Pagination
- Filtering support

### 📄 Documentation
- Swagger UI
- ReDoc
- Postman collection included

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|-----|
| Backend | Django 5.0 |
| API Framework | Django REST Framework |
| Database | PostgreSQL |
| Authentication | JWT (SimpleJWT) |
| Documentation | Swagger |
| Deployment | Render |

---

## 📋 Requirements Coverage

| Requirement | Status |
|------|------|
User & Role Management | ✅ |
Financial Records CRUD | ✅ |
Filtering & Pagination | ✅ |
Dashboard Analytics APIs | ✅ |
Role-Based Access Control | ✅ |
Validation & Error Handling | ✅ |
Persistent Database | ✅ |

---

## 🚀 Quick Start

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Neeraj-op/finance-dashboard-backend.git
cd finance-backend
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate environment

**Linux / Mac**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment

```bash
cp .env.example .env
```

Edit `.env` file with required settings.

---

### 5️⃣ Run Database Migrations

```bash
python manage.py migrate
```

---

### 6️⃣ Create Admin User

```bash
python manage.py createsuperuser
```

---

### 7️⃣ Start Development Server

```bash
python manage.py runserver
```

Open:

```
http://localhost:8000/api/docs/
```

## 🧪 Testing

| **API Testing Documentation** | https://finance-backend-2m27.onrender.com/api/docs |


---

## 📊 API Endpoints

Full API reference available at:

```
/api/docs/
```

### Authentication

```
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/refresh/
```

### Users

```
GET /api/users/me/
GET /api/users/
POST /api/users/change-password/
```

### Financial Records

```
GET /api/records/
POST /api/records/
PUT /api/records/{id}/
DELETE /api/records/{id}/
```

### Dashboard Analytics

```
GET /api/dashboard/summary/
GET /api/dashboard/category-wise/
GET /api/dashboard/trends/
GET /api/dashboard/recent/
GET /api/dashboard/top-expenses/
```



## 👤 Author

**Niraj Jadhav**

📧 neerajjadhav789@gmail.com.com

---

