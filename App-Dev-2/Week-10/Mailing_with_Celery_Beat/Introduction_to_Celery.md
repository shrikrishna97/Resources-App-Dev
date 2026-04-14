---

# **Introduction to Asynchronous Tasks with Celery**

---

## **1. What is Celery and Why Do We Need It?**

### **The Problem**

Imagine your Flask app needs to:

* Send a **monthly report** email to the admin with all reservations data.
* Send **daily reminders** to users who have active bookings.
* **Export a CSV/HTML report** and email it to a user on request.

If you do these inside a normal Flask route:

```
User clicks "Export Report"
  → Flask starts generating the report (5-10 seconds)
  → Flask sends the email (2-3 seconds)
  → User stares at a loading screen for 13 seconds
  → Other users' requests are BLOCKED
```

**This is terrible!** Flask handles one request at a time (per worker). Long tasks block everything.

### **The Solution: Celery**

Celery is a **task queue** — it lets you run time-consuming tasks **in the background**, outside of your Flask request-response cycle.

```
User clicks "Export Report"
  → Flask tells Celery: "Hey, do this task in the background"
  → Flask immediately responds: "Your report is being generated!"
  → User is happy, can keep using the app
  → Celery quietly generates and emails the report in the background
```

### **Simple Analogy**

Think of a restaurant:

* **Without Celery** = The waiter takes your order, goes to the kitchen, cooks the food himself, then comes back. Other customers wait.
* **With Celery** = The waiter takes your order, hands it to the kitchen (task queue), and immediately goes to serve other customers. The kitchen (Celery worker) prepares the food in the background.

---

## **2. How Celery Works — The Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    HOW CELERY WORKS                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Flask App ──sends task──▶ Redis (Broker) ──▶ Celery   │
│  (Producer)              (Message Queue)    (Worker)    │
│                                                         │
│  Flask says:             Redis stores:     Worker does: │
│  "Send email"            the task message  the actual   │
│                          until a worker    email sending│
│                          picks it up                    │
│                                                         │
│  Worker stores result back in Redis (Backend)           │
└─────────────────────────────────────────────────────────┘
```

### **Three Key Components**

| Component | What It Is | Our Choice |
|-----------|-----------|------------|
| **Producer** | The app that creates tasks (Flask) | Flask app |
| **Broker** | Message queue that holds tasks | Redis |
| **Worker** | Process that executes tasks | Celery worker |
| **Backend** | Stores task results | Redis |

### **Why Redis?**

Redis is an **in-memory key-value store** — extremely fast. Celery uses it as:

1. **Broker** — to queue task messages (like a to-do list for workers).
2. **Backend** — to store task results (so you can check if a task succeeded).

We already use Redis for Flask-Caching (Week-11), so it serves double duty here.

---

## **3. Setup and Installation**

### **3.1 Install Python Packages**

```bash
pip install flask flask-sqlalchemy celery redis
```

### **3.2 Install and Start Redis**

#### **Windows (WSL — Windows Subsystem for Linux)**

⚠ Redis does not run natively on Windows. You **must** use WSL.

**Step 1: Open PowerShell as Administrator and install WSL (if not done already)**

```powershell
wsl --install
```

Restart your PC after installation. Then open WSL terminal.

**Step 2: Install Redis inside WSL**

```bash
sudo apt update
sudo apt install -y redis-server
```

**Step 3: Start Redis server**

```bash
redis-server
```

**Step 4: Test Redis (in a new WSL terminal tab)**

```bash
redis-cli ping
```

Output: `PONG` 

#### **macOS**

```bash
brew install redis
redis-server
```

Test:

```bash
redis-cli ping
```

#### **Linux / Ubuntu**

```bash
sudo apt update
sudo apt install -y redis-server
redis-server
```

---

## **4. Project Structure**

Here is how we organize celery in a Flask project:

```
project/
├── app.py              # Flask application
├── models.py           # SQLAlchemy models
├── celery_worker.py    # Celery configuration + beat schedule
├── tasks.py            # All Celery tasks (monthly report, daily reminder, etc.)
├── templates/
│   └── monthly_report.html
└── instance/
    └── database.db
```

> **Why separate files?**
> - `celery_worker.py` — Celery config stays separate from Flask. The celery worker process imports this file.
> - `tasks.py` — All background tasks in one place. Easy to find and maintain.
> - This avoids **circular imports** (Flask imports Celery, Celery imports Flask — breaks!).

---

## **5. Step-by-Step Code — Complete Example**

We will build a simple app with:
- A `User` model and a `BookRequest` model (like a library book request).
- A **monthly report** task that emails the admin a summary.
- A **daily reminder** task that emails users with pending requests.
- A **trigger export** route that starts a background task on demand.

---

### **5.1 `models.py` — Database Models**

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'admin' or 'user'

    requests = db.relationship('BookRequest', backref='user', lazy=True)

class BookRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'returned'
    request_date = db.Column(db.DateTime, server_default=db.func.now())
```

---

### **5.2 `app.py` — Flask Application**

```python
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from models import db, User, BookRequest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

# ---------- Auth Routes ----------

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'user')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'User registered'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if not user:
        return jsonify({'msg': 'Invalid credentials'}), 401
    token = create_access_token(identity=user.id, additional_claims={'role': user.role})
    return jsonify({'access_token': token}), 200

# ---------- Book Request Routes ----------

@app.route('/request-book', methods=['POST'])
@jwt_required()
def request_book():
    data = request.get_json()
    user_id = get_jwt_identity()
    req = BookRequest(user_id=user_id, book_name=data['book_name'])
    db.session.add(req)
    db.session.commit()
    return jsonify({'msg': 'Book requested'}), 201

# ---------- Trigger Export (Async Task) ----------

@app.route('/export-report', methods=['GET'])
@jwt_required()
def export_report():
    user_id = get_jwt_identity()

    # Import here to avoid circular imports
    from tasks import generate_user_report

    # .delay() sends the task to Celery worker in background
    generate_user_report.delay(user_id)

    return jsonify({'msg': 'Report is being generated. You will receive it via email.'}), 200


if __name__ == '__main__':
    app.run(debug=True)
```

**Key point:** Notice `generate_user_report.delay(user_id)` — the `.delay()` method sends the task to the Celery worker. Flask does NOT wait for it to finish. It immediately returns the response to the user.

---

### **5.3 `celery_worker.py` — Celery Configuration**

This is the **brain** of Celery. It configures:
- Which broker (Redis) to use
- How to access Flask's app context (so tasks can use `db`, `render_template`, etc.)
- The **beat schedule** (automated periodic tasks)

```python
from celery import Celery, Task
from celery.schedules import crontab
from app import app

# Create Celery app
# broker = where tasks are queued (Redis DB 1)
# backend = where results are stored (Redis DB 2)
celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/1',
    backend='redis://localhost:6379/2',
    include=['tasks']  # tells Celery where to find task functions
)


# This class ensures every task runs inside Flask's app context
# Without this, tasks can't use db.session, render_template, etc.
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

### **Understanding Each Part**

#### **Broker and Backend URLs**

```
redis://localhost:6379/1
        ↑         ↑    ↑
        host     port  database number
```

Redis has 16 databases (0-15). We use:
- DB 0 → Flask-Caching (if used)
- DB 1 → Celery broker (task queue)
- DB 2 → Celery backend (task results)

This keeps things separate and clean.

#### **`include=['tasks']`**

Tells Celery: "Look in `tasks.py` to find the task functions." Without this, Celery won't know about your `@celery_app.task` functions.

#### **`FlaskTask` — Why Do We Need This?**

Celery workers run in a **separate process** from Flask. They don't have Flask's application context by default. But our tasks need:
- `db.session` to query the database
- `render_template` to generate HTML emails

The `FlaskTask` class wraps every task execution inside `with app.app_context()`, giving tasks access to Flask features.

```
Without FlaskTask:
  Celery worker runs task → tries db.session → CRASH! "Working outside of application context"

With FlaskTask:
  Celery worker runs task → FlaskTask wraps it in app.app_context() → db.session works ✓
```

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

**For testing**, you can temporarily set the schedule to run every 30 seconds:

```python
celery_app.conf.beat_schedule = {
    'test-task': {
        'task': 'tasks.send_daily_reminder',
        'schedule': 30.0,  # every 30 seconds
    },
}
```

---

### **5.4 `tasks.py` — The Actual Tasks**

This is where you write the functions that Celery will execute in the background.

```python
from celery_worker import celery_app
from models import User, BookRequest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import render_template

# ---------- Email Configuration ----------
# Using MailHog for local development (catches all emails without actually sending)
SMTP_HOST = 'localhost'
SMTP_PORT = 1025
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


# ---------- Task 1: Monthly Report ----------
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

    # You can use render_template for a nice HTML email
    html_body = render_template('monthly_report.html', requests=request_data)
    send_email(admin.email, "Monthly Library Report", html_body, content="html")

    return "Monthly report sent to admin."


# ---------- Task 2: Daily Reminder ----------
@celery_app.task
def send_daily_reminder():
    """Sends reminders to users with pending book requests."""
    pending = BookRequest.query.filter_by(status='pending').all()

    for req in pending:
        user = User.query.get(req.user_id)
        send_email(
            user.email,
            "Reminder: Pending Book Request",
            f"Hi {user.username}, your request for '{req.book_name}' is still pending."
        )

    return f"Daily reminders sent to {len(pending)} users."


# ---------- Task 3: Export Report (Triggered by User) ----------
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

    html_body = render_template(
        'monthly_report.html',
        requests=request_data
    )
    send_email(user.email, "Your Book Requests Report", html_body, content="html")

    return f"Report sent to {user.username}."
```

### **Understanding `@celery_app.task`**

The `@celery_app.task` decorator converts a normal Python function into a Celery task. This gives the function special methods:

```python
# Normal call (runs immediately, blocks)
send_monthly_report()

# Async call (sends to Celery worker, does NOT block)
send_monthly_report.delay()

# Async call with more options
send_monthly_report.apply_async(countdown=60)  # run after 60 seconds
```

| Method | What Happens |
|--------|-------------|
| `task()` | Runs immediately (normal function call, no Celery involved) |
| `task.delay(args)` | Sends to Celery worker, runs in background |
| `task.apply_async(args, kwargs)` | Like delay() but with extra options (countdown, eta, etc.) |

---

### **5.5 `templates/monthly_report.html` — Email Template**

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

---

## **6. Running Everything — Step by Step**

You need **4 separate terminals** running at the same time. Here's what to run in each:

### **6.1 Terminal Layout**

```
┌───────────────────────────┬───────────────────────────┐
│  Terminal 1: Redis        │  Terminal 2: Flask App     │
│  redis-server             │  python app.py             │
├───────────────────────────┼───────────────────────────┤
│  Terminal 3: Celery       │  Terminal 4: Celery Beat   │
│  Worker                   │  (Scheduler)               │
│  celery -A celery_worker  │  celery -A celery_worker   │
│  .celery_app worker ...   │  .celery_app beat ...      │
└───────────────────────────┴───────────────────────────┘
```

### **6.2 Commands for WSL (Windows Users)**

Open **4 WSL terminal tabs/windows**.

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

**Terminal 4 — Celery Beat (Scheduler):**

```bash
cd /path/to/your/project
source env/bin/activate
celery -A celery_worker.celery_app beat --loglevel=info
```

### **6.3 Commands for macOS / Linux**

Same commands as above. Open 4 terminal tabs.

**Terminal 1:** `redis-server`
**Terminal 2:** `python app.py`
**Terminal 3:** `celery -A celery_worker.celery_app worker --loglevel=info`
**Terminal 4:** `celery -A celery_worker.celery_app beat --loglevel=info`

### **6.4 Using Windows PowerShell (Running WSL commands from PowerShell)**

If you prefer PowerShell, you can run WSL commands by prefixing with `wsl`:

```powershell
# Terminal 1: Redis
wsl redis-server

# Terminal 2: Flask (run normally in PowerShell if Python is installed on Windows)
python app.py

# Terminal 3: Celery Worker (run inside WSL)
wsl bash -c "cd /mnt/c/path/to/project && source env/bin/activate && celery -A celery_worker.celery_app worker --loglevel=info"

# Terminal 4: Celery Beat (run inside WSL)
wsl bash -c "cd /mnt/c/path/to/project && source env/bin/activate && celery -A celery_worker.celery_app beat --loglevel=info"
```

> **Tip:** Celery does not work natively on Windows. Always run Celery worker and Celery beat inside WSL or use a Linux/macOS machine.

---

## **7. What is Celery Worker vs Celery Beat?**

| | Celery Worker | Celery Beat |
|---|---|---|
| **What it does** | Picks up tasks from the queue and **executes** them | **Schedules** periodic tasks and puts them in the queue |
| **Analogy** | The cook in the kitchen who makes the food | The manager who says "make lunch at 12 PM every day" |
| **Runs tasks?** | Yes | No — it only sends task messages to the broker |
| **Required?** | Always (without it, no tasks run) | Only if you have periodic/scheduled tasks |
| **Command** | `celery -A celery_worker.celery_app worker --loglevel=info` | `celery -A celery_worker.celery_app beat --loglevel=info` |

```
How they work together:

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

## **8. MailHog — Catching Emails Locally**

In development, you don't want to send real emails. **MailHog** is a fake SMTP server that catches all outgoing emails and shows them in a web UI.

### **Install MailHog (WSL)**

```bash
sudo apt update
sudo apt install -y golang-go
go install github.com/mailhog/MailHog@latest
```

### **Run MailHog**

```bash
~/go/bin/MailHog
```

### **Install and Run MailHog (macOS)**

```bash
brew install mailhog
mailhog
```

### **Access MailHog UI**

Open browser: **http://localhost:8025**

All emails sent by your tasks will appear here.

### **SMTP Settings for MailHog**

In `tasks.py`, these settings point to MailHog:

```python
SMTP_HOST = 'localhost'
SMTP_PORT = 1025       # MailHog SMTP port
SENDER_EMAIL = 'library@example.com'
SENDER_PASSWORD = ''   # MailHog doesn't need a password
```

---

## **9. Understanding the Complete Flow**

### **Flow 1: User Triggers Export (On-Demand Task)**

```
1. User sends GET /export-report with JWT token
2. Flask route calls: generate_user_report.delay(user_id)
3. Flask immediately returns: {"msg": "Report is being generated..."}
4. Celery worker picks up the task from Redis
5. Worker queries database, generates HTML report
6. Worker sends email via MailHog
7. Email appears in MailHog UI at localhost:8025
```

### **Flow 2: Monthly Report (Scheduled by Beat)**

```
1. Celery Beat checks the beat_schedule
2. On the 1st of every month at 9:00 AM:
   Beat sends 'tasks.send_monthly_report' message to Redis
3. Celery Worker picks up the message
4. Worker runs send_monthly_report()
5. Worker queries all book requests from database
6. Worker generates HTML email using render_template
7. Worker sends email to admin via MailHog
```

### **Flow 3: Daily Reminder (Scheduled by Beat)**

```
1. Every day at 8:00 AM:
   Beat sends 'tasks.send_daily_reminder' message to Redis
2. Worker picks up the message
3. Worker queries all pending book requests
4. For each pending request, worker sends reminder email to the user
5. All emails appear in MailHog
```

---

## **10. Common Errors and Fixes**

### **Error 1: "Working outside of application context"**

```
RuntimeError: Working outside of application context.
```

**Cause:** Your task is trying to use `db.session` or `render_template` without Flask context.

**Fix:** Make sure your `FlaskTask` class is set up in `celery_worker.py`:

```python
class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = FlaskTask
```

### **Error 2: "Received unregistered task"**

```
KeyError: 'tasks.send_monthly_report'
```

**Cause:** Celery doesn't know about your tasks.

**Fix:** Make sure `include=['tasks']` is in your Celery config:

```python
celery_app = Celery('tasks', broker='...', backend='...', include=['tasks'])
```

And the task name in `beat_schedule` matches exactly:

```python
'task': 'tasks.send_monthly_report',  # must match file.function_name
```

### **Error 3: "Connection refused" to Redis**

```
redis.exceptions.ConnectionError: Error connecting to localhost:6379
```

**Cause:** Redis server is not running.

**Fix:** Start Redis:

```bash
redis-server
```

### **Error 4: Celery not working on Windows**

```
ValueError: not enough values to unpack
```

**Cause:** Celery 4+ does not support Windows natively.

**Fix:** Run Celery inside WSL. See Section 6.2.

---

## **11. Using a Simple List Instead of Database (For Quick Testing)**

If you just want to understand Celery without a database, here's a minimal example:

### `app.py` (Minimal)

```python
from flask import Flask, jsonify

app = Flask(__name__)

# Simple in-memory data
users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
]

books = [
    {'user_id': 1, 'book': 'Flask Mastery', 'status': 'pending'},
    {'user_id': 2, 'book': 'Vue.js Guide', 'status': 'pending'},
]

@app.route('/send-reminders')
def send_reminders():
    from tasks import send_reminder_to_all
    send_reminder_to_all.delay()
    return jsonify({'msg': 'Reminders are being sent in background!'})

if __name__ == '__main__':
    app.run(debug=True)
```

### `celery_worker.py` (Minimal)

```python
from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/1',
    backend='redis://localhost:6379/2',
    include=['tasks']
)
```

### `tasks.py` (Minimal)

```python
from celery_worker import celery_app
import time

@celery_app.task
def send_reminder_to_all():
    users = [
        {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
        {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
    ]
    for user in users:
        print(f"Sending reminder to {user['name']} at {user['email']}...")
        time.sleep(2)  # Simulating email sending
    return "All reminders sent!"
```

Run the same 3 terminals (Redis, Flask, Celery worker) and hit `http://localhost:5000/send-reminders`. You'll see the task running in the Celery worker terminal.

---

## **12. Quick Reference — All Commands**

### **Install**

```bash
pip install flask flask-sqlalchemy flask-jwt-extended celery redis
```

### **Run (4 terminals needed)**

| Terminal | Command | Purpose |
|----------|---------|---------|
| 1 | `redis-server` | Start message broker |
| 2 | `python app.py` | Start Flask app |
| 3 | `celery -A celery_worker.celery_app worker --loglevel=info` | Start task executor |
| 4 | `celery -A celery_worker.celery_app beat --loglevel=info` | Start task scheduler |
| 5 (optional) | `~/go/bin/MailHog` | Start email catcher |

### **requirements.txt**

```
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
celery
redis
```

> **Note:** MailHog is NOT a Python package. Install it separately via `go install`.

---

## **13. Summary — What You Need for MAD-2 Project**

| Feature | What to Use | File |
|---------|------------|------|
| Background task on demand (export) | `task.delay()` in a Flask route | `tasks.py`, `app.py` |
| Monthly report to admin | `celery beat` with `crontab(day_of_month=1)` | `celery_worker.py`, `tasks.py` |
| Daily reminder to users | `celery beat` with `crontab(hour=8)` | `celery_worker.py`, `tasks.py` |
| Email sending | `smtplib` with MailHog (development) | `tasks.py` |
| Flask context in tasks | `FlaskTask` class | `celery_worker.py` |
| Task queue broker | Redis | `celery_worker.py` |

### **Checklist for Your Project**

- [ ] Redis installed and running (WSL for Windows)
- [ ] `celery_worker.py` with broker, backend, FlaskTask, and beat_schedule
- [ ] `tasks.py` with `@celery_app.task` for each background task
- [ ] Monthly report task that queries data and sends HTML email
- [ ] Daily reminder task that finds active/pending items and emails users
- [ ] At least one route that triggers a task using `.delay()`
- [ ] MailHog installed for testing emails locally
- [ ] All 4 terminals running: Redis, Flask, Celery Worker, Celery Beat
