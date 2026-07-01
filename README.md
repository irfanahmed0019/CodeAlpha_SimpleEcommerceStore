# 🛒 CodeAlpha - Simple E-Commerce Store

A modern full-stack **E-Commerce Web Application** built with **Django**, featuring secure authentication, Google Sign-In, product management, shopping cart, checkout, and order tracking.

Developed as **Task 1** of the **CodeAlpha Full Stack Development Internship (July 2026)**.

---


---

#  Preview


- 🏠 Home Page
- 📦 Product Details
- 🛍️ Shopping Cart
- 🚚 Checkout
- 📜 Orders
- 🔐 Login / Register
- 🌐 Google Sign-In


# ✨ Features

## 👤 User Authentication

- User Registration
- Secure Login & Logout
- Google OAuth Authentication
- Session-based Authentication

---

## 🛒 E-Commerce Features

- Browse Products
- Featured Products
- Product Categories
- Product Detail Page
- Product Specifications
- Product Search
- Responsive Product Grid

---

## 🛍️ Shopping Cart

- Add Products to Cart
- Update Quantity
- Remove Products
- Dynamic Cart Count
- Price Calculation
- Shipping Cost Calculation
- Tax Calculation
- Grand Total

---

## 💳 Checkout

- Shipping Information
- Order Summary
- Payment Page
- Order Confirmation

---

## 📦 Order Management

- View Previous Orders
- Purchased Products
- Order Details
- Quantity Tracking

---

## 🎨 User Interface

- Responsive Design
- Material Design Inspired UI
- Modern Product Cards
- Mobile Friendly Layout
- Clean Navigation

---

# 🐳 Docker Support

This project includes Docker support for easy setup and deployment.

### Build Docker Image

```bash
docker build -t ecommerce-store .
```

### Run Container

```bash
docker run -p 8000:8000 ecommerce-store
```

### Using Docker Compose

```bash
docker compose up --build
```

Application will be available at:

```
http://localhost:8000
```

---

# 🛠 Tech Stack

## Backend

- Python
- Django

## Frontend

- HTML5
- CSS3
- JavaScript

## Database

- SQLite

## Authentication

- Django Authentication
- Django Allauth
- Google OAuth

## Deployment & DevOps

- Docker
- Docker Compose
- Gunicorn
- WhiteNoise
- Vercel Configuration

---

# 📂 Project Structure

```
CodeAlpha_SimpleEcommerceStore
│
├── ecommerce/
├── store/
├── static/
├── templates/
├── media/
├── products/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── build_files.sh
└── vercel.json
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/irfanahmed0019/CodeAlpha_SimpleEcommerceStore.git
```

---

## 2. Navigate to Project

```bash
cd CodeAlpha_SimpleEcommerceStore
```

---

## 3. Create Virtual Environment

```bash
python -m venv .venv
```

---

## 4. Activate Virtual Environment

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Apply Database Migrations

```bash
python manage.py migrate
```

---

## 7. Run Development Server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

# 📚 Key Learning Outcomes

Through this project I gained hands-on experience with:

- Django Project Structure
- Django ORM
- Authentication System
- Google OAuth Integration
- Model Relationships
- CRUD Operations
- Shopping Cart Logic
- Checkout Workflow
- Order Management
- Django Template Inheritance
- Static & Media File Management
- Docker Containerization
- Deployment Preparation
- Git & GitHub Workflow

---

# 🌟 Project Highlights

- 🔐 Secure User Authentication
- 🌐 Google Login Integration
- 🛒 Shopping Cart System
- 💳 Checkout Workflow
- 📦 Order Tracking
- 📱 Fully Responsive Design
- 🐳 Dockerized Application
- 🚀 Deployment Ready
- 🧩 Clean & Scalable Django Architecture

---

# 🎯 Internship Information

**Internship:** CodeAlpha Full Stack Development Internship

**Duration:** July 1, 2026 – July 30, 2026

**Completed Task:**

- ✅ Task 1 — Simple E-Commerce Store

---

# 🚀 Future Improvements

- Payment Gateway Integration (Stripe/Razorpay)
- Wishlist Feature
- Product Reviews & Ratings
- Email Notifications
- Inventory Management
- Admin Dashboard Analytics
- PostgreSQL Support
- REST API Integration

---

# 👨‍💻 Author

**Irfan Ahammad J**

📧 LinkedIn: https://linkedin.com/in/irfan-ahammad-j

💻 GitHub: https://github.com/irfanahmed0019

---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.

It helps support my learning journey and future open-source projects.

---

## 📄 License

This project is created for educational and internship purposes under the **CodeAlpha Full Stack Development Internship**.
