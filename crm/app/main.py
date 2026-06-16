from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .routers import leads, visits, dashboard, reminders
from .database import engine, Base, SessionLocal
from .seed import seed_database
app = FastAPI(title="Gharpayy CRM")

# create tables
Base.metadata.create_all(bind=engine)

# compute absolute path for template directory so UI routes work regardless of
# the current working directory. This prevents Render from failing when the
# process is launched from the repository root.
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")


def render_html(filename: str) -> HTMLResponse:
    path = os.path.join(TEMPLATES_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

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
    return render_html("home.html")

@app.get("/ui/dashboard", response_class=HTMLResponse)
def dashboard_ui_old():
    # serve the simple frontend dashboard
    return render_html("dashboard.html")

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_ui():
    # serve the simple frontend dashboard
    return render_html("dashboard.html")

@app.get("/capture", response_class=HTMLResponse)
def lead_capture_ui():
    """Lead capture form page."""
    return render_html("capture.html")

@app.get("/leads", response_class=HTMLResponse)
def leads_ui():
    """Leads management page."""
    return render_html("leads.html")

@app.get("/visits", response_class=HTMLResponse)
def visits_ui():
    """Visit scheduling page."""
    return render_html("visits.html")
