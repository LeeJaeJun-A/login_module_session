from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from typing import Dict
from backend.auth.manager.jwt_manager import JWTManager

router = APIRouter()
token_manager = JWTManager()


class TokenRequest(BaseModel):
    access_token: str


class TokenResponse(BaseModel):
    payload: Dict


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str


@router.post("/verify-token", response_model=TokenResponse)
def verify_token(request: TokenRequest):
    try:
        payload = token_manager.verify_token(request.access_token)
        return {"payload": payload}
    except HTTPException as e:
        raise e


@router.post("/refresh-token", response_model=RefreshTokenResponse)
def refresh_access_token(request: RefreshTokenRequest):
    try:
        new_access_token = token_manager.refresh_token(request.refresh_token)
        return {"access_token": new_access_token}
    except HTTPException as e:
        raise e
