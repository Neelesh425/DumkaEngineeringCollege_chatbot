# 🤖 DEC Chatbot — Dumka Engineering College

A smart chatbot built for **Dumka Engineering College** to assist students, prospective applicants, and faculty members by answering common queries (courses, fees, faculty, rules, events, etc.).  
The chatbot reduces admin workload and improves accessibility of information through a web/mobile interface.

---

## 📌 Features

- 💬 **Natural Language Query Handling** (Dialogflow NLP)
- 📚 **Knowledge Base Retrieval** (courses, fees, rules, contacts)
- 🧠 **Intent Classification & Entity Extraction**
- 👨‍🏫 **Human Handover** (low-confidence → admin panel)
- 📝 **Session Logs & History**
- 🔔 **Notifications** (deadlines, events, escalations)
- 📊 **Admin Dashboard** (manage KB, view analytics)
- 🌐 **Web & Mobile friendly UI**

---

## 🏗️ Tech Stack

### Backend
- [Python](https://www.python.org/) 3.10+
- [Flask](https://flask.palletsprojects.com/) — REST API
- [Dialogflow](https://cloud.google.com/dialogflow) — NLP & Intent Classification
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- PostgreSQL / MySQL — Database
- Redis — Caching & Session store
- Celery / RQ — Background tasks
- Flask-SocketIO — Real-time admin handover

### Frontend
- HTML5, CSS3, JavaScript (vanilla or React)
- Bootstrap / Tailwind for responsive UI

### Deployment
- Gunicorn + Nginx
- Docker / Docker Compose
- Optional: Kubernetes for scaling

### Utilities
- `python-dotenv` — Environment variables
- `pytest` — Testing
- `sentry-sdk` — Error tracking
- Prometheus + Grafana — Monitoring

---

## ⚙️ Installation & Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/dec-chatbot.git
   cd dec-chatbot
