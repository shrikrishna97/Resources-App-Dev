---
layout: default
---

# MAD-2 Recap End-Sem ( Week 7-12)

---

## 1. Vuex Store

Vuex is a **central state management** library for Vue 2. Instead of passing data between components manually, all shared state lives in one store.

### 4 Core Concepts (Revisited with Full Example)

| Concept | Role | Rule |
|---|---|---|
| `state` | Holds raw data | Never mutate directly |
| `getters` | Derived/computed values from state | Return a value, no side effects |
| `mutations` | The ONLY way to change state | Must be synchronous |
| `actions` | Async logic → commits mutations | Use for API calls |

```html
{% raw %}
<div id="app">
  <p>Count: {{ $store.state.count }}</p>
  <p>Double: {{ $store.getters.doubleCount }}</p>
  <button @click="$store.commit('INCREMENT')">+1 (mutation)</button>
  <button @click="$store.dispatch('delayedIncrement')">+1 after 1s (action)</button>
  <hr>
  <p>Users: {{ $store.state.users.join(', ') || 'None loaded' }}</p>
  <button @click="$store.dispatch('loadUsers')">Load Users (async action)</button>
</div>

<script>
const store = new Vuex.Store({
  state: {
    count: 0,
    users: []
  },

  getters: {
    // Like a computed property — auto-recalculates when state changes
    doubleCount: state => state.count * 2
  },

  mutations: {
    // Direct state change — MUST be synchronous
    INCREMENT(state) {
      state.count++;
    },
    SET_USERS(state, users) {
      state.users = users;
    }
  },

  actions: {
    // Can be async — calls commit to change state
    delayedIncrement({ commit }) {
      setTimeout(() => {
        commit('INCREMENT');
      }, 1000);
    },

    loadUsers({ commit }) {
      // Simulating an API call
      Promise.resolve(['Alice', 'Bob', 'Carol']).then(data => {
        commit('SET_USERS', data);
      });
    }
  }
});

new Vue({
  el: '#app',
  store
});
</script>
{% endraw %}
```

### Data Flow in Vuex

```
Component                  Store
─────────                  ─────
this.$store.dispatch()  →  Action  (async, can call API)
                               ↓
this.$store.commit()    →  Mutation  (sync, changes state)
                               ↓
                           State  (single source of truth)
                               ↓
this.$store.state.x     ←  Component reads updated state
this.$store.getters.x   ←  Component reads derived values
```

> **Quick rule:** Never change `state` directly from a component. Always go `dispatch → action → commit → mutation → state`.

---

## 2. JWT vs Session-Based Authentication

Both are ways to identify a logged-in user. They differ in **where the user's identity is stored**.

### Side-by-Side Comparison

| Feature | JWT (Stateless) | Session (Stateful) |
|---|---|---|
| Where identity stored | Inside the token (client) | Server-side (DB/memory) |
| Server needs to store anything? | No | Yes (session table/store) |
| How client sends it | `Authorization: Bearer <token>` header | Cookie with session ID |
| Logout | Hard (token valid until expiry) | Easy (delete session from server) |
| Scalability | Great (no shared state between servers) | Harder (all servers must share session store) |
| Token readable by client? | Yes (payload is Base64) | No (just an opaque ID) |

### JWT Flow

```
1) POST /login  →  Server checks credentials
2) Server creates JWT: { user_id: 5, role: "admin", exp: ... }
3) Client stores JWT (localStorage or httpOnly cookie)
4) Every request: Authorization: Bearer eyJ...
5) Server verifies signature — no DB lookup needed
```

```python
# Flask-JWT-Extended example (backend)
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(email=request.json['email']).first()
    if user and user.check_password(request.json['password']):
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token)
    return jsonify(msg="Bad credentials"), 401

@app.route('/profile')
@jwt_required()
def profile():
    user_id = get_jwt_identity()   # decoded from token — no DB hit
    return jsonify(user_id=user_id)
```

### Session Flow

```
1) POST /login  →  Server checks credentials
2) Server creates session record: { session_id: "abc123", user_id: 5 }
3) Server sends cookie: Set-Cookie: session=abc123
4) Browser sends cookie automatically on every request
5) Server looks up session_id in DB/Redis to get user_id
```

```python
# Flask session example (backend)
from flask import session

@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(email=request.json['email']).first()
    if user and user.check_password(request.json['password']):
        session['user_id'] = user.id   # stored server-side
        return jsonify(msg="Logged in")
    return jsonify(msg="Bad credentials"), 401

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return jsonify(msg="Not logged in"), 401
    return jsonify(user_id=session['user_id'])
```

### When to Use Which

```
JWT       → APIs, mobile apps, microservices, multiple servers
Session   → Traditional web apps, when instant logout is critical
```

> **Quick rule:** JWT lives on the client — the server cannot invalidate it early. Session lives on the server — you can kill it instantly.

---

## 3. Flask-Security: 401 Unauthorized vs 403 Forbidden

These two HTTP status codes are often confused. They come from different problems.

| Code | Name | Meaning | Real-world analogy |
|---|---|---|---|
| `401 Unauthorized` | Not authenticated | Server does not know who you are | Trying to enter a building with no ID badge |
| `403 Forbidden` | Not authorized | Server knows who you are but you lack permission | Showing your ID but you don't have clearance for that room |

### Simple Rule

```
401  →  "Who are you? Please log in first."
403  →  "I know who you are, but you can't do this."
```

```python
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# Simulated user roles
USERS = {
    1: {'name': 'Alice', 'role': 'user'},
    2: {'name': 'Bob',   'role': 'admin'}
}

@app.route('/dashboard')
@jwt_required()   # no valid token → 401 Unauthorized
def dashboard():
    return jsonify(msg="Welcome to dashboard")

@app.route('/admin')
@jwt_required()
def admin_panel():
    user_id = get_jwt_identity()
    user = USERS.get(user_id)
    if not user or user['role'] != 'admin':
        return jsonify(msg="You do not have permission"), 403  # known user, wrong role
    return jsonify(msg="Welcome, Admin")
```

### What Happens Without a Token (Flask-JWT-Extended default)

```
GET /dashboard
  No Authorization header → flask-jwt-extended raises 401 automatically
  Response: { "msg": "Missing Authorization Header" }

GET /admin
  Valid token (user Alice, role=user) → passes @jwt_required
  But role check fails → our code returns 403
  Response: { "msg": "You do not have permission" }
```

### Flask-Security Specific Behavior

Flask-Security (the `flask-security-too` library) uses these codes precisely:

```
@auth_required()   →  missing/invalid token/session → 401
@roles_required('admin')  →  logged in but wrong role → 403
```

> **Exam tip:** 401 means "go log in". 403 means "you are logged in but still blocked". The fix for 401 is authentication; the fix for 403 is authorization (changing permissions).

---

## 4. GraphQL: How It Works

GraphQL is a **query language for APIs**. Instead of multiple REST endpoints, you have one endpoint where the client asks for exactly what it needs.

### REST vs GraphQL

```
REST (multiple endpoints, fixed response shape):
  GET /users/1        →  { id, name, email, address, phone, ... }
  GET /users/1/posts  →  [ { id, title, body, ... }, ... ]

GraphQL (one endpoint, client controls shape):
  POST /graphql  with body:
  {
    user(id: 1) {
      name
      posts {
        title
      }
    }
  }
  Response:
  {
    "data": {
      "user": {
        "name": "Alice",
        "posts": [{ "title": "Hello World" }]
      }
    }
  }
```

### 3 Operation Types

| Type | Purpose | Like REST |
|---|---|---|
| `query` | Read data | GET |
| `mutation` | Create / Update / Delete | POST / PUT / DELETE |
| `subscription` | Real-time stream | WebSocket |

### How GraphQL Resolves a Query (Step by Step)

```
1) Client sends POST /graphql with a query string
2) GraphQL parser reads the query and builds an execution tree
3) For each field in the query, GraphQL calls the matching resolver function
4) Resolver fetches data (DB, API, etc.) for that field
5) Only the requested fields are returned — nothing extra
6) Response is always JSON: { "data": { ... }, "errors": [...] }
```

> **Quick rule:** One endpoint, client controls shape, resolvers fetch data field by field.

---

## 5. Git: Branch Creation and Merge

A **branch** is an independent line of development. You create one to work on a feature without touching the main code.

### Common Commands

```bash
# See all branches
git branch

# Create a new branch
git branch feature/login

# Switch to it
git checkout feature/login

# Create AND switch in one step (modern Git)
git checkout -b feature/login

# Make changes, then commit
git add .
git commit -m "Add login page"

# Go back to main and merge
git checkout main
git merge feature/login

# Delete branch after merge
git branch -d feature/login
```

### What Happens During a Merge

```
Before merge:

main:    A --- B --- C
                      \
feature:               D --- E

After: git checkout main && git merge feature/login

main:    A --- B --- C ----------- F  (merge commit)
                      \           /
feature:               D --- E --
```

### Fast-Forward vs Merge Commit

```
Fast-forward (no diverged history):
  main:    A --- B
  feature:         C --- D   ← feature is ahead of main
  After merge: main just moves pointer → A --- B --- C --- D
  No merge commit created.

Merge commit (histories diverged):
  main:    A --- B --- C
  feature:       D --- E
  After merge: creates new commit F that joins both lines
```

### Merge Conflict — What It Looks Like

```
<<<<<<< HEAD
  line from main branch
=======
  line from feature branch
>>>>>>> feature/login
```

Fix: edit the file to keep the right version, then:

```bash
git add conflicted-file.py
git commit   # completes the merge
```

> **Quick rule:** Branch → commit → checkout main → merge → delete branch. Always pull latest main before merging to reduce conflicts.

---

## 6. Server-Sent Events (SSE): Theory

SSE is a browser technology where the **server continuously pushes one-way updates** to the client over a single long-lived HTTP connection.

### SSE in One Line

```
SSE = Server -> Client streaming over HTTP (text/event-stream), one-way only.
```

### How SSE Works

```
1) Client opens EventSource connection to an SSE endpoint (e.g., /events)
2) Server keeps the HTTP response open with Content-Type: text/event-stream
3) Server sends events in chunks as new data arrives
4) Browser receives each event immediately without polling
5) If disconnected, browser auto-reconnects by default
```

### SSE Message Format

```
event: notification
id: 101
data: {"msg":"New update available"}

event: score
data: Team A 2 - 1 Team B

```

Each event ends with a blank line, and `data:` can appear multiple times for multi-line payloads.

### SSE vs WebSocket

| Feature | SSE | WebSocket |
|---|---|---|
| Direction | One-way (server -> client) | Two-way (client <-> server) |
| Protocol | Plain HTTP | HTTP upgrade to WS |
| Reconnect | Built-in auto-reconnect | Manual reconnect logic usually needed |
| Good for | Notifications, live dashboards, logs | Chats, games, collaborative apps |

> **Quick rule:** Use SSE when client only needs live updates from server. Use WebSocket when both sides need to send frequent real-time messages.

---

## 7. WebSocket: Initial Handshake

WebSocket gives a **persistent, full-duplex** connection between client and server. The connection starts as an HTTP request, then **upgrades** to WebSocket.

### Why WebSocket Instead of HTTP?

```
HTTP:    Client → Request → Server → Response → Connection closed
         (must re-open for every message)

WebSocket: Client ←→ Server (one open connection, both can send any time)
```

### The Handshake (Step by Step)

```
1) Client sends HTTP GET with upgrade headers:

   GET /chat HTTP/1.1
   Host: example.com
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
   Sec-WebSocket-Version: 13

2) Server responds with 101 Switching Protocols:

   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=

3) After 101, HTTP is done. The TCP connection stays open as WebSocket.
   Both sides can now send/receive frames directly.
```

### Key Headers Explained

| Header | Who sends it | Purpose |
|---|---|---|
| `Upgrade: websocket` | Client | Request protocol switch |
| `Connection: Upgrade` | Client | Tell server this is an upgrade request |
| `Sec-WebSocket-Key` | Client | Random Base64 nonce for handshake verification |
| `101 Switching Protocols` | Server | Handshake accepted |
| `Sec-WebSocket-Accept` | Server | Derived from client's key (proves server handled it) |

> **Quick rule:** WebSocket starts as HTTP then upgrades with a 101 response. After that, it is a raw TCP pipe — no headers, no request-response, just frames going both ways.

---

## 8. Flask Caching: `@cache.memoize()`

Caching stores the result of an expensive function call so it does not have to run again for the same inputs.

**One-line setup note:** `SimpleCache` is best for local/single-process development, while `RedisCache` is preferred for production or multi-instance deployments.

### `@cache.cached` vs `@cache.memoize`

| Decorator | Caches by | Use for |
|---|---|---|
| `@cache.cached(timeout=60)` | URL / fixed key | Views with no dynamic argument |
| `@cache.memoize(timeout=60)` | Function arguments | Functions called with different parameters |

```python
from flask import Flask, jsonify
from flask_caching import Cache

app = Flask(__name__)

# Simple in-memory cache (use Redis in production)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)

@app.route('/home')
@cache.cached(timeout=60)
def home():
    print("home() actually ran")   # only prints on first call, then cached
    return jsonify(msg="Home page data")

@cache.memoize(timeout=120)
def get_user_report(user_id, year):
    print(f"Computing report for user={user_id}, year={year}")
    # Expensive DB query / calculation here
    return {'user_id': user_id, 'year': year, 'sales': user_id * year}

@app.route('/report/<int:user_id>/<int:year>')
def report(user_id, year):
    data = get_user_report(user_id, year)  # cached per (user_id, year) combo
    return jsonify(data)

# Clear a memoized result (e.g. after data changes)
@app.route('/clear-report/<int:user_id>/<int:year>')
def clear_report(user_id, year):
    cache.delete_memoized(get_user_report, user_id, year)
    return jsonify(msg="Cache cleared")
```

### What Gets Cached and When

```
First call:  get_user_report(1, 2024)
  → print runs, result computed, stored in cache under key (1, 2024)

Second call: get_user_report(1, 2024)
  → print does NOT run, cached result returned immediately

Third call:  get_user_report(2, 2024)   ← different argument!
  → print runs again, new result stored under key (2, 2024)
```

### Caching with Redis (Production Setup)

```python
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
```

> **Quick rule:** Use `@cache.cached` for whole-page or view caching. Use `@cache.memoize` when the same function is called with different arguments and each combination needs its own cached result.

---

## 9. CORS: Frontend to Backend Access Control

**CORS** (Cross-Origin Resource Sharing) — browser blocks requests from one origin to another unless the **server explicitly allows it**.

```
Origin = protocol + domain + port
http://localhost:5173  ≠  http://localhost:5000   ← DIFFERENT (port differs)
https://myapp.com      ≠  https://api.myapp.com   ← DIFFERENT (subdomain differs)
```

### Simple vs Preflight Request

```
Simple (GET / basic POST):   Browser sends request → checks response headers
Preflight (PUT/DELETE/custom headers): Browser sends OPTIONS first → then actual request
```

### Flask-CORS Setup

```python
from flask_cors import CORS

CORS(app)   # dev only — allows ALL origins

# Production: restrict to specific origin
CORS(app, resources={r"/api/*": {
    "origins": ["http://localhost:5173"],
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization"]
}})
```

### Manual Response with CORS Header + Status Code

If not using flask-cors, you can set the header directly on any response:

```python
from flask import jsonify, make_response

@app.route('/api/data')
def get_data():
    resp = make_response(jsonify(data="Hello"), 200)   # 200 = status code
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    return resp

# Inline: return (body, status_code, headers_dict) directly — no make_response needed
@app.route('/api/hello')
def hello():
    return jsonify(msg="Hello"), 200, {'Access-Control-Allow-Origin': 'http://localhost:5173'}

# For preflight OPTIONS:
@app.route('/api/data', methods=['OPTIONS'])
def preflight():
    resp = make_response('', 204)
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return resp
```

### Key Response Headers

```
Access-Control-Allow-Origin: http://localhost:5173   ← who is allowed
Access-Control-Allow-Methods: GET, POST, PUT, DELETE ← what methods
Access-Control-Allow-Headers: Content-Type, Authorization ← what headers
```

### Common Mistakes

| Error | Cause | Fix |
|---|---|---|
| "Blocked by CORS policy" | No CORS headers on backend | Add flask-cors or set headers manually |
| Still blocked after adding CORS | `Authorization` header triggers preflight | Add `"Authorization"` to `allow_headers` |
| Works dev, fails prod | `CORS(app)` allows all in dev | Set exact origin in production config |

> **Quick rule:** CORS is enforced by the **browser**, not the server. The server just adds headers to say "this origin is allowed". Backend-to-backend calls are never blocked by CORS.

---

## 10. Cookies: Use Cases

A **cookie** is a small key-value string stored in the browser and **automatically sent** with every HTTP request to the matching domain.

### Cookie vs localStorage vs sessionStorage

| | Cookie | localStorage | sessionStorage |
|---|---|---|---|
| Sent with requests? | Yes (automatic) | No | No |
| JS accessible? | Yes (unless `HttpOnly`) | Yes | Yes |
| Expiry | Set by server | Never | Window close |
| Size limit | ~4 KB | ~5 MB | ~5 MB |
| Best for | Auth sessions, tracking | Preferences, cached data | Temp form data |

### Flow: Set → Store → Send → Read

```
Server response:  Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Lax
Browser stores it, then on every request:
Request header:   Cookie: session_id=abc123
```

### Flask: Set / Read / Delete

```python
from flask import Flask, make_response, request, jsonify
app = Flask(__name__)

@app.route('/set-cookie')
def set_cookie():
    resp = make_response(jsonify(msg="Cookie set"))
    resp.set_cookie('user_pref', 'dark_mode',
        max_age=60*60*24*7,  # 7 days
        httponly=True,       # JS cannot read → blocks XSS theft
        secure=True,         # HTTPS only
        samesite='Lax'       # CSRF protection
    )
    return resp

@app.route('/read-cookie')
def read_cookie():
    return jsonify(preference=request.cookies.get('user_pref', 'light_mode'))

@app.route('/delete-cookie')
def delete_cookie():
    resp = make_response(jsonify(msg="Deleted"))
    resp.delete_cookie('user_pref')
    return resp
```

### Key Cookie Flags

| Flag | Effect | Why |
|---|---|---|
| `HttpOnly` | JS cannot read it | Blocks XSS token theft |
| `Secure` | HTTPS only | Prevents interception |
| `SameSite=Strict` | Never sent cross-site | Strong CSRF protection |
| `SameSite=Lax` | Top-level nav only | Good default |
| `SameSite=None` | Always cross-site | Embedded content (needs `Secure`) |
| `Max-Age` / `Expires` | When it dies | No value = session cookie |
| `Domain` | Who gets it | `.example.com` = all subdomains |

### Vue2 — Read/Write a Cookie from JS

```javascript
// Read
getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? match[2] : null;
},
// Write (only works if NOT HttpOnly)
setTheme(value) {
  document.cookie = `theme=${value}; max-age=${60*60*24*365}; path=/`;
}
```

### Cookie Size → Performance Impact

Cookies are sent on **every** request — including images, CSS, JS files.

```
10 cookies × 400 B = 4 KB added to every single request
Page with 50 resources → 200 KB of wasted cookie data
```

| Issue | Fix |
|---|---|
| Cookie bloats all requests | Keep cookies small; use `localStorage` for large data |
| Static assets also carry cookies | Serve images/CSS/JS from a cookie-free CDN domain |
| Limits: ~4 KB/cookie, ~50 cookies/domain | Stay well under budget |

### Cookie Domain and Subdomains

```
Domain=.y.com  → sent to  y.com ✓  x.y.com ✓  a.b.y.com ✓
Domain=x.y.com → sent to  x.y.com ✓  y.com ✗  z.y.com ✗
```

```python
resp.set_cookie('auth_token', 'abc123',
    domain='.y.com',   # leading dot = all subdomains share this cookie
    httponly=True, secure=True, samesite='Lax')
```

> **Security note:** `Domain=.y.com` means every subdomain (including a compromised one) gets your cookie. Use exact domain for sensitive auth tokens.

> **Quick rules:**
> - `HttpOnly` → security-sensitive tokens (JS cannot steal them)
> - `localStorage` → large non-sensitive data (not sent with requests)
> - `Domain=.y.com` → cookie shared across `y.com` + all subdomains
> - Keep total cookie size small — it's added to every request

---

## Quick Revision Table

| Topic | One-line Remember |
|---|---|
| Vuex | state → getters → mutations (sync) → actions (async) |
| JWT | Token on client, server verifies signature, no DB lookup |
| Session auth | Session ID on client, identity stored on server |
| 401 | Not authenticated — go log in |
| 403 | Authenticated but not authorized — wrong role/permission |
| GraphQL | One endpoint, client defines shape, resolvers fetch each field |
| Git branch | `checkout -b` → commit → back to main → `merge` |
| SSE | One-way server push over HTTP (`text/event-stream`) |
| WebSocket | HTTP GET upgrades to WS on `101 Switching Protocols` |
| `@cache.memoize` | Caches by function arguments, not just URL |
| CORS | Server must send `Access-Control-Allow-Origin` header |
| Cookies | Auto-sent with requests; use `HttpOnly` for token security |
