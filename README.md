# 🧠 Advanced Bulk Product Upload API

An advanced Django-based API that supports **bulk product upload via CSV files**, **asynchronous background processing**, **progress tracking**, and **Swagger documentation**.  
This project is production-ready, containerized, and designed for clarity and extensibility.

---

## 🚀 Features

- 📦 Bulk upload of product data using CSV files.
- 🧵 Asynchronous background processing via Celery + Redis.
- 🗂️ Real-time task progress tracking (upload status API).
- 🌐 API documentation using Swagger (via `drf-spectacular`).
- ⚙️ Environment-based configuration using `.env`.
- 🐳 Optional Docker setup for production and local testing.
- 💾 PostgreSQL support (compatible with [Neon Database](https://neon.tech)).

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend Framework | Django 5 + Django REST Framework |
| Asynchronous Tasks | Celery + Redis |
| Database | PostgreSQL (Neon-hosted or local) |
| Documentation | drf-spectacular (Swagger UI) |
| Environment Management | python-dotenv / django-environ |
| Deployment | Gunicorn + Docker |

---

## ⚙️ Environment Setup

### 1. Clone and Navigate
```bash
git clone https://github.com/<your-username>/advanced_bulk_upload.git
cd advanced_bulk_upload
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup `.env`
Create a `.env` file at the project root:

```env
SECRET_KEY=dev-secret-key
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# Database (Example: Neon)
POSTGRES_DB=neondb
POSTGRES_USER=neondb_owner
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=ep-tiny-smoke-ah1c4szd-pooler.c-3.us-east-1.aws.neon.tech
POSTGRES_PORT=5432

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
MEDIA_ROOT=media/
```

---

## 🧩 Database Setup

Run migrations:
```bash
python manage.py migrate
```

Create an admin user (optional):
```bash
python manage.py createsuperuser
```

---

## 🧠 Running the Application

### 1. Start Redis
```bash
redis-server
```

### 2. Start Celery Worker
```bash
celery -A project worker --loglevel=info
```

### 3. Run Django Server
```bash
python manage.py runserver
```

Visit:
- API UI → http://127.0.0.1:8000/upload/products/
- Swagger Docs → http://127.0.0.1:8000/api/schema/swagger-ui/

---

## 🧪 Quick API Testing

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `POST` | `/upload/products/bulk-upload/` | Upload a CSV file for processing |
| `GET`  | `/upload/products/status/<task_id>/` | Get upload task progress |
| `GET`  | `/upload/products/` | View all uploaded products |
| `GET`  | `/api/schema/swagger-ui/` | Interactive Swagger Docs |

### Upload CSV Example
```bash
curl -X POST -F "file=@grocery_products.csv" http://127.0.0.1:8000/upload/products/bulk-upload/
```

Response:
```json
{"task_id": "5d7f6a6b-a8f2-4e3a-a513-86f7ec4b7f3b"}
```

Track progress:
```bash
curl http://127.0.0.1:8000/upload/products/status/5d7f6a6b-a8f2-4e3a-a513-86f7ec4b7f3b/
```

View uploaded data:
```bash
curl http://127.0.0.1:8000/upload/products/
```

---

## 🧾 Example CSV Files

Included sample files:
- `grocery_products.csv` 🍎
- `electronics_products.csv` ⚡
- `fashion_products.csv` 👗

Each has **50+ records** for testing.

---

## 🐳 Docker Setup

```bash
docker-compose up --build
```

This launches:
- Django API
- Redis
- PostgreSQL
- Celery worker

---

## 🧭 Interviewer Notes

- Demonstrates **asynchronous processing**, **REST principles**, and **environment-driven config**.
- Swagger for easy API testing.
- Uses Celery to handle heavy CSV uploads in background.
- Clean modular architecture, extensible for production use.

---

## 🧑‍💻 Author

**Camaraderie Mavenga**  
Full Stack Developer | Django, React, Node.js  
📧 camaradery303@gmail.com  
🌍 [camathedev.vercel.app](https://camathedev.vercel.app)
