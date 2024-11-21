
### **Day 1: Introduction to Flask, Jinja2, HTML/CSS, and Setup**
**Theory (10 AM - 12:30 PM)**  
- **Introduction to Flask**: Understanding Flask's structure (app.py, templates, static).
- **Setting up your Flask Environment**: Install necessary dependencies and initialize your project.  
  ```bash
  pip install flask flask-sqlalchemy flask-wtf
  ```

- **Jinja2 Templating Engine**: Basic structure of a Flask app using Jinja2 templates to render dynamic content.

- **HTML & CSS Basics with Bootstrap**: Learn how to structure HTML files and use Bootstrap for UI design.

**Lunch Break (12:30 PM - 2:00 PM)**

**Coding (2 PM - 4 PM)**  
- **Create Project Structure**:
  - **app.py**: Main entry point for the Flask app.
  - **models.py**: Where database models will reside.
  - **templates/**: Create `index.html` as a base template.
  - **static/**: Store your CSS and JS files (use Bootstrap CDN for styling).

  Example app.py:
  ```python
  from flask import Flask, render_template
  app = Flask(__name__)
  
  @app.route('/')
  def home():
      return render_template('index.html')
  
  if __name__ == "__main__":
      app.run(debug=True)
  ```

- **Create a Simple HTML Template** in `templates/index.html`:
  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Flask App</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body>
      <div class="container">
          <h1>Welcome to Flask!</h1>
      </div>
  </body>
  </html>
  ```

**Prep/Doubt Clearing (4 PM - 5 PM)**  
- Discuss the Flask structure, routing, and templates.

---

### **Day 2: Database Setup, Models, and User Authentication**
**Theory (10 AM - 12:30 PM)**  
- **Flask-SQLAlchemy**: Learn how to set up SQLAlchemy to handle SQLite database operations.
- **Database Models**: Create models for User, CrudOperation, and other required entities.
- **User Authentication**: Learn how to set up password hashing and user authentication.

**Lunch Break (12:30 PM - 2:00 PM)**

**Coding (2 PM - 4 PM)**  
- **Setting up the Database**: In `app.py`, configure the SQLite database.
  ```python
  from flask_sqlalchemy import SQLAlchemy
  db = SQLAlchemy()
  
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.init_app(app)
  ```

- **Create Database Models** in `models.py`:
  ```python
  from datetime import datetime
  from flask_sqlalchemy import SQLAlchemy
  db = SQLAlchemy()
  
  class User(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(120), unique=True, nullable=False)
      password_hash = db.Column(db.String(128), nullable=False)
      role = db.Column(db.String(50), nullable=False)
  
  class CrudOperation(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      data = db.Column(db.String(100), nullable=False)
      date_created = db.Column(db.DateTime, default=datetime.utcnow)
  ```

- **Initialize Database**: After defining your models, run the following commands in the terminal to create the database:
  ```bash
  flask shell
  >>> from app import db
  >>> db.create_all()
  ```

**Prep/Doubt Clearing (4 PM - 5 PM)**  
- Discuss models and the database initialization process.

---

### **Day 3: User Registration, Login, and Role-Based Access**
**Theory (10 AM - 12:30 PM)**  
- **Flask Forms**: Learn how to create forms using `Flask-WTF` to handle registration, login, etc.
- **Role-based Views**: Implement role-based authentication using Flask decorators.

**Lunch Break (12:30 PM - 2:00 PM)**

**Coding (2 PM - 4 PM)**  
- **Create User Registration Form** in `forms.py`:
  ```python
  from flask_wtf import FlaskForm
  from wtforms import StringField, PasswordField
  from wtforms.validators import DataRequired, Length
  
  class RegistrationForm(FlaskForm):
      username = StringField('Username', validators=[DataRequired(), Length(min=3, max=120)])
      password = PasswordField('Password', validators=[DataRequired()])
  ```

- **Create Views for Registration and Login** in `app.py`:
  ```python
  from flask import render_template, redirect, url_for, request
  from werkzeug.security import generate_password_hash, check_password_hash
  from models import db, User
  from forms import RegistrationForm
  
  @app.route("/register", methods=['GET', 'POST'])
  def register():
      form = RegistrationForm()
      if form.validate_on_submit():
          hashed_password = generate_password_hash(form.password.data)
          user = User(username=form.username.data, password_hash=hashed_password, role="customer")
          db.session.add(user)
          db.session.commit()
          return redirect(url_for('login'))
      return render_template('register.html', form=form)
  ```

- **Create Login Functionality**:
  ```python
  @app.route("/login", methods=['GET', 'POST'])
  def login():
      # Logic for login with password check
  ```

**Prep/Doubt Clearing (4 PM - 5 PM)**  
- Discuss user registration flow, form validation, and how to secure passwords.

---

### **Day 4: Admin Role - Dashboard and CRUD Operations**
**Theory (10 AM - 12:30 PM)**  
- **Admin Role CRUD**: Learn how to manage users via an Admin dashboard.
- **Creating CRUD Operations**: Admin can create, update, and delete data.

**Lunch Break (12:30 PM - 2:00 PM)**

**Coding (2 PM - 4 PM)**  
- **Admin Dashboard** (app.py):
  ```python
  @app.route("/admin/dashboard")
  def admin_dashboard():
      users = User.query.all()
      return render_template('admin_dashboard.html', users=users)
  ```

- **Admin CRUD for Users** (app.py):
  ```python
  @app.route("/admin/update_user/<int:user_id>", methods=['GET', 'POST'])
  def update_user(user_id):
      user = User.query.get_or_404(user_id)
      form = RegistrationForm()  # Reuse registration form for updates
      if form.validate_on_submit():
          user.username = form.username.data
          db.session.commit()
          return redirect(url_for('admin_dashboard'))
      return render_template('update_user.html', form=form, user=user)
  ```

**Prep/Doubt Clearing (4 PM - 5 PM)**  
- Discuss Admin Dashboard functionalities and how to handle CRUD operations for users.

---

### **Day 5: Manager Role - Dashboard and CRUD Operations**
**Theory (10 AM - 12:30 PM)**  
- **Manager Role CRUD**: Learn how managers can interact with operations data.
- **Managing Interconnected Data**: How to work with multiple related tables.

**Lunch Break (12:30 PM - 2:00 PM)**

**Coding (2 PM - 4 PM)**  
- **Manager Dashboard and CRUD** (app.py):
  ```python
  @app.route("/manager/dashboard")
  def manager_dashboard():
      operations = CrudOperation.query.all()
      return render_template('manager_dashboard.html', operations=operations)
  ```

- **Manager Create/Update Operations**:
  ```python
  @app.route("/manager/create_operation", methods=['GET', 'POST'])
  def create_operation():
      form = CreateOperationForm()
      if form.validate_on_submit():
          operation = CrudOperation(data=form.data.data)
          db.session.add(operation)
          db.session.commit()
          return redirect(url_for('manager_dashboard'))
      return render_template('create_operation.html', form=form)
  ```

**Prep/Doubt Clearing (4 PM - 5 PM)**  
- Discuss the role and CRUD operations from the manager's perspective.

---

### **Day 6: Customer Role - Profile and Operations**
**Theory (10 AM - 12:30 PM)**  
- **Customer Role**: Profile page functionality and CRUD operations from the customer's perspective.

**Lunch Break (12:30 PM - 2:00 PM)**

**Coding (2 PM - 4 PM)**  
- **Customer Profile Page**:
  ```python
  @app.route("/customer/profile")
  def customer_profile():
      user = User.query.filter_by(id=current_user.id).first()
      return render_template('customer_profile.html', user=user)
  ```

- **Customer CRUD Operations**

:
  ```python
  @app.route("/customer/create_operation", methods=['GET', 'POST'])
  def customer_create_operation():
      form = CreateOperationForm()
      if form.validate_on_submit():
          operation = CrudOperation(data=form.data.data)
          db.session.add(operation)
          db.session.commit()
          return redirect(url_for('customer_profile'))
      return render_template('create_operation_customer.html', form=form)
  ```

**Prep/Doubt Clearing (4 PM - 5 PM)**  
- Discuss how the customer interacts with their profile and manages operations.

---

### **Day 7: Finalizing, Testing, and Deployment**
**Theory (10 AM - 12:30 PM)**  
- **Testing and Debugging**: Best practices for debugging Flask apps.
- **Problem Statement Discussion**: Have a discussion over problem statement.
- **Deployment**: Deploying your Flask app.[Not Core]

**Lunch Break (12:30 PM - 2:00 PM)**

**Coding (2 PM - 4 PM)**  
- **Testing CRUD Functionality**: Ensure that all roles are functioning correctly.
- **[Extra] Deploying**: Guide on pushing your project.

---

By following this approach with **full code examples** and **detailed explanations**, you’ll have a more structured learning experience that will help you get comfortable with Flask and the project requirements.
