# Errand.NG Backend v2 (FastAPI + Socket.IO + PostgreSQL)

## 🚀 Quick Start (Development)

```bash
cd ERRAND.NG/backend
pip install -r requirements.txt
uvicorn main:socket_app --host 0.0.0.0 --port 8000 --reload
```

**API Docs:** http://localhost:8000/docs  
**WebSocket Test:** Connect to `ws://localhost:8000/socket.io/`

## 🐳 Docker Production

```bash
cd ERRAND.NG/backend
cp .env.example .env  # Edit DATABASE_URL etc.
docker compose up --build
```

Frontend auto-serves on http://localhost (nginx static)

## 📋 Features (Production Ready)

✅ **REST API** (Swagger docs)
- Users (CRUD, runners list)
- Errands (post/list/update status/filter posted/active)
- Validation (Pydantic + enums)

✅ **Real-time Socket.IO**
- GPS `location_update`
- Errand rooms `join_errand`
- Notifications `new_errand`, `errand_update`

✅ **Database**
- PostgreSQL/SQLite switch (env var)
- Alembic migrations ready
- Indexes (location queries O(1))

✅ **Security Prep**
- JWT auth (auth.py ready)
- CORS locked to frontend
- Password hashing ready

## 🧪 Testing

```bash
pytest test_main.py -v
```

## 📐 Architecture

```
Frontend (HTML/JS/PWA) <-> Socket.IO + REST <- FastAPI <- PostgreSQL
                    ↕
                nginx/Docker (prod)
```

## 🚀 Next Steps

1. `alembic revision --autogenerate -m "init"`
2. `.env` + migrate Postgres
3. JWT login/register endpoints
4. Frontend integration (booking form)
5. Paystack payments

## Environment

Copy `.env.example` → `.env`

**DB Example:**
```
DATABASE_URL=postgresql://postgres:password@localhost/errand_ng
```

## Logs

Backend logs GPS connects/updates. Check `/health` endpoint.

**Made with ❤️ by BLACKBOXAI**


