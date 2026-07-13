
# Week 5: Fetch API and Data Communication Between Vue.js and Flask API

## 1. Introduction to Fetch API

Modern web applications usually have two separate parts:

1. **Frontend (Client Side)**

   * Responsible for displaying UI and user interaction.
   * Example: Vue.js application running in the browser.

2. **Backend (Server Side)**

   * Responsible for business logic, database operations, authentication, etc.
   * Example: Flask API.

The frontend and backend communicate using **HTTP requests**.

Example:

```
Vue.js Frontend
        |
        | HTTP Request (GET /api/notes)
        |
        ↓
Flask Backend API
        |
        | Fetch data from database
        |
        ↓
JSON Response
        |
        ↓
Vue.js displays notes
```

---

# 2. What is Fetch API?

The **Fetch API** is a JavaScript feature used to make HTTP requests from the browser.

It allows frontend applications to:

* Fetch data from backend APIs.
* Send data to backend APIs.
* Update existing data.
* Delete data.

The basic syntax:

```javascript
fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });
```

### Explanation

`fetch()` sends a request to the given URL.

Example:

```javascript
fetch("http://localhost:5000/api/notes")
```

The server sends a response.

The response is converted into JSON:

```javascript
response.json()
```

Finally, we process the received data:

```javascript
.then(data => {
    console.log(data);
});
```

---

# 3. HTTP Methods Used with Fetch API

| Method | Purpose              | Example        |
| ------ | -------------------- | -------------- |
| GET    | Retrieve data        | Get all notes  |
| POST   | Create new data      | Add a new note |
| PUT    | Update existing data | Edit a note    |
| DELETE | Remove data          | Delete a note  |

Example:

```
GET     /api/notes
POST    /api/notes
PUT     /api/notes/1
DELETE  /api/notes/1
```

---

# 4. Why do we need Fetch API in Vue?

Vue manages the frontend UI.

However, Vue does not directly access the database.

The flow is:

```
Database
    ↑
    |
Flask API
    ↑
    |
Fetch API
    ↑
    |
Vue Component
```

Vue uses Fetch API to communicate with Flask.

Example:

```javascript
fetch("/api/notes")
```

Vue receives the response:

```json
[
    {
        "id":1,
        "title":"Learn Vue",
        "content":"Study Fetch API"
    }
]
```

Then Vue displays this data dynamically.

---

# 5. Creating Flask Backend API

## Project Structure

```
MAD2_Fetch_Demo
|
|-- app.py
|
|-- templates
    |
    |-- index.html
```

---

## Flask API Code

### app.py

```python
from flask import Flask, jsonify, request

app = Flask(__name__)


notes = [
    {
        "id": 1,
        "title": "Learn Flask",
        "content": "Create REST APIs"
    },
    {
        "id": 2,
        "title": "Learn Vue",
        "content": "Use Vue CDN"
    }
]


@app.route("/api/notes", methods=["GET"])
def get_notes():

    return jsonify(notes)



@app.route("/api/notes", methods=["POST"])
def add_note():

    data = request.json

    new_note = {
        "id": len(notes)+1,
        "title": data["title"],
        "content": data["content"]
    }

    notes.append(new_note)

    return jsonify(new_note)



if __name__ == "__main__":
    app.run(debug=True)
```

---

## Testing API

Open browser:

```
http://localhost:5000/api/notes
```

Response:

```json
[
    {
        "id":1,
        "title":"Learn Flask",
        "content":"Create REST APIs"
    },
    {
        "id":2,
        "title":"Learn Vue",
        "content":"Use Vue CDN"
    }
]
```

---

# 6. Using Fetch API with Vue CDN

Now we create the frontend.

## index.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Notes App</title>
    <!-- Vue 2 CDN -->
    <script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
    <!-- Bootstrap CSS -->
    <link 
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
        rel="stylesheet">
</head>
<body>
    <div id="app" class="container mt-4">
        <h2>My Notes</h2>
        <div 
            v-for="note in notes" 
            class="card mt-3">
            <div class="card-body">
                <h5>
                    {{ note.title }}
                </h5>
                <p>
                    {{ note.content }}
                </p>
            </div>
        </div>
    </div>
    <script>
        new Vue({
            el: "#app",
            data: {
                notes: []
            },
            methods: {
                fetchNotes: function() {
                    fetch("/api/notes")
                    .then(response => response.json())
                    .then(data => {
                        this.notes = data;
                    });
                }
            },
            mounted: function() {
                this.fetchNotes();
            }
        });
    </script>
</body>
</html>
```

---

# 7. Understanding Vue Fetch Code

## Step 1: Creating Data Variable

```javascript
data:{
    notes:[]
}
```

Initially:

```
notes = []
```

No data is available.

---

## Step 2: Calling API

```javascript
fetch("/api/notes")
```

Browser sends:

```
GET /api/notes
```

to Flask.

---

## Step 3: Convert Response to JSON

```javascript
response.json()
```

Flask response:

```json
[
 {
  "id":1,
  "title":"Learn Flask"
 }
]
```

is converted into JavaScript object.

---

## Step 4: Store Data in Vue

```javascript
this.notes=data;
```

Now:

```javascript
notes=[
 {
  id:1,
  title:"Learn Flask"
 }
]
```

Vue automatically updates the UI.

---

# 8. Adding Data Using POST Request

Now let's add a new note.

## Vue Method

```javascript
addNote: function() {
    fetch("/api/notes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: "Fetch API",
            content: "Learning API communication"
        })
    })
    .then(response => response.json())
    .then(data => {
        this.notes.push(data);
    });
}
```

---

## Explanation

### Method

```javascript
method:"POST"
```

means:

```
Create new resource
```

---

### Headers

```javascript
"Content-Type":"application/json"
```

tells Flask:

"The request body contains JSON data."

---

### Sending Data

JavaScript object:

```javascript
{
title:"Fetch API",
content:"Learning API communication"
}
```

is converted to JSON:

```javascript
JSON.stringify()
```

because HTTP requests send data as text.

---

# 9. Complete Data Flow

When the page loads:

```
Vue mounted()
        |
        |
fetch("/api/notes")
        |
        |
Flask GET API
        |
        |
Return JSON
        |
        |
this.notes=data
        |
        |
Vue updates HTML
```

When adding a note:

```
User clicks Add
        |
        |
Vue fetch POST request
        |
        |
Flask receives JSON
        |
        |
New note created
        |
        |
Response returned
        |
        |
Vue updates notes list
```

---

# 10. Important Points for MAD-2

* Vue is responsible only for UI management.
* Flask provides APIs for data operations.
* Fetch API is the bridge between frontend and backend.
* API responses are usually exchanged in JSON format.
* Vue updates UI automatically when data variables change.
* Do not directly connect Vue with the database.
* All database operations should happen through Flask APIs.

---

# Summary

In this tutorial we learned:

1. What Fetch API is.
2. How frontend communicates with backend.
3. Creating Flask REST APIs.
4. Fetching data using Vue CDN.
5. Displaying API response dynamically.
6. Sending data using POST requests.

The same concept is used in MAD-2 projects where Vue frontend communicates with Flask APIs for features like login, search, dashboard, reports, and CRUD operations.

> **Note:** Besides the built-in **Fetch API**, developers often use third-party HTTP client libraries such as **Axios**. Axios provides a simpler syntax for many use cases, automatically parses JSON responses, and offers features like request/response interceptors, timeout handling, and centralized error handling. In this course, we will primarily use the **Fetch API** because it is built into modern browsers and helps build a strong understanding of how client-server communication works. Students interested in learning more about these libraries can refer to the official documentation:
>
> * [MDN Web Docs – Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API?utm_source=chatgpt.com)
> * [MDN – Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch?utm_source=chatgpt.com)
> * [Axios Documentation](https://axios-http.com/?utm_source=chatgpt.com)

