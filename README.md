# 📦 Inventory Management API

A high-performance RESTful API designed for user registration and dynamic inventory tracking. This backend architecture was built utilizing FastAPI, which operates as one of the fastest Python frameworks available today.

## 🌐 Live Demo
* **API Base URL:** `https://inventory-managemen-api.onrender.com/`
* **Interactive Documentation (Swagger):** `https://inventory-managemen-api.onrender.com/docs`

## 🛠️ Tech Stack
* **Language:** Python 3
* **Framework:** FastAPI
* **ORM & Data Validation:** SQLModel / Pydantic
* **Database:** SQLite
* **Hosting / Deployment:** Render

## ✨ Key Features
* **Relational Data Mapping:** Securely links user accounts to their respective inventory items using standard Foreign Keys and bidirectional relationships, preventing infinite recursion loops during JSON serialization.
* **Token-Based Security:** Employs FastAPI's Dependency Injection system via an `APIRouter` to lock down sensitive data-modifying routes (POST, PUT, PATCH, DELETE), strictly requiring an `X-Token` header for access while leaving GET routes public.
* **Full CRUD Operations:** Comprehensive endpoint structure allowing for the complete lifecycle management of database records.
* **Clean Error Handling:** Graceful HTTP exception handling that prevents server crashes on invalid queries (e.g., returning proper `404 Not Found` and `401 Unauthorized` status codes).

## 🚀 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/omnik7/inventory_managemen_api.git
   cd inventory_managemen_api
