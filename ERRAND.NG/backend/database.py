from sqlalchemy import create_engine
import os
from alembic import command
from alembic.config import Config

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./errand.db")

# PostgreSQL for prod
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL)
else:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
LocalSession = scoped_session(SessionLocal)

Base = declarative_base()

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create tables and run migrations"""
    Base.metadata.create_all(bind=engine)
    alembic_cfg = Config("alembic.ini")
    command stamp(alembic_cfg, "head")
    command upgrade(alembic_cfg, "head")

def get_alembic_config():
    return Config("alembic.ini")

