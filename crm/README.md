# Gharpayy CRM MVP

This is a minimal lead management application built for a startup helping students and professionals find PG accommodations.

## Stack
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Frontend:** Basic HTML dashboard using Tailwind CSS

## Features
1. Capture leads via API with automatic round-robin agent assignment
2. Track lead pipeline stages
3. Schedule visits and record outcomes
4. Fetch inactive leads (>24h without activity)
5. Dashboard analytics for total leads, stage breakdown, visits and bookings
6. Simple web UI to view metrics and lead list

## Project Structure
```
crm/
  app/
    main.py
    database.py
    models.py
    schemas.py
    routers/
      leads.py
      visits.py
      dashboard.py
    services/
      assignment.py
      reminders.py
    templates/
      dashboard.html
  requirements.txt
  README.md
  FEATURES.md
  QUICKSTART.md
  VERIFICATION.md
```

## Setup Instructions
1. **Install Dependencies**
   ```bash
   cd crm
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Database**
   Create a PostgreSQL database (e.g. `gharpayy`) and update `DATABASE_URL` in `app/database.py` or set the environment variable:
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost:5432/gharpayy"
   ```

3. **Run the Server**
   ```bash
   uvicorn app.main:app --reload
   ```
   The application will create the tables and insert sample agents on startup.

4. **API Endpoints**
   - `POST /leads` – create a new lead
   - `GET /leads` – list all leads
   - `GET /leads/{id}` – get lead by ID
   - `PATCH /leads/{id}/stage` – update lead pipeline stage (pass `status` param)
   - `GET /leads/inactive` – leads inactive >24 hours
   - `POST /visits` – schedule a visit
   - `GET /visits` – list visits
   - `GET /dashboard` – analytics metrics
   - `GET /ui/dashboard` – simple web dashboard

5. **Using the UI**
   Navigate to http://localhost:8000/ui/dashboard to view the dashboard and leads table.

## Notes
- Tailwind is included via CDN in the HTML template for simplicity.
- The round-robin logic is in `app/services/assignment.py`.
- Inactive leads calculation is in `app/services/reminders.py`.

## Seed Data
On startup, the app adds three sample agents: Alice, Bob, and Carol (only if the agents table is empty).

## Extending
This MVP can be extended by adding authentication, property management, email notifications, more detailed activity tracking, etc.
