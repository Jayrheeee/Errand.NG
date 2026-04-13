from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
from datetime import datetime

Base = declarative_base()

class UserRole(str, Enum):
    CLIENT = "client"
    RUNNER = "runner"

class StatusEnum(str, Enum):
    POSTED = "posted"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    role = Column(String, default="client")  # client, runner
    is_verified = Column(Boolean, default=False)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    availability_status = Column(String, default="available")  # for runners
    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('ix_users_email', 'email'),
        Index('ix_users_role', 'role'),
        Index('ix_users_location', 'current_lat', 'current_lng'),
    )

    errands_posted = relationship("Errand", foreign_keys="Errand.client_id", back_populates="client")
    errands_assigned = relationship("Errand", foreign_keys="Errand.runner_id", back_populates="runner")

class Errand(Base):
    __tablename__ = "errands"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, nullable=False)  # domestic, skilled, delivery
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    runner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="posted")
    pickup_lat = Column(Float, nullable=False)
    pickup_lng = Column(Float, nullable=False)
    dropoff_lat = Column(Float, nullable=False)
    dropoff_lng = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    eta = Column(Integer, nullable=True)  # minutes
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('ix_errands_status', 'status'),
        Index('ix_errands_client', 'client_id'),
        Index('ix_errands_runner', 'runner_id'),
        Index('ix_errands_pickup', 'pickup_lat', 'pickup_lng'),
    )

    client = relationship("User", foreign_keys=[client_id], back_populates="errands_posted")
    runner = relationship("User", foreign_keys=[runner_id], back_populates="errands_assigned")

    def current_location(self):
        if self.runner and self.runner.current_lat and self.runner.current_lng:
            return (self.runner.current_lat, self.runner.current_lng)
        return None

# Enhanced Pydantic Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: str
    role: UserRole = "client"

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    availability_status: Optional[str] = None
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None

class UserOut(UserBase):
    id: int
    is_verified: bool
    rating: float
    rating_count: int
    availability_status: Optional[str]
    current_lat: Optional[float]
    current_lng: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True

class ErrandBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    category: str
    pickup_lat: float
    pickup_lng: float
    dropoff_lat: float
    dropoff_lng: float
    price: float = Field(..., gt=0)

class ErrandCreate(ErrandBase):
    pass

class ErrandUpdate(BaseModel):
    status: Optional[StatusEnum] = None
    eta: Optional[int] = None

class ErrandOut(ErrandBase):
    id: int
    status: StatusEnum
    client_id: int
    runner_id: Optional[int]
    eta: Optional[int]
    created_at: datetime
    runner: Optional[UserOut] = None

    class Config:
        from_attributes = True


