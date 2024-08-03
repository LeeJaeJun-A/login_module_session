import bcrypt
from sqlalchemy.orm import Session
from backend.model import User, Base
from backend.database.database import engine
from backend.config import DEFAULT_ROOT_ACCOUNT_ID, DEFAULT_ROOT_ACCOUNT_PASSWORD
from datetime import datetime

def init_database(db: Session):
    Base.metadata.create_all(bind=engine)
    user = db.query(User).filter(User.id == DEFAULT_ROOT_ACCOUNT_ID).one_or_none()
    if not user:
        salt = bcrypt.gensalt().decode('utf-8')
        hashed_password = bcrypt.hashpw(DEFAULT_ROOT_ACCOUNT_PASSWORD.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
        root_user = User(
            id=DEFAULT_ROOT_ACCOUNT_ID,
            password=hashed_password,
            salt=salt,
            authorizer="self",
            role="admin",
            request_success_count=0,
            failed_attempts=0,
            is_locked=False,
            locked_at=None,
            created_at=datetime.now()
        )
        db.add(root_user)
        db.commit()
        db.refresh(root_user)