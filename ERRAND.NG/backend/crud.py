from sqlalchemy.orm import Session
from typing import List, Optional
from models import User, Errand, UserCreate, ErrandCreate, StatusEnum

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        hashed_password=user.password,  # Will be hashed in service layer
        full_name=user.full_name,
        phone=user.phone,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_errands(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None):
    query = db.query(Errand)
    if status:
        query = query.filter(Errand.status == status)
    return query.offset(skip).limit(limit).all()

def create_errand(db: Session, errand: ErrandCreate, client_id: int) -> Errand:
    db_errand = Errand(**errand.dict(), client_id=client_id)
    db.add(db_errand)
    db.commit()
    db.refresh(db_errand)
    return db_errand

def get_errand(db: Session, errand_id: int) -> Optional[Errand]:
    return db.query(Errand).filter(Errand.id == errand_id).first()

def update_errand(db: Session, errand: Errand, updates: dict):
    for field, value in updates.items():
        setattr(errand, field, value)
    db.commit()
    return errand

def get_available_runners(db: Session) -> List[User]:
    return db.query(User).filter(
        User.role == "runner",
        User.is_verified == True,
        User.availability_status == "available"
    ).all()
