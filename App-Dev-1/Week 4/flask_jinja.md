

---

### Flask and Jinja Templates

**Flask** is a Python framework used for building web applications. It allows you to easily create routes and handle requests. An essential feature of Flask is its ability to use **Jinja templates** for rendering dynamic HTML.

### Folder Structure for a Flask App

To build a proper Flask app, it’s important to follow a specific folder structure. Below is the typical structure of a Flask project:

```
my-flask-app/
   ├── static/
   │   └── css/
   │       └── main.css
   ├── templates/
   │   ├── index.html
   │   └── student.html
   ├── data.py
   └── students.py
```

- **Project Folder (my-flask-app/)**: This is the main folder containing all files for the Flask application.
- **`static/` folder**: Stores static files like CSS, JavaScript, and images.
  - Example: `css/main.css` is stored in `static/css/`.
- **`templates/` folder**: Contains HTML files that serve as templates. In the example, it has `index.html` and `student.html`.
- **Python files**: Files like `data.py` and `students.py` are placed directly in the project folder (outside `static` and `templates`).

> **Note**: The names of the folders `static` and `templates` are essential for Flask to locate and serve static assets and templates properly. The project folder can be named anything, but the structure inside it should remain consistent.

---

### Using Jinja Templates

Flask uses the **Jinja2** template engine, which allows for creating HTML templates that can dynamically render data. It helps avoid repetitive HTML coding and allows you to inject data directly from the Flask app into the templates.







---

### Using Templates in Flask Routes

You can render a template and pass data to it directly from a Flask route using the `render_template` function.

**Example: Basic Route with Template**:
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/user/<name>')
def user(name):
    return render_template('hello.html', name=name)
```

- **Importing `render_template`**: This function is used to render HTML templates.
- **Route Function**: The `user` function renders `hello.html` and passes the `name` variable to it.
- **Template (`hello.html`)**:
  ```html
  <h1>Hello, {{ name }}!</h1>
  <p>Change the name in the <em>browser address bar</em> and reload the page.</p>
  ```

#### Linking Static Files

To use assets like CSS in your templates, Flask provides the `url_for` function:

**Example**:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
```

- The `url_for()` function ensures that Flask correctly links to the `main.css` file located in the `static/css/` folder.

---

### Passing Variables to Templates

With `render_template()`, you can pass variables like strings, integers, lists, or dictionaries:

**Example**:
```python
@app.route('/president/<int:ord>')
def president(ord):
    # pres_dict is a dictionary containing president data.
    return render_template('president.html', pres=pres_dict, ord=ord, the_title=pres_dict['President'])
```

- **Passing Variables**: Here, `pres=pres_dict`, `ord=ord`, and `the_title=pres_dict['President']` are passed to `president.html`.
- **Using Variables in the Template**:
  ```html
  <h1>{{ pres['President'] }}</h1>
  <title>{{ the_title }}</title>
  ```

This example demonstrates how `pres` is used in the template as a shorthand for `pres_dict`, making the template code more concise.

#### Why Use Jinja with Flask?

- **Dynamic Content**: Jinja allows injecting dynamic content into HTML.
- **Reuse of Layouts**: Templates reduce redundancy, allowing for consistent layout across multiple pages.
- **Cleaner Code**: It separates the HTML structure from Python logic, making code more maintainable.

---

### Summary

- **Folder Structure**: The project must include `static/` for assets and `templates/` for HTML files.
- **Jinja Templates**: Use `{{ }}` for variables and `{% %}` for control structures (like loops or conditions).
- **`render_template`**: Renders templates and passes variables, making it possible to create dynamic and reusable HTML.
- **Static File Management**: Use `url_for('static', filename='...')` for linking CSS, JavaScript, or image files.

By following these guidelines, you can build a Flask app that is well-organized and capable of serving dynamic web pages using Jinja templates.

--- 

