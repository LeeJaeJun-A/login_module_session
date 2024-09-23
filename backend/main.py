from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.auth.api import jwt, user, session
from backend.auth.manager.session_manager import SessionManager
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

session_manager = SessionManager()

scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(session_manager.delete_expired_sessions, "interval", minutes=60)
    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI()

app.include_router(jwt.router, tags=["jwt"], prefix="/api/auth")
app.include_router(user.router, tags=["user"], prefix="/api/auth")
app.include_router(session.router, tags=["session"], prefix="/api/auth")

origins = ["http://localhost:5173", "http://localhost:4173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello World!"}
