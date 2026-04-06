---

# **Introduction to Asynchronous Tasks with Celery**

---

## **1. What is Celery and Why Do We Need It?**

### **The Problem**

Imagine your Flask app needs to:

* **Export a CSV/HTML report** and email it to a user on request.
* Send a **monthly report** email to the admin with all data.
* Send **daily reminders** to users who have active bookings.

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

We will use Redis for Flask-Caching (Week-11), so it serves double duty here.

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

Here is how we organize Celery in a Flask project:

```
project/
├── app.py              # Flask application
├── models.py           # SQLAlchemy models
├── celery_worker.py    # Celery configuration
├── tasks.py            # All Celery tasks
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

## **5. Step-by-Step Code**

We will build a simple app with:
- A `User` model and a `BookRequest` model (like a library book request).
- A **trigger export** route that starts a background task on demand using `.delay()`.

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

```python
from celery import Celery, Task
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

---

### **5.4 `tasks.py` — An On-Demand Export Task**

This task is triggered by the user via the `/export-report` route. It runs in the background.

```python
from celery_worker import celery_app
from models import User, BookRequest


# ---------- Task: Export Report (Triggered by User via .delay()) ----------
@celery_app.task
def generate_user_report(user_id):
    """Generates and prints a report for a specific user's book requests."""
    user = User.query.get(user_id)
    if not user:
        return "User not found"

    requests = BookRequest.query.filter_by(user_id=user_id).all()
    
    print(f"\n--- Report for {user.username} ---")
    for req in requests:
        print(f"  Book: {req.book_name} | Status: {req.status} | Date: {req.request_date}")
    print("--- End Report ---\n")

    return f"Report generated for {user.username}."
```

> We are just printing the report here. In the **next session (Mailing with Celery Beat)**, we will add email sending, HTML templates, and scheduled tasks.

### **Understanding `@celery_app.task`**

The `@celery_app.task` decorator converts a normal Python function into a Celery task. This gives the function special methods:

```python
# Normal call (runs immediately, blocks)
generate_user_report(1)

# Async call (sends to Celery worker, does NOT block)
generate_user_report.delay(1)

# Async call with more options
generate_user_report.apply_async(args=[1], countdown=60)  # run after 60 seconds
```

| Method | What Happens |
|--------|-------------|
| `task()` | Runs immediately (normal function call, no Celery involved) |
| `task.delay(args)` | Sends to Celery worker, runs in background |
| `task.apply_async(args, kwargs)` | Like delay() but with extra options (countdown, eta, etc.) |

---

## **6. Running Everything — Step by Step**

You need **3 separate terminals** running at the same time:

### **6.1 Terminal Layout**

```
┌───────────────────────────┬───────────────────────────┐
│  Terminal 1: Redis        │  Terminal 2: Flask App     │
│  redis-server             │  python app.py             │
├───────────────────────────┼───────────────────────────┤
│  Terminal 3: Celery       │                            │
│  Worker                   │                            │
│  celery -A celery_worker  │                            │
│  .celery_app worker ...   │                            │
└───────────────────────────┴───────────────────────────┘
```

### **6.2 Commands for WSL (Windows Users)**

Open **3 WSL terminal tabs/windows**.

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

### **6.3 Commands for macOS / Linux**

Same commands as above. Open 3 terminal tabs.

**Terminal 1:** `redis-server`
**Terminal 2:** `python app.py`
**Terminal 3:** `celery -A celery_worker.celery_app worker --loglevel=info`

### **6.4 Using Windows PowerShell (Running WSL commands from PowerShell)**

If you prefer PowerShell, you can run WSL commands by prefixing with `wsl`:

```powershell
# Terminal 1: Redis
wsl redis-server

# Terminal 2: Flask (run normally in PowerShell if Python is installed on Windows)
python app.py

# Terminal 3: Celery Worker (run inside WSL)
wsl bash -c "cd /mnt/c/path/to/project && source env/bin/activate && celery -A celery_worker.celery_app worker --loglevel=info"
```

> **Tip:** Celery does not work natively on Windows. Always run Celery worker inside WSL or use a Linux/macOS machine.

---

## **7. What Happens When You Hit the Route**

```
1. User sends GET /export-report with JWT token
2. Flask route calls: generate_user_report.delay(user_id)
3. Flask immediately returns: {"msg": "Report is being generated..."}
4. Meanwhile, in your Celery Worker terminal you will see:
   [2026-04-04 10:00:00] Task tasks.generate_user_report[abc-123] received
   --- Report for Alice ---
     Book: Flask Mastery | Status: pending | Date: 2026-04-01
   --- End Report ---
   [2026-04-04 10:00:01] Task tasks.generate_user_report[abc-123] succeeded
```

The user got an instant response. The heavy work happened in the worker process.

---

## **8. Using a Simple List Instead of Database (For Quick Testing)**

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
        time.sleep(2)  # Simulating a slow operation
    return "All reminders sent!"
```

Run 3 terminals (Redis, Flask, Celery worker) and hit `http://localhost:5000/send-reminders`. You'll see the task running in the Celery worker terminal with a 2-second gap between each user — but the browser response was instant!

---

## **9. Common Errors and Fixes**

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
KeyError: 'tasks.generate_user_report'
```

**Cause:** Celery doesn't know about your tasks.

**Fix:** Make sure `include=['tasks']` is in your Celery config:

```python
celery_app = Celery('tasks', broker='...', backend='...', include=['tasks'])
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

## **10. Quick Reference**

### **Install**

```bash
pip install flask flask-sqlalchemy flask-jwt-extended celery redis
```

### **Run (3 terminals needed)**

| Terminal | Command | Purpose |
|----------|---------|---------|
| 1 | `redis-server` | Start message broker |
| 2 | `python app.py` | Start Flask app |
| 3 | `celery -A celery_worker.celery_app worker --loglevel=info` | Start task executor |

### **requirements.txt**

```
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
celery
redis
```

---

## **11. What's Next?**

In this session we covered the **Celery Worker** — how to run tasks in the background using `.delay()`.

But what about tasks that need to run **automatically on a schedule**? Like:
- Send a monthly report on the 1st of every month
- Send daily reminders every morning at 8 AM

That's where **Celery Beat** comes in. In the next session, we will cover:

- **Celery Beat** — the scheduler that triggers tasks automatically
- **Sending emails** with Python's `smtplib`
- **MailHog** — catching emails locally for testing
- **HTML email templates** with Jinja2
- **Monthly report** and **daily reminder** tasks

👉 **Next: Mailing with Python — How to Send E-mails with Celery Beat**
