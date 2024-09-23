# RMS

![Svelte](https://img.shields.io/badge/svelte-%23f1413d.svg?style=for-the-badge&logo=svelte&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Requirements

- Python 3.9 or higher
- Node.js 16.x or higher
- pip (Python package manager)
- npm or yarn (JavaScript package managers)
- MySQL 8.0 or higher
- Docker 20.10 or higher

## Installation and Setup (Dev)

### 1. Clone this repository or download it, and place it where you want to.

### 2. Set Up the FastAPI Backend

1. Install Backend Dependencies:

```bash
cd backend
pip install -r requirements.txt
```

2. Configure .env File:
   You should update .env file properly. Don't use default value.

```.env
# JWT configuration settings
JWT_SECRET_KEY="SERVER_BY_ENKI_LEEJAEJUN"  # Secret key used to sign JWT tokens
JWT_ALGORITHM="HS256"  # Algorithm used for encoding JWT
JWT_ACCESS_TOKEN_EXPIRE_SECONDS=3600  # Access token expiration time in seconds (1 hour)
JWT_REFRESH_TOKEN_EXPIRE_SECONDS=86400  # Refresh token expiration time in seconds (1 day)

# Session expiration settings
SESSION_EXPIRE_MINUTE=30  # Session expiration time in minutes

# Database connection URIs for Docker and local environments
DOCKER_USER_DATABASE_URI="mysql+pymysql://user:user1234@mysql:3306/rms_user_db"  # URI for the user database in a Docker environment
USER_DATABASE_URI="mysql+pymysql://user:user1234@127.0.0.1/rms_user_db"  # URI for the user database in a local environment
DOCKER_SESSION_DATABASE_URI="mysql+pymysql://user:user1234@mysql:3306/rms_session_db"  # URI for the session database in a Docker environment
SESSION_DATABASE_URI="mysql+pymysql://user:user1234@127.0.0.1/rms_session_db"  # URI for the session database in a local environment

# Default root account credentials
DEFAULT_ROOT_ACCOUNT_ID="root"  # Default root account username
DEFAULT_ROOT_ACCOUNT_PASSWORD="root1234"  # Default root account password

# Account lockout settings
MAX_FAILURES=5  # Maximum allowed failed login attempts before account is locked
LOCK_TIME_MINUTES=5  # Lockout duration in minutes after reaching the maximum failed attempts

# Password rehashing settings
REHASH_COUNT_STANDARD=10  # Number of successful logins before rehashing the password

```

If you want to use the default MySQL URI, you must have a user named 'user' with the password 'user1234' in MySQL

3. Run the Backend Server:

```
uvicorn backend.main:app --reload
```

### 3. Set Up the SvelteKit Frontend

1. Install Frontend Dependencies:

```bash
cd frontend
npm install
```

2. Configure .env File:

```frontend/.env
# FastAPI URL Configuration
# URL for the FastAPI application. Change this to the production URL.  # Replace with your production FastAPI URL
VITE_FASTAPI_URL="http://127.0.0.1:8000"
```

3. Run the Frontend Development Server:

```bash
npm run dev
```

## Running with Docker Compose

If you prefer to run the entire application using Docker Compose, follow these steps:

1. Ensure you have Docker and Docker Compose installed on your system.

2. In the root directory of the project (where docker-compose.yml is located), run the following command:

```bash
docker-compose up --build
```

This command will:

- Build the Docker images for both the backend and frontend services.
- Start the backend FastAPI server, and frontend SvelteKit server.

3. Access the application:

- Frontend: Visit http://localhost:4173 in your web browser to view the frontend application.
- Backend: The FastAPI backend will be running at http://localhost:8000.

To stop the application, press CTRL + C in the terminal where Docker Compose is running, or use:

```bash
docker-compose down
```

This command will stop and remove the containers, but your data will persist in the Docker volumes.
