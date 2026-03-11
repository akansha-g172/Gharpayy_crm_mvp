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
import os
from fastapi import Request

# compute absolute path for templates directory so UI routes work regardless of
# the current working directory.  On Railway the process may start outside of
# the crm folder which caused earlier 500 errors when using relative paths.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

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
def root(request: Request):
    """Home page with navigation and quick stats."""
    # render via Jinja2 so template inheritance or path resolution is consistent
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/ui/dashboard", response_class=HTMLResponse)
def dashboard_ui_old(request: Request):
    # serve the simple frontend dashboard
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_ui(request: Request):
    # serve the simple frontend dashboard
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/capture", response_class=HTMLResponse)
def lead_capture_ui(request: Request):
    """Lead capture form page."""
    return templates.TemplateResponse("capture.html", {"request": request})

@app.get("/leads", response_class=HTMLResponse)
def leads_ui(request: Request):
    """Leads management page."""
    return templates.TemplateResponse("leads.html", {"request": request})

@app.get("/visits", response_class=HTMLResponse)
def visits_ui(request: Request):
    """Visit scheduling page."""
    return templates.TemplateResponse("visits.html", {"request": request})
