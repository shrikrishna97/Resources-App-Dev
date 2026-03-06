# Backend Setup Guide - Flask + SQLAlchemy + JWT + RBAC

Complete backend implementation for the Vehicle Parking Application. This guide includes full code, explanations, and testing procedures.

---

## What This Guide Covers

- Flask application setup and configuration
- SQLAlchemy database models and relationships
- JWT authentication system
- RBAC (Role-Based Access Control)
- Complete API endpoints with examples
- Error handling and validation
- Testing all endpoints

---

## Backend Architecture Overview

### How It Works

```
Frontend (Vue 3 on port 5173)
    ↓
HTTP Requests with JWT token
    ↓
Flask Backend (port 5000)
    ├─ Route Handler
    ├─ JWT Verification
    ├─ RBAC Permission Check
    ├─ Database Operation
    └─ JSON Response
    ↓
SQLite Database (instance/database.db)
    ├─ Users table (username, email, password_hash, role)
    ├─ ParkingLots table (name, location, total_spots)
    ├─ ParkingSpots table (parking_lot_id, spot_number, status)
    └─ Reservations table (user_id, parking_spot_id, start_time, end_time)
```

### Key Components

#### 1. **Flask App** (app.py)
- Initializes Flask application
- Registers routes (endpoints)
- Handles HTTP requests/responses
- Integrates CORS for cross-origin requests

#### 2. **Database Models** (models.py)
- **User** - Stores user credentials and role
- **ParkingLot** - Parking areas/facilities
- **ParkingSpot** - Individual spots in a lot
- **Reservation** - User bookings with time slots

#### 3. **Configuration** (config.py)
- Database connection settings
- JWT secret key and expiration
- Debug mode and environment variables

#### 4. **Authentication** (JWT Implementation)
- Users login → receive time-limited token
- Token included in request headers
- Backend verifies token signature before processing
- Automatically denies for expired/invalid tokens

#### 5. **Authorization** (RBAC)
- Admin role - Full access to create/delete park lots/spots
- User role - Can only make reservations and view data
- Routes check user role before allowing operations

### Authentication & Authorization Flow

```
1. Registration
   User sends: {username, email, password}
   Backend: Hash password → Store in User table
   Response: user_id

2. Login
   User sends: {username, password}
   Backend: Verify password → Create JWT token
   Response: access_token (valid for 1 hour)
   Frontend: Store token in localStorage

3. Authenticated Request
     Frontend sends: GET /api/auth/profile
   With header: Authorization: Bearer <access_token>
   Backend: Verify token signature → Extract user_id → Process request

4. Permission Check (RBAC)
   If route is admin-only:
     ├─ Backend checks: user.role == 'admin'?
     ├─ YES → Allow request
     └─ NO → Return 403 Forbidden

5. Response
   Backend: Execute database operation → Send JSON response
   Frontend: Receive data and update UI
```

### API Endpoints Overview

**Authentication:**
- `POST /api/auth/register` - Create new user
- `POST /api/auth/login` - Login and get token
- `GET /api/auth/profile` - Get current user info

**Admin Routes (admin only):**
- `POST /api/parking-lots` - Create parking lot
- `DELETE /api/parking-lots/<id>` - Delete parking lot

**Public/User Routes:**
- `GET /api/parking-lots` - List all parking lots
- `GET /api/parking-lots/<id>/spots` - List spots in a lot
- `POST /api/reservations` - Create reservation
- `GET /api/reservations` - Get user's reservations

---

## Step 1: Create Backend Project Structure

If you already completed backend setup in `00_PREREQUISITES_AND_SETUP.md`, you can skip Steps 1–3 and start from **Step 4 (config.py)**.

```bash
mkdir vehicle-parking-backend
cd vehicle-parking-backend
```

Create the following folder structure:

```
vehicle-parking-backend/
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── venv/
└── instance/
    └── database.db
```

## Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Create requirements.txt

Create a `requirements.txt` file with the following dependencies:

```
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Flask-CORS
```

```bash
# Install all dependencies
pip install -r requirements.txt
```

## Step 4: Create config.py

This file contains all configuration settings for your Flask app.

```python
import os
from datetime import timedelta

# Configuration for development
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT Configuration
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

# Debug mode
DEBUG = True
```

## Step 5: Create models.py

This file contains all database models with relationships:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ==================== MODELS ====================

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'admin' or 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'


class ParkingLot(db.Model):
    """Parking lot model"""
    __tablename__ = 'parking_lots'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(80))
    total_spots = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    parking_spots = db.relationship('ParkingSpot', backref='parking_lot', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ParkingLot {self.name}>'


class ParkingSpot(db.Model):
    """Parking spot model"""
    __tablename__ = 'parking_spots'
    
    id = db.Column(db.Integer, primary_key=True)
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    spot_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='available', nullable=False)  # available, occupied, reserved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reservations = db.relationship('Reservation', backref='parking_spot', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ParkingSpot {self.parking_lot_id}-{self.spot_number}>'


class Reservation(db.Model):
    """Reservation model"""
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='active', nullable=False)  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='reservations')
    
    def __repr__(self):
        return f'<Reservation {self.id}>'
```

## Step 6: Create app.py

This is your main Flask application file with routes and JWT setup:

```python
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import config
from models import db, User, ParkingLot, ParkingSpot, Reservation
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
app.config['DEBUG'] = config.DEBUG

# Initialize extensions
db.init_app(app)
CORS(app)
jwt = JWTManager(app)

# ==================== AUTH ROUTES ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 409
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role='user'  # New users are regular users
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "message": "User registered successfully",
        "user_id": user.id
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Create JWT tokens
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }), 200


@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at.isoformat()
    }), 200

# ==================== PARKING LOT ROUTES ====================

@app.route('/api/parking-lots', methods=['GET'])
def get_parking_lots():
    """Get all parking lots"""
    lots = ParkingLot.query.all()
    
    result = []
    for lot in lots:
        # Count available spots
        available = ParkingSpot.query.filter_by(parking_lot_id=lot.id, status='available').count()
        
        result.append({
            "id": lot.id,
            "name": lot.name,
            "location": lot.location,
            "city": lot.city,
            "total_spots": lot.total_spots,
            "available_spots": available
        })
    
    return jsonify({
        "total": len(result),
        "parking_lots": result
    }), 200


@app.route('/api/parking-lots/<int:lot_id>', methods=['GET'])
def get_parking_lot(lot_id):
    """Get parking lot details"""
    lot = ParkingLot.query.get(lot_id)
    
    if not lot:
        return jsonify({"error": "Parking lot not found"}), 404
    
    # Count available spots
    available = ParkingSpot.query.filter_by(parking_lot_id=lot.id, status='available').count()
    
    return jsonify({
        "id": lot.id,
        "name": lot.name,
        "location": lot.location,
        "city": lot.city,
        "total_spots": lot.total_spots,
        "available_spots": available
    }), 200


@app.route('/api/parking-lots', methods=['POST'])
@jwt_required()
def create_parking_lot():
    """Create a new parking lot (Admin only)"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # Check if user is admin
    if not user or user.role != 'admin':
        return jsonify({"error": "Insufficient permissions"}), 403
    
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('location'):
        return jsonify({"error": "Missing required fields"}), 400
    
    lot = ParkingLot(
        name=data['name'],
        location=data['location'],
        city=data.get('city', ''),
        total_spots=data.get('total_spots', 0)
    )
    
    db.session.add(lot)
    db.session.commit()
    
    return jsonify({
        "message": "Parking lot created successfully",
        "id": lot.id
    }), 201

# ==================== PARKING SPOT ROUTES ====================

@app.route('/api/parking-lots/<int:lot_id>/spots', methods=['GET'])
def get_parking_spots(lot_id):
    """Get all parking spots in a lot"""
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"error": "Parking lot not found"}), 404
    
    spots = ParkingSpot.query.filter_by(parking_lot_id=lot_id).all()
    
    return jsonify({
        "total": len(spots),
        "parking_spots": [
            {
                "id": spot.id,
                "spot_number": spot.spot_number,
                "status": spot.status
            }
            for spot in spots
        ]
    }), 200

# ==================== RESERVATION ROUTES ====================

@app.route('/api/reservations', methods=['POST'])
@jwt_required()
def create_reservation():
    """Create a new parking reservation"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('parking_spot_id') or not data.get('vehicle_number'):
        return jsonify({"error": "Missing required fields"}), 400
    
    spot = ParkingSpot.query.get(data['parking_spot_id'])
    
    # Check if spot exists and is available
    if not spot or spot.status != 'available':
        return jsonify({"error": "Parking spot not available"}), 400
    
    # Parse dates
    try:
        start_time = datetime.fromisoformat(data['start_time'])
        end_time = datetime.fromisoformat(data['end_time'])
    except:
        return jsonify({"error": "Invalid date format"}), 400
    
    if start_time >= end_time:
        return jsonify({"error": "Start time must be before end time"}), 400
    
    # Create reservation
    reservation = Reservation(
        user_id=current_user_id,
        parking_spot_id=data['parking_spot_id'],
        vehicle_number=data['vehicle_number'],
        start_time=start_time,
        end_time=end_time,
        status='active'
    )
    
    # Update spot status to reserved
    spot.status = 'reserved'
    
    db.session.add(reservation)
    db.session.commit()
    
    return jsonify({
        "message": "Reservation created successfully",
        "reservation_id": reservation.id
    }), 201


@app.route('/api/reservations', methods=['GET'])
@jwt_required()
def get_user_reservations():
    """Get current user's reservations"""
    current_user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        "total": len(reservations),
        "reservations": [
            {
                "id": res.id,
                "parking_spot_id": res.parking_spot_id,
                "vehicle_number": res.vehicle_number,
                "start_time": res.start_time.isoformat(),
                "end_time": res.end_time.isoformat(),
                "status": res.status,
                "created_at": res.created_at.isoformat()
            }
            for res in reservations
        ]
    }), 200


@app.route('/api/reservations/<int:res_id>', methods=['PUT'])
@jwt_required()
def update_reservation(res_id):
    """Update reservation status"""
    current_user_id = get_jwt_identity()
    reservation = Reservation.query.get(res_id)
    
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404
    
    if reservation.user_id != current_user_id:
        return jsonify({"error": "You can only update your own reservations"}), 403
    
    data = request.get_json()
    
    if not data or not data.get('status'):
        return jsonify({"error": "Missing status field"}), 400
    
    if data['status'] not in ['active', 'completed', 'cancelled']:
        return jsonify({"error": "Invalid status"}), 400
    
    # If cancelling, free up the parking spot
    if data['status'] == 'cancelled' and reservation.status == 'active':
        spot = ParkingSpot.query.get(reservation.parking_spot_id)
        if spot:
            spot.status = 'available'
    
    reservation.status = data['status']
    db.session.commit()
    
    return jsonify({
        "message": "Reservation updated successfully",
        "reservation_id": reservation.id,
        "status": reservation.status
    }), 200


@app.route('/api/reservations/<int:res_id>', methods=['DELETE'])
@jwt_required()
def delete_reservation(res_id):
    """Delete a reservation"""
    current_user_id = get_jwt_identity()
    reservation = Reservation.query.get(res_id)
    
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404
    
    if reservation.user_id != current_user_id:
        return jsonify({"error": "You can only delete your own reservations"}), 403
    
    # Free up the parking spot
    spot = ParkingSpot.query.get(reservation.parking_spot_id)
    if spot:
        spot.status = 'available'
    
    db.session.delete(reservation)
    db.session.commit()
    
    return jsonify({
        "message": "Reservation deleted successfully",
        "reservation_id": res_id
    }), 200

# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
```

## Step 7: Run the Flask Application

```bash
# Make sure you're in the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Run the app
python app.py
```

The server should start at `http://localhost:5000` (port number may vary if 5000 is in use).

## Testing the API

You can test these endpoints with:
- `curl` (examples below)
- Thunder Client (VS Code extension)
- Postman (desktop/web app)

If you use Thunder Client or Postman, copy the same method, URL, headers, and JSON body from each `curl` example.

### Thunder Client Quick Tutorial (POST + GET with JWT)

Use this exact flow to understand JWT authentication:

#### A) POST Login (Get Token)
1. Open Thunder Client in VS Code.
2. Click **New Request**.
3. Set:
     - Method: `POST`
     - URL: `http://localhost:5000/api/auth/login`
4. Open **Body** → select **JSON**.
5. Paste:
```json
{
    "username": "john123",
    "password": "password123"
}
```
6. Click **Send**.
7. In response, copy `access_token`.

Expected success response (example):
```json
{
    "access_token": "<JWT_TOKEN>",
    "user": {
        "id": 1,
        "username": "john123",
        "role": "user"
    }
}
```

#### B) GET Profile (Verify Token)
1. Create another request in Thunder Client.
2. Set:
     - Method: `GET`
     - URL: `http://localhost:5000/api/auth/profile`
3. Open **Headers** and add:
     - Key: `Authorization`
     - Value: `Bearer YOUR_ACCESS_TOKEN`
4. Click **Send**.

If token is valid:
- You get `200 OK` with user profile data.

If token is missing/invalid/expired:
- You get `401 Unauthorized`.

This is exactly how `@jwt_required()` works in Flask-JWT-Extended:
- It checks the Authorization header.
- It validates token signature and expiry.
- Only valid tokens can access protected routes.

### 1. Register a User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john123",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john123",
    "password": "password123"
  }'
```

This returns an `access_token`. Use this token for authenticated requests.

### 3. Get Profile
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Get All Parking Lots
```bash
curl -X GET http://localhost:5000/api/parking-lots
```

### 5. Update Reservation Status
```bash
curl -X PUT http://localhost:5000/api/reservations/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "status": "cancelled"
  }'
```

### 6. Delete a Reservation
```bash
curl -X DELETE http://localhost:5000/api/reservations/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Key Concepts

### RBAC (Role-Based Access Control)
- **ADMIN**: Full access to create parking lots
- **USER**: Regular user, can make reservations

Implementation:
```python
# Check if user is admin
if user.role != 'admin':
    return jsonify({"error": "Insufficient permissions"}), 403
```

### JWT (JSON Web Tokens)
- Tokens are created on login
- Sent in the `Authorization: Bearer <token>` header
- Verified on protected routes using `@jwt_required()` decorator
- Tokens expire after 1 hour (configurable in config.py)

### Database Models
- **User**: Stores username, email, password, and role
- **ParkingLot**: Represents a parking area
- **ParkingSpot**: Individual parking spaces with status
- **Reservation**: User bookings with start/end times

## Troubleshooting

**Port 5000 already in use?**
```bash
# Windows
netstat -ano | findstr :5000

# macOS/Linux
lsof -i :5000
```
Kill the process using port 5000, or change the Flask port in `app.py`:

```python
app.run(debug=True, port=5001)
```

**Module not found (Python)?**
```bash
# Activate venv first
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**JWT/auth issues?**
- Ensure `Authorization` header is sent as: `Bearer <token>`
- Check token expiration (default 1 hour)
- Verify `SECRET_KEY` and `JWT_SECRET_KEY` values in `config.py`

## Next Steps

1. Verify all routes are working
2. Install the frontend dependencies (see FRONTEND_SETUP.md)
3. Create additional API endpoints as needed
4. Implement token refresh mechanism
5. Add input validation and error handling


