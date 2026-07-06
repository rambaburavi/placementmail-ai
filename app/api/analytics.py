from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.dashboard.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/")
def analytics(
    db: Session = Depends(get_db),
):
    return AnalyticsService(db).analytics()


@router.get("/categories")
def categories(
    db: Session = Depends(get_db),
):
    return AnalyticsService(db).categories()


@router.get("/priorities")
def priorities(
    db: Session = Depends(get_db),
):
    return AnalyticsService(db).priorities()


@router.get("/companies")
def companies(
    db: Session = Depends(get_db),
):
    return AnalyticsService(db).companies()


@router.get("/placement")
def placement(
    db: Session = Depends(get_db),
):
    return AnalyticsService(db).placement()


@router.get("/trend")
def trend(
    db: Session = Depends(get_db),
):
    return AnalyticsService(db).trend()