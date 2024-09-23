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
            samesite="Lax",
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
def get_session(request: Request):
    try:
        session_id = request.cookies.get("session_id")

        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is missing")

        db_session = session_manager.get_session_by_id(session_id)

        return {
            "user_id": db_session.user_id,
            "role": db_session.role,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


import logging


@router.post("/logout")
def logout(request: Request, response: Response):
    try:
        # Log the attempt to logout
        logging.info("Attempting to log out")

        session_id = request.cookies.get("session_id")
        if not session_id:
            logging.error("No session ID found in cookies")
            raise HTTPException(
                status_code=400, detail="No session ID found in cookies"
            )

        # Clear the session cookie
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

        # Attempt to delete the session
        session_deleted = session_manager.delete_session(session_id)
        if not session_deleted:
            logging.error(f"Session {session_id} not found")
            raise HTTPException(status_code=404, detail="Session not found")

        logging.info(f"Session {session_id} deleted successfully")
        return {"message": "Logged out successfully"}
    except HTTPException as e:
        logging.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An internal error occurred")
