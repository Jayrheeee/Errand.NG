# ERRAND.NG Improvement Plan & Progress Tracker
Status: Backend Step 1 Complete ✓

## Backend Improvements (Priority 1)
- [x] Step 1: Fix models.py - Merge Runner into User, add indexes/timestamps/enums/Pydantic
- [x] Step 2: Update database.py - PostgreSQL support + Alembic setup (env.py, alembic.ini, script.mako)
- [x] Step 3: Refactor main.py - Pydantic models, full CRUD, SocketIO rooms, health checks, validation/errors
- [x] Step 4: Add auth.py (JWT deps), crud.py (business logic)
- [ ] Step 5: Alembic revision/migrate, pytest unit tests
- [ ] Step 6: Docker + docker-compose (Postgres + backend + Redis?)
- [ ] Step 4: Add auth.py, crud.py, schemas.py
- [ ] Step 5: Setup Alembic migrations, tests
- [ ] Step 6: Dockerize (Dockerfile, docker-compose.yml, .env)

## Frontend Improvements (Priority 2)
- [x] Step 7: Fix index.html bugs (chatbot button, CSS escapes, duplicates)
- [x] Step 8: Add booking modal form + API integration (/errands POST)
- [x] Step 9: Add runner signup modal + POST /users (role=runner)
- [ ] Step 10: Testimonials carousel, testimonials, improved mobile nav, PWA polish

- [ ] Step 10: Testimonials, improved mobile nav, PWA polish
- [ ] Step 11: Connect real Socket.IO to backend

## Integration & Deploy
- [ ] Step 12: Test full flow (post errand -> assign runner -> live track)
- [ ] Step 13: Deploy (Vercel frontend + Render backend + Supabase DB)

**Next: Step 2 - database.py & alembic.ini. Then Step 3 main.py.**

Updated: $(date)
