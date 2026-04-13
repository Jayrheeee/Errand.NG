from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from socketio import ASGIApp
import socketio
from typing import List
from models import User, Errand, UserCreate, UserOut, ErrandCreate, ErrandOut, StatusEnum
from database import get_db, init_db

app = FastAPI(title="Errand.NG Backend v2", version="2.0.0", docs_url="/docs")

# CORS - Tighten for prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5500"],  # Frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO with auth-ready
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
socket_app = ASGIApp(sio, app)

@sio.event
async def connect(sid, environ, auth=None):
    print(f"Client {sid} connected (auth: {auth})")
    # TODO: JWT auth

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")

@sio.event
async def location_update(sid, data):
    """Real-time GPS for runner tracking"""
    print(f"GPS from {sid}: {data}")
    # Emit to errand room or specific clients
    await sio.emit("location_update", data, room="errand_updates")

@sio.event
async def join_errand(sid, errand_id: str):
    """Runner joins specific errand room"""
    await sio.enter_room(sid, f"errand_{errand_id}")
    print(f"{sid} joined errand {errand_id}")

# Root & Health
@app.get("/")
async def root():
    return {"message": "Errand.NG Backend v2 - Production Ready 🚀", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2.0.0"}

@app.on_event("startup")
async def startup():
    init_db()
    print("✅ Database initialized & migrations applied")

# Users API
@app.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check existing
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # TODO: Implement password hashing (bcrypt)
    db_user = User(
        email=user.email,
        hashed_password=user.password,  # Temp - hash in prod
        full_name=user.full_name,
        phone=user.phone,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, not_found="User not found")
    return user

# Errands API
@app.post("/errands/", response_model=ErrandOut, status_code=status.HTTP_201_CREATED)
async def create_errand(errand: ErrandCreate, db: Session = Depends(get_db)):
    db_errand = Errand(**errand.dict())
    db.add(db_errand)
    db.commit()
    db.refresh(db_errand)
    
    # Emit real-time notification
    await sio.emit("new_errand", {"id": db_errand.id, "title": db_errand.title})
    
    return db_errand

@app.get("/errands/", response_model=List[ErrandOut])
async def list_errands(status: Optional[StatusEnum] = None, db: Session = Depends(get_db)):
    query = db.query(Errand)
    if status:
        query = query.filter(Errand.status == status.value)
    return query.all()

@app.get("/errands/{errand_id}", response_model=ErrandOut)
async def get_errand(errand_id: int, db: Session = Depends(get_db)):
    errand = db.query(Errand).filter(Errand.id == errand_id).first()
    if not errand:
        raise HTTPException(status_code=404, detail="Errand not found")
    return errand

@app.put("/errands/{errand_id}/status")
async def update_errand_status(errand_id: int, status_update: dict, db: Session = Depends(get_db)):
    errand = db.query(Errand).filter(Errand.id == errand_id).first()
    if not errand:
        raise HTTPException(status_code=404, detail="Errand not found")
    
    if status_update.get("status") not in [s.value for s in StatusEnum]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    for key, value in status_update.items():
        setattr(errand, key, value)
    
    db.commit()
    db.refresh(errand)
    
    # Real-time update
    await sio.emit("errand_update", {"id": errand_id, "status": errand.status})
    
    return {"message": "Status updated", "errand": errand}

# Runner endpoints
@app.get("/runners/", response_model=List[UserOut])
async def list_runners(available: bool = True, db: Session = Depends(get_db)):
    query = db.query(User).filter(User.role == "runner", User.is_verified == True)
    if available:
        query = query.filter(User.availability_status == "available")
    return query.all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:socket_app", host="0.0.0.0", port=8000, reload=True)



