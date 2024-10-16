
---

### Installing Flask
To begin, install Flask using pip:
```bash
pip install Flask
```

### Flask Application Overview
The Flask app is created using the `Flask` class, which will serve as the core of your application:
```python
from flask import Flask, render_template, request

app = Flask(__name__)
```
- `app` is an instance of the `Flask` class. This instance is the application, which handles incoming web requests and serves responses.
- The `Flask` constructor takes `__name__` as an argument to determine the location of the module.

### Creating Routes
Routes in Flask define the URLs that users can access. Each route is associated with a function that determines the response for that URL.

#### Home Route
```python
@app.route('/')  # http://127.0.0.1:5000/
@app.route('/home')
def home():
    return "<h1>My first Webpage with debug mode on</h1>"
```
- `@app.route('/')` and `@app.route('/home')` define two URLs that both map to the `home()` function.
- When you navigate to `http://127.0.0.1:5000/` or `http://127.0.0.1:5000/home`, the `home()` function is triggered, returning a simple HTML message.
- This route uses the `GET` method by default, which means it simply retrieves the resource (in this case, the HTML content).

#### Custom Route with GET and POST: `/my_app`
```python
@app.route('/my_app', methods=["GET", "POST"])
def my_app():
    if request.method == "POST":
        form_data = request.form.get("course")
        return render_template("course.html", jinja=form_data)
    return render_template("home.html")
```
- `@app.route('/my_app', methods=["GET", "POST"])`: This route allows both `GET` and `POST` methods.
  - **GET Method**: When the user accesses this URL directly, it will return the `home.html` template (if defined).
  - **POST Method**: When a form is submitted to this URL, the `POST` method processes the form data.
    - `form_data = request.form.get("course")`: Retrieves form input with the name "course".
    - `render_template("course.html", jinja=form_data)`: Renders the `course.html` template and passes the variable `form_data` as `jinja` to be used in the template.

#### Second Route: `/second`
```python
@app.route('/second')
def second():
    if request.method == "POST":
        form_data = request.form.get("course")
        return render_template("course.html", jinja=form_data)
    return render_template("home.html")
```
- This route is similar to `/my_app`, but it lacks the method specification in the decorator, so it will only respond to `GET` requests.
- The `request.method` check for `POST` within the function won’t be relevant without specifying `"POST"` in the route methods, so the `POST` condition will not be triggered.

### Running the App
```python
app.run(debug=True)
```
- `app.run(debug=True)`: Starts the Flask development server. The `debug=True` argument enables:
  - Automatic reloading when code changes.
  - More detailed error messages, useful during development.

### Explanation of Key Concepts
- **GET vs. POST**:
  - **GET**: Retrieves information from the server. It is the default method for Flask routes.
  - **POST**: Sends data to the server, often used for submitting forms.
- **Templates**:
  - Templates like `home.html` and `course.html` are used to render dynamic content using Jinja.
  - `render_template()` allows data (e.g., `form_data`) to be passed to HTML templates, where it can be displayed using `{{ jinja }}`.

### Example of a Jinja Template (`course.html`)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Course</title>
</head>
<body>
    <h1>Your selected course: {{ jinja }}</h1>
</body>
</html>
```
- This template would display a message like "Your selected course: Data Science" based on the form input passed from the `/my_app` route.

### Example of `home.html` (For GET Request)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Home</title>
</head>
<body>
    <h1>Welcome to the Flask App</h1>
    <form action="/my_app" method="POST">
        <label for="course">Enter Course:</label>
        <input type="text" name="course" id="course">
        <button type="submit">Submit</button>
    </form>
</body>
</html>
```
- The form in this template submits the entered course name to the `/my_app` route using `POST`.

---

### Summary
- **Flask** allows you to build web applications with minimal setup.
- **Routes** define how different URLs are handled.
- **Jinja templates** are used to render dynamic HTML content.
- Using **`app.run(debug=True)`** enables a development mode that aids in identifying errors.
- With `GET` and `POST` methods, you can control how data is retrieved or submitted through web forms.

This setup provides a solid foundation for creating interactive web applications using Flask.