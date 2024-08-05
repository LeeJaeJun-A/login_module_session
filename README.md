# JWT-Based Login Module
This project implements JWT (JSON Web Token) based authentication using FastAPI for the backend and SvelteKit for the frontend. This document explains how to set up the project, configure the .env file, and get started.

![Svelte](https://img.shields.io/badge/svelte-%23f1413d.svg?style=for-the-badge&logo=svelte&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

## Requirements
- Python 3.9 or higher
- Node.js 16.x or higher
- pip (Python package manager)
- npm or yarn (JavaScript package managers)

## Installation and Setup
### 1. Clone this repository or download it, and place it where you want to.

### 2. Set Up the FastAPI Backend
1. Install Backend Dependencies:
```bash
cd backend
pip install -r requirements.txt
```
2. Configure .env File:
``` .env
# JWT (JSON Web Token) Configuration
JWT_SECRET_KEY="your_generated_secret_key_here"  # Replace with a strong secret key
JWT_ALGORITHM="HS256"  # Algorithm used for encoding and decoding JWTs
JWT_ACCESS_TOKEN_EXPIRE_SECONDS=3600  # Access token expiry time in seconds (1 hour)
JWT_REFRESH_TOKEN_EXPIRE_SECONDS=86400  # Refresh token expiry time in seconds (24 hours)

# Database Configuration
AUTH_MODULE_DB_PATH="sqlite:///./auth.db"  # Replace with your actual database URL or path

# Account Settings for the Service Web Application
DEFAULT_ROOT_ACCOUNT_ID="root"  # Replace with a secure root account ID
DEFAULT_ROOT_ACCOUNT_PASSWORD="root1234"  # Replace with a secure root account password

# Account Lockout Settings
MAX_FAILURES=5  # Adjust based on your security policy
LOCK_TIME_MINUTES=5  # Adjust based on your security policy

# FastAPI URL Configuration
VITE_FASTAPI_URL="http://127.0.0.1:8000"  # Replace with your production FastAPI URL

# Password Rehashing Configuration
REHASH_COUNT_STANDARD=10  # Adjust based on your security requirements
```
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
if you get bleow error,
``` bash
Error: Cannot find module 'sweetalert2' imported from 'C:/projects/rcs-web-v2/frontend/src/lib/components/LoginForm.svelte'
    at nodeImport (file:///C:/projects/rcs-web-v2/frontend/node_modules/vite/dist/node/chunks/dep-mCdpKltl.js:52726:19)
    at ssrImport (file:///C:/projects/rcs-web-v2/frontend/node_modules/vite/dist/node/chunks/dep-mCdpKltl.js:52591:22)
    at eval (C:/projects/rcs-web-v2/frontend/src/lib/components/LoginForm.svelte:7:37)
    at async instantiateModule (file:///C:/projects/rcs-web-v2/frontend/node_modules/vite/dist/node/chunks/dep-mCdpKltl.js:52650:5) {
  code: 'ERR_MODULE_NOT_FOUND'
}
```
you need to insatll the 'sweetalert2' package specifically:
```bash
npm install sweetalert2
```

2. Run the Frontend Development Server:
```bash
npm run dev
```

## API Endpoints (backend/routes)
### post /token
Handles user login and returns an access token and refresh token.

### post /refresh
Refreshes the access token using the provided refresh token.

### get /verify-token
Verifies the validity of a provided JWT and returns user information.

### post /users
Creates a new user in the database.

### delete /users/{id}
Deletes a user by ID, except the root administrator account.

### get /users
Retrieves a list of users, optionally filtered by role.

### get /users/locked
Retrieves a list of locked user accounts.

### post /users/{id}/unlock
Unlocks a user account by ID.

### post /users/{id}/lock"
Locks a user account by ID.