#  Bulk Product Upload API

 Django-based API that supports **bulk product upload via CSV files**, **asynchronous background processing**, **progress tracking**, and **Swagger documentation**.  
This project is production-ready, containerized, and designed for clarity and extensibility.

---

##  Features

-  Bulk upload of product data using CSV files.
-  Asynchronous background processing via Celery + Redis.
- ️ Real-time task progress tracking (upload status API).
-  API documentation using Swagger (via `drf-spectacular`).
- Environment-based configuration using `.env`.
- Docker setup for production and local testing.
-  PostgreSQL support (compatible with [Neon Database](https://neon.tech)).

---

##  Tech Stack

| Component | Technology |
|------------|-------------|
| Backend Framework | Django 5 + Django REST Framework |
| Asynchronous Tasks | Celery + Redis |
| Database | PostgreSQL (Neon-hosted ) |
| Documentation | drf-spectacular (Swagger UI) |
| Environment Management | django-environ |
| Deployment | Gunicorn + Docker |

---

##  Environment Setup

### 1. Clone and Navigate
```bash
git clone git@github.com:Kuvimbanashe/django_backend_test.git
cd django_backend_test
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
DJANGO_ALLOWED_HOSTS=['*'] 
POSTGRES_DB=neondb
POSTGRES_USER=neondb_owner
POSTGRES_PASSWORD=npg_iYcuKfy68ISH
POSTGRES_HOST=ep-tiny-smoke-ah1c4szd-pooler.c-3.us-east-1.aws.neon.tech
POSTGRES_PORT=5432

CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1
MEDIA_ROOT=/media/


```

---

##  Database Setup

Run migrations:
```bash
python manage.py migrate
```

Create an admin user (optional):
```bash
python manage.py createsuperuser
```

---

##  Running the Application

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
- API UI → http://127.0.0.1:8000/api/products/
- Swagger Docs → http://127.0.0.1:8000/api/schema/swagger-ui/

---

##  Quick API Testing

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `POST` | `/api/products/bulk-upload/` | Upload a CSV file for processing |
| `GET`  | `/api/tasks/<task_id>/status/` | Get upload task progress |
| `GET`  | `/api/products/` | View all uploaded products |
| `GET`  | `/api/schema/swagger-ui/` | Interactive Swagger Docs |

### Upload CSV Example
```bash
curl -X POST -F "file=@./sample_data/grocery_products.csv" http://127.0.0.1:8000/api/products/bulk-upload/
```

Response:
```json
{"task_id": "5d7f6a6b-a8f2-4e3a-a513-86f7ec4b7f3b"}
```

Track progress:
```bash
curl http://127.0.0.1:8000/api/tasks/5d7f6a6b-a8f2-4e3a-a513-86f7ec4b7f3b/status
```

View uploaded data:
```bash
curl http://127.0.0.1:8000/api/products/
```

---

##  Example CSV Files

Included sample files in sample_data folder:
- `grocery_products.csv` 
- `electronics_products.csv` 
- `fashion_products.csv` 

Each has **50+ records** for testing.

---

##  Docker Setup

```bash
docker-compose up --build
```

This launches:
- Django API
- Redis
- PostgreSQL
- Celery worker

---

##  Author

**Camaraderie Mavenga**  
Full Stack Developer | Django, React, Node.js  
📧 camaradery303@gmail.com  
🌍 [cama-1z3r.onrender.com](https://cama-1z3r.onrender.com)
