# Complete Captcha App Explanation

## Folder Structure

```
Captcha/
├── app.py                      # Backend (Flask + API + Routes)
├── instance/
│   └── users.db               # SQLite database (stores users)
├── templates/
│   ├── index.html             # Login/Signup page (Flask-rendered)
│   └── dashboard.html         # Protected page (after login)
└── static/
    ├── script.js              # Handles login/signup logic
    └── captcha.html           # Captcha verification page
```

---

## Complete User Journey

### **Step 1: User Opens App**

```
Browser → http://localhost:5000/
         ↓
Flask (app.py Line 84)
@app.route("/")
def home():
    return render_template("index.html")
         ↓
Shows: index.html (Login + Signup forms)
```

**User sees:** Two forms - Login and Signup

---

### **Step 2A: User Signs Up (New User)**

```
User fills signup form → Clicks "Sign Up"
         ↓
JavaScript (script.js Line 2-14)
document.getElementById("signupForm").addEventListener("submit", async (e) => {
  // Sends POST request to /api/signup
  fetch("/api/signup", {
    method: "POST",
    body: JSON.stringify({ username, password })
  });
})
         ↓
Flask (app.py Line 25-35)
class SignupAPI(Resource):
    def post(self):
        # Check if username exists
        # Create new user in database
        # Return success/error
         ↓
Database: New user saved in users.db
         ↓
Response to Browser: {"status": "success", "message": "User registered successfully"}
```

**Result:** User account created, can now login

---

### **Step 2B: User Logs In**

```
User fills login form → Clicks "Login"
         ↓
JavaScript (script.js Line 17-37)
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  // Sends POST request to /api/login
  fetch("/api/login", {
    method: "POST",
    body: JSON.stringify({ username, password })
  });
})
         ↓
Flask (app.py Line 38-62)
class LoginAPI(Resource):
    def post(self):
        # Check username + password
        user = User.query.filter_by(username=username, password=password).first()
        
        session["user"] = username  # Create session cookie
        
        if password == "1234":  # SPECIAL CASE
            # Generate random math question
            a, b = random.randint(1, 9), random.randint(1, 9)
            session["captcha_answer"] = str(a + b)  # Store answer in session
            return {"status": "captcha_required", "question": f"{a} + {b}"}
        
        return {"status": "success", "message": "Login successful"}
```

---

### **Two Possible Login Paths:**

#### **Path A: Normal Login (password ≠ "1234")**

```
Flask returns: {"status": "success"}
         ↓
JavaScript (script.js Line 31-32)
else if (data.status === "success") {
    window.location.href = "/dashboard";  // Redirect to dashboard
}
         ↓
Browser → http://localhost:5000/dashboard
         ↓
Flask (app.py Line 89-92)
@app.route("/dashboard")
def dashboard():
    if "user" not in session:  # Check if logged in
        return render_template("index.html")  # Not logged in → back to login
    return render_template("dashboard.html", user=session["user"])
         ↓
Shows: dashboard.html with "Welcome, [username]!"
```

**Result:** User logged in successfully

---

#### **Path B: Special Login (password = "1234") → CAPTCHA Required**

```
Flask returns: {"status": "captcha_required", "question": "5 + 3"}
         ↓
JavaScript (script.js Line 28-30)
if (data.status === "captcha_required") {
    sessionStorage.setItem("captcha_question", data.question);  // Save question in browser
    window.location.href = "/static/captcha.html";  // Redirect to captcha page
}
         ↓
Browser → http://localhost:5000/static/captcha.html
         ↓
captcha.html loads
         ↓
JavaScript (captcha.html Line 23-25)
const question = sessionStorage.getItem('captcha_question');  // Get "5 + 3"
document.getElementById('captcha-question').innerText = question;  // Show it
```

**User sees:** CAPTCHA page with math question: "5 + 3"

---

### **Step 3: User Solves CAPTCHA**

```
User enters answer (e.g., "8") → Clicks "Verify"
         ↓
JavaScript (captcha.html Line 27-46)
document.getElementById('verifyCaptcha').addEventListener('click', async () => {
  const answer = document.getElementById('captcha-answer').value;  // Get "8"
  fetch('/api/captcha', {
    method: 'POST',
    body: JSON.stringify({ answer })  // Send answer to server
  });
})
         ↓
Flask (app.py Line 65-72)
class CaptchaAPI(Resource):
    def post(self):
        answer = data.get("answer")  # Get "8"
        correct = session.get("captcha_answer")  # Get correct answer from session
        
        if answer == correct:  # "8" == "8"
            return {"status": "success", "message": "CAPTCHA passed"}
        else:
            return {"status": "error", "message": "Incorrect CAPTCHA"}
         ↓
JavaScript (captcha.html Line 38-43)
if (data.status === 'success') {
    alertBox.innerText = 'CAPTCHA passed! Redirecting...';
    setTimeout(() => window.location.href = '/dashboard', 1000);  // Redirect after 1 second
}
         ↓
Browser → http://localhost:5000/dashboard
         ↓
Shows: Dashboard with "Welcome, [username]!"
```

**Result:** CAPTCHA verified, user logged in

---

### **Step 4: User Logs Out**

```
User clicks "Logout" button
         ↓
Browser → http://localhost:5000/logout
         ↓
Flask (app.py Line 95-99)
@app.route("/logout")
def logout():
    session.pop("user", None)  # Remove user from session (delete session cookie)
    return redirect("/")  # Redirect to home
         ↓
Browser → http://localhost:5000/
         ↓
Shows: index.html (Login page again)
```

**Result:** User logged out

---

## Key Concepts Used

### 1. **Flask Session (Backend)**
```python
session["user"] = username           # Store user in session cookie
session["captcha_answer"] = "8"      # Store captcha answer in session
if "user" not in session:            # Check if logged in
session.pop("user", None)            # Remove user (logout)
```

**How it works:**
- Flask creates an encrypted cookie named `session`
- Stored in browser but **JavaScript cannot read it** (HttpOnly)
- Browser automatically sends it with every request
- Flask decrypts and validates it on each request

---

### 2. **sessionStorage (Frontend)**
```javascript
sessionStorage.setItem("captcha_question", "5 + 3");  // Store question in browser
const question = sessionStorage.getItem("captcha_question");  // Get question
```

**How it works:**
- Stored in browser memory
- JavaScript CAN read and modify it
- Cleared when browser tab closes
- NOT sent to server automatically
- Used for temporary client-side data

---

### 3. **RESTful API Endpoints**
```python
/api/signup    → POST → Create new user
/api/login     → POST → Authenticate user
/api/captcha   → POST → Verify captcha answer
```

**Why use APIs?**
- Clean separation between frontend and backend
- Frontend (JavaScript) communicates with backend (Flask) via JSON
- Easy to test and maintain

---

### 4. **Protected Route**
```python
@app.route("/dashboard")
def dashboard():
    if "user" not in session:  # Not logged in
        return render_template("index.html")  # Redirect to login
    return render_template("dashboard.html", user=session["user"])
```

**Security:**
- Checks if user is logged in before showing dashboard
- If not logged in, shows login page
- Session cookie proves user is authenticated

---

## Data Flow Diagram

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       │ 1. Visit /
       ↓
┌─────────────────────┐
│  index.html         │  (Login/Signup forms)
│  + script.js        │
└──────┬──────────────┘
       │
       │ 2. Submit login (password = "1234")
       ↓
┌─────────────────────┐
│  Flask /api/login   │
│  - Check user       │
│  - Create session   │ session["user"] = "john"
│  - Generate captcha │ session["captcha_answer"] = "8"
└──────┬──────────────┘
       │
       │ 3. Return {"status": "captcha_required", "question": "5 + 3"}
       ↓
┌─────────────────────┐
│  captcha.html       │  (Shows "5 + 3")
│  sessionStorage     │ captcha_question = "5 + 3"
└──────┬──────────────┘
       │
       │ 4. User enters "8" → Click Verify
       ↓
┌─────────────────────┐
│  Flask /api/captcha │
│  - Compare answer   │  "8" == session["captcha_answer"]
└──────┬──────────────┘
       │
       │ 5. Return {"status": "success"}
       ↓
┌─────────────────────┐
│  dashboard.html     │  Welcome, {{ user }}!
└─────────────────────┘
```

---

## Why `templates/` vs `static/` Folders?

### `templates/` Folder - Server-Side Rendering

**Files here are RENDERED by Flask using Jinja2**

```python
@app.route("/")
def home():
    return render_template("index.html")  # Flask processes this

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", user=session["user"])
    # Flask injects session["user"] into the template
```

**What happens:**
1. Flask reads the HTML file
2. Processes Jinja2 syntax `{{ user }}`, `{% if %}`, etc.
3. Injects Python variables
4. Sends final HTML to browser

**Example:**
```html
<!-- dashboard.html -->
<h1>Welcome, {{ user }}!</h1>  <!-- Flask replaces {{ user }} with actual username -->
```

---

### `static/` Folder - Direct Access (No Processing)

**Files here are sent AS-IS to the browser**

```javascript
// In script.js
window.location.href = "/static/captcha.html";  // Direct access, no Flask processing
```

**What happens:**
1. Browser requests `/static/captcha.html`
2. Flask sends the file **without any processing**
3. No Jinja2, no Python variables
4. Pure HTML/CSS/JS

**Why captcha.html is in static?**
- Captcha page doesn't need Flask to inject any data
- The captcha question is stored in `sessionStorage` (frontend)
- It's a pure JavaScript page
- No server-side rendering needed
- Faster loading (no server processing)

---

## Why This Design?

1. **Security:** Password "1234" triggers extra verification (CAPTCHA)
2. **Session Management:** User stays logged in across pages using session cookies
3. **API Structure:** Clean separation between frontend (JavaScript) and backend (Flask)
4. **User Experience:** Smooth flow with redirects and alerts
5. **Protection:** Dashboard is protected - requires login to access

---

## Session vs sessionStorage

| Aspect | Flask Session | sessionStorage |
|--------|--------------|----------------|
| **Location** | Server-side (cookie in browser) | Client-side (browser memory) |
| **Created By** | Backend (Flask) | Frontend (JavaScript) |
| **Security** | High (encrypted/signed) | Low (visible to user) |
| **JS Access** | No (HttpOnly) | Yes |
| **Auto-sent to Server** | Yes | No |
| **Use Case** | User authentication | Temporary UI data |
| **Example in App** | `session["user"]` | `sessionStorage.getItem("captcha_question")` |

---

## How to Run

1. **Install dependencies:**
   ```bash
   pip install flask flask-sqlalchemy flask-restful
   ```

2. **Run the app:**
   ```bash
   python app.py
   ```

3. **Open browser:**
   ```
   http://localhost:5000/
   ```

4. **Test the flow:**
   - Sign up with any username/password
   - Login with password = "1234" to trigger CAPTCHA
   - Solve the math question
   - Access dashboard
   - Logout

---

## API Endpoints Summary

| Endpoint | Method | Purpose | Request Body | Response |
|----------|--------|---------|--------------|----------|
| `/` | GET | Show login page | - | HTML page |
| `/dashboard` | GET | Show dashboard (protected) | - | HTML page |
| `/logout` | GET | Logout user | - | Redirect to `/` |
| `/api/signup` | POST | Create new user | `{username, password}` | `{status, message}` |
| `/api/login` | POST | Authenticate user | `{username, password}` | `{status, message/question}` |
| `/api/captcha` | POST | Verify captcha | `{answer}` | `{status, message}` |

---

## Key Takeaways

1. **Flask session cookies** are secure and managed by the backend
2. **sessionStorage** is for temporary client-side data
3. **templates/** = Files rendered by Flask with Jinja2
4. **static/** = Pure HTML/CSS/JS files served as-is
5. **Protected routes** check session before allowing access
6. **RESTful APIs** enable clean frontend-backend communication
