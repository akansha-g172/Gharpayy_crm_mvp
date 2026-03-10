from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/visits", tags=["visits"])

@router.post("/", response_model=schemas.Visit)
def schedule_visit(visit: schemas.VisitCreate, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == visit.lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    new_visit = models.Visit(**visit.dict())
    db.add(new_visit)
    # update lead stage and last activity
    lead.status = "Visit Scheduled"
    lead.last_activity_at = datetime.utcnow()
    db.commit()
    db.refresh(new_visit)
    return new_visit

@router.get("/", response_model=list[schemas.Visit])
def get_visits(db: Session = Depends(get_db)):
    return db.query(models.Visit).all()
