from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/", response_model=schemas.DashboardMetrics)
def get_metrics(db: Session = Depends(get_db)):
    total_leads = db.query(func.count(models.Lead.id)).scalar()
    # leads by stage
    stages = db.query(models.Lead.status, func.count(models.Lead.id)).group_by(models.Lead.status).all()
    leads_by_stage = {status: count for status, count in stages}
    visits_scheduled = db.query(func.count(models.Visit.id)).scalar()
    bookings_confirmed = db.query(func.count(models.Visit.id)).filter(models.Visit.outcome == "Booked").scalar()
    return schemas.DashboardMetrics(
        total_leads=total_leads or 0,
        leads_by_stage=leads_by_stage,
        visits_scheduled=visits_scheduled or 0,
        bookings_confirmed=bookings_confirmed or 0,
    )
