
---

### Introduction to Flask

**Flask** is a Python framework used for building web applications. It allows you to easily create routes, handle requests, and render dynamic content using **Jinja templates**.

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

---

### Folder Structure for a Flask App

To build a proper Flask app, it’s important to follow a specific folder structure. Below is the typical structure of a Flask project:

```
my-flask-app/
   ├── static/
   │   └── css/
   │       └── main.css
   ├── templates/
   │   ├── index.html
   │   └── course.html
   ├── hello.py
   └── data.py
```

- **Project Folder (my-flask-app/)**: This is the main folder containing all files for the Flask application.
- **`static/` folder**: Stores static files like CSS, JavaScript, and images.
  - Example: `css/main.css` is stored in `static/css/`.
- **`templates/` folder**: Contains HTML files that serve as templates. In the example, it has `index.html` and `course.html`.
- **Python files**: Files like `hello.py` and `data.py` are placed directly in the project folder (outside `static` and `templates`).

> **Note**: The names of the folders `static` and `templates` are essential for Flask to locate and serve static assets and templates properly. The project folder can be named anything, but the structure inside it should remain consistent.

---

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
    return render_template("home.html")
```
- This route responds to `GET` requests by rendering the `home.html` template.

---

### Using Jinja Templates

Flask uses the **Jinja2** template engine, which allows for creating HTML templates that can dynamically render data. It helps avoid repetitive HTML coding and allows you to inject data directly from the Flask app into the templates.

#### Example: Basic Route with Template
```python
@app.route('/user/<name>')
def user(name):
    return render_template('index.html', name=name)
```
- **Template (`index.html`)**:
  ```html
  <h1>Hello, {{ name }}!</h1>
  <p>Change the name in the <em>browser address bar</em> and reload the page.</p>
  ```

#### Linking Static Files
To use assets like CSS in your templates, Flask provides the `url_for` function:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
```

#### Passing Variables to Templates
With `render_template()`, you can pass variables like strings, integers, lists, or dictionaries:
```python
@app.route('/president/<int:ord>')
def president(ord):
    return render_template('course.html', pres=pres_dict, ord=ord, the_title=pres_dict['President'])
```

---

### Running the App
```python
app.run(debug=True)
```
- `app.run(debug=True)`: Starts the Flask development server. The `debug=True` argument enables:
  - Automatic reloading when code changes.
  - More detailed error messages, useful during development.

- **Using the `--app` Option**:
   - You can also run your app using the `--app` option, which is particularly useful for Flask versions 2.2 and later:
     ```bash
     flask --app hello run --debug
     ```
   - The `--debug` flag enables the debug mode, which provides detailed error messages and automatically reloads the server when code changes are made. This is especially helpful during development.

---

### Explanation of Key Concepts

- **GET vs. POST**:
  - **GET**: Retrieves information from the server. It is the default method for Flask routes.
  - **POST**: Sends data to the server, often used for submitting forms.
- **Templates**:
  - Templates like `home.html` and `course.html` are used to render dynamic content using Jinja.
  - `render_template()` allows data (e.g., `form_data`) to be passed to HTML templates, where it can be displayed using `{{ jinja }}`.

- **The `__name__` Variable**:
  - In Python, `__name__` is a special built-in variable that represents the name of the current module.
  - When a Python script is run directly, the `__name__` variable is set to `"__main__"`.
  - When a script is imported as a module in another script, `__name__` is set to the name of that module.

- **Using `if __name__ == "__main__":`**:
  - This construct is used to determine if a script is being run directly or being imported:
    ```python
    if __name__ == "__main__":
        app.run()
    ```
  - If the script is executed directly, the code inside this block will run (like starting the Flask application).
  - If the script is imported into another module, the code inside this block will not run. This is useful for writing code that should only execute when the file is run as the main program.

---

### Summary
- **Flask** allows you to build web applications with minimal setup.
- **Routes** define how different URLs are handled.
- **Jinja templates** are used to render dynamic HTML content.
- Using **`app.run(debug=True)`** enables a development mode that aids in identifying errors.
- **Folder Structure** is important for managing assets and templates.
- With **`GET` and `POST` methods**, you can control how data is retrieved or submitted through web forms.

By following these guidelines, you can build a Flask app that is well-organized and capable of serving dynamic web pages using Jinja templates.

---
