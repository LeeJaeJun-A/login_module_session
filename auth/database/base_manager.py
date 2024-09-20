from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from auth.database.models import Base


class BaseManager:
    def __init__(self, database_uri, docker_database_uri, is_docker):
        self.database_uri = docker_database_uri if is_docker == "true" else database_uri
        base_url, db_name = self.extract_db_url_and_name(self.database_uri)
        base_engine = create_engine(base_url)
        self.create_database_if_not_exists(base_engine, db_name)

        self.engine = create_engine(self.database_uri)
        self.SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )
        Base.metadata.create_all(bind=self.engine)

    def extract_db_url_and_name(self, database_url):
        base_url = database_url.rsplit("/", 1)[0]
        db_name = database_url.rsplit("/", 1)[-1]
        return base_url, db_name

    def create_database_if_not_exists(self, engine, db_name):
        with engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))

    def get_session(self):
        return self.SessionLocal()

    def __del__(self):
        self.SessionLocal.remove()
        self.engine.dispose()
