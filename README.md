#  PlacementMail AI

> AI-Powered Gmail Assistant for Placement & Internship Season

PlacementMail AI is an intelligent email assistant that continuously monitors Gmail, analyzes incoming emails using Large Language Models (Gemini & Groq), extracts deadlines, categorizes placement-related emails, schedules reminders, and sends instant Telegram notifications.

Built for students during placement season so they never miss an interview, assessment, internship opportunity, or application deadline.

---

#  Features

##  Intelligent Gmail Monitoring
- Continuously monitors Gmail inbox
- Detects newly received emails
- Avoids duplicate processing
- Stores processed emails in SQLite

---

##  AI Email Analysis

Uses multiple AI providers:

- Google Gemini
- Groq LLM
- Keyword-based fallback analyzer

Extracts:

- Company Name
- Category
- Priority
- Placement Relevance
- Deadline
- Summary
- Action Required

---

##  Email Categorization

Automatically classifies emails into:

- Placement
- Internship
- Interview
- Assessment
- Offer
- Rejection
- Newsletter
- Other

---

##  Priority Detection

Assigns priority levels:

- 🔴 Critical
- 🟠 High
- 🟡 Medium
- 🟢 Low
- ⚪ Ignore

---

##  Smart Deadline Extraction

Recognizes deadlines such as:

- Tomorrow
- Today
- July 15
- 10 AM Tomorrow
- 15 Aug 2026
- Natural language deadlines

Converts them into actual DateTime values.

---

##  Reminder Scheduler

Automatically schedules reminders:

- 24 Hours Before
- 12 Hours Before
- 6 Hours Before
- 1 Hour Before
- 15 Minutes Before

Uses APScheduler.

---

##  Telegram Notifications

Instant notifications for:

- New Placement Email
- Interview Calls
- Critical Deadlines
- Reminder Alerts

---

##  Dashboard APIs

Provides endpoints for:

- Dashboard Summary
- Recent Emails
- Critical Emails
- Upcoming Deadlines
- Email Search
- Analytics

---

##  Analytics

Generates:

- Category Distribution
- Priority Distribution
- Company Statistics
- Daily Email Trends
- Placement Statistics

---

##  Search

Search emails using:

- Company Name
- Subject
- Sender

---

##  Docker Support

Application is fully containerized using Docker.

Includes:

- Dockerfile
- Docker Compose
- Docker Ignore

---

#  Architecture

```
                Gmail API
                    │
                    ▼
           Gmail Monitoring Service
                    │
                    ▼
             Email Parser Agent
                    │
                    ▼
           AI Analyzer (Gemini/Groq)
                    │
                    ▼
         Deadline Extraction Engine
                    │
                    ▼
             SQLite Database
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 Reminder Scheduler      Telegram Notification
        │
        ▼
 Dashboard & Analytics APIs
```

---

#  Tech Stack

## Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- APScheduler
- SQLite

## AI

- Google Gemini
- Groq LLM

## APIs

- Gmail API
- Telegram Bot API

## Deployment

- Docker
- Docker Compose

---

#  Project Structure

```
placementmail_ai/

├── app/
│
├── api/
├── agents/
├── services/
├── repositories/
├── workflows/
├── reminder/
├── scheduler/
├── models/
├── database/
├── config/
│
├── frontend/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

#  Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/placementmail-ai.git

cd placementmail-ai
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux/Mac

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create:

```
.env
```

using

```
.env.example
```

Fill in your API keys.

---

## Gmail Authentication

Place

```
credentials.json
```

in the project root.

Run the application once to generate

```
token.json
```

---

#  Running the Project

```bash
uvicorn app.main:app --reload
```

Swagger

```
http://localhost:8000/docs
```

---

#  Docker

Build Image

```bash
docker build -t placementmail-ai .
```

Run Container

```bash
docker run -d \
-p 8000:8000 \
--name placementmail-ai \
placementmail-ai
```

Using Docker Compose

```bash
docker compose up -d
```

Stop

```bash
docker compose down
```

---

#  API Endpoints

## Dashboard

```
GET /dashboard/summary

GET /dashboard/recent

GET /dashboard/critical

GET /dashboard/deadlines
```

---

## Emails

```
GET /emails

GET /emails/latest

POST /emails/process/{id}

POST /emails/process-latest
```

---

## Analytics

```
GET /dashboard/analytics

GET /dashboard/analytics/categories

GET /dashboard/analytics/priorities

GET /dashboard/analytics/companies

GET /dashboard/analytics/trend
```

---

## Search

```
GET /dashboard/search?query=
```

---

#  AI Workflow

```
Incoming Gmail

↓

Parser Agent

↓

Gemini

↓

Groq (Fallback)

↓

Keyword Analyzer (Final Fallback)

↓

Database

↓

Scheduler

↓

Telegram Notification
```

---

#  Reminder Workflow

```
Deadline Detected

↓

Parse Date

↓

Schedule Jobs

↓

24h Reminder

↓

12h Reminder

↓

6h Reminder

↓

1h Reminder

↓

15m Reminder
```

---

#  Future Roadmap

- Web Dashboard
- Telegram AI Chatbot
- WhatsApp Notifications
- Resume Matching
- Company Insights
- Interview Preparation
- Calendar Integration
- Voice Assistant
- Mobile App
- Multi-user Authentication
- PostgreSQL Support
- Redis Queue
- RAG-based Email Search

---

#  Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a Pull Request

---

#  License

This project is licensed under the MIT License.

---

# 👨 Author

**Rambabu R**

B.E. Computer Science (AI & ML)

KPR Institute of Engineering and Technology

GitHub: https://github.com/rambaburavi

LinkedIn: https://www.linkedin.com/in/rambaburavi

---

⭐ If you found this project useful, consider giving it a star!