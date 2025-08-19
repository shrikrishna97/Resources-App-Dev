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
  * `SameSite` → controls cross-site sending (`Lax`, `Strict`, `None`).

---

## **3. Flask Setup (Backend with CORS + Cookies)**

### **Install dependencies**

```bash
pip install flask flask-cors
```

### **Flask app (`app.py`)**

```python
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS with support for cookies
CORS(app, supports_credentials=True, origins=["http://localhost:8080"])

@app.route("/set-cookie")
def set_cookie():
    resp = make_response(jsonify({"message": "Cookie is set!"}))
    resp.set_cookie(
        "user_token", 
        "abc123", 
        httponly=True, 
        secure=False,      # Use True in production (with HTTPS)
        samesite="None"    # Required for cross-site cookies
    )
    return resp

@app.route("/get-cookie")
def get_cookie():
    token = request.cookies.get("user_token")
    if token:
        return jsonify({"message": "Cookie retrieved!", "token": token})
    return jsonify({"message": "No cookie found!"}), 404

if __name__ == "__main__":
    app.run(port=5000, debug=True)
```

---

## **4. Vue.js Setup (Frontend)**

### **Install Axios**

```bash
npm install axios
```

### **Vue Component (`App.vue`)**

```vue
<template>
  <div class="p-6">
    <h1 class="text-xl font-bold">CORS + Cookies Demo</h1>
    <button @click="setCookie" class="m-2 p-2 bg-blue-500 text-white rounded">
      Set Cookie
    </button>
    <button @click="getCookie" class="m-2 p-2 bg-green-500 text-white rounded">
      Get Cookie
    </button>
    <p>{{ message }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      message: ""
    };
  },
  methods: {
    async setCookie() {
      try {
        const res = await axios.get("http://localhost:5000/set-cookie", {
          withCredentials: true // Important for cookies
        });
        this.message = res.data.message;
      } catch (err) {
        this.message = "Error setting cookie!";
      }
    },
    async getCookie() {
      try {
        const res = await axios.get("http://localhost:5000/get-cookie", {
          withCredentials: true
        });
        this.message = res.data.message + " (Token: " + res.data.token + ")";
      } catch (err) {
        this.message = "Error retrieving cookie!";
      }
    }
  }
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
}
</style>
```

---

## **5. How It Works**

1. **User clicks “Set Cookie”** → Vue sends a request to Flask → Flask sets a `user_token` cookie.
2. **User clicks “Get Cookie”** → Vue sends request with credentials → Flask retrieves cookie and returns token.
3. CORS is enabled in Flask with `supports_credentials=True`, so cookies can cross origins.

---

## **6. Key Notes**

* Without `withCredentials: true`, cookies won’t be sent from Vue.
* Flask must have `supports_credentials=True` and specify allowed `origins`.
* In production:

  * Use **HTTPS** with `Secure=True`.
  * Avoid `samesite="None"` unless necessary.
  * Use `HttpOnly=True` for sensitive cookies (prevents XSS attacks).

---
