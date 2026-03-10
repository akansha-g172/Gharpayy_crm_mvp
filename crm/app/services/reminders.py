from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .. import models


def get_inactive_leads(db: Session, hours: int = 24):
    """Fetch leads that haven't been active for the specified hours."""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    return db.query(models.Lead).filter(models.Lead.last_activity_at < cutoff).all()


def send_follow_up_reminder(db: Session, lead_id: int):
    """
    Send a follow-up reminder for a lead.
    In future, this would send an email/SMS.
    For MVP, we log it as an activity.
    """
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        return False
    
    # Create an activity log for the reminder
    reminder_activity = models.Activity(
        lead_id=lead_id,
        type="Follow-up Reminder",
        note=f"Automated follow-up reminder sent for lead {lead.name}. Last activity: {lead.last_activity_at}"
    )
    db.add(reminder_activity)
    
    # In production, would send email/SMS here
    # Example: send_email(lead.email, f"Follow-up: {lead.name}")
    # Example: send_sms(lead.phone, "Hi! Checking in about your PG search")
    
    db.commit()
    return True


def get_leads_needing_reminder(db: Session, hours: int = 24):
    """Get leads that need a follow-up reminder (inactive > 24h)."""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    
    return db.query(models.Lead).filter(
        models.Lead.last_activity_at < cutoff
    ).all()
