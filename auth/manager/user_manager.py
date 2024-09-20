import bcrypt
from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from auth.database.models import User
from auth.database.base_manager import BaseManager
from datetime import datetime, timedelta
from auth.config import (
    LOCK_TIME_MINUTES,
    MAX_FAILURES,
    REHASH_COUNT_STANDARD,
    DEFAULT_ROOT_ACCOUNT_ID,
    DEFAULT_ROOT_ACCOUNT_PASSWORD,
    DOCKER_USER_DATABASE_URI,
    USER_DATABASE_URI,
    IS_DOCKER,
)


class UserManager(BaseManager):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        user_database_uri=USER_DATABASE_URI,
        docker_user_database_uri=DOCKER_USER_DATABASE_URI,
        is_docker=IS_DOCKER,
    ):
        if not hasattr(self, "initialized"):
            super().__init__(user_database_uri, docker_user_database_uri, is_docker)
            self.create_root()
            self.initialized = True

    def create_root(self):
        session = self.get_session()
        try:
            user = (
                session.query(User)
                .filter(User.id == DEFAULT_ROOT_ACCOUNT_ID)
                .one_or_none()
            )
            if not user:
                salt, hashed_password = self.hash_password(
                    DEFAULT_ROOT_ACCOUNT_PASSWORD
                )
                root_user = User(
                    id=DEFAULT_ROOT_ACCOUNT_ID,
                    password=hashed_password,
                    salt=salt,
                    role="admin",
                    logins_before_rehash=0,
                    failed_attempts=0,
                    is_locked=False,
                )
                session.add(root_user)
                session.commit()
                session.refresh(root_user)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def hash_password(self, password: str) -> tuple[str, str]:
        salt = bcrypt.gensalt().decode("utf-8")
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), salt.encode("utf-8")
        ).decode("utf-8")
        return salt, hashed_password

    def get_all_users(self):
        session = self.get_session()
        try:
            users = session.query(User).all()
            return users
        except Exception as e:
            session.rollback()
            raise ValueError("Failed to retrieve users") from e
        finally:
            session.close()

    def create_user(self, user_id: str, password: str, role: str):
        session = self.get_session()
        try:
            existing_user = session.query(User).filter(User.id == user_id).one_or_none()
            if existing_user:
                return False

            salt, hashed_password = self.hash_password(password)
            new_user = User(
                id=user_id,
                password=hashed_password,
                salt=salt,
                role=role,
                logins_before_rehash=0,
                failed_attempts=0,
                is_locked=False,
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_user(self, user_id: str) -> bool:
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                return False

            session.delete(user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise ValueError("Failed to delete user") from e
        finally:
            session.close()

    def login(self, user_id: str, plain_password: str) -> str:
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                raise HTTPException(
                    status_code=HTTP_404_NOT_FOUND, detail="User not found"
                )

            if user.is_locked:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Account is locked due to too many failed login attempts",
                )

            stored_hashed_password = user.password.encode("utf-8")
            stored_salt = user.salt.encode("utf-8")
            hashed_input_password = bcrypt.hashpw(
                plain_password.encode("utf-8"), stored_salt
            )

            if hashed_input_password == stored_hashed_password:
                user.logins_before_rehash += 1
                user.failed_attempts = 0

                if user.logins_before_rehash >= REHASH_COUNT_STANDARD:
                    salt, hashed_password = self.hash_password(plain_password)
                    user.password = hashed_password
                    user.salt = salt
                    user.logins_before_rehash = 0
                session.commit()
                return user.role
            else:
                now = datetime.now()

                if user.last_failed_login and now - user.last_failed_login < timedelta(
                    minutes=LOCK_TIME_MINUTES
                ):
                    user.failed_attempts += 1

                    if user.failed_attempts >= MAX_FAILURES:
                        user.is_locked = True
                        session.commit()
                        raise HTTPException(
                            status_code=HTTP_403_FORBIDDEN,
                            detail="Account is locked due to too many failed login attempts",
                        )
                else:
                    user.failed_attempts = 1

                user.last_failed_login = now
                session.commit()
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail=f"Incorrect password",
                )
        except HTTPException as http_err:
            raise http_err
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=500, detail="An internal error occurred during login"
            ) from e
        finally:
            session.close()

    def login_root(self, user_id: str, plain_password: str) -> str:
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                raise HTTPException(
                    status_code=HTTP_404_NOT_FOUND, detail="User not found"
                )

            stored_hashed_password = user.password.encode("utf-8")
            stored_salt = user.salt.encode("utf-8")
            hashed_input_password = bcrypt.hashpw(
                plain_password.encode("utf-8"), stored_salt
            )

            if hashed_input_password == stored_hashed_password:
                return user.role
            else:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail=f"Incorrect password",
                )
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=500, detail="An internal error occurred during login"
            ) from e
        finally:
            session.close()

    def unlock_account(self, user_id: str) -> bool:
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                return False

            if not user.is_locked:
                return False

            user.is_locked = False
            user.failed_attempts = 0
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise ValueError("Failed to unlock account") from e
        finally:
            session.close()
