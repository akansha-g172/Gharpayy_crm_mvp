# Quick Start Guide - Gharpayy CRM MVP

## 🚀 Running the Application


# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload
```

Server runs on: `http://localhost:8000`

---

## 📖 User Interfaces

### 1. **Home Page**
- URL: `http://localhost:8000/`
- Shows welcome message
- Navigation to all features

### 2. **Lead Capture Form** ⭐
- URL: `http://localhost:8000/capture`
- Form to add new leads
- Auto-assigns agent (round-robin)
- Shows success message with lead ID

### 3. **Leads Management** ⭐
- URL: `http://localhost:8000/leads`
- Table of all leads
- Search by name/phone
- **Change Status** button to move through pipeline
- Color-coded status badges

### 4. **Visit Scheduling** ⭐
- URL: `http://localhost:8000/visits`
- Schedule property visits
- Select lead from dropdown
- Set date, time, property, outcome
- View all upcoming visits

### 5. **Dashboard** ⭐
- URL: `http://localhost:8000/dashboard`
- Key metrics at top (4 cards)
- Pipeline stage breakdown
- Follow-up reminders section
- Complete leads table
- Auto-refreshes every 30 seconds

---

## 🔌 API Endpoints

### Lead Management
```bash
# Create lead
curl -X POST http://localhost:8000/leads \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","phone":"9876543210","source":"Google Search"}'

# Get all leads
curl http://localhost:8000/leads

# Get specific lead
curl http://localhost:8000/leads/1

# Update lead status
curl -X PATCH "http://localhost:8000/leads/1/stage?status=Contacted"
```

### Visit Management
```bash
# Schedule visit
curl -X POST http://localhost:8000/visits \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": 1,
    "property_name": "Green Park PG",
    "visit_date": "2026-03-15T14:00:00",
    "visit_time": "14:00",
    "assigned_staff": "Alice"
  }'

# Get all visits
curl http://localhost:8000/visits
```

### Reminders
```bash
# Get inactive leads (>24 hours)
curl http://localhost:8000/reminders/inactive

# Get leads needing reminder (24-48 hours)
curl http://localhost:8000/reminders/needs-reminder

# Send reminder for specific lead
curl -X POST http://localhost:8000/reminders/send-reminder/1

# Send bulk reminders
curl -X POST http://localhost:8000/reminders/send-bulk-reminders
```

### Dashboard
```bash
# Get all metrics
curl http://localhost:8000/dashboard
```

---

## 📊 Dashboard Metrics Explained

### Key Cards
- **Total Leads**: All captured leads
- **Visits Scheduled**: Number of visits booked
- **Bookings Confirmed**: Visits with "Booked" outcome
- **Inactive Leads**: No activity >24 hours with option to view the inactive lead

### Pipeline Stages
Shows count of leads in each stage:
- New Lead, Contacted, Requirement Collected, Property Suggested
- Visit Scheduled, Visit Completed, Booked, Lost

### Follow-up Section
- Leads needing reminder (24-48h inactive)
- Inactive leads warning (>24h)
- Quick "Send Reminders" button

---

## 🎯 Sample Data

On startup, app creates:
- **4 Agents**: Alice Johnson, Bob Smith, Carol Williams, David Brown
- **6 Leads**: At various pipeline stages
- **3 Visits**: With outcomes
- **Realistic timestamps**: Varying days/hours ago

Leads automatically assigned round-robin to agents.

---

## 🔍 Testing the Features

### Test Lead Capture
1. Go to `/capture`
2. Fill form with name, phone, source
3. Click "Capture Lead"
4. Check `/leads` to see it appeared

### Test Pipeline Movement
1. Go to `/leads`
2. Click "Change Status" on any lead
3. Select new status
4. Watch status update in table

### Test Visit Scheduling
1. Go to `/visits`
2. Select lead from dropdown
3. Fill property, date, time
4. Click "Schedule Visit"
5. See visit appear in "Upcoming Visits"

### Test Dashboard
1. Go to `/dashboard`
2. See all metrics update
3. Metrics auto-refresh every 30 seconds
4. Click "Send Reminders" to trigger follow-ups

### Test Reminders
```bash
# Check inactive leads
curl http://localhost:8000/reminders/inactive | jq

# Check leads needing reminder
curl http://localhost:8000/reminders/needs-reminder | jq
```

---

## 📁 Project Structure

```
crm/
├── app/
│   ├── main.py                 # FastAPI app, routes, startup
│   ├── database.py             # DB config, SessionLocal
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── seed.py                 # Sample data loader
│   ├── routers/
│   │   ├── leads.py            # Lead CRUD endpoints
│   │   ├── visits.py           # Visit scheduling
│   │   ├── dashboard.py        # Metrics API
│   │   ├── reminders.py        # Reminder endpoints
│   │   └── __init__.py
│   ├── services/
│   │   ├── assignment.py       # Round-robin logic
│   │   ├── reminders.py        # Reminder logic
│   │   └── __init__.py
│   ├── templates/
│   │   ├── capture.html        # Lead form
│   │   ├── leads.html          # Leads table
│   │   ├── visits.html         # Visit scheduling
│   │   └── dashboard.html      # Analytics dashboard
│   └── __init__.py
├── requirements.txt
├── README.md
└── FEATURES.md
```

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Use different port
uvicorn app.main:app --port 8001 --reload
```

### No Agents Appearing
- Check database connection
- Ensure seed data loaded (check startup logs)
- Manually add agents via API:
```bash
curl -X POST http://localhost:8000/leads \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","phone":"1234567890","source":"Test"}'
```

---

## 📚 API Documentation

Auto-generated docs available:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 🎓 Key Features Summary

| Feature | Status | URL/Endpoint |
|---------|--------|-------------|
| Lead Capture | ✅ | POST /leads or /capture UI |
| Lead Pipeline | ✅ | /leads UI + PATCH /leads/{id}/stage |
| Visit Scheduling | ✅ | POST /visits or /visits UI |
| Follow-up Reminders | ✅ | /reminders/* endpoints |
| Dashboard | ✅ | /dashboard endpoint + UI |
| Agent Assignment | ✅ | Auto round-robin |
| Search & Filter | ✅ | /leads UI with search |
| Status Tracking | ✅ | Color-coded badges |

---

Enjoy! 🚀
