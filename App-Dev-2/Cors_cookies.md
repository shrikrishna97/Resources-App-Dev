---

# **CORS and Cookies with Vue.js and Flask**

---

## **1. What is CORS?**

* **CORS (Cross-Origin Resource Sharing)** is a mechanism that allows a web application running at one origin (domain) to access resources from another origin.
* By default, browsers enforce the **Same-Origin Policy**:

  * A script loaded from `http://localhost:8080` cannot make AJAX requests to `http://localhost:5000` unless the server explicitly allows it.
  * 👉 The primary purpose of CORS is to control which domains can access resources on a server.
It is not about encryption, compression, or authentication — those are handled by other mechanisms (HTTPS, gzip, sessions/JWT, etc.).
* Example:

  * Vue frontend runs at: `http://localhost:8080`
  * Flask backend runs at: `http://localhost:5000`
  * Without CORS enabled on Flask, the request will be **blocked**.


---

## **2. What are Cookies?**

* Cookies are small pieces of data stored in the client’s browser.
* They can be used for:

  * **Authentication** (storing session IDs / JWT tokens)
  * **Preferences** (dark mode, language, etc.)
  * **Tracking**
 
* Important cookie flags:

  * `HttpOnly` → prevents JavaScript access.
  * `Secure` → only sent over HTTPS.
  * `SameSite`:
    * `"Lax"` → Sent for top-level navigation (safe for dev).
    * `"Strict"` → Sent only if frontend and backend are same origin.
    * `"None"` → Always sent, requires `Secure=True`.
---

# 🍪 **Important Cookie Flags**

### 1. **HttpOnly**

* **Meaning**: If set, JavaScript (`document.cookie`) **cannot access** the cookie.
* **Why**: Protects cookies (like session IDs or tokens) from **XSS (Cross-Site Scripting)** attacks.
* **Use case**: Always set `HttpOnly=True` for sensitive cookies like authentication/session tokens.
* Example:

  ```python
  resp.set_cookie("auth_token", "abc123", httponly=True)
  ```

---

### 2. **Secure**

* **Meaning**: Cookie will only be sent over **HTTPS** connections.
* **Why**: Prevents exposure of cookies over insecure HTTP.
* **Use case**: In **production**, always set `Secure=True` for authentication cookies. In **local development**, you may temporarily use `False`.
* Example:

  ```python
  resp.set_cookie("auth_token", "abc123", secure=True)
  ```

---

### 3. **SameSite**

* **Meaning**: Controls whether the cookie can be sent with **cross-site requests** (important for CORS).

* **Options**:

  * **`Lax` (default in modern browsers)** → Cookie is sent for *same-site requests* and **top-level navigations** (like clicking a link), but **not for cross-origin AJAX/fetch calls**.
  * **`Strict`** → Cookie is **only sent** if request originates from the *same site*. Blocks all cross-site usage (very secure but restrictive).
  * **`None`** → Cookie is sent **in all cross-site requests**, **but only if `Secure=True`** (required by Chrome, Firefox, Edge).

* **Use case**:

  * If your frontend (`http://localhost:5173`) and backend (`http://localhost:5000`) are on different origins → you **must use `SameSite=None` + Secure=True**.

* Example:

  ```python
  resp.set_cookie("auth_token", "abc123", samesite="None", secure=True)
  ```

---

### 4. **Domain**

* **Meaning**: Defines which domain(s) can access the cookie.
* If not set → defaults to the domain that set the cookie.
* Example:

  ```python
  resp.set_cookie("auth_token", "abc123", domain=".example.com")
  ```

  → Will be accessible from `sub1.example.com`, `sub2.example.com`, etc.

---

### 5. **Path**

* **Meaning**: Defines the URL path for which the cookie is valid.
* Default → `/` (accessible everywhere in the site).
* Example:

  ```python
  resp.set_cookie("auth_token", "abc123", path="/admin")
  ```

  → Cookie will only be sent for requests starting with `/admin`.

---

# Example (Recommended for Auth Cookies)

```python
resp.set_cookie(
    "auth_token",
    "abc123",
    httponly=True,   # Protect from XSS
    secure=True,     # Only send over HTTPS
    samesite="None" or "Lax, # Allow cross-origin requests (needed for CORS)
    path="/",       # Available across site
)
```

---

# Debugging Tip

To **check stored cookies**:

1. Open **DevTools → Application → Storage → Cookies** in Chrome/Edge/Firefox.
2. Look for:

   * **Name/Value**
   * **Domain**
   * **Path**
   * **HttpOnly**
   * **Secure**
   * **SameSite**

---

## **3. Flask Setup (Backend with CORS + Cookies)**

### **Install dependencies**

```bash
pip install flask flask-cors
```

### **Flask app (`cors.py`)**

```python
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from datatime import datetime, timedelta

app = Flask(__name__)

# Enable CORS with credentials support
CORS(app, supports_credentials=True,
     origins=["http://127.0.0.1:5500", "http://localhost:5500"])

@app.route("/set-cookie")
def set_cookie():
    resp = make_response(jsonify({"message": "Cookie is set!"}))
    resp.set_cookie(
        "user_token",
        "abc123",
        # max_age=10 # seconds
        expires=datetime.utcnow() + timedelta(minutes=1) # deletes in 1 minute
        httponly=True,    # JS cannot read this cookie
        # secure=False,     # True in production with HTTPS
        secure=True,
        samesite=None,
        # samesite="Lax"    # Works locally for cross-site cookies
    )
    return resp

@app.route("/get-cookie")
def get_cookie():
    token = request.cookies.get("user_token")
    if token:
        return jsonify({"message": "Cookie retrieved!", "token": token})
    return jsonify({"message": "No cookie found!"}), 404

@app.route("/delete-cookie")
def delete_cookie():
    resp = make_response({"msg": "Cookie deleted"})
    resp.delete_cookie("auth_token")
    return resp


if __name__ == "__main__":
    app.run(debug=True)
```
###  Why this code?

* `CORS(... supports_credentials=True ...)` → allows cookies to be sent across origins.
* `set_cookie()` → backend sends a `Set-Cookie` header → browser stores the cookie locally.
* `get_cookie()` → backend reads cookies that the browser automatically attaches to the request.



---

## **4. Vue.js Setup (Frontend)**

### **Vue Component (`app.html`)**

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <script src="https://unpkg.com/vue@2/dist/vue.js"></script>
    <title>CORS + Cookies Demo</title>
  </head>
  <body>
    <div id="app">
      <h1>CORS + Cookies Demo</h1>
      <button @click="setCookie">Set Cookie</button>
      <button @click="getCookie">Get Cookie</button>
      Create a delete button ( task )
      <p>{{ message }}</p>
    </div>

    <script>
      new Vue({
        el: "#app",
        data: {
          message: "hi",
        },
        methods: {
          async setCookie() {
            try {
              const res = await fetch("http://127.0.0.1:5000/set-cookie", {
                method: "GET",
                credentials: "include", // include cookies
              });
              const data = await res.json();
              this.message = data.message;
            } catch {
              this.message = "Error setting cookie!";
            }
          },
          async getCookie() {
            try {
              const res = await fetch("http://127.0.0.1:5000/get-cookie", {
                credentials: "include",
              });
              const data = await res.json();
              this.message = data.message + " (Token: " + data.token + ")";
            } catch {
              this.message = "Error retrieving cookie!";
            }
          },
          async deleteCookie() {
            try {
              const res = await fetch("http://127.0.0.1:5000/delete-cookie", {
                method: "GET",
                credentials: "include",
              });
              const data = await res.json();
              this.message = data.msg;
            } catch {
              this.message = "Error deleting cookie!";
            }
          },
        },
      });
    </script>
  </body>
</html>
```

### Why this code?

* `credentials: "include"` → ensures cookies are included in cross-origin requests.
* `fetch(...).json()` → parses the JSON response from Flask.
* Buttons call `setCookie` and `getCookie` methods → triggers the API calls.

---
## **5. Where Cookies Are Stored**

* After clicking **Set Cookie**, Flask sends:

  ```
  Set-Cookie: user_token=abc123; HttpOnly; SameSite=Lax
  ```
* Browser stores this cookie under **DevTools → Application → Cookies → [http://127.0.0.1:5000](http://127.0.0.1:5000)**.
* On the next request to `http://127.0.0.1:5000/get-cookie`, the browser **automatically attaches**:

  ```
  Cookie: user_token=abc123
  ```

The frontend (Vue) does **not manually send the cookie** — the **browser handles it automatically** when `credentials: "include"` is set.

---

## **6. Frontend vs Backend Roles**

* **Frontend (Vue):**

  * Initiates requests (`fetch` with credentials).
  * Displays messages from backend.
  * Does **not** directly manage secure cookies.

* **Backend (Flask):**

  * Controls cookie creation (`resp.set_cookie`).
  * Validates cookies on requests (`request.cookies.get`).
  * Decides whether a cookie is valid and what data to send back.

---

## **7. How It Works – Flow**

1. User clicks **Set Cookie** → Vue calls Flask → Flask responds with `Set-Cookie`.
2. Browser stores `user_token` locally.
3. User clicks **Get Cookie** → Vue calls Flask with credentials → browser attaches `user_token` → Flask reads it and returns token.

---

## **8. Key Notes**

* **Development:** use `samesite="Lax"` and `secure=False`.
* **Production:** use `samesite="None"`, `secure=True` (HTTPS required).
* CORS must **explicitly allow your frontend’s origin** (not `*`) when using cookies.

---

## 🔹 Ways to Auto-Delete Cookies (Extra)

1. **Session Cookies (Default)**

   * If you don’t set `expires` or `max_age`, the cookie will **auto-delete when the browser/tab closes**.

   ```python
   resp.set_cookie("auth_token", "abc123")
   ```

   Auto-deletes when user closes the browser.

---

2. **Time-Limited Cookies (Max-Age / Expires)**

   * Set an explicit lifetime (e.g., 10 seconds).

   ```python
   resp.set_cookie(
       "auth_token",
       "abc123",
       max_age=10   # seconds
   )
   ```

   Auto-deletes after 10 seconds (browser will drop it).

   Or with `expires`:

   ```python
   from datetime import datetime, timedelta
   resp.set_cookie(
       "auth_token",
       "abc123",
       expires=datetime.utcnow() + timedelta(minutes=1)
   )
   ```

   Auto-deletes after 1 minute.

---

3. **Manual Delete (Server-Controlled)**

   * If you want the user to log out immediately, you must explicitly call `delete_cookie`.
   * Auto-delete only works **based on time or session**, not on events like "logout".

---

## 🔹 Important Notes

* **Session cookies** vanish on browser close.
* **Max-Age/Expires cookies** vanish automatically after the set duration.
* If you need "logout now" behavior → you still need to **delete\_cookie**.

---

👉 So yes, auto-deletion is possible, but only **time-based** or **session-based**.
For **instant removal**, you’ll need explicit deletion code.

