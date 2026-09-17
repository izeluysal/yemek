from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# PostgreSQL Bağlantı Havuzu
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI endpoint dependency:
    Her istekte bir veritabanı oturumu açar ve işlem bitince oturumu otomatik kapatır.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()