# Server-Sent Events (SSE) — Complete Notes

---

## Table of Contents

1. [What is SSE?](#1-what-is-sse)
2. [How SSE Works (The Flow)](#2-how-sse-works-the-flow)
3. [SSE Event Stream Format](#3-sse-event-stream-format)
4. [Flask-SSE with Blueprint ](#4-flask-sse-with-blueprint)
5. [Can We Use SSE Without Blueprint?](#5-can-we-use-sse-without-blueprint)
6. [How Client Sends Data to Server for SSE Push](#6-how-client-sends-data-to-server-for-sse-push)
7. [Pub/Sub Pattern and SSE](#7-pubsub-pattern-and-sse)
8. [SSE vs WebSockets vs Polling vs Webhooks](#8-sse-vs-websockets-vs-polling-vs-webhooks)
9. [JSON Data Exchange Between Frontend and Backend](#9-json-data-exchange-between-frontend-and-backend)

---

## 1. What is SSE?

**Server-Sent Events (SSE)** is a technology where the **server pushes data to the client** over a single, long-lived HTTP connection. The client opens a connection once, and the server keeps sending updates whenever it wants.

**Key Points:**
- **One-way communication**: Server → Client only
- Uses plain HTTP (no special protocol like WebSocket)
- Client uses the browser's built-in `EventSource` API
- Server responds with `Content-Type: text/event-stream`
- Connection **auto-reconnects** if dropped (built-in browser behavior)
- Works over HTTP/1.1 and HTTP/2

**Real-world analogy:** Think of a radio station. You tune in (open connection), and the station keeps broadcasting (server keeps pushing). You can't talk back through the radio.

**Use cases:**
- Live notifications
- Stock price tickers
- Live score updates
- Social media feed updates
- Server log streaming

---

## 2. How SSE Works (The Flow)

```
Client (Browser)                         Server (Flask)
     |                                        |
     |--- GET /stream  ---------------------->|  (EventSource opens connection)
     |                                        |
     |<-- text/event-stream (kept open) ------|  (Server keeps connection alive)
     |                                        |
     |<-- data: {"message": "Hello"} --------|  (Server pushes event)
     |                                        |
     |<-- data: {"message": "Update!"} ------|  (Another push whenever needed)
     |                                        |
     |  (connection stays open...)            |
```

Step by step:
1. Client creates `new EventSource("/stream")` — this opens a GET request
2. Server responds with `Content-Type: text/event-stream` and keeps the connection open
3. Whenever the server has new data, it writes to this open connection
4. Client receives the data through event listeners
5. If the connection drops, the browser **automatically reconnects** after a few seconds

---

## 3. SSE Event Stream Format

The server sends data in a specific text format. Each message is separated by **two newlines** (`\n\n`).

**Fields available:**

| Field   | Purpose                                    |
|---------|--------------------------------------------|
| `data:` | The actual data payload                    |
| `event:`| Custom event name (like "notify", "update")|
| `id:`   | Unique ID for the event (for reconnection) |
| `retry:`| Reconnection time in milliseconds          |

**Example of raw SSE stream:**

```
event: notify
data: {"message": "Hello World"}

event: notify
data: {"message": "Another notification"}

data: This is a message without a custom event name

```

- If no `event:` field → received as a generic `message` event
- If `event: notify` is set → must use `addEventListener('notify', ...)` on client

---

## 4. Flask-SSE with Blueprint

Before using Blueprint with SSE, first understand Blueprint in normal Flask apps.

### What is a Blueprint?

A Blueprint in Flask is a way to organize your application into reusable components. Think of it as a "mini-app" that can be plugged into your main app.

### How Blueprint Works in Normal Flask Apps (Not Only SSE)

Blueprint is a Flask feature for organizing routes into modules.

Without Blueprint, all routes usually stay in one big app file.
With Blueprint, we split routes by feature, and then attach them to the main app.

Typical pattern:
1. Create a blueprint in a feature file (for example auth, blog, admin).
2. Add routes to that blueprint (login route, signup route, dashboard route, etc.).
3. Register that blueprint in main app using app.register_blueprint(...).
4. Flask adds those routes into the app under the given prefix.

Simple mental model:
- Main app = central router
- Blueprint = feature route group
- register_blueprint = plug that route group into main app

### Code Example (Normal Blueprint)

**auth.py**
```python
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return 'Login Page'
```

**app.py**
```python
from flask import Flask
from auth import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/auth')
```

### URL at the End (How It Looks)

- Route written inside blueprint: `/login`
- Prefix used while registering: `/auth`
- Final URL in browser: `/auth/login`

Formula:

`final_url = url_prefix + route_inside_blueprint`

If you do not use Blueprint, you usually write directly in app:

```python
@app.route('/login')
def login():
    return 'Login Page'
```

Then final URL is simply: `/login`

Example structure (concept only):
- auth blueprint handles routes like /auth/login, /auth/logout
- blog blueprint handles routes like /blog/create, /blog/list
- admin blueprint handles routes like /admin/users, /admin/reports

Why teams use Blueprint in general:
- Better project structure as app grows
- Easier maintenance (feature-wise separation)
- Reusability across projects
- Cleaner collaboration (different people can work on different blueprints)

### Now Apply This to SSE

In this session, we use `flask-sse` library, which already provides a ready-made Blueprint named `sse` for SSE streaming.

```python
# Flask-SSE gives you a pre-built blueprint called `sse`
from flask_sse import sse

app.register_blueprint(sse, url_prefix="/stream")
```

This single line creates a `/stream` endpoint that:
- Handles the `EventSource` connection from the client
- Streams events using Redis as a message broker (Pub/Sub)
- Manages the `text/event-stream` response automatically

### Blueprint Working Here (SSE Mental Model)

Think of Flask-SSE Blueprint as a prebuilt SSE route pack.

When we do:

`app.register_blueprint(sse, url_prefix="/stream")`

Flask adds the SSE routes under `/stream`, so we do not have to manually write low-level streaming route code.

In simple SSE flow:
- Your app receives normal requests like `/` and `/send_notification`
- Flask-SSE Blueprint handles the streaming route (for example `/stream`)
- When you call `sse.publish(...)`, the message goes to Redis
- The Blueprint is subscribed to Redis and forwards that message to connected browsers

So Blueprint here helps with:
- clean structure (SSE logic stays separate)
- less boilerplate
- safer first setup for beginners

### Session's Code 

**app.py:**
```python
from flask import Flask, render_template, request, jsonify
from flask_sse import sse          # import the SSE blueprint
import redis

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379"  # Redis is REQUIRED for flask-sse

app.register_blueprint(sse, url_prefix="/stream")   # Register at /stream

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_notification', methods=['POST'])
def notify():
    data = request.json                              # Get JSON from client
    message = data.get("message", "")

    if not message:
        return jsonify(status="error", message="No message provided"), 400

    with app.app_context():
        sse.publish({"message": message}, type='notify')  # Push to all listeners
        # type='notify' means the event name is "notify"

    return jsonify(status="success", message="Notification sent")

if __name__ == "__main__":
    app.run(debug=True)
```

**templates/index.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask - Notification System</title>
    <script src="https://cdn.jsdelivr.net/npm/vue@2.7.16/dist/vue.js"></script>
</head>
<body>
    <h1>Real-Time Notification</h1>
    <div id="app">
        <div>
            <label for="message">Notification Text</label>
            <input type="text" id="message" v-model="message">
        </div>
        <div>
            <button @click="textToBackend" type="button">Send</button>
        </div>
        <h2>Notifications</h2>
        <div id="notification"></div>
    </div>
</body>
<script src="../static/script.js"></script>
</html>
```

**script.js (Client Side):**
```javascript
const app = new Vue({
    el: "#app",
    data: {
        message: ""
    },
    mounted(){
        this.loadEventSource()    // Start listening when page loads
    },
    methods: {
        loadEventSource(){
            // Open SSE connection to /stream
            const eventSource = new EventSource("/stream")

            // Listen for 'notify' events specifically
            eventSource.addEventListener('notify', function(event){
                const data = JSON.parse(event.data)       // Parse the JSON
                const container = document.getElementById('notification')
                const notification1 = document.createElement('div')
                notification1.textContent = data.message
                container.prepend(notification1)           // Add to top of list
            })
        },

        textToBackend(){
            // Send data to server via regular POST (NOT through SSE)
            fetch('/send_notification', {
                method: 'POST',
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: this.message })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status == "success"){
                    console.log(data.message)
                }
                this.message = ""
            })
        }
    }
})
```

### How to Run Session's Code

1. Start Redis in one terminal.
2. Install required packages in another terminal.
3. Run the Flask app.
4. Open the app in browser and test notifications.

```bash
# Terminal 1
redis-server

# Terminal 2
pip install flask flask-sse redis
python app.py
```

- Event names must match:
    - Server sends `type='notify'`
    - Client listens with `addEventListener('notify', ...)`
- Endpoint paths must match:
    - SSE endpoint in JS: `/stream`
    - POST endpoint in JS: `/send_notification`
- Keep Redis running while testing, otherwise SSE publish will fail.
- Test with two browser tabs to verify real-time broadcast to multiple listeners.

### Why does flask-sse need Redis?

`flask-sse` uses Redis **Pub/Sub** internally. When you call `sse.publish(...)`, it publishes the message to a Redis channel. The SSE blueprint endpoint subscribes to that channel and forwards messages to all connected clients. This is how multiple browser tabs/users all receive the same notification.

### Why is it a Blueprint?

The `flask-sse` library chose the Blueprint pattern because:
- The `/stream` endpoint needs special handling (long-lived connection, streaming response)
- It keeps the SSE logic separate and reusable
- You can mount it at any URL prefix you want (`/stream`, `/events`, `/sse`, etc.)

---

## 5. Can We Use SSE Without Blueprint?

### YES! Absolutely.

You do NOT need `flask-sse` or a Blueprint to use SSE. It is possible to build SSE directly with Flask streaming responses.

### Then why are we not starting with that approach?

For first learning sessions, we usually avoid the manual approach because it adds many moving parts at once:
- You must manage long-lived client connections yourself
- You must handle disconnects/reconnect behavior cleanly
- You must think about concurrency (multiple clients at same time)
- You may need extra production setup details early (workers, scaling, buffering)

That can hide the core SSE idea for beginners.

### Why Blueprint-first is easier to understand

Using Flask-SSE + Blueprint lets you focus on the main concept first:
- client opens EventSource
- server publishes event
- client receives update

Once this mental model is clear, then learning "SSE without Blueprint" becomes much easier because you already understand what should happen end-to-end.

### Simple learning path

1. Start with Blueprint-based SSE to understand the flow.
2. Practice event types and channels.
3. Then move to manual SSE implementation to learn internals.

So yes, SSE without Blueprint is valid and useful, but for teaching and first-time clarity, Blueprint is the smoother starting point.

---

## 6. How Client Sends Data to Server for SSE Push

**SSE is one-way (Server → Client). The client CANNOT send data through the SSE connection.**

So how does data get to the server? Through **regular HTTP requests** (POST, PUT, etc.)!

### The Pattern:

```
Client A(admin) (sends data)          Server              Client B(user) (receives SSE)
     |                           |                        |
     |--- POST /send_notification -->|                    |
     |   {message: "Hello"}      |                        |
     |                           |--- SSE push ---------->|
     |                           |   data: {"message":    |
     |                           |          "Hello"}      |
     |<-- 200 OK ---------------|                        |
```

### In Our Code:

1. (Admin)User types a message in the input box
2. Clicks "Send" button → triggers `textToBackend()` method
3. `textToBackend()` makes a **regular `fetch()` POST request** to `/send_notification`
4. The server receives the POST, then uses `sse.publish()` to push it to all SSE listeners
5. All connected browsers receive the message through their `EventSource`

```javascript
// This is a REGULAR HTTP POST — NOT related to SSE
textToBackend(){
    fetch('/send_notification', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: this.message })
    })
}
```

### Other Ways the Server Can Get Data to Push via SSE:

- **Celery task completion** — when an async task finishes, publish a notification
- **Database change** — a trigger or periodic check detects a new row
- **Scheduled job** — Celery Beat sends periodic updates
- **External API** — server polls an external API and pushes updates to clients
...etc.

---

## 7. Pub/Sub Pattern and SSE

### What is Pub/Sub?

**Pub/Sub (Publish/Subscribe)** is a messaging pattern where:
- **Publishers** send messages to a **channel/topic** (they don't know who is listening)
- **Subscribers** listen to a **channel/topic** (they don't know who is sending)
- A **message broker** (like Redis) sits in the middle and routes messages

```
Publisher ──> [Redis Channel: "notifications"] ──> Subscriber 1
                                                ──> Subscriber 2
                                                ──> Subscriber 3
```

### How Pub/Sub Relates to SSE

`flask-sse` uses **Redis Pub/Sub** internally:

1. When you call `sse.publish({"message": "Hello"}, type='notify')`:
   - Flask publishes the message to a **Redis channel**

2. The `/stream` endpoint (SSE Blueprint):
   - Subscribes to that Redis channel
   - When a message arrives on the channel, it forwards it to the client via SSE

```
POST /send_notification
        |
        v
sse.publish() ──> Redis Channel "sse" ──> /stream endpoint ──> EventSource (Browser)
                                       ──> /stream endpoint ──> EventSource (Browser)
                                       ──> /stream endpoint ──> EventSource (Browser)
```

---

## 8. SSE vs WebSockets vs Polling vs Webhooks

### Quick Comparison

| Feature         | SSE                  | WebSockets         | Polling              | Webhooks            |
|-----------------|----------------------|--------------------|----------------------|---------------------|
| Direction       | Server → Client      | Both ways          | Client → Server      | Server → Server     |
| Protocol        | HTTP                 | ws:// (upgrade)    | HTTP                 | HTTP                |
| Connection      | Long-lived           | Long-lived         | Short (repeated)     | Short (one-shot)    |
| Auto-reconnect  | Yes (built-in)       | No (manual)        | N/A                  | N/A                 |
| Browser API     | `EventSource`        | `WebSocket`        | `fetch`/`setInterval`| N/A (server-side)   |
| Complexity      | Low                  | Medium             | Very Low             | Low                 |
| Real-time       | Yes                  | Yes                | No (delayed)         | Yes                 |
| Binary data     | No (text only)       | Yes                | Yes                  | Yes                 |

---

### Polling (Short Polling)

**What:** Client repeatedly asks the server "Any updates?" at fixed intervals.

```
Client                    Server
  |--- GET /updates ------->|  (any new data?)
  |<-- 200 "no" ------------|
  |                          |  (wait 5 seconds)
  |--- GET /updates ------->|  (any new data?)
  |<-- 200 "no" ------------|
  |                          |  (wait 5 seconds)
  |--- GET /updates ------->|  (any new data?)
  |<-- 200 {"msg":"Hello"} -|  (yes! here it is)
```

```javascript
// Client-side polling
setInterval(() => {
    fetch('/api/updates')
        .then(res => res.json())
        .then(data => {
            if (data.hasUpdate) {
                console.log(data.message)
            }
        })
}, 5000)  // Every 5 seconds
```

```python
# Server-side
@app.route('/api/updates')
def check_updates():
    # Check database or cache for new data
    new_data = get_latest_notification()
    if new_data:
        return jsonify(hasUpdate=True, message=new_data)
    return jsonify(hasUpdate=False)
```

**Pros:** Simple, works everywhere, no special server setup
**Cons:** Wastes bandwidth, not truly real-time, unnecessary requests when no data

---

### Long Polling

**What:** Client sends a request, server **holds it open** until there's new data, then responds.

```
Client                    Server
  |--- GET /updates ------->|  (any new data?)
  |                          |  (holds connection... waits...)
  |                          |  (30 seconds later, new data arrives)
  |<-- 200 {"msg":"Hello"} -|
  |--- GET /updates ------->|  (immediately reconnects)
  |                          |  (holds connection again...)
```

```python
# Server-side long polling
import queue

update_queue = queue.Queue()

@app.route('/api/updates')
def long_poll():
    try:
        data = update_queue.get(timeout=30)  # Block for up to 30 seconds
        return jsonify(data)
    except queue.Empty:
        return jsonify(hasUpdate=False)
```

**Pros:** More efficient than short polling, near real-time
**Cons:** Still uses many HTTP connections, complex to implement properly

---

### WebSockets

**What:** Full-duplex (two-way) communication channel. Both client and server can send messages at any time.

```
Client                    Server
  |--- HTTP Upgrade ------->|  (Upgrade to WebSocket)
  |<-- 101 Switching -------|
  |                          |
  |<=== WebSocket Open ====>|  (Full-duplex connection)
  |                          |
  |--- "Hello server" ----->|  (Client can send)
  |<-- "Hello client" ------|  (Server can send)
  |--- "Chat message" ----->|  (Client can send anytime)
  |<-- "Notification" ------|  (Server can send anytime)
```

```javascript
// Client-side WebSocket
const ws = new WebSocket('ws://localhost:5000/ws')

ws.onopen = function() {
    ws.send("Hello from client!")     // Client sends to server
}

ws.onmessage = function(event) {
    console.log("From server:", event.data)  // Server sends to client
}

ws.onclose = function() {
    console.log("Connection closed")
    // Must manually reconnect!
}
```

```python
# Server-side (using flask-socketio or similar)
from flask_socketio import SocketIO

socketio = SocketIO(app)

@socketio.on('message')
def handle_message(data):
    print('Received:', data)
    socketio.emit('response', {'msg': 'Hello from server'})
```

**When to use WebSockets over SSE:**
- Chat applications (need two-way)
- Online gaming
- Collaborative editing (Google Docs-like)
- When client needs to send frequent messages to server

**When SSE is better than WebSockets:**
- Notifications (one-way push)
- Live feeds, dashboards
- When simplicity matters
- When auto-reconnect is important

---

### Webhooks

**What:** Server-to-server notification. When an event happens on Service A, it makes an HTTP POST to Service B's URL.

```
Service A (GitHub)              Your Server
     |                              |
     | (someone pushes code)        |
     |--- POST /webhook ----------->|  (HTTP callback)
     |    {event: "push",           |
     |     repo: "myapp"}           |
     |<-- 200 OK ------------------|
```

**Webhooks are NOT related to the browser at all.** They are server-to-server.

**Example: GitHub Webhook**

When someone pushes to your repo, GitHub POSTs to your server:

```python
@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    data = request.json
    event = request.headers.get('X-GitHub-Event')
    
    if event == 'push':
        branch = data['ref']
        pusher = data['pusher']['name']
        print(f"{pusher} pushed to {branch}")
        
        # You could push this to clients via SSE!
        sse.publish({"message": f"{pusher} pushed to {branch}"}, type='notify')
    
    return jsonify(status="ok"), 200
```

**Combining Webhooks + SSE:**
```
GitHub ──webhook POST──> Your Flask Server ──SSE push──> Browser
```

This is a powerful pattern! External services notify your server via webhooks, and you push those updates to browser clients via SSE.

**Common Webhook providers:**
- GitHub (repo events)
- Stripe (payment events)
- Razorpay (payment events)
- Slack (message events)
- Twilio (SMS events)

---

### Visual Summary

```
POLLING:      Client ──asks──> Server   (repeated, wasteful)
LONG POLL:    Client ──waits──> Server  (held open, one response)
SSE:          Client <──stream── Server (one-way, auto-reconnect)
WEBSOCKET:    Client <══════> Server    (two-way, full-duplex)
WEBHOOK:      Server A ──POST──> Server B (server-to-server callback)
```

---

## 9. JSON Data Exchange Between Frontend and Backend

When frontend and backend talk through APIs, data travels as **plain text** over HTTP. JSON (JavaScript Object Notation) is the standard format used. But both sides need to **convert** between their native data types and JSON text. This is where `JSON.stringify()`, `JSON.parse()`, `jsonify()`, and `request.json` come in.

### The Core Idea

```
Frontend (JavaScript)                    Network (HTTP)                    Backend (Flask/Python)
                                                    
 JS Object/Dict                          JSON String                       Python Dict
 {message: "Hello"}  ──stringify──>  '{"message": "Hello"}'  ──request──>  {"message": "Hello"}
                                                    
 JS Object/Dict                          JSON String                       Python Dict
 {message: "Hello"}  <──parse────  '{"message": "Hello"}'  <──jsonify──  {"message": "Hello"}
```

**Key rule:** Data on the wire (HTTP body) is always a **JSON string** (plain text). Both sides must convert to/from their native objects.

---

### What is a JSON String?

A JSON string is just **plain text** that follows JSON formatting rules.

```
'{"message": "Hello", "count": 5}'
```

This is NOT a JavaScript object or a Python dict. It is a **string** — a sequence of characters. You cannot do `.message` or `["message"]` on it directly. You must **parse** it first.

---

### Frontend Side (JavaScript)

#### `JSON.stringify()` — Object → JSON String

Converts a JavaScript object into a JSON string. Used when **sending data to the server**.

```javascript
const obj = { message: "Hello", count: 5 };
const jsonString = JSON.stringify(obj);

console.log(typeof obj);         // "object"
console.log(typeof jsonString);  // "string"
console.log(jsonString);         // '{"message":"Hello","count":5}'
```

**Where you use it:** Inside `fetch()` when sending POST/PUT requests.

```javascript
fetch('/api/data', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: "Hello" })   // Must stringify!
})
```

If you forget `JSON.stringify()` and pass the raw object, the server receives `[object Object]` as text — which is useless.

#### `JSON.parse()` — JSON String → Object

Converts a JSON string back into a JavaScript object. Used when **receiving data from the server**.

```javascript
const jsonString = '{"message":"Hello","count":5}';
const obj = JSON.parse(jsonString);

console.log(typeof jsonString);  // "string"
console.log(typeof obj);         // "object"
console.log(obj.message);        // "Hello"
```

**Where you use it:** After receiving a response, or inside SSE event listeners.

```javascript
// After fetch
fetch('/api/data')
    .then(res => res.json())       // res.json() internally does JSON.parse()
    .then(data => {
        console.log(data.message)  // Now it's a JS object, can access properties
    })

// Inside SSE listener
eventSource.addEventListener('notify', function(event) {
    const data = JSON.parse(event.data);  // event.data is a JSON string
    console.log(data.message);            // Now it's a JS object
})
```

**Note:** `res.json()` in fetch is a shortcut — it reads the response body and runs `JSON.parse()` on it automatically.

---

### Backend Side (Flask/Python)

#### `jsonify()` — Python Dict → JSON Response

Converts a Python dict into a proper HTTP response with JSON body and correct headers.

```python
from flask import jsonify

@app.route('/api/data')
def get_data():
    result = {"message": "Hello", "count": 5}   # Python dict
    return jsonify(result)                         # Converts to JSON response
```

What `jsonify()` does internally:
1. Takes the Python dict
2. Converts it to a JSON string using `json.dumps()` (Python's built-in serializer)
3. Wraps it in a Flask `Response` object
4. Sets `Content-Type: application/json` header automatically

So when the frontend receives this response, it gets:
- Body: `'{"message": "Hello", "count": 5}'` (JSON string)
- Header: `Content-Type: application/json`

#### `jsonify()` vs `json.dumps()`

```python
import json
from flask import jsonify

data = {"message": "Hello"}

# json.dumps() — just converts dict to JSON string (plain text)
json_string = json.dumps(data)       # '{"message": "Hello"}'
# type: str

# jsonify() — converts dict to a full Flask Response with JSON content type
response = jsonify(data)             # Response object
# type: flask.wrappers.Response
# Content-Type header is set to application/json
```

Use `jsonify()` when returning API responses. Use `json.dumps()` when you just need the string (e.g., inside SSE event data).

#### `request.json` — Reading JSON from Incoming Request

When the frontend sends JSON via POST, Flask can read it with `request.json`.

```python
from flask import request, jsonify

@app.route('/send_notification', methods=['POST'])
def notify():
    data = request.json                # Parses JSON body into Python dict
    message = data.get("message", "")
    return jsonify(status="success")
```

What `request.json` does internally:
1. Reads the raw request body (which is a JSON string)
2. Runs `json.loads()` on it (Python's built-in deserializer)
3. Returns a Python dict

This only works if the client sent `Content-Type: application/json` header.

---

### Complete Flow: Frontend Sends, Backend Receives, Backend Responds, Frontend Reads

```
Step 1: Frontend prepares data
         JS Object: { message: "Hello" }
                |
                | JSON.stringify()
                v
         JSON String: '{"message":"Hello"}'
                |
                | fetch() sends this as HTTP body
                v

Step 2: Backend receives data
         Raw HTTP body: '{"message":"Hello"}'  (JSON string)
                |
                | request.json (internally json.loads())
                v
         Python Dict: {"message": "Hello"}
                |
                | process, validate, save to DB, etc.
                v

Step 3: Backend sends response
         Python Dict: {"status": "success", "message": "Saved"}
                |
                | jsonify() (internally json.dumps() + Response wrapper)
                v
         HTTP Response body: '{"status":"success","message":"Saved"}'
                |
                | sent back to frontend
                v

Step 4: Frontend reads response
         Raw response body: '{"status":"success","message":"Saved"}'
                |
                | res.json() (internally JSON.parse())
                v
         JS Object: { status: "success", message: "Saved" }
         Now you can do: data.status, data.message
```

---

### SSE-Specific JSON Flow

In SSE, the server pushes data as a string inside the `data:` field of the event stream.

```python
# Server side — flask-sse
sse.publish({"message": "Hello"}, type='notify')
# Internally, flask-sse does json.dumps({"message": "Hello"})
# So the event stream looks like:
#   event: notify
#   data: {"message": "Hello"}
```

```javascript
// Client side — EventSource
eventSource.addEventListener('notify', function(event) {
    console.log(typeof event.data);        // "string"  ← It's a JSON string!
    console.log(event.data);               // '{"message":"Hello"}'

    const parsed = JSON.parse(event.data); // Parse it into JS object
    console.log(parsed.message);           // "Hello"
})
```

`event.data` is ALWAYS a string. If the server sends JSON, you MUST `JSON.parse()` it on the client.

---

### Quick Reference Table

| What | Where | Direction | Input | Output |
|------|-------|-----------|-------|--------|
| `JSON.stringify()` | JavaScript (Frontend) | Object → String | JS Object | JSON String |
| `JSON.parse()` | JavaScript (Frontend) | String → Object | JSON String | JS Object |
| `res.json()` | JavaScript (Frontend) | String → Object | Response body | JS Object (shortcut for JSON.parse) |
| `jsonify()` | Flask (Backend) | Dict → Response | Python Dict | Flask Response (JSON body + headers) |
| `json.dumps()` | Python (Backend) | Dict → String | Python Dict | JSON String (plain text) |
| `json.loads()` | Python (Backend) | String → Dict | JSON String | Python Dict |
| `request.json` | Flask (Backend) | String → Dict | Request body | Python Dict (shortcut for json.loads) |

---

### Common Mistakes

1. **Forgetting `JSON.stringify()` in fetch body**
   ```javascript
   // WRONG — sends "[object Object]" as text
   body: { message: "Hello" }

   // CORRECT
   body: JSON.stringify({ message: "Hello" })
   ```

2. **Forgetting `Content-Type` header**
   ```javascript
   // WRONG — Flask won't parse request.json without this
   fetch('/api', { method: 'POST', body: JSON.stringify(data) })

   // CORRECT
   fetch('/api', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify(data)
   })
   ```

3. **Using `event.data` without parsing in SSE**
   ```javascript
   // WRONG — event.data is a string, not an object
   console.log(event.data.message)   // undefined

   // CORRECT
   const data = JSON.parse(event.data)
   console.log(data.message)         // "Hello"
   ```

4. **Confusing `jsonify()` with `json.dumps()`**
   ```python
   # WRONG for API response — returns plain text, no JSON content-type
   return json.dumps({"status": "ok"})

   # CORRECT for API response
   return jsonify(status="ok")
   ```

---

## Quick Revision Cheat Sheet

```
SSE = Server pushes to client (one-way, HTTP, auto-reconnect)
WebSocket = Both can talk (two-way, ws://, manual reconnect)
Polling = Client keeps asking (wasteful, simple)
Long Polling = Client asks, server waits to reply (less waste)
Webhook = Server-to-server callback (HTTP POST on event)

flask-sse = Blueprint + Redis Pub/Sub (easy but needs Redis)
Pure Flask SSE = Response generator + queue (no extras needed)

Client sends data via regular POST → Server pushes via SSE
EventSource API = Browser's built-in SSE client
Content-Type: text/event-stream = What makes it SSE

Format:
    event: notify\n
    data: {"message": "hello"}\n
    \n

JSON Flow:
    Frontend sends:  JSON.stringify(obj) → JSON string → fetch body
    Backend reads:   request.json → Python dict (json.loads internally)
    Backend sends:   jsonify(dict) → JSON response (json.dumps + headers)
    Frontend reads:  res.json() → JS object (JSON.parse internally)
    SSE data:        event.data is always a string → JSON.parse(event.data)
```

---
