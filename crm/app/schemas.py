from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AgentBase(BaseModel):
    name: str
    email: str

class AgentCreate(AgentBase):
    pass

class Agent(AgentBase):
    id: int

    class Config:
        orm_mode = True

class LeadBase(BaseModel):
    name: str
    phone: str
    source: Optional[str] = None
    assigned_agent_id: Optional[int] = None

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    status: Optional[str]
    created_at: datetime
    updated_at: datetime
    last_activity_at: datetime

    class Config:
        orm_mode = True

class VisitBase(BaseModel):
    lead_id: int
    property_name: str
    visit_date: datetime
    visit_time: Optional[str] = None
    assigned_staff: Optional[str] = None
    outcome: Optional[str] = None

class VisitCreate(VisitBase):
    pass

class Visit(VisitBase):
    id: int

    class Config:
        orm_mode = True

class ActivityBase(BaseModel):
    lead_id: int
    type: str
    note: Optional[str] = None

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# dashboard schemas
class DashboardMetrics(BaseModel):
    total_leads: int
    leads_by_stage: dict
    visits_scheduled: int
    bookings_confirmed: int
