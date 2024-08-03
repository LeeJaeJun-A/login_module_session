from datetime import datetime, timedelta
from backend.model import User
from sqlalchemy.orm import Session
from backend.config import MAX_FAILURES, LOCK_TIME_MINUTES, DEFAULT_ROOT_ACCOUNT_ID


def increment_failed_attempts(user_id: str, database: Session) -> None:
    user = database.query(User).filter(User.id == user_id).one_or_none()
    if user and user.id != DEFAULT_ROOT_ACCOUNT_ID:
        now = datetime.now()
        if user.last_failed_login:
            if now - user.last_failed_login < timedelta(minutes=LOCK_TIME_MINUTES):
                user.failed_attempts += 1
            else:
                user.failed_attempts = 1
        else:
            user.failed_attempts = 1
        user.last_failed_login = now
        
        if user.failed_attempts >= MAX_FAILURES:
            user.is_locked = True
            user.locked_at = now
        database.commit()


def check_account_locked(user_id: str, database: Session) -> bool:
    user = database.query(User).filter(User.id == user_id).one_or_none()
    if user and user.is_locked:
        return True
    return False


def unlock_account(user_id: str, database: Session) -> bool:
    user = database.query(User).filter(User.id == user_id).one_or_none()
    if user and user.is_locked:
        user.failed_attempts = 0
        user.is_locked = False
        user.locked_at = None
        database.commit()
        return True
    return False


def lock_account(user_id: str, database: Session) -> bool:
    user = database.query(User).filter(User.id == user_id).one_or_none()
    if user:
        user.is_locked = True
        user.locked_at = datetime.now()
        database.commit()
        return True
    return False
