from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .routers import leads, visits, dashboard, reminders
from .database import engine, Base, SessionLocal
from .seed import seed_database
app = FastAPI(title="Gharpayy CRM")

# create tables
Base.metadata.create_all(bind=engine)

# mount templates and static if any
templates = Jinja2Templates(directory="app/templates")

# include routers
app.include_router(leads.router)
app.include_router(visits.router)
app.include_router(dashboard.router)
app.include_router(reminders.router)

@app.on_event("startup")
def startup():
    """Initialize database and seed sample data on startup."""
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

@app.get("/", include_in_schema=False, response_class=HTMLResponse)
def root():
    """Home page with navigation and quick stats."""
    with open("app/templates/home.html") as f:
        return HTMLResponse(f.read())

@app.get("/ui/dashboard", response_class=HTMLResponse)
def dashboard_ui_old():
    # serve the simple frontend dashboard
    with open("app/templates/dashboard.html") as f:
        return HTMLResponse(f.read())

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_ui():
    # serve the simple frontend dashboard
    with open("app/templates/dashboard.html") as f:
        return HTMLResponse(f.read())

@app.get("/capture", response_class=HTMLResponse)
def lead_capture_ui():
    """Lead capture form page."""
    with open("app/templates/capture.html") as f:
        return HTMLResponse(f.read())

@app.get("/leads", response_class=HTMLResponse)
def leads_ui():
    """Leads management page."""
    with open("app/templates/leads.html") as f:
        return HTMLResponse(f.read())

@app.get("/visits", response_class=HTMLResponse)
def visits_ui():
    """Visit scheduling page."""
    with open("app/templates/visits.html") as f:
        return HTMLResponse(f.read())
