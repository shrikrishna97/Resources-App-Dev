
---

### **Day 2: Database Setup, Models, and User Authentication - Coding Session**

### **Objective:**
By the end of this session, you will learn how to set up a database in Flask using **Flask-SQLAlchemy**, define models, perform basic CRUD operations (Create, Read, Update, Delete), and implement user authentication with **Flask-Security**.

---

### **1. Setting Up the Database with Flask-SQLAlchemy**

#### **Step 1: Install Required Libraries**
Ensure you have Flask-SQLAlchemy and Flask-Security installed. In your terminal, run:

```bash
pip install flask flask_sqlalchemy flask_security
```

#### **Step 2: Configure the Database**

In your `app.py` file, add the following configuration to set up **Flask-SQLAlchemy** and **Flask-Security** for user authentication:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_bcrypt import Bcrypt

# Initialize the Flask application
app = Flask(__name__)

# Flask-SQLAlchemy Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database URI for SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.config['SECRET_KEY'] = 'mysecretkey'  # Secret key for session protection
app.config['SECURITY_PASSWORD_SALT'] = 'somesalt'  # Salt for password hashing

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize SQLAlchemy with the app
db = SQLAlchemy(app)

# Initialize Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
```

**Explanation**:
- **`SQLALCHEMY_DATABASE_URI`**: Specifies the database URI (SQLite in this case).
- **`SECRET_KEY`**: Protects Flask sessions.
- **`SECURITY_PASSWORD_SALT`**: A salt value for securely hashing passwords.
- **`Flask-Security` Setup**: We initialize **Flask-Security** by creating a **`SQLAlchemyUserDatastore`** object, which connects the user model with **Flask-Security**'s built-in functionalities.

---

### **2. Creating Database Models for User Authentication**

Now we will define the models for **User** and **Role** that are used by **Flask-Security**.

#### **Step 1: Define the User and Role Models**

In `models.py`, create the following models:

```python
from flask_security import UserMixin, RoleMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize db object
db = SQLAlchemy()

# Role Model
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    # For relationship with CRUD operations
    operations = db.relationship('CrudOperation', backref='user', lazy=True)
```

**Explanation**:
- **Role Model**: The `Role` model represents the roles (like Admin, Manager, Customer). It uses **`RoleMixin`** to integrate with Flask-Security.
- **User Model**: The `User` model includes essential fields like `username`, `email`, and `password_hash`. It also uses **`UserMixin`** from Flask-Security, which provides common functionalities like `is_authenticated`, `is_active`, etc.
- **Relationship**: A `User` can have many `CrudOperation` records, and we use **`db.relationship`** to define this one-to-many relationship.

---

### **3. Initializing the Database**

After defining the models, let’s initialize the database by creating the tables.

#### **Step 1: Initialize the Database**

Run the following commands in your terminal to create the database:

1. Open the Flask shell:

```bash
flask shell
```

2. Import the `db` object from your app and create all tables:

```python
from app import db
db.create_all()  # Create all tables defined in models.py
```

---

### **4. User Authentication with Flask-Security**

Now that we have set up the database models, let’s implement user authentication.

#### **Step 1: Registering a New User**

Here’s how you can register a new user in Flask:

```python
from flask import request, render_template, redirect, url_for, flash
from flask_security import login_user
from app import db, bcrypt
from models import User, Role

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')  # Hashing the password
        
        # Create a new user with a role (e.g., 'Customer')
        role = Role.query.filter_by(name='Customer').first()
        new_user = User(username=username, email=email, password_hash=password_hash, role=role)
        
        db.session.add(new_user)  # Add to the session
        db.session.commit()  # Commit to the database
        
        flash('Your account has been created!', 'success')  # Flash success message
        return redirect(url_for('login'))  # Redirect to login page

    return render_template('register.html')
```

**Explanation**:
- **Flask-Security** does the heavy lifting of handling user login, authentication, and security. The `register` function creates a new user, hashes the password using **Bcrypt**, and assigns them a role (e.g., `Customer`).

#### **Step 2: Logging in a User**

Flask-Security provides **login management** out of the box. Here’s how you log a user in:

```python
from flask_security import login_required, login_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and if password matches
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)  # Log the user in
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard
        else:
            flash('Login failed. Check username and/or password.', 'danger')

    return render_template('login.html')
```

**Explanation**:
- **`login_user(user)`**: This function logs the user in by setting the appropriate session variables.
- **Password Validation**: The **`bcrypt.check_password_hash()`** function compares the entered password with the hashed password stored in the database.

#### **Step 3: Protecting Routes with Authentication**

We can restrict certain routes to logged-in users only using Flask-Security's **`@login_required`** decorator.

```python
from flask_security import login_required

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')  # Accessible only to logged-in users
```

**Explanation**:
- **`@login_required`** ensures that only authenticated users can access the `dashboard` route.

---

### **5. Implementing CRUD Operations**

#### **Create, Read, Update, Delete Users**

Refer to the previous sections for **CRUD operations** on users, which include creating, reading, updating, and deleting users in the database.

---

### **6. Handling Forms and Flash Messages**

**Forms** allow you to gather user input, and **flash messages** provide feedback after actions like adding or updating records.

#### **Using Flash Messages for Feedback**

Add the following to your templates to show flash messages:

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        <ul class="flashes">
            {% for category, message in messages %}
                <li class="{{ category }}">{{ message }}</li>
            {% endfor %}
        </ul>
    {% endif %}
{% endwith %}
```

---

### **7. Conclusion**

In this session, you've learned:
- How to set up and configure a database with **Flask-SQLAlchemy**.
- How to create database models (representing tables) for **User** and **Role**.
- How to implement **user authentication** with **Flask-Security**: registering, logging in, and restricting access to routes.
- How to perform basic **CRUD operations**: create, read, update, and delete records.
- How to handle **forms** and display **flash messages** to give feedback to users.

With this foundational knowledge, you can now start building more secure and interactive Flask applications.

---


**Questions**:
- What are the differences between **Flask-SQLAlchemy** and **Flask-Migrate**?
- How do you use **Flask-Security** for user authentication?
- What is the difference between **UserMixin** and **RoleMixin** in **Flask-Security**?

**Resources**:
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/en/latest/)
- [Flask-Security Documentation](https://flask-security.readthedocs.io/en/stable/)
- [Flask-Security Quickstart](https://flask-security.readthedocs.io/en/stable/quickstart.html)

**Additional Resources**:
- [Flask-Security Cookbook](https://flask-security.readthedocs.io/en/stable/cookbook.html)
- [Flask-SQLAlchemy Cookbook](https://flask-sqlalchemy.palletsprojects.com/en/2.x/cookbook/)

[Shri Krishna's github](https://github.com/shrikrishna97/Resources-App-Dev/tree/main)