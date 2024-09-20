from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from jose import jwt
from fastapi import HTTPException, status
from auth.config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_ACCESS_TOKEN_EXPIRE_SECONDS,
)


class JWTManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(JWTManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True

    def create_token(self, data: dict, expire_second: int) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(seconds=expire_second)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[Dict]:
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

    def refresh_token(self, refresh_token: str) -> str:
        try:
            payload = self.verify_token(refresh_token)
            user_data = {"user_id": payload.get("user_id"), "role": payload.get("role")}
            new_access_token = self.create_token(
                user_data, JWT_ACCESS_TOKEN_EXPIRE_SECONDS
            )
            return new_access_token
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
