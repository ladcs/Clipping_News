from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from core.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_db_with_depends():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

