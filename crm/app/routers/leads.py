from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from .. import models, schemas
from ..database import get_db
from ..services import assignment

router = APIRouter(prefix="/api/leads", tags=["leads"])

@router.post("/", response_model=schemas.Lead)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    # assign agent round-robin
    agent_id = assignment.assign_agent(db)
    new_lead = models.Lead(
        **lead.dict(exclude_unset=True),
        assigned_agent_id=agent_id,
        status="New Lead",
        last_activity_at=datetime.utcnow(),
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead

@router.get("/", response_model=list[schemas.Lead])
def get_leads(db: Session = Depends(get_db)):
    return db.query(models.Lead).all()

@router.get("/inactive", response_model=list[schemas.Lead])
def inactive_leads(db: Session = Depends(get_db)):
    cutoff = datetime.utcnow() - timedelta(hours=24)
    leads = db.query(models.Lead).filter(models.Lead.last_activity_at < cutoff).all()
    return leads

@router.get("/{lead_id}", response_model=schemas.Lead)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.patch("/{lead_id}/stage", response_model=schemas.Lead)
def update_stage(lead_id: int, status: str, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.status = status
    lead.last_activity_at = datetime.utcnow()
    db.commit()
    db.refresh(lead)
    return lead
