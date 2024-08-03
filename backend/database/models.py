from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from backend.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)

    # Password for the user, should be stored as a hashed value
    password = Column(String, nullable=False)

    # Salt value used for hashing the password
    salt = Column(String, nullable=False)

    # Authorizer's id for the user
    authorizer = Column(String, nullable=False)

    # Role of the user (e.g., 'admin', 'user')
    role = Column(String, nullable=False)

    # The number of successful requests
    request_success_count = Column(Integer, nullable=False, default=0)

    # Last failed login attempt time
    last_failed_login = Column(DateTime, nullable=True)

    # Number of consecutive failed attempts
    failed_attempts = Column(Integer, nullable=False, default=0)

    # Account lock status
    is_locked = Column(Boolean, default=False)

    # Time the account is locked
    locked_at = Column(DateTime, nullable=True, default=None)
    
    # Timestamp when the user was created, defaults to the current time
    created_at = Column(DateTime, default=datetime.now, nullable=False)

