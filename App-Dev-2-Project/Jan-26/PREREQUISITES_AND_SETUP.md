# Prerequisites & Setup Guide - Vehicle Parking Application

Welcome! This guide gets you from zero to running. It covers prerequisites, technology stack, setup, and testing.

---

## What You Need & Why

### Prerequisites (Check These First)

#### 1. **Python 3.8+** (Backend) We will be using wsl in windows for backend
**Why?** We use Flask (lightweight web framework), SQLAlchemy (database ORM), and JWT (authentication).

Check if installed:
```bash
python --version   # or python3 --version
```

Not installed? Download from [python.org](https://python.org/)

#### 2. **Node.js 16+ & npm** (Frontend) We will be using powershell/cmd in windows for frontend
**Why?** We use Vue 3 (UI framework), Vite (fast bundler), and npm (package manager).

Check if installed:
```bash
node --version     # Should be v16 or higher
npm --version      # Should be v7 or higher
```

Not installed? Download from [nodejs.org](https://nodejs.org/) (choose LTS)

#### 3. **Git** (Version Control)
**Why?** Version control and managing code changes.

Check if installed:
```bash
git --version
```

Not installed? Download from [git-scm.com](https://git-scm.com/downloads)

Don't know how to do github setup ? Watch this Github Adding Collaborator Video: [Adding Github Collaborator using VSCode and WSL](https://youtu.be/fUY1MtqCoRU)


### Verify Everything is Ready

Run this command:
```bash
echo "=== Node.js ===" && node --version && npm --version
echo "=== Python ===" && python --version
echo "All prerequisites installed!"
```

---

## Technology Stack - Why We're Using What

### Backend Stack

| Technology | Purpose | Why? |
|-----------|---------|------|
| **Flask** | Web framework | Lightweight, easy to learn, great for APIs |
| **SQLAlchemy** | Database ORM | Easy to define and manage database models |
| **SQLite** | Database | Simple file-based database, perfect for learning |
| **JWT (JSON Web Tokens)** | Authentication | Secure token-based auth, stateless, scalable |
| **RBAC** | Authorization | Role-based access control (Admin vs User) |
| **CORS** | Cross-origin | Allow frontend (different port) to call backend |

**Backend Architecture:**
```
Browser (5173)
    ↓
Frontend (Vue)
    ↓ HTTP Requests
    ↓
Backend (Flask) on 5000
    ↓
SQLite Database (instance/database.db)
```

**Authentication Flow:**
```
1. User registers → Password hashed → Stored in User table
2. User logs in → Credentials verified → JWT token created
3. Token sent to frontend → Stored in localStorage
4. Requests include token in Authorization header
5. Backend verifies token signature → Request processed
```

### Frontend Stack

| Technology | Purpose | Why? |
|-----------|---------|------|
| **Vue 3** | UI Framework | Modern, reactive, easy component management |
| **Vite** | Build tool | 10x faster than webpack, instant HMR (hot reload) |
| **Vue Router 4** | Routing | Multi-page navigation within single app |
| **Axios/fetch** | HTTP Client | Easy API requests with error handling |
| **CSS** | Styling | Modern CSS features, responsive design |

**Frontend Architecture:**
```
Landing Page
    ↓
Routes:
├─ /admin → Admin Portal
│  ├─ AdminLogin (authenticate)
│  └─ Dashboard (tabs: lots, spots, users, reservations, analytics)
│
└─ /user → User Portal
   ├─ UserLogin/Register
   └─ Dashboard (tabs: my reservations, analytics)
```

**Component Structure:**
```
Views (Pages):
├─ LandingPage (portal selection)
├─ AdminView (admin portal container)
└─ UserView (user portal container)

Components:
├─ AdminLogin (authenticate)
├─ AdminDashboard, AdminLots, AdminSpots, etc.
├─ UserLogin (authenticate)
├─ UserRegister (register)
└─ UserDashboard, UserReservations, UserAnalytics
```

---

## Complete Setup (Backend + Frontend)

### Step 1: Backend Setup

**Windows:**
```bash
# Create project directory
mkdir vehicle-parking-backend
cd vehicle-parking-backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
mkdir vehicle-parking-backend
cd vehicle-parking-backend
python3 -m venv venv
source venv/bin/activate
```

**Check:** Terminal should show `(venv)` prefix

**Install Dependencies:**
```bash
# Create requirements.txt with these packages
pip install Flask Flask-SQLAlchemy Flask-JWT-Extended Flask-CORS
```

**Check:** Verify packages installed
```bash
pip list | grep -E "Flask|SQLAlchemy|JWT|CORS"
```

**Create Files:** (See BACKEND_SETUP.md for full code)
- `config.py` - Configuration settings
- `models.py` - Database models (User, ParkingLot, ParkingSpot, Reservation)
- `app.py` - Flask application with all routes

**Start Backend Server:**
```bash
python app.py
```

**Expected output:**
```
WARNING in app.py: * Running on http://localhost:5000
* Debugger is active!
```

---

### Step 2: Frontend Setup

**Create Vue 3 + Vite Project:**
```bash
npm create vite@latest vehicle-parking-frontend 
cd vehicle-parking-frontend
```

When prompted, choose:
- Framework: `Vue`
- Variant: `Official Vue Starter`
- Features: include `Router (SPA development)`

**Install Dependencies:**
```bash
npm install
npm install axios
```

**Check:** Verify packages installed
```bash
npm list vue vue-router axios
```

If `npm ls vue-router` shows `(empty)`, run `npm install` first. If it still shows empty, install router manually:
```bash
npm install vue-router@4
```

**Project Structure (Optional):**

If your scaffold already created `src/components`, `src/views`, `src/router`, and `src/assets`, skip manual folder creation.

Only create missing folders/files as needed (see FRONTEND_SETUP.md for full code).

**Frontend API URL (simple):**

Use a direct backend URL in frontend code examples:

- `http://localhost:5000/api`

**Start Frontend Server:**
```bash
npm run dev
```

**Expected output:**
```
VITE v5.x.x ready in xxx ms
➜ Local: http://localhost:5173/
```

---

## Running Both Together

Open **2 separate terminals:**

**Terminal 1 - Backend:** ( wsl in windows is prefered for backend)
```bash
cd vehicle-parking-backend
source venv/bin/activate    # macOS/Linux/wsl
# OR venv\Scripts\activate  # Windows

python app.py
# Running on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd vehicle-parking-frontend
npm run dev
# Running on http://localhost:5173
```

Open browser to `http://localhost:5173` - You should see the application!

For API testing (curl / Thunder Client / Postman), use the testing section in **BACKEND_SETUP.md** after backend APIs are implemented.

## Next Steps

1. Run both servers together
2. Test all endpoints
3. Quick pre-read: **SECURITY_GUIDE.md** (JWT + RBAC basics only)
4. Read **BACKEND_SETUP.md** for detailed backend code explanation
5. Read **FRONTEND_SETUP.md** for detailed frontend code explanation
6. Revisit **SECURITY_GUIDE.md** for full security flow and debugging

---

## Quick Reference

| What | Where | Port |
|------|-------|------|
| Backend API | http://localhost:5000 | 5000 |
| Frontend App | http://localhost:5173 | 5173 |
| Database | instance/database.db | (file) |
| API Base URL | /api | (path) |

### Database Models
- **User** - username, email, password, role (admin/user)
- **ParkingLot** - name, location, city, total_spots
- **ParkingSpot** - spot_number, status (available/occupied/reserved)
- **Reservation** - user_id, parking_spot_id, vehicle_number, start_time, end_time

### Key Features
- JWT-based authentication
- Role-based access control (Admin/User)
- Parking lot and spot management
- Reservation system
- Responsive UI

---

**Ready? Start with these files in order:**
1. This file (Prerequisites & Setup) ← You are here
2. SECURITY_GUIDE.md (Quick skim: JWT + RBAC basics)
3. BACKEND_SETUP.md (Backend implementation)
4. FRONTEND_SETUP.md (Frontend implementation)

Let's build the Vehicle Parking Application!
