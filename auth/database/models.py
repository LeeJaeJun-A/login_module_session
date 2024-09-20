from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)

    # Password for the user, should be stored as a hashed value
    password = Column(String, nullable=False)

    # Salt value used for hashing the password
    salt = Column(String, nullable=False)

    # Role of the user (e.g., 'admin', 'user')
    role = Column(String, nullable=False)

    # The number of successful requests
    logins_before_rehash = Column(Integer, nullable=False, default=0)

    # Last failed login attempt time
    last_failed_login = Column(DateTime, nullable=True)

    # Number of consecutive failed attempts
    failed_attempts = Column(Integer, nullable=False, default=0)

    # Account lock status
    is_locked = Column(Boolean, default=False)

    # Timestamp when the user was created, defaults to the current time
    created_at = Column(DateTime, default=datetime.now, nullable=False)


class SessionModel(Base):
    __tablename__ = "sessions"

    session_id = Column(String(255), primary_key=True)
    user_id = Column(String(255))
    role = Column(String(255))
    expires_at = Column(DateTime)
