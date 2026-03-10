from sqlalchemy.orm import Session
from .. import models

# simple round-robin: keep track of last assigned agent in memory or db
_last_assigned_id = None

def assign_agent(db: Session):
    """Return an agent id using round-robin over all agents."""
    global _last_assigned_id
    agents = db.query(models.Agent).order_by(models.Agent.id).all()
    if not agents:
        return None
    if _last_assigned_id is None:
        # first time, pick first agent
        chosen = agents[0]
    else:
        # find index of last_assigned and choose next
        ids = [a.id for a in agents]
        try:
            idx = ids.index(_last_assigned_id)
            chosen = agents[(idx + 1) % len(agents)]
        except ValueError:
            chosen = agents[0]
    _last_assigned_id = chosen.id
    return chosen.id
