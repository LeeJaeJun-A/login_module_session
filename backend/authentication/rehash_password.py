from backend.database.models import User
import bcrypt
from typing import Optional
from sqlalchemy.orm import Session

def rehash_password(user_id: str, password: str, database: Session) -> Optional[str]:
    try:
        user = database.query(User).filter(User.id == user_id).one_or_none()
        if not user:
            return None
        
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        
        user.password = hashed_password
        user.salt = salt
        database.commit()
        database.refresh(user)

        return hashed_password
    except Exception as e:
        database.rollback()
        return None