# Security Guide - JWT & RBAC

This guide explains Role-Based Access Control (RBAC) and JWT (JSON Web Tokens) - two key security concepts used in the Vehicle Parking application.

---

## JWT (JSON Web Tokens) - Understanding Token-Based Authentication

### What is JWT?

JWT is a secure way to transmit information between frontend and backend without storing user credentials in a session.

### How Traditional Sessions Work (Old Way)

```
1. User logs in
   └─ Server creates a session (stored in memory/database)
   └─ Server sends Session ID to browser

2. User makes request
   └─ Browser sends Session ID
   └─ Server looks up session in database
   └─ Server responds if valid

Problem: Server must store and look up sessions for every request
```

### How JWT Works (Modern Way)

```
1. User logs in
   ├─ Server verifies credentials
   ├─ Server creates a JWT token
   ├─ Token contains: user_id, role, expiration
   ├─ Token is SIGNED with secret key (verified, but not modified)
   └─ Token sent to client

2. User makes request
   ├─ Browser sends JWT in Authorization header
   ├─ Server verifies JWT signature
   ├─ If valid, server processes request (NO database lookup needed)
   ├─ If invalid/expired, server rejects request
   └─ Server responds

Benefit: Stateless - server doesn't store anything about the user
```

### JWT Structure

A JWT has 3 parts separated by dots (`.`):

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImlhdCI6MTcwMDAwMDAwMH0.signature

Part 1: Header (eyJhbGc...)
├─ Algorithm: HS256 (signature algorithm)
└─ Type: JWT

Part 2: Payload (eyJzdWI...)
├─ sub: 1 (subject = user_id)
├─ iat: 1700000000 (issued at)
├─ exp: 1700003600 (expiration timestamp)
└─ Other claims (custom data)

Part 3: Signature (signature)
└─ HMAC-SHA256(Header + Payload, SECRET_KEY)
└─ Proves token hasn't been tampered with
```

### JWT in Our Application

**Sample JWT Payload:**
```json
{
  "sub": 1,              // User ID
  "username": "john123",
  "role": "user",
  "iat": 1700000000,     // Issued at timestamp
  "exp": 1700003600      // Expires in 1 hour
}
```

### Implementation in Your App

**Creating a Token (in app.py):**
```python
from flask_jwt_extended import create_access_token

@app.route('/api/auth/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=data['username']).first()
    
    # Create token with user_id
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        "access_token": access_token,
        "user": { ... }
    })
```

**Protecting Routes (in app.py):**
```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()  # This decorator validates the JWT
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({ ... })
```

**Sending Token (in Vue):**
```javascript
// 1. After login, store token
const response = await axios.post('/api/auth/login', credentials)
localStorage.setItem('userToken', response.data.access_token)

// 2. Include token in requests
const config = {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('userToken')}`
  }
}
axios.get('/api/auth/profile', config)
```

### JWT Token Lifecycle

```
Timeline:
├─ 00:00 - User logs in
│         ├─ Token created with expiration set to 01:00
│         └─ Token sent to client
│
├─ 00:30 - User makes request
│         ├─ Client sends token
│         ├─ Server verifies signature and expiration
│         ├─ Expiration is OK (01:00 > 00:30)
│         └─ Request allowed ✓
│
├─ 01:00 - Token expires (auto)
│
└─ 01:15 - User tries to use expired token
          ├─ Client sends token
          ├─ Server checks expiration
          ├─ Expiration is NOT OK (01:00 < 01:15)
          └─ Request rejected with 401 ✗
          └─ User redirected to login
```

### Advantages of JWT

| Advantage | Explanation |
|-----------|-------------|
| **Stateless** | Server doesn't store token info |
| **Scalable** | Works across multiple servers |
| **Secure** | Token can't be modified without key |
| **Standards** | Works with third-party APIs |
| **Mobile-friendly** | Easy to use in mobile apps |

### Security Best Practices

```
✓ DO:
  - Store token in localStorage (or secure cookies)
  - Include in Authorization header: "Bearer <token>"
  - Verify token expiration server-side
  - Use HTTPS in production
  - Use strong SECRET_KEY
  - Set reasonable expiration (1-24 hours)

✗ DON'T:
  - Put sensitive data in token (it's just base64 encoded, not encrypted)
  - Use weak SECRET_KEY
  - Store token in URL or query parameters
  - Use HTTP in production
  - Forget to use @jwt_required() on protected routes
```

---

## RBAC (Role-Based Access Control)

### What is RBAC?

RBAC is a security approach where access to resources is restricted based on a user's assigned role.

### Why Use RBAC?

```
Without RBAC:
- Every user can do everything
- No distinction between admin and regular user
- Anyone can delete parking lots or create unauthorized spots
- Security nightmare!

With RBAC:
- Admin: Can manage everything
- User: Can only make reservations and view data
- Clear permissions structure
```

### Roles in Vehicle Parking Application

```
Admin (admin)
├─ Full system access
├─ Create parking lots
├─ Create/delete parking spots
├─ View all reservations
├─ Manage users
└─ View reports

Regular User (user)
├─ View parking lots
├─ View available spots
├─ Make reservations
├─ View own reservations
└─ Cannot create or delete parking data
```

### Implementing RBAC

**1. Store Role in User Model:**

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(20), default='user')  # 'admin' or 'user'
    
    def has_role(self, role):
        """Check if user has specific role"""
        return self.role == role
```

**2. Include Role in JWT:**

```python
@app.route('/api/auth/login')
def login():
    user = User.query.filter_by(username=username).first()
    
    # Token includes user role
    access_token = create_access_token(
        identity=user.id,
        additional_claims={'role': user.role}
    )
    
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role  # Send role to frontend
        }
    })
```

**3. Direct Role Check in Protected Routes:**

```python
# Only admin can access
@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # RBAC Check
    if not user or user.role != 'admin':
        return jsonify({"error": "Insufficient permissions"}), 403

    users = User.query.all()
    return jsonify({ ... })

# Only admin can create parking lot
@app.route('/api/parking-lots', methods=['POST'])
@jwt_required()
def create_parking_lot():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # RBAC Check
    if not user or user.role != 'admin':
        return jsonify({"error": "Insufficient permissions"}), 403
    
    # Create parking lot
    lot = ParkingLot(...)
    db.session.add(lot)
    db.session.commit()
    
    return jsonify({ ... })

# Anyone logged in can view parking lots
@app.route('/api/parking-lots', methods=['GET'])
@jwt_required()
def get_parking_lots():
    lots = ParkingLot.query.all()
    return jsonify({ ... })
```

### RBAC Access Matrix

```
                 │ Admin │ User │
──────────────────────────────────
View Lots        │   ✓   │  ✓  │
Create Lot       │   ✓   │  ✗  │
Delete Lot       │   ✓   │  ✗  │
Create Spot      │   ✓   │  ✗  │
Delete Spot      │   ✓   │  ✗  │
Make Reservation │   ✓   │  ✓  │
View Own Res.    │   ✓   │  ✓  │
Manage Users     │   ✓   │  ✗  │
View Reports     │   ✓   │  ✗  │
```

### Frontend-Side Authorization (UI Based)

You can also hide/show UI elements based on role:

```vue
<template>
  <div>
    <!-- Show to everyone -->
    <button @click="viewLots">View Lots</button>
    
    <!-- Show only to admin -->
    <button v-if="user && user.role === 'admin'" @click="createLot">
      Create Lot
    </button>
    
    <!-- Show only to admin -->
    <button v-if="user && user.role === 'admin'" @click="manageUsers">
      Manage Users
    </button>
  </div>
</template>

<script setup>
const user = JSON.parse(localStorage.getItem('user'))

// Now you can use user.role directly in the template
// Check if user exists and has admin role:
// if (user && user.role === 'admin') { ... }
</script>
```

### Important Note

**Frontend authorization is NOT secure!** Users can:
- Modify localStorage
- Edit JavaScript in devtools
- Change role in local storage

**Always validate on backend!** Server-side RBAC is mandatory.

---

## JWT + RBAC Flow Combined

### Complete Authentication & Authorization Flow

```
┌──────────────────────────────────────────────┐
│ 1. USER REGISTRATION                         │
├──────────────────────────────────────────────┤
│ Frontend: POST /api/auth/register            │
│ Backend: Create user with role='user'        │
│                                              │
│ 2. USER LOGIN                                │
├──────────────────────────────────────────────┤
│ Frontend: POST /api/auth/login               │
│ Backend: Create JWT with user_id and role    │
│ Frontend: Store token in localStorage        │
│                                              │
│ 3. PROTECTED API REQUEST                     │
├──────────────────────────────────────────────┤
│ Frontend: GET /api/parking-lots              │
│ Backend: Verify JWT → Check RBAC → Respond   │
│                                              │
│ 4. TOKEN EXPIRATION                          │
├──────────────────────────────────────────────┤
│ After 1 hour: Token invalid                  │
│ User redirected to login                     │
└──────────────────────────────────────────────┘
```

### Code Example: Admin Creates Parking Lot

```python
@app.route('/api/parking-lots', methods=['POST'])
@jwt_required()  # ← JWT Validation
def create_parking_lot():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # RBAC Check - only admin can create
  if not user or user.role != 'admin':
        return jsonify({"error": "Insufficient permissions"}), 403
    
    lot = ParkingLot(...)
    db.session.add(lot)
    db.session.commit()
    
    return jsonify({"message": "Parking lot created", "id": lot.id}), 201
```

---

## 🔍 Debugging Issues

### "Token is missing" or "Invalid token"
Check that Authorization header is sent: `Authorization: Bearer <token>`

### "Invalid signature"  
Ensure same SECRET_KEY used throughout app.py

### "Insufficient permissions" (403)
Check user role in database: `User.query.get(user_id).role`

### Token expired
Default expiration is 1 hour (configurable in config.py)

---

## Summary

| Concept | Purpose |
|---------|---------|
| **JWT** | Authenticate (prove who you are) |
| **RBAC** | Authorize (prove what you can do) |

```
Authentication = "Who are you?" → JWT signature
Authorization = "What can you do?" → RBAC role
```

---

This understanding will help you build secure applications!
