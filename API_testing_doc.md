# 📊 Finance Dashboard Backend – Testing Guide

## 1️⃣ Project Overview

This project is a **Finance Dashboard Backend API** built using **Django** and **Django REST Framework**.

It provides APIs for:

- User authentication using **JWT**
- **Role Based Access Control (RBAC)**
- **Financial records management**
- **Dashboard analytics and reporting**

The system supports **three user roles with different permissions**.

---

# 🌐 2️⃣ Live Application Links

**Base API URL**

```
https://finance-backend-2m27.onrender.com/api
```

**Swagger API Documentation**

```
https://finance-backend-2m27.onrender.com/api/docs/
```

Swagger allows to **test APIs directly from the browser**.

---

# 🔑 3️⃣ Demo Credentials

### 👑 Admin (Full Access)

```
Username: demo_admin
Password: DemoAdmin123!
```

Permissions:

- Create records
- Update records
- Delete records
- Manage users
- Access all analytics

---

### 📊 Analyst (Read Only)

```
Username: demo_analyst
Password: DemoAnalyst123!
```

Permissions:

- View all financial records
- Access analytics dashboard
- Cannot modify data

---

### 👁️ Viewer (Own Data Only)

```
Username: demo_viewer
Password: DemoViewer123!
```

Permissions:

- View only their own records
- Access personal dashboard
- Cannot modify data

---

# 🧪 4️⃣ Testing Steps

### Step 1 — Open Swagger

```
https://finance-backend-2m27.onrender.com/api/docs/
```

---

### Step 2 — Login

Endpoint:

```
POST /api/auth/login/
```

Example request:

```json
{
 "username": "demo_admin",
 "password": "DemoAdmin123!"
}
```

The response will return:

- **access token**
- **refresh token**

Copy the **access token**.

---

### Step 3 — Authorize

Click **Authorize** in Swagger and enter:

```
Bearer YOUR_ACCESS_TOKEN
```

Now all APIs can be tested.

⚠️ **Note:**  
Steps **1–3 must be repeated for Admin, Analyst, and Viewer** to test role-based access control.

---

# 🔌 5️⃣ Key APIs to Evaluate

### Authentication

```
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/refresh/
```

---

### User APIs

```
GET /api/users/me/
GET /api/users/        (Admin only)
POST /api/users/change-password/
```

---

### Financial Records

```
GET /api/records/
POST /api/records/           (Admin only)
GET /api/records/{id}/
PUT /api/records/{id}/       (Admin only)
DELETE /api/records/{id}/    (Admin only)
```

---

### Dashboard APIs

```
GET /api/dashboard/summary/
GET /api/dashboard/category-wise/
GET /api/dashboard/trends/
GET /api/dashboard/recent/
GET /api/dashboard/top-expenses/
```

📌 **Note:**  
Additional API endpoints are available in **Swagger documentation**.

---

# 📊 6️⃣ Demo Data

The database contains **pre-populated financial data for testing**.

```
Total Income: ₹310000
Total Expenses: ₹144500
Net Balance: ₹165500
Total Records: 18+
```

---

# 🔐 7️⃣ Role Based Access Control

| Role | Permissions |
|-----|-------------|
| **Admin** | Full access (Create, Read, Update, Delete, Analytics) |
| **Analyst** | Read-only access to all records and analytics |
| **Viewer** | Can only view their own records |

---

# ⚙️ 8️⃣ Technology Stack

- **Backend:** Django 5
- **API Framework:** Django REST Framework
- **Authentication:** JWT (SimpleJWT)
- **Database:** PostgreSQL
- **Deployment:** Render

---

# ✨ 9️⃣ Key Features

- JWT Authentication
- Role Based Access Control
- Financial Records CRUD
- Dashboard Analytics
- Filtering and Pagination
- Input Validation
- Soft Delete
- Swagger API Documentation
- PostgreSQL Data Persistence

---

# 💻 🔟 GitHub Repository

```
https://github.com/Neeraj-op/finance-dashboard-backend
```

---

# 📧 1️⃣1️⃣ Contact

For queries:

```
neerajjadhav789@gmail.com
```

---

⭐ Thank you
