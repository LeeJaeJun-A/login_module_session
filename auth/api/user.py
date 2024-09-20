from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Response
from auth.manager.user_manager import UserManager
from auth.manager.session_manager import SessionManager
from starlette.status import HTTP_401_UNAUTHORIZED
from config import (
    DEFAULT_ROOT_ACCOUNT_ID,
    SESSION_EXPIRE_MINUTE
)

router = APIRouter()
user_manager = UserManager()
session_manager = SessionManager()

class UserCreateRequest(BaseModel):
    user_id: str
    password: str
    role: str


class UserResponse(BaseModel):
    user_id: str
    role: str
    is_locked: bool


class LockUnlockRequest(BaseModel):
    user_id: str


class UserDeleteRequest(BaseModel):
    user_id: str


@router.post("/login")
def login_user(user_id: str, password: str, response: Response):
    try:
        if user_id != DEFAULT_ROOT_ACCOUNT_ID:
            user_role = user_manager.login(user_id, password)
        else:
            user_role = user_manager.login_root(user_id, password)

        if user_role:
            session_id = session_manager.create_session(
                user_id=user_id, 
                role=user_role, 
                expires_in_minutes=SESSION_EXPIRE_MINUTE
            )
            
            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True,
                max_age=SESSION_EXPIRE_MINUTE * 60,
                samesite="Lax",
                secure=False  # Set to True in production when using HTTPS
            )

            return {"message": "Login successful", "role": user_role}

        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred") from e


@router.post("/user")
def create_user(request: UserCreateRequest):
    success = user_manager.create_user(request.user_id, request.password, request.role)
    if success:
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=400, detail="User already exists")


@router.get("/user")
def get_user_list():
    users = user_manager.get_all_users()
    return [
        UserResponse(user_id=user.id, role=user.role, is_locked=user.is_locked)
        for user in users
    ]


@router.delete("/user")
def delete_user(request: UserDeleteRequest):
    if request.user_id == DEFAULT_ROOT_ACCOUNT_ID:
        raise HTTPException(status_code=403, detail="Cannot delete the root account")
    success = user_manager.delete_user(request.user_id)
    if success:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found or deletion failed")


@router.post("/unlock")
def unlock_user(request: LockUnlockRequest):
    success = user_manager.unlock_account(request.user_id)
    if success:
        return {"message": "User account unlocked successfully"}
    else:
        raise HTTPException(
            status_code=400,
            detail="Failed to unlock user account or user is not locked",
        )
