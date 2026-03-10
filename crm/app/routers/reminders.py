from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..services import reminders
from .. import models, schemas

router = APIRouter(prefix="/api/reminders", tags=["reminders"])

@router.get("/inactive")
def get_inactive_leads_endpoint(hours: int = 24, db: Session = Depends(get_db)):
    """
    Get all leads that are inactive for more than the specified hours.
    Default: 24 hours
    """
    leads = reminders.get_inactive_leads(db, hours=hours)
    return {
        "inactive_hours": hours,
        "count": len(leads),
        "leads": [
            {
                "id": lead.id,
                "name": lead.name,
                "phone": lead.phone,
                "status": lead.status,
                "last_activity": lead.last_activity_at,
                "days_inactive": (datetime.utcnow() - lead.last_activity_at).days
            }
            for lead in leads
        ]
    }

@router.get("/needs-reminder")
def get_leads_needing_reminder(db: Session = Depends(get_db)):
    """
    Get leads that need a follow-up reminder.
    These are leads inactive between 24-48 hours.
    """
    leads = reminders.get_leads_needing_reminder(db)
    return {
        "count": len(leads),
        "leads": [
            {
                "id": lead.id,
                "name": lead.name,
                "phone": lead.phone,
                "status": lead.status,
                "assigned_agent_id": lead.assigned_agent_id,
                "last_activity": lead.last_activity_at
            }
            for lead in leads
        ]
    }

@router.post("/send-reminder/{lead_id}")
def send_reminder(lead_id: int, db: Session = Depends(get_db)):
    """
    Manually trigger a follow-up reminder for a specific lead.
    In production, this would send an email or SMS.
    """
    success = reminders.send_follow_up_reminder(db, lead_id)
    if success:
        return {"message": f"Reminder sent for lead {lead_id}", "status": "success"}
    else:
        return {"message": f"Lead {lead_id} not found", "status": "error"}

@router.post("/send-bulk-reminders")
def send_bulk_reminders(db: Session = Depends(get_db)):
    """
    Send reminders to all leads that need them (inactive 24-48 hours).
    Usually called by a scheduled background job.
    """
    leads = reminders.get_leads_needing_reminder(db)
    count = 0
    for lead in leads:
        if reminders.send_follow_up_reminder(db, lead.id):
            count += 1
    
    return {
        "message": f"Reminders sent to {count} leads",
        "status": "success",
        "leads_count": count
    }
