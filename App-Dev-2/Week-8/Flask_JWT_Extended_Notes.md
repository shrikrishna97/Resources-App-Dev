# Flask-JWT-Extended Complete Guide

## What is JWT?

**JWT (JSON Web Token)** is a compact, URL-safe way to represent claims between two parties. It's commonly used for **authentication** in web applications.

A JWT consists of three parts separated by dots (`.`):
```
header.payload.signature
```

Example:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzAxIiwiZXhwIjoxNzYyODc4NzI3fQ.abc123signature
```

---

## Why Use JWT?

| Feature | Session-Based Auth | JWT-Based Auth |
|---------|-------------------|----------------|
| Storage | Server stores session | Client stores token |
| Scalability | Harder (session sharing needed) | Easier (stateless) |
| API-friendly | No | Yes |
| Mobile-friendly | Limited | Excellent |

### What do these terms mean?

**Stateless:**  
The server does NOT remember anything about the user between requests. Each request carries all the information needed (the JWT token) to verify the user. The server doesn't need to store any session data.

```
Request 1: "Here's my token" → Server validates token → Response
Request 2: "Here's my token" → Server validates token → Response
(Server doesn't remember Request 1 when handling Request 2)
```

**API-friendly (Why Sessions are NOT):**  
Sessions rely on **cookies**, which browsers handle automatically. But APIs are used by:
- Mobile apps (Android/iOS)
- Other servers (backend-to-backend)
- JavaScript frontend (Vue, React)

These clients don't automatically handle cookies like browsers do. JWT tokens are easier - just send the token in the header!

```
Session-Based (Cookie):
Browser automatically sends cookie ✓
Mobile App needs extra work to handle cookies ✗
Other APIs need extra work ✗

JWT-Based (Header):
Browser: Add "Authorization: Bearer token" ✓
Mobile App: Add "Authorization: Bearer token" ✓  
Other APIs: Add "Authorization: Bearer token" ✓
(Same simple approach works everywhere!)
```

**Session Sharing Needed:**  
In session-based auth, the server stores user sessions in memory. Problem: If you have multiple servers (for scaling), they don't share memory!

```
┌─────────────────────────────────────────────────────────┐
│  Session-Based Problem (Multiple Servers)               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  User logs in → Server 1 (stores session in memory)    │
│                                                         │
│  Next request goes to → Server 2                        │
│  Server 2: "Who are you? I don't have your session!"   │
│                                                         │
│  Solution: Share sessions via Redis/Database (complex) │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  JWT Solution (Stateless)                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  User logs in → Gets token                              │
│                                                         │
│  Request to Server 1: "Bearer token..." → Works!       │
│  Request to Server 2: "Bearer token..." → Works!       │
│  Request to Server 3: "Bearer token..." → Works!       │
│                                                         │
│  (All servers can verify token using the same secret)  │
└─────────────────────────────────────────────────────────┘
```

---

## Installing Flask-JWT-Extended

```bash
pip install flask-jwt-extended
```

---

## Basic Configuration

```python
from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Change this in production!

jwt = JWTManager(app)
```

### Important Configuration Options

| Config Key | Description | Default |
|------------|-------------|---------|
| `JWT_SECRET_KEY` | Secret key for signing tokens | Required |
| `JWT_ACCESS_TOKEN_EXPIRES` | Token expiry time | 15 minutes |
| `JWT_TOKEN_LOCATION` | Where to look for tokens | `["headers"]` |

---

## Core Concepts

### 1. User Identity Loader (`@jwt.user_identity_loader`)

This decorator defines **what information** will be stored in the token to identify the user.

```python
@jwt.user_identity_loader
def load(user):
    return user.username  # This becomes the "identity" stored in the token
```

**Key Point:** The return value is stored in the token's `sub` (subject) claim.

---

### 2. User Lookup Loader (`@jwt.user_lookup_loader`)

This decorator defines **how to retrieve the user object** from the database using the identity stored in the token.

```python
@jwt.user_lookup_loader
def user_lookup(_jwt_header, jwt_data):
    identity = jwt_data["sub"]  # Get the identity from token
    return User.query.filter_by(username=identity).one_or_none()
```

**Key Point:** This enables the use of `current_user` in protected routes.

---

### 3. Creating Access Tokens

```python
from flask_jwt_extended import create_access_token

# Create token with user object
token = create_access_token(identity=user)

# Create token with just username
token = create_access_token(identity="user_01")
```

---

### 4. Protecting Routes (`@jwt_required()`)

```python
from flask_jwt_extended import jwt_required, current_user

@app.route('/protected')
@jwt_required()
def protected():
    return {"user": current_user.username}
```

---

### 5. Getting Identity (`get_jwt_identity()`)

```python
from flask_jwt_extended import get_jwt_identity

@app.route('/profile')
@jwt_required()
def profile():
    current_username = get_jwt_identity()  # Returns what user_identity_loader returned
    return {"username": current_username}
```

| Method | Returns |
|--------|---------|
| `current_user` | Full user object (from database) |
| `get_jwt_identity()` | Just the identity (e.g., username) |

---

## Role-Based Access Control (RBAC)

### Method 1: Store Role in Token Claims

```python
from flask_jwt_extended import create_access_token, get_jwt

# When creating token, add extra claims
token = create_access_token(
    identity=user,
    additional_claims={"role": user.role}
)

# In protected route, check the role
@app.route('/admin')
@jwt_required()
def admin_only():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return {"message": "Admin access required"}, 403
    return {"message": "Welcome, Admin!"}
```

### Method 2: Check Role from Database (via current_user)

```python
@app.route('/admin')
@jwt_required()
def admin_only():
    if current_user.role != "admin":
        return {"message": "Admin access required"}, 403
    return {"message": "Welcome, Admin!"}
```

---

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        JWT Authentication Flow                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. LOGIN REQUEST                                                │
│     Client ──────────────────────────────────► Server           │
│     POST /login                                                  │
│     {"username": "user_01", "password": "1234"}                 │
│                                                                  │
│  2. TOKEN CREATION                                               │
│     Server validates credentials                                 │
│     ↓                                                            │
│     @jwt.user_identity_loader runs                               │
│     ↓                                                            │
│     create_access_token(identity=user)                          │
│     ↓                                                            │
│     Token created with user.username as "sub"                   │
│                                                                  │
│  3. TOKEN RESPONSE                                               │
│     Server ──────────────────────────────────► Client           │
│     {"access_token": "eyJhbGciOi..."}                           │
│                                                                  │
│  4. PROTECTED REQUEST                                            │
│     Client ──────────────────────────────────► Server           │
│     GET /dashboard                                               │
│     Authorization: Bearer eyJhbGciOi...                          │
│                                                                  │
│  5. TOKEN VERIFICATION                                           │
│     @jwt_required() validates token                              │
│     ↓                                                            │
│     @jwt.user_lookup_loader runs                                 │
│     ↓                                                            │
│     current_user is now available                                │
│                                                                  │
│  6. PROTECTED RESPONSE                                           │
│     Server ──────────────────────────────────► Client           │
│     {"username": "user_01", "message": "success"}               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Complete Example with Roles

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, 
    create_access_token, 
    jwt_required, 
    current_user,
    get_jwt_identity,
    get_jwt
)
from datetime import timedelta

# ============== APP CONFIGURATION ==============
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jwt-roles.sqlite3"
app.config["JWT_SECRET_KEY"] = "super-secret-key-change-in-production"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Token valid for 1 hour

db = SQLAlchemy(app)
jwt = JWTManager(app)
app.app_context().push()


# ============== USER MODEL ==============
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default="user")  # "user" or "admin"

    def __repr__(self):
        return f"<User {self.username}>"


# ============== JWT CALLBACKS ==============

@jwt.user_identity_loader
def user_identity_callback(user):
    """
    This function is called when creating a token.
    It defines WHAT to store in the token to identify the user.
    Here, we store the username.
    """
    return user.username


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    This function is called on every protected route.
    It defines HOW to load the user from the database.
    The 'sub' claim contains the identity (username in our case).
    """
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()


# ============== ROUTES ==============

@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    POST /register
    Body: {"username": "john", "password": "secret", "role": "user"}
    """
    data = request.get_json()
    
    # Check if user already exists
    if User.query.filter_by(username=data["username"]).first():
        return jsonify(message="Username already exists"), 400
    
    new_user = User(
        username=data["username"],
        password=data["password"],  # In production, hash this!
        role=data.get("role", "user")
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(message="User registered successfully"), 201


@app.route('/login', methods=['POST'])
def login():
    """
    Login and get access token.
    POST /login
    Body: {"username": "john", "password": "secret"}
    Returns: {"access_token": "eyJ..."}
    """
    credentials = request.get_json()
    
    user = User.query.filter_by(username=credentials["username"]).one_or_none()
    
    if not user or user.password != credentials["password"]:
        return jsonify(message="Invalid username or password"), 401
    
    # Create token with additional claims (role)
    access_token = create_access_token(
        identity=user,
        additional_claims={"role": user.role}  # Store role in token
    )
    
    return jsonify(access_token=access_token)


@app.route('/dashboard')
@jwt_required()
def dashboard():
    """
    Protected route - accessible by any logged-in user.
    GET /dashboard
    Header: Authorization: Bearer <token>
    """
    return jsonify(
        message="Welcome to your dashboard!",
        user_id=current_user.id,
        username=current_user.username,
        role=current_user.role
    )


@app.route('/profile')
@jwt_required()
def profile():
    """
    Example using get_jwt_identity() vs current_user
    """
    # Method 1: Using get_jwt_identity() - returns just the identity (username)
    identity = get_jwt_identity()
    
    # Method 2: Using current_user - returns the full User object
    user = current_user
    
    return jsonify(
        identity_from_get_jwt_identity=identity,  # "john"
        username_from_current_user=user.username,  # "john"
        full_user_details={
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    )


@app.route('/admin')
@jwt_required()
def admin_panel():
    """
    Admin-only route.
    Checks role from token claims.
    """
    # Get claims from token
    claims = get_jwt()
    
    if claims.get("role") != "admin":
        return jsonify(message="Admin access required"), 403
    
    return jsonify(
        message="Welcome to Admin Panel!",
        admin_user=current_user.username
    )


@app.route('/users')
@jwt_required()
def list_users():
    """
    Admin-only route - checks role from database.
    Alternative approach using current_user.role
    """
    if current_user.role != "admin":
        return jsonify(message="Admin access required"), 403
    
    users = User.query.all()
    return jsonify(
        users=[{"id": u.id, "username": u.username, "role": u.role} for u in users]
    )


# ============== DATABASE INITIALIZATION ==============

def init_db():
    """Create tables and add sample users"""
    db.create_all()
    
    # Add sample users if database is empty
    if not User.query.first():
        admin = User(username="admin", password="admin123", role="admin")
        user1 = User(username="user_01", password="1234", role="user")
        user2 = User(username="user_02", password="5678", role="user")
        
        db.session.add_all([admin, user1, user2])
        db.session.commit()
        print("Sample users created!")


# ============== MAIN ==============

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
```

---

## Testing the API (Thunder Client / Browser)

### Using Thunder Client (VS Code Extension)

#### 1. Register a User
- **Method:** `POST`
- **URL:** `http://localhost:5000/register`
- **Body Tab:** Select `JSON`
```json
{
    "username": "john",
    "password": "secret123",
    "role": "user"
}
```

#### 2. Login
- **Method:** `POST`
- **URL:** `http://localhost:5000/login`
- **Body Tab:** Select `JSON`
```json
{
    "username": "john",
    "password": "secret123"
}
```
- **Response:** Copy the `access_token` value
```json
{"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
```

#### 3. Access Protected Route
- **Method:** `GET`
- **URL:** `http://localhost:5000/dashboard`
- **Headers Tab:** Add header:
  | Header | Value |
  |--------|-------|
  | `Authorization` | `Bearer <paste_your_token_here>` |

#### 4. Try Admin Route
- **Method:** `GET`
- **URL:** `http://localhost:5000/admin`
- **Headers Tab:** Same `Authorization: Bearer <token>` header

> **Note:** GET routes like `/dashboard` can also be tested in browser, but you cannot easily add headers. Use Thunder Client for protected routes.

### Thunder Client Screenshot Reference

```
┌────────────────────────────────────────────────────────┐
│  Thunder Client                                         │
├────────────────────────────────────────────────────────┤
│  [POST ▼]  http://localhost:5000/login      [Send]     │
├────────────────────────────────────────────────────────┤
│  Body  │  Headers  │  Auth  │  Tests                   │
├────────────────────────────────────────────────────────┤
│  ○ None  ○ Form  ● JSON  ○ XML  ○ Text                │
│  ┌──────────────────────────────────────────────────┐ │
│  │ {                                                 │ │
│  │     "username": "john",                          │ │
│  │     "password": "secret123"                      │ │
│  │ }                                                 │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘

For Protected Routes - Headers Tab:
┌────────────────────────────────────────────────────────┐
│  Header Name        │  Header Value                    │
├────────────────────────────────────────────────────────┤
│  Authorization      │  Bearer eyJhbGciOi...            │
└────────────────────────────────────────────────────────┘
```

---

## Quick Reference

| Function/Decorator | Purpose | Returns |
|-------------------|---------|---------|
| `@jwt.user_identity_loader` | Define what to store in token | Identity value |
| `@jwt.user_lookup_loader` | Define how to load user from identity | User object |
| `create_access_token(identity=user)` | Create a new JWT token | Token string |
| `@jwt_required()` | Protect a route | - |
| `current_user` | Get loaded user object | User model instance |
| `get_jwt_identity()` | Get identity from token | Identity value (e.g., username) |
| `get_jwt()` | Get all claims from token | Dict with all claims |

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Missing Authorization Header` | No token sent | Add `Authorization: Bearer <token>` header |
| `Token has expired` | Token expired | Login again to get new token |
| `Invalid token` | Wrong or tampered token | Use correct token |
| `User not found` | user_lookup_loader returned None | Check database |

---

## Summary

1. **Setup**: Configure `JWT_SECRET_KEY` and initialize `JWTManager`
2. **Identity Loader**: Decides what to store in token (e.g., username)
3. **Lookup Loader**: Loads user from database using identity
4. **Login**: Validate credentials → Create token → Return token
5. **Protected Routes**: Use `@jwt_required()` decorator
6. **Access User**: Use `current_user` (full object) or `get_jwt_identity()` (identity only)
7. **Roles**: Store in token claims or check from database

---

## Resources

- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [JWT.io - Decode and verify tokens](https://jwt.io/)
