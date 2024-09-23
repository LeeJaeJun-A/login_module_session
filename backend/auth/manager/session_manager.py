from backend.auth.database.models import SessionModel
from backend.auth.database.base_manager import BaseManager
from datetime import datetime, timedelta
import uuid
from fastapi import HTTPException
from backend.config import DOCKER_SESSION_DATABASE_URI, SESSION_DATABASE_URI, IS_DOCKER


class SessionManager(BaseManager):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        session_database_uri=SESSION_DATABASE_URI,
        docker_session_database_uri=DOCKER_SESSION_DATABASE_URI,
        is_docker=IS_DOCKER,
    ):
        if not hasattr(self, "initialized"):
            super().__init__(
                session_database_uri, docker_session_database_uri, is_docker
            )
            self.initialized = True

    def create_session(
        self, user_id: str, role: str, expires_in_minutes: int = 30
    ) -> str:
        session_id = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(minutes=expires_in_minutes)
        session = self.get_session()

        try:
            db_session = SessionModel(
                session_id=session_id, user_id=user_id, role=role, expires_at=expires_at
            )
            session.add(db_session)
            session.commit()
            return session_id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_session_by_id(self, session_id: str) -> SessionModel:
        session = self.get_session()
        try:
            db_session = (
                session.query(SessionModel)
                .filter(SessionModel.session_id == session_id)
                .one_or_none()
            )
            if not db_session:
                raise HTTPException(status_code=401, detail="Session not found")

            if db_session.expires_at < datetime.now():
                session.delete(db_session)
                session.commit()
                raise HTTPException(status_code=401, detail="Session expired")

            return db_session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_session(self, session_id: str) -> bool:
        session = self.get_session()
        try:
            db_session = (
                session.query(SessionModel)
                .filter(SessionModel.session_id == session_id)
                .one_or_none()
            )
            if db_session:
                session.delete(db_session)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_expired_sessions(self):
        session = self.get_session()
        now = datetime.now()
        try:
            expired_sessions = (
                session.query(SessionModel).filter(SessionModel.expires_at < now).all()
            )
            deleted_count = len(expired_sessions)
            for db_session in expired_sessions:
                session.delete(db_session)
            session.commit()
            return {"deleted_sessions": deleted_count}
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
