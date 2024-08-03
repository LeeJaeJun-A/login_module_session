from backend.database.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Generator

def get_database() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()