# Documentation Index - Vehicle Parking Application

Welcome to Day 1 Session Setup! This file guides you to the right documentation for your needs.

---

## Quick Navigation

### I Want to Get Started Immediately
**Read:** [00_PREREQUISITES_AND_SETUP.md](00_PREREQUISITES_AND_SETUP.md) (20-30 min)
- Prerequisites checking
- Why we use each technology
- Step-by-step backend setup
- Step-by-step frontend setup
- Running both servers
- Link to backend API testing section
- Troubleshooting pointers to backend/frontend guides

**Result:** You'll have the application running locally on http://localhost:5173 (frontend) and http://localhost:5000 (backend)

---

## Complete Documentation (Read in This Order)

### 1. **START: Prerequisites & Setup** 
📄 [00_PREREQUISITES_AND_SETUP.md](00_PREREQUISITES_AND_SETUP.md) (20-30 min read)

**What's covered:**
- Do you have Python 3.8+ and Node.js 16+ installed?
- Quick overview of technology choices and why they matter
- Complete copy-paste instructions for backend setup
- Complete copy-paste instructions for frontend setup
- How to run both servers simultaneously
- Where to test APIs after backend implementation
- Troubleshooting pointers

**Start here unless you already have the app running.**

---

### 2. **Backend Deep Dive**
📄 [BACKEND_SETUP.md](BACKEND_SETUP.md) (45-60 min read)

**What's covered:**
- Backend Architecture Overview (component flow, auth/authz design)
- Complete Flask application code
- Database models: User, ParkingLot, ParkingSpot, Reservation
- Configuration setup (Flask, JWT, CORS, SQLAlchemy)
- Authentication routes: /api/auth/register, /api/auth/login, /api/auth/profile
- Admin routes: /api/parking-lots (POST), role-based access checks
- User/Public routes: /api/parking-lots (GET), /api/parking-lots/<id>/spots (GET)
- Reservation routes: Create, Read, Update, Delete with role-based access
- JWT verification and token lifecycle
- RBAC implementation (Admin vs User role checks)
- Error handling patterns
- Testing with curl examples

**Read this if:**
- You're building or understanding the backend
- You need to know how authentication works
- You want to add or modify API endpoints
- You're debugging backend issues

---

### 3. **Frontend Deep Dive**
📄 [FRONTEND_SETUP.md](FRONTEND_SETUP.md) (45-60 min read)

**What's covered:**
- Frontend Architecture Overview (routing, component hierarchy, portals)
- Two portal system: Admin and User (separate login flows)
- Component organization (views, components, router structure)
- Component-by-component explanation:
  - LandingPage (portal selection)
  - AdminView & AdminLogin (admin portal with tabs)
  - UserView, UserLogin, UserRegister (user portal)
  - Dashboard, Lots, Spots, Reservations components
- Vue Router configuration
- Axios API request patterns
- localStorage token management
- Styling and responsive design
- Environment variables setup
- HMR (hot module replacement) during development

**Read this if:**
- You're building or understanding the frontend
- You need to know how components interact
- You want to add new features or modify existing components  
- You're debugging frontend issues

---

### 4. **Security Reference**
📄 [SECURITY_GUIDE.md](SECURITY_GUIDE.md) (30-45 min read)

**What's covered:**
- JWT (JSON Web Tokens) explained step-by-step
- JWT structure and anatomy
- Token lifecycle (creation → validation → expiration)
- RBAC (Role-Based Access Control) explained
- Admin vs User roles and permissions
- Role-based decorators in Flask
- RBAC access matrix (who can access what)
- Frontend authorization patterns (UI based on role)
- Combined JWT + RBAC flow diagrams
- Debugging authentication/authorization issues
- Common security mistakes to avoid

**Read this if:**
- You want to understand JWT and RBAC concepts
- You're implementing new role-based features
- You're debugging authentication/authorization issues
- You want to know how tokens work "under the hood"

---

## Reading Paths by Role

### I'm Not Sure Where to Start
1. [00_PREREQUISITES_AND_SETUP.md](00_PREREQUISITES_AND_SETUP.md) ← **Start here**
2. [SECURITY_GUIDE.md](SECURITY_GUIDE.md) (optional, read if interested in auth)

### I'm Building the Backend
1. [00_PREREQUISITES_AND_SETUP.md](00_PREREQUISITES_AND_SETUP.md) (setup)
2. [BACKEND_SETUP.md](BACKEND_SETUP.md) ← **Focus here**
3. [SECURITY_GUIDE.md](SECURITY_GUIDE.md) (understand JWT/RBAC)

### I'm Building the Frontend
1. [00_PREREQUISITES_AND_SETUP.md](00_PREREQUISITES_AND_SETUP.md) (setup)
2. [FRONTEND_SETUP.md](FRONTEND_SETUP.md) ← **Focus here**
3. [SECURITY_GUIDE.md](SECURITY_GUIDE.md) (understand token management)

### I'm Building Both (Full Stack)
1. [00_PREREQUISITES_AND_SETUP.md](00_PREREQUISITES_AND_SETUP.md) (setup)
2. [BACKEND_SETUP.md](BACKEND_SETUP.md) (backend code)
3. [FRONTEND_SETUP.md](FRONTEND_SETUP.md) (frontend code)
4. [SECURITY_GUIDE.md](SECURITY_GUIDE.md) (how they communicate securely)

### I Just Need Quick Troubleshooting
- [00_PREREQUISITES_AND_SETUP.md](00_PREREQUISITES_AND_SETUP.md) → Go to "Troubleshooting" section
- [BACKEND_SETUP.md](BACKEND_SETUP.md) → Use "Troubleshooting" + API testing sections
- [FRONTEND_SETUP.md](FRONTEND_SETUP.md) → Use "Troubleshooting" section
- [SECURITY_GUIDE.md](SECURITY_GUIDE.md) → Read "Debugging Authentication" section

---

## File Overview

| File | Purpose | Duration | When to Read |
|------|---------|----------|--------------|
| 00_PREREQUISITES_AND_SETUP.md | Entry point with full setup | 20-30 min | First thing |
| BACKEND_SETUP.md | Flask implementation | 45-60 min | Building backend |
| FRONTEND_SETUP.md | Vue 3 implementation | 45-60 min | Building frontend |
| SECURITY_GUIDE.md | Auth concepts reference | 30-45 min | Understanding JWT/RBAC |

---

## How Do I Know When I'm Ready?

After reading [00_PREREQUISITES_AND_SETUP.md](00_PREREQUISITES_AND_SETUP.md), you should be able to:

- [ ] Run `python --version` and `node --version` successfully
- [ ] Start the backend server with `python app.py` (runs on 5000)
- [ ] Start the frontend server with `npm run dev` (runs on 5173)
- [ ] Open http://localhost:5173 and see the landing page
- [ ] Create a test user account (register)
- [ ] Log in as that user
- [ ] See the user dashboard

If all checkboxes are done, you're ready to build!

---

## Pro Tips

1. **Keep both servers running** - One terminal for backend, one for frontend
2. **Check ports 5000 and 5173** - Must be available (not already in use)
3. **Save tokens locally** - Don't reload the page, tokens are in localStorage
4. **Use the curl examples** - In BACKEND_SETUP.md to test API directly
5. **Hot module reload** - Vite reloads frontend automatically when you save (you'll see changes instantly)
6. **Check browser console** - Press F12, go to Console tab to see debugging info

---

## Need Help?

1. **Setup failing?** → Check [00_PREREQUISITES_AND_SETUP.md](00_PREREQUISITES_AND_SETUP.md) "Troubleshooting"
2. **API returning errors?** → Check [BACKEND_SETUP.md](BACKEND_SETUP.md) error handling and curl examples
3. **Frontend not working?** → Check [FRONTEND_SETUP.md](FRONTEND_SETUP.md) component explanations
4. **Authentication issues?** → Check [SECURITY_GUIDE.md](SECURITY_GUIDE.md) debugging section

---

## Reading Duration Estimate

- **Total first-time**: ~2-3 hours (prerequisites + setup + testing)
- **Just setup**: 20-30 minutes
- **Backend focus**: 50-75 minutes
- **Frontend focus**: 50-75 minutes
- **Full stack**: 2-3 hours
- **Reference lookup**: 5-15 minutes

**Don't read everything at once** - Start with [00_PREREQUISITES_AND_SETUP.md](00_PREREQUISITES_AND_SETUP.md), get it running, then read the deep dives as needed.

---

## Learning Outcomes

After completing this Day 1 setup, you'll understand:

- How Flask backends handle authentication and authorization  
- How Vue frontends communicate with backends via API  
- How JWT tokens work and why they're secure  
- How role-based access control (RBAC) restricts what users can do  
- How to structure a full-stack application  
- How to debug common authentication issues  

---

**Ready to start?** → [Go to 00_PREREQUISITES_AND_SETUP.md](00_PREREQUISITES_AND_SETUP.md)
