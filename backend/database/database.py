from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from backend.config import AUTH_MODULE_DB_PATH

# Create the database engine
engine = create_engine(AUTH_MODULE_DB_PATH, connect_args={"check_same_thread": False})

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create scoped_session
SessionLocal = scoped_session(session_factory)

Base = declarative_base()