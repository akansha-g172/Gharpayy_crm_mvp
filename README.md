# Gharpayy Lead Management System (CRM) – MVP

A Minimum Viable Product (MVP) CRM system built for **Gharpayy** to capture, manage, and track customer leads efficiently.

The system centralizes lead management, assigns leads to agents, tracks the sales pipeline, schedules property visits, and provides basic analytics.

---

# Project Structure

The main application code is inside the `crm/` directory.

---

# Features Implemented (MVP)

### Lead Capture

* Capture leads through form submission
* Automatically create a **Lead Profile**
* Store:

  * Name
  * Phone Number
  * Lead Source
  * Timestamp
  * Assigned Agent
  * Lead Status

### Automatic Lead Assignment

* Round Robin assignment of leads to agents
* Ensures **one clear owner per lead**

### Lead Pipeline

Pipeline stages implemented:

* New Lead
* Contacted
* Requirement Collected
* Property Suggested
* Visit Scheduled
* Visit Completed
* Booked
* Lost

Agents can move leads between stages.

### Visit Scheduling

Agents can:

* Select a property
* Choose visit date and time
* Update visit outcome

### Follow-up Reminder

Inactive leads trigger a **Day-1 follow-up reminder**.

### Dashboard

Basic analytics showing:

* Total leads received
* Leads per pipeline stage
* Visits scheduled
* Confirmed bookings

---

# Tech Stack

Backend

* Python
* FastAPI

Database

* PostgreSQL
* SQLAlchemy ORM

API Server

* Uvicorn

Version Control

* Git + GitHub

---

# Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/akansha-g172/Gharpayy_crm.git
cd Gharpayy_crm/crm
```

---

### 2. Create Virtual Environment

```
python -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Configure Database

Create a PostgreSQL database:

```
createdb gharpayy
```

Set the database connection string:

```
export DATABASE_URL="postgresql://user:password@localhost:5432/gharpayy"
```

---

### 5. Run the Application

```
uvicorn app.main:app --reload
```

API will run at:

```
http://127.0.0.1:8000
```

Interactive API docs:

```
http://127.0.0.1:8000/docs
```

---

# System Architecture

The system follows a **layered backend architecture**:

Client (Forms / Integrations)
↓
FastAPI API Layer
↓
Business Logic (Lead Assignment, Pipeline Management)
↓
SQLAlchemy ORM
↓
PostgreSQL Database

---

# Database Design

Main entities:

* Agents
* Leads
* Visits
* Lead Activities

Relationships:

* One Agent → Many Leads
* One Lead → Many Activities
* One Lead → Visit Scheduling

---

# Scalability Considerations

For production scaling, the system can evolve with:

* Message queues for async lead ingestion
* Background workers for reminders
* Redis caching
* Horizontal API scaling with load balancers
* Webhook integrations for WhatsApp, forms, and social media
* Event-based lead processing pipeline

---

# Future Improvements

* WhatsApp API integration
* Automated lead reassignment
* Agent performance leaderboard
* Lead activity timeline
* Smart property recommendations

---

# Author

Akansha Gupta
Full Stack Developer

This project demonstrates system design, backend architecture, and scalable CRM workflow implementation.
