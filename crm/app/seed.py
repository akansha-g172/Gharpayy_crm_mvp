from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models


def seed_database(db: Session):
    """
    Seed the database with sample agents and leads for testing.
    Only inserts if tables are empty to avoid duplicates.
    """
    # Add sample agents
    if db.query(models.Agent).count() == 0:
        agents = [
            models.Agent(name="Alice Johnson", email="alice@gharpayy.com"),
            models.Agent(name="Bob Smith", email="bob@gharpayy.com"),
            models.Agent(name="Carol Williams", email="carol@gharpayy.com"),
            models.Agent(name="David Brown", email="david@gharpayy.com"),
        ]
        db.add_all(agents)
        db.commit()
    
    # Add sample leads
    if db.query(models.Lead).count() == 0:
        agents = db.query(models.Agent).all()
        if agents:
            leads = [
                models.Lead(
                    name="Rahul Kumar",
                    phone="9876543210",
                    source="Google Search",
                    status="New Lead",
                    assigned_agent_id=agents[0 % len(agents)].id,
                    created_at=datetime.utcnow() - timedelta(days=5),
                    last_activity_at=datetime.utcnow() - timedelta(days=5),
                ),
                models.Lead(
                    name="Priya Sharma",
                    phone="9123456789",
                    source="Facebook Ads",
                    status="Contacted",
                    assigned_agent_id=agents[1 % len(agents)].id,
                    created_at=datetime.utcnow() - timedelta(days=3),
                    last_activity_at=datetime.utcnow() - timedelta(hours=12),
                ),
                models.Lead(
                    name="Arjun Patel",
                    phone="9234567890",
                    source="Instagram",
                    status="Requirement Collected",
                    assigned_agent_id=agents[2 % len(agents)].id,
                    created_at=datetime.utcnow() - timedelta(days=2),
                    last_activity_at=datetime.utcnow() - timedelta(hours=6),
                ),
                models.Lead(
                    name="Neha Singh",
                    phone="9345678901",
                    source="Referral",
                    status="Property Suggested",
                    assigned_agent_id=agents[3 % len(agents)].id,
                    created_at=datetime.utcnow() - timedelta(days=1),
                    last_activity_at=datetime.utcnow() - timedelta(hours=2),
                ),
                models.Lead(
                    name="Aditya Verma",
                    phone="9456789012",
                    source="Google Search",
                    status="Visit Scheduled",
                    assigned_agent_id=agents[4 % len(agents)].id,
                    created_at=datetime.utcnow() - timedelta(hours=12),
                    last_activity_at=datetime.utcnow() - timedelta(hours=1),
                ),
                models.Lead(
                    name="Zara Khan",
                    phone="9567890123",
                    source="WhatsApp",
                    status="Visit Completed",
                    assigned_agent_id=agents[5 % len(agents)].id,
                    created_at=datetime.utcnow() - timedelta(hours=20),
                    last_activity_at=datetime.utcnow() - timedelta(hours=3),
                ),
            ]
            db.add_all(leads)
            db.commit()
            
            # Add sample visits for some leads
            visits = [
                models.Visit(
                    lead_id=leads[3].id,  # Neha Singh
                    property_name="Green Park PG, Bangalore",
                    visit_date=datetime.utcnow() + timedelta(days=2),
                    visit_time="14:00",
                    assigned_staff="Alice Johnson",
                    outcome=None,
                ),
                models.Visit(
                    lead_id=leads[4].id,  # Aditya Verma
                    property_name="Comfort Zone Hostel, Mumbai",
                    visit_date=datetime.utcnow() + timedelta(days=1),
                    visit_time="10:00",
                    assigned_staff="Bob Smith",
                    outcome=None,
                ),
                models.Visit(
                    lead_id=leads[5].id,  # Zara Khan
                    property_name="Home Away, Delhi",
                    visit_date=datetime.utcnow() - timedelta(hours=3),
                    visit_time="15:30",
                    assigned_staff="Carol Williams",
                    outcome="Booked",
                ),
            ]
            db.add_all(visits)
            db.commit()
