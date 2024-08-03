import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from fastapi import  HTTPException, status
from backend.config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM
)

def create_token(data: dict, expire_second: int):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=expire_second)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )