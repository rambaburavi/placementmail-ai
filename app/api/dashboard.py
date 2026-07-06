from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.dashboard.dashboard_service import DashboardService

router = APIRouter()


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return DashboardService(db).get_summary()


@router.get("/recent")
def recent(db: Session = Depends(get_db)):
    return DashboardService(db).get_recent()


@router.get("/critical")
def critical(db: Session = Depends(get_db)):
    return DashboardService(db).get_critical()


@router.get("/deadlines")
def deadlines(db: Session = Depends(get_db)):
    return DashboardService(db).get_upcoming_deadlines()


@router.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    return DashboardService(db).search(q)


@router.get("/email/{email_id}")
def email(email_id: int, db: Session = Depends(get_db)):
    return DashboardService(db).get_email(email_id)