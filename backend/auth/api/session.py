from fastapi import APIRouter, HTTPException, Response, Request
from backend.auth.manager.session_manager import SessionManager
from pydantic import BaseModel
from backend.config import SESSION_EXPIRE_MINUTE

router = APIRouter()
session_manager = SessionManager()


class CreateSessionRequest(BaseModel):
    user_id: str
    role: str


class CreateSessionResponse(BaseModel):
    session_id: str
    user_id: str
    role: str


class GetSessionResponse(BaseModel):
    user_id: str
    role: str


@router.post("/session", response_model=CreateSessionResponse)
def create_session(request: CreateSessionRequest, response: Response):
    try:
        session_id = session_manager.create_session(
            user_id=request.user_id,
            role=request.role,
            expires_in_minutes=SESSION_EXPIRE_MINUTE,
        )
        db_session = session_manager.get_session_by_id(session_id)

        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=SESSION_EXPIRE_MINUTE * 60,
            samesite="Strict",
            secure=False,  # Set to True in production when using HTTPS
        )

        return {
            "session_id": db_session.session_id,
            "user_id": db_session.user_id,
            "role": db_session.role,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session", response_model=GetSessionResponse)
def get_session(request: Request, user_id: str):
    try:
        session_id = request.cookies.get("session_id")

        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is missing")

        db_session = session_manager.get_session_by_id(session_id)

        if db_session.user_id != user_id:
            raise HTTPException(status_code=403, detail="Invalid session for this user")

        return {
            "user_id": db_session.user_id,
            "role": db_session.role,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/logout")
def logout(response: Response):
    try:
        session_id = response.cookies.get("session_id")

        if not session_id:
            raise HTTPException(
                status_code=400, detail="No session ID found in cookies"
            )

        response.set_cookie(
            key="session_id",
            value="",
            httponly=True,
            max_age=0,
            expires="Thu, 01 Jan 1970 00:00:00 GMT",
            path="/",
            samesite="Lax",
            secure=False,
        )

        session_deleted = session_manager.delete_session(session_id)
        if not session_deleted:
            raise HTTPException(status_code=404, detail="Session not found")

        return {"message": "Logged out successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred")
