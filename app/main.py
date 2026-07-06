from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.init_db import init_db
from app.database.database import SessionLocal
from app.api.dashboard import router as dashboard_router
from app.api.email import router as email_router
from app.api.webhook import router as webhook_router
from app.api.analytics import router as analytics_router
from app.scheduler.scheduler import start_scheduler

# Import models so SQLAlchemy registers them
from app.models.email import Email
from app.models.gmail_state import GmailState
from app.models.email_reminder import EmailReminder

from app.reminder.recovery_service import ReminderRecoveryService

init_db()

app = FastAPI(
    title="PlacementMail AI",
    version="1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():

    # Start APScheduler
    start_scheduler()

    # Restore reminder jobs
    db = SessionLocal()

    try:
        ReminderRecoveryService(db).restore()
    finally:
        db.close()


app.include_router(
    email_router,
    prefix="/emails",
    tags=["Emails"],
)

app.include_router(
    webhook_router,
    prefix="/webhook",
    tags=["Webhook"],
)

app.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"],
)
app.include_router(
    analytics_router,
    prefix="/dashboard/analytics",
    tags=["Dashboard Analytics"],
)

@app.get("/")
def home():
    return {
        "status": "running",
        "project": "PlacementMail AI",
    }