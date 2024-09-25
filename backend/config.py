import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SESSION_EXPIRE_MINUTE = int(os.getenv("SESSION_EXPIRE_MINUTE", 30))

DOCKER_USER_DATABASE_URI = os.getenv(
    "DOCKER_USER_DATABASE_URI", "mysql+pymysql://user:user1234@mysql:3306/rms_user_db"
)
USER_DATABASE_URI = os.getenv(
    "USER_DATABASE_URI", "mysql+pymysql://user:user1234@127.0.0.1/rms_user_db"
)
DOCKER_SESSION_DATABASE_URI = os.getenv(
    "DOCKER_SESSION_DATABASE_URI", "mysql+pymysql://user:user1234@mysql:3306/rms_session_db"
)
SESSION_DATABASE_URI = os.getenv(
    "SESSION_DATABASE_URI", "mysql+pymysql://user:user1234@127.0.0.1/rms_session_db"
)

MAX_FAILURES = int(os.getenv("MAX_FAILURES", 5))
LOCK_TIME_MINUTES = int(os.getenv("LOCK_TIME_MINUTES", 5))
REHASH_COUNT_STANDARD = int(os.getenv("REHASH_COUNT_STANDARD", 10))

DEFAULT_ROOT_ACCOUNT_ID = os.getenv("DEFAULT_ROOT_ACCOUNT_ID", "root")
DEFAULT_ROOT_ACCOUNT_PASSWORD = os.getenv("DEFAULT_ROOT_ACCOUNT_PASSWORD", "root1234")


IS_DOCKER = os.getenv("IS_DOCKER", "false")
