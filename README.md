# Swiggy Clone (Monolith)

Django REST backend + React frontend + PostgreSQL. Application code only.
No Dockerfile, Compose file, or CI pipeline is included on purpose.

## Run locally (no Docker)

Backend (uses SQLite unless DB_HOST is set):

    cd backend
    pip install -r requirements.txt
    cp .env.example .env && export $(grep -v '^#' .env | xargs)
    python manage.py migrate
    python manage.py seed
    python manage.py createsuperuser      # optional, for /admin/
    python manage.py runserver 8000

Frontend:

    cd frontend
    npm ci        # or npm install the first time (creates package-lock.json)
    npm run dev   # http://localhost:3000

## API

| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | /health/ | no | liveness + DB check |
| POST | /api/register/ | no | create user, returns token |
| POST | /api/login/ | no | returns token |
| GET | /api/restaurants/ | no | list |
| GET | /api/restaurants/{id}/ | no | detail with menu |
| GET/POST | /api/orders/ | token | my orders / place order |

## Build facts (for packaging)

| Item | Backend | Frontend |
|---|---|---|
| Runtime | Python 3.12 | Node 20 (build only) |
| Install | pip install -r requirements.txt | npm ci |
| Build step | python manage.py collectstatic --noinput | npm run build (output: dist/) |
| Start | gunicorn config.wsgi:application -b 0.0.0.0:8000 | static files, serve with Nginx |
| Port | 8000 | 80 (Nginx) |
| Needs | PostgreSQL, env vars in backend/.env.example | /api routed to backend |
| Pre-start | python manage.py migrate | none |
| Health | GET /health/ | GET / |
