
---
# **Mailing with Python — How to Send E-mails with Celery Beat**

> **Prerequisite:** Make sure you have read/watched the first session — **Introduction to Asynchronous Tasks with Celery** — where we covered Celery Worker, Redis, `.delay()`, and the basic project setup.

---

## **1. What is Celery Beat?**

In the previous session, we learned how to trigger tasks **manually** using `.delay()` — for example, when a user clicks "Export Report."

But some tasks need to run **automatically on a schedule**:
- Send a **monthly report** to the admin on the 1st of every month.
- Send **daily reminders** to users who have pending book requests.

**Celery Beat** is the scheduler. It watches the clock and pushes tasks into the queue at the right time.

### **Analogy**

- **Celery Worker** = The cook in the kitchen who makes the food.
- **Celery Beat** = The manager who says "make lunch at 12 PM every day."

Beat does **NOT** execute tasks. It only tells the worker **when** to execute them.

```
Celery Beat (scheduler)
  │
  │ "It's 8:00 AM, time for daily_reminder"
  │
  ▼
Redis Broker (queue)
  │
  │ task message waiting...
  │
  ▼
Celery Worker (executor)
  │
  │ picks up task, runs send_daily_reminder()
  │
  ▼
Task Complete ✓
```

---

## **2. Celery Worker vs Celery Beat**

| | Celery Worker | Celery Beat |
|---|---|---|
| **What it does** | Picks up tasks from the queue and **executes** them | **Schedules** periodic tasks and puts them in the queue |
| **Analogy** | The cook in the kitchen | The manager who makes the schedule |
| **Runs tasks?** | Yes | No — it only sends task messages to the broker |
| **Required?** | Always (without it, no tasks run) | Only if you have periodic/scheduled tasks |
| **Command** | `celery -A celery_worker.celery_app worker --loglevel=info` | `celery -A celery_worker.celery_app beat --loglevel=info` |

---

## **3. Sending Emails with Python**

Before we get to Celery Beat, let's understand how to send emails in Python. We use the built-in `smtplib` and `email` libraries — no extra install needed.

### **3.1 How SMTP Works**

```
Your Python code
  │
  │ Connects to SMTP server (like a post office)
  │
  ▼
SMTP Server (MailHog in development / Gmail in production)
  │
  │ Delivers the email
  │
  ▼
Recipient's inbox
```

### **3.2 Basic Email Sending Code**

```python
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_email(to_address, subject, message, content="text"):
    """Send an email using SMTP."""
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['From'] = 'library@example.com'
    msg['Subject'] = subject

    if content == "html":
        msg.attach(MIMEText(message, 'html'))  # HTML email body
    else:
        msg.attach(MIMEText(message, 'plain'))  # Plain text email body

    # Connect to SMTP server and send
    s = smtplib.SMTP(host='localhost', port=1025)  # MailHog
    s.login('library@example.com', '')  # MailHog doesn't need a real password
    s.send_message(msg)
    s.quit()
    return True
```

### **What is MIMEMultipart / MIMEText?**

| Class | Purpose |
|-------|---------|
| `MIMEMultipart` | Creates the email "envelope" — holds To, From, Subject, and the body |
| `MIMEText` | The actual message content — can be plain text or HTML |

Think of it like a physical letter:
- `MIMEMultipart` = the envelope (has the address, return address, stamp)
- `MIMEText` = the letter inside the envelope

---

## **4. MailHog — Catching Emails Locally**

In development, you don't want to send real emails. **MailHog** is a fake SMTP server that catches all outgoing emails and shows them in a web UI.

### **4.1 Install MailHog**

#### **WSL (Windows Users)**

```bash
sudo apt update
sudo apt install -y golang-go
go install github.com/mailhog/MailHog@latest
```

#### **macOS**

```bash
brew install mailhog
```

### **4.2 Run MailHog**

#### **WSL**

```bash
~/go/bin/MailHog
```

#### **macOS**

```bash
mailhog
```

### **4.3 Access MailHog UI**

Open browser: **http://localhost:8025**

All emails sent by your tasks will appear here — no real emails are sent!

### **4.4 SMTP Settings for MailHog**

```python
SMTP_HOST = 'localhost'
SMTP_PORT = 1025       # MailHog's SMTP port
SENDER_EMAIL = 'library@example.com'
SENDER_PASSWORD = ''   # MailHog doesn't need a password
```

> **Note:** MailHog is NOT a Python package. It is a standalone tool installed via Go.

---

## **5. Adding Beat Schedule to `celery_worker.py`**

In the previous session, our `celery_worker.py` only had the Celery config and `FlaskTask`. Now we add the **beat schedule**.

```python
from celery import Celery, Task
from celery.schedules import crontab
from app import app

# Create Celery app
celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/1',
    backend='redis://localhost:6379/2',
    include=['tasks']
)


# Flask app context for tasks
class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = FlaskTask

# Set timezone (important for scheduled tasks)
celery_app.conf.timezone = 'Asia/Kolkata'

# ---------- Beat Schedule (Periodic Tasks) ----------
celery_app.conf.beat_schedule = {
    'monthly-report': {
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(hour=9, minute=0, day_of_month=1),
        # Runs at 9:00 AM on the 1st of every month
    },
    'daily-reminder': {
        'task': 'tasks.send_daily_reminder',
        'schedule': crontab(hour=8, minute=0),
        # Runs every day at 8:00 AM
    },
}
```

### **New Parts Explained**

#### **`from celery.schedules import crontab`**

This is what lets us define "when" to run tasks.

#### **`celery_app.conf.timezone = 'Asia/Kolkata'`**

Important! Without this, Celery uses UTC. If you set `crontab(hour=8)`, it will run at 8 AM UTC, not 8 AM IST. Set the timezone to match your location.

#### **`beat_schedule` — Crontab Explained**

`crontab()` follows the same pattern as Linux cron:

```
crontab(minute, hour, day_of_week, day_of_month, month_of_year)
```

| Schedule | Crontab | Meaning |
|----------|---------|---------|
| Every minute | `crontab()` | Default — runs every minute |
| Every day at 8 AM | `crontab(hour=8, minute=0)` | Daily at 8:00 |
| Every Monday at 9 AM | `crontab(hour=9, minute=0, day_of_week=1)` | Weekly |
| 1st of every month at 9 AM | `crontab(hour=9, minute=0, day_of_month=1)` | Monthly |
| Every 30 seconds | Not directly — use `30.0` (float) instead of crontab | Testing only |

#### **The `'task'` key must match exactly**

```python
'task': 'tasks.send_monthly_report',
#        ↑       ↑
#        file    function name
```

This must match the actual function name in `tasks.py`. If you rename the function, update this too.

#### **For Testing — Run Every 30 Seconds**

Don't wait for 8 AM during development! Temporarily change the schedule:

```python
celery_app.conf.beat_schedule = {
    'test-monthly-report': {
        'task': 'tasks.send_monthly_report',
        'schedule': 30.0,  # every 30 seconds
    },
    'test-daily-reminder': {
        'task': 'tasks.send_daily_reminder',
        'schedule': 30.0,  # every 30 seconds
    },
}
```

---

## **6. Writing the Tasks — `tasks.py`**

Now we write the actual scheduled tasks that send emails.

```python
from celery_worker import celery_app
from models import User, BookRequest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import render_template

# ---------- Email Configuration ----------
SMTP_HOST = 'localhost'
SMTP_PORT = 1025       # MailHog
SENDER_EMAIL = 'library@example.com'
SENDER_PASSWORD = ''


def send_email(to_address, subject, message, content="text"):
    """Helper function to send emails via MailHog (local SMTP)."""
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['From'] = SENDER_EMAIL
    msg['Subject'] = subject

    if content == "html":
        msg.attach(MIMEText(message, 'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    s = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
    s.login(SENDER_EMAIL, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True


# ============================================================
# Task 1: Monthly Report (Scheduled by Beat — 1st of every month)
# ============================================================
@celery_app.task
def send_monthly_report():
    """Sends a monthly summary report to the admin."""
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        return "No admin found"

    # Gather all book requests data
    all_requests = BookRequest.query.all()
    request_data = []
    for req in all_requests:
        user = User.query.get(req.user_id)
        request_data.append({
            'username': user.username,
            'book_name': req.book_name,
            'status': req.status,
            'date': str(req.request_date)
        })

    # Generate HTML email using Jinja2 template
    html_body = render_template('monthly_report.html', requests=request_data)
    send_email(admin.email, "Monthly Library Report", html_body, content="html")

    return "Monthly report sent to admin."


# ============================================================
# Task 2: Daily Reminder (Scheduled by Beat — every day at 8 AM)
# ============================================================
@celery_app.task
def send_daily_reminder():
    """Sends reminders to users with pending book requests."""
    pending = BookRequest.query.filter_by(status='pending').all()

    for req in pending:
        user = User.query.get(req.user_id)
        send_email(
            user.email,
            "Reminder: Pending Book Request",
            f"Hi {user.username}, your request for '{req.book_name}' is still pending. "
            f"Please visit the library to collect it."
        )

    return f"Daily reminders sent to {len(pending)} users."


# ============================================================
# Task 3: Export Report (Triggered by user via .delay())
# ============================================================
@celery_app.task
def generate_user_report(user_id):
    """Generates and emails a report for a specific user's book requests."""
    user = User.query.get(user_id)
    if not user:
        return "User not found"

    requests = BookRequest.query.filter_by(user_id=user_id).all()
    request_data = []
    for req in requests:
        request_data.append({
            'book_name': req.book_name,
            'status': req.status,
            'date': str(req.request_date)
        })

    html_body = render_template('monthly_report.html', requests=request_data)
    send_email(user.email, "Your Book Requests Report", html_body, content="html")

    return f"Report sent to {user.username}."
```

### **How Each Task Gets Triggered**

| Task | Triggered By | How |
|------|-------------|-----|
| `send_monthly_report` | Celery Beat (automatic) | Beat checks crontab → sends to Redis → Worker executes |
| `send_daily_reminder` | Celery Beat (automatic) | Beat checks crontab → sends to Redis → Worker executes |
| `generate_user_report` | User hitting `/export-report` | Flask calls `.delay()` → sends to Redis → Worker executes |

---

## **7. HTML Email Template — `templates/monthly_report.html`**

This is a Jinja2 template used by `render_template()` inside tasks. It generates a nice HTML email.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Monthly Report</title>
</head>
<body>
    <h1>Monthly Library Report</h1>
    <table border="1" cellpadding="8" cellspacing="0">
        <thead>
            <tr>
                <th>Username</th>
                <th>Book</th>
                <th>Status</th>
                <th>Date</th>
            </tr>
        </thead>
        <tbody>
            {% for req in requests %}
            <tr>
                <td>{{ req.username }}</td>
                <td>{{ req.book_name }}</td>
                <td>{{ req.status }}</td>
                <td>{{ req.date }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
```

> **Why HTML?** Plain text emails look boring. With HTML you can add tables, colors, and formatting — which is expected in a professional report email.

---

## **8. Running Everything — 4 Terminals + MailHog**

Now you need **4 terminals** (+ optional 5th for MailHog):

### **8.1 Terminal Layout**

```
┌───────────────────────────┬───────────────────────────┐
│  Terminal 1: Redis        │  Terminal 2: Flask App     │
│  redis-server             │  python app.py             │
├───────────────────────────┼───────────────────────────┤
│  Terminal 3: Celery       │  Terminal 4: Celery Beat   │
│  Worker                   │  (Scheduler)               │
│  celery -A celery_worker  │  celery -A celery_worker   │
│  .celery_app worker ...   │  .celery_app beat ...      │
├───────────────────────────┴───────────────────────────┤
│  Terminal 5 (optional): MailHog                        │
│  ~/go/bin/MailHog                                      │
└───────────────────────────────────────────────────────┘
```

### **8.2 Commands for WSL (Windows Users)**

**Terminal 1 — Redis Server:**

```bash
redis-server
```

**Terminal 2 — Flask App:**

```bash
cd /path/to/your/project
source env/bin/activate
python app.py
```

**Terminal 3 — Celery Worker:**

```bash
cd /path/to/your/project
source env/bin/activate
celery -A celery_worker.celery_app worker --loglevel=info
```

**Terminal 4 — Celery Beat:**

```bash
cd /path/to/your/project
source env/bin/activate
celery -A celery_worker.celery_app beat --loglevel=info
```

**Terminal 5 — MailHog (optional but recommended):**

```bash
~/go/bin/MailHog
```

Then open **http://localhost:8025** in your browser to see caught emails.

### **8.3 Commands for macOS / Linux**

Same as above — open 4-5 terminal tabs.

### **8.4 Using Windows PowerShell**

```powershell
# Terminal 1: Redis
wsl redis-server

# Terminal 2: Flask
python app.py

# Terminal 3: Celery Worker
wsl bash -c "cd /mnt/c/path/to/project && source env/bin/activate && celery -A celery_worker.celery_app worker --loglevel=info"

# Terminal 4: Celery Beat
wsl bash -c "cd /mnt/c/path/to/project && source env/bin/activate && celery -A celery_worker.celery_app beat --loglevel=info"

# Terminal 5: MailHog
wsl ~/go/bin/MailHog
```

---

## **9. Complete Flow — What Happens When**

### **Flow 1: Monthly Report (Automatic — Beat Scheduled)**

```
1. Celery Beat is running, watching the clock
2. It's the 1st of the month, 9:00 AM IST
3. Beat sends message: "run tasks.send_monthly_report" → Redis
4. Celery Worker picks up the message from Redis
5. Worker runs send_monthly_report():
   a. Queries the admin user from database
   b. Queries all book requests
   c. Renders monthly_report.html template
   d. Sends HTML email to admin via MailHog
6. Email appears in MailHog UI at localhost:8025
7. In worker terminal: "Task tasks.send_monthly_report succeeded"
```

### **Flow 2: Daily Reminder (Automatic — Beat Scheduled)**

```
1. Every day at 8:00 AM IST
2. Beat sends message: "run tasks.send_daily_reminder" → Redis
3. Worker picks up the message
4. Worker runs send_daily_reminder():
   a. Queries all pending book requests
   b. For each pending request:
      - Finds the user
      - Sends a plain text reminder email
5. All reminder emails appear in MailHog
6. In worker terminal: "Daily reminders sent to 3 users."
```

### **Flow 3: User Export (Manual — Triggered by `.delay()`)**

```
1. User sends GET /export-report with JWT token
2. Flask calls generate_user_report.delay(user_id)
3. Flask immediately returns: {"msg": "Report is being generated..."}
4. Worker picks up the task
5. Worker queries user's book requests, generates HTML, sends email
6. Email appears in MailHog
```

---

## **10. Testing Tips**

### **10.1 Set Beat Schedule to 30 Seconds for Testing**

```python
celery_app.conf.beat_schedule = {
    'test-monthly': {
        'task': 'tasks.send_monthly_report',
        'schedule': 30.0,  # every 30 seconds
    },
    'test-reminder': {
        'task': 'tasks.send_daily_reminder',
        'schedule': 30.0,  # every 30 seconds
    },
}
```

### **10.2 Add Test Data**

Before testing, register some users and create book requests using **Thunder Client** (VS Code extension).

**Step 1 — Register an admin**

- Method: `POST`
- URL: `http://localhost:5000/register`
- Body → JSON:
```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "pass",
  "role": "admin"
}
```

---

**Step 2 — Register a regular user**

- Method: `POST`
- URL: `http://localhost:5000/register`
- Body → JSON:
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "pass"
}
```

---

**Step 3 — Login as alice (get the token)**

- Method: `POST`
- URL: `http://localhost:5000/login`
- Body → JSON:
```json
{
  "username": "alice",
  "password": "pass"
}
```
- Copy the `access_token` from the response.

---

**Step 4 — Request a book**

- Method: `POST`
- URL: `http://localhost:5000/request-book`
- Headers → Add: `Authorization` : `Bearer <paste_token_here>`
- Body → JSON:
```json
{
  "book_name": "Flask Mastery"
}
```

### **10.3 Check MailHog**

Open **http://localhost:8025** — you should see the monthly report email and daily reminder emails appearing every 30 seconds.

---

## **11. Summary — What You Need for MAD-2 Project**

| Feature | What to Use | File |
|---------|------------|------|
| Background task on demand (export) | `task.delay()` in a Flask route | `tasks.py`, `app.py` |
| Monthly report to admin | `celery beat` with `crontab(day_of_month=1)` | `celery_worker.py`, `tasks.py` |
| Daily reminder to users | `celery beat` with `crontab(hour=8)` | `celery_worker.py`, `tasks.py` |
| Email sending | `smtplib` with MailHog (development) | `tasks.py` |
| HTML email template | Jinja2 `render_template` | `templates/monthly_report.html` |
| Flask context in tasks | `FlaskTask` class | `celery_worker.py` |
| Task queue broker | Redis | `celery_worker.py` |

### **Checklist for Your Project**

- [ ] Redis installed and running (WSL for Windows)
- [ ] `celery_worker.py` with broker, backend, FlaskTask, and beat_schedule
- [ ] `tasks.py` with `@celery_app.task` for each background task
- [ ] `send_email()` helper function using `smtplib`
- [ ] Monthly report task that queries data and sends HTML email to admin
- [ ] Daily reminder task that finds pending items and emails users
- [ ] At least one route that triggers a task using `.delay()`
- [ ] HTML email template in `templates/`
- [ ] MailHog installed for testing emails locally
- [ ] All 4-5 terminals running: Redis, Flask, Celery Worker, Celery Beat, MailHog

### **Remember**

- **Celery Worker** = executes tasks (always needed)
- **Celery Beat** = schedules periodic tasks (needed for monthly/daily tasks)
- **`.delay()`** = trigger a task manually from a Flask route
- **MailHog** = catches emails locally so you can test without sending real emails
- **FlaskTask** = gives Celery access to Flask's `db.session` and `render_template`
