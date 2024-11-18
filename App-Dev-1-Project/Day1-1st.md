### **Day 1: Introduction to Flask, Jinja2, HTML/CSS, and Setup**

**Theory (10 AM - 12:30 PM)**

#### **Introduction to Flask**  
Flask is a micro web framework for Python that is simple, flexible, and powerful. Its lightweight nature allows developers to build web applications quickly without the overhead of more extensive frameworks. A typical Flask project structure includes:

- **app.py**: The main entry point for your application.
- **templates/**: Directory for storing HTML templates rendered by Flask.
- **static/**: Directory for storing static files such as CSS, JavaScript, and images.

Understanding how these components interact is essential for developing a Flask application effectively.

#### **Setting up your Flask Environment**  
To get started, ensure Python is installed on your system. Next, follow these steps to set up your Flask environment:

1. **Create a virtual environment** (recommended for isolating your project dependencies):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. **Install Flask and necessary extensions**:
   ```bash
   pip install flask flask-sqlalchemy flask-wtf
   ```

These packages include:
- **Flask**: The core framework for building your web app.
- **Flask-SQLAlchemy**: A SQL toolkit and Object-Relational Mapping (ORM) for managing database operations.
- **Flask-WTF**: An extension for integrating WTForms for form handling and validation.

#### **Jinja2 Templating Engine**  
Jinja2 is Flask's built-in templating engine used for rendering dynamic web pages. It allows developers to embed Python-like expressions in HTML. Here’s a simple example of a Jinja2 template:

**Basic structure in a template file (`templates/index.html`)**:

**Python Flask Code (`app.py`)**:
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='Home Page', username='John Doe')

if __name__ == '__main__':
    app.run(debug=True)
```

**Template Code (`templates/index.html`)**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <h1>Welcome, {{ username }}!</h1>
</body>
</html>
```
In this example, `{{ title }}` and `{{ username }}` are placeholders that Flask can replace with actual data passed from `app.py`.

#### **HTML & CSS Basics with Bootstrap**  
Understanding HTML and CSS is key to building the front end of your Flask app. Additionally, using Bootstrap, a popular CSS framework, can help create responsive and visually appealing designs with minimal effort.

**Key Bootstrap components to learn**:
- **Container**: A layout element to center content.
- **Grid system**: For creating flexible layouts.
- **Buttons, Forms, and Navbars**: Essential for user interaction.

**Sample HTML structure with Bootstrap**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Flask App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center">Welcome to My Flask App!</h1>
        <p class="text-muted">This is a simple web page styled with Bootstrap.</p>
    </div>
</body>
</html>
```
With this foundational knowledge, you’ll be ready to dive deeper into building and styling your Flask web applications.

**Resources**:
- [Flask Documentation](https://flask.palletsprojects.com/en/2.2.x/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/en/3.1.x/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)

**Additional Resources**:
- [Flask Quickstart](https://flask.palletsprojects.com/en/2.2.x/quickstart/)
- [Jinja2 Quickstart](https://jinja.palletsprojects.com/en/3.1.x/quickstart/)
- [Bootstrap Quickstart](https://getbootstrap.com/docs/5.3/getting-started/introduction/)

[Shri Krishna's github](https://github.com/shrikrishna97/Resources-App-Dev/tree/main)

**Questions**:
- What are the differences between Flask and Django?
- What are the main components of a Flask app?
- How do you handle user input in Flask?    
- How do you handle user authentication in Flask?
- How do you handle database operations in Flask?




