
---

### **Day 2: Database Setup, Models, and User Authentication**

---

**Theory (10 AM - 12:30 PM)**

---

### 1. **Flask-SQLAlchemy: Introduction and Setup**

**Objective:** Learn how to set up and use Flask-SQLAlchemy for handling SQLite database operations in a Flask web application.

---

**What is SQLAlchemy?**
- **SQLAlchemy** is an Object Relational Mapper (ORM) that allows you to interact with a database using Python objects instead of raw SQL queries. It abstracts database operations, making it easier to manage and interact with databases.
- **Flask-SQLAlchemy** is an extension that integrates SQLAlchemy into Flask applications, simplifying database management by providing tools to work with SQLAlchemy seamlessly in a Flask environment.

---

**Steps to Set Up Flask-SQLAlchemy:**
1. **Install Flask-SQLAlchemy via pip**:
   ```bash
   pip install flask-sqlalchemy
   ```

2. **Flask App Configuration**:
   Flask-SQLAlchemy needs to be configured to connect your Flask application with a database. In this example, we use **SQLite**, a lightweight relational database.

   Here's the basic configuration I used in the Python code:

   ```python
   from flask import Flask
   from flask_sqlalchemy import SQLAlchemy

   app = Flask(__name__)

   # Flask-SQLAlchemy Configuration
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database file
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking (to reduce overhead)
   app.config['SECRET_KEY'] = 'mysecretkey'  # Secret key for session management
   app.config['SECURITY_PASSWORD_SALT'] = 'mysecretsalt'  # Salt for password hashing

   db = SQLAlchemy(app)
   ```

---

**Explanation of the Configuration:**
- **`SQLALCHEMY_DATABASE_URI`**:
   - This configuration setting tells Flask-SQLAlchemy where to find your database. In this case, `'sqlite:///site.db'` refers to an SQLite database stored in a file called `site.db` in your project directory. The `sqlite:///` prefix indicates you're using an SQLite database.
   - If you wanted to use another type of database, like MySQL or PostgreSQL, you would change the URI accordingly (e.g., `'mysql://username:password@localhost/dbname'` for MySQL).

- **`SQLALCHEMY_TRACK_MODIFICATIONS`**:
   - This setting is set to `False` to disable the modification tracking feature in SQLAlchemy. By default, SQLAlchemy tracks modifications to objects, which adds some overhead. We don't need this feature in most cases, so it is turned off to improve performance.

- **`SECRET_KEY`**:
   - The `SECRET_KEY` is used by Flask for cryptographic operations like signing cookies and sessions. It's important for securing sessions and forms. You should replace `'mysecretkey'` with a more secure, random string in production.

- **`SECURITY_PASSWORD_SALT`**:
   - This setting is used for password hashing. It's the "salt" used by **Flask-Security** when hashing user passwords. Salts help make password hashes more secure by adding random data before the hash operation.

---

### 2. **Database Models: Defining Entities**

**Objective:** Learn how to define models (representations of tables) in your SQLite database using SQLAlchemy.

**Creating Models in SQLAlchemy:**
Models are Python classes that represent database tables. Each class corresponds to a table, and each attribute corresponds to a column in the table.

---

**Example: Defining a User Model**

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique identifier for each user
    username = db.Column(db.String(120), unique=True, nullable=False)  # user's username
    email = db.Column(db.String(120), unique=True, nullable=False)  # user's email
    password = db.Column(db.String(60), nullable=False)  # hashed password
    roles = db.relationship('Role', secondary='user_roles')  # many-to-many relationship with Role
```

**Explanation of Attributes:**
- **`id`**: The primary key of the table. This uniquely identifies each user in the database.
- **`username`** and **`email`**: These columns are marked as `unique=True`, meaning no two users can have the same username or email. The `nullable=False` constraint makes these fields required.
- **`password`**: Stores the hashed password of the user. It’s marked as `nullable=False`, so every user must have a password.
- **`roles`**: This is a **many-to-many** relationship. A user can have multiple roles (like "Admin", "Manager", etc.), and each role can be assigned to multiple users.

---

### 3. **User Authentication: Setting Up with Flask-Security**

**Objective:** Learn how to handle user authentication securely using **Flask-Security**, which integrates user authentication, role management, password hashing, and more.

---

### **`UserMixin` and `RoleMixin`:**

- **`UserMixin`** and **`RoleMixin`** are classes provided by **Flask-Security** that provide the necessary methods for managing authentication and role-based access control.

1. **`UserMixin`**:
   - The `UserMixin` class gives the `User` model a set of methods that Flask-Security needs for user management. These include methods like `get_id()`, `is_authenticated()`, `is_active()`, `is_anonymous()`, and `set_password()`. These methods are used by **Flask-Login** (used internally by Flask-Security) to manage user sessions.
   
   ```python
   class User(db.Model, UserMixin):
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(120), unique=True, nullable=False)
       email = db.Column(db.String(120), unique=True, nullable=False)
       password = db.Column(db.String(60), nullable=False)
       roles = db.relationship('Role', secondary='user_roles')
   ```

2. **`RoleMixin`**:
   - The `RoleMixin` class gives the `Role` model a set of methods for role management, including the ability to check whether a user has a certain role or permission.
   
   ```python
   class Role(db.Model, RoleMixin):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(80), unique=True)
   ```

---

### 4. **Relationship: One-to-Many and Many-to-Many**

**One-to-Many Relationship**:
- A **One-to-Many** relationship is used when one record in a table is associated with multiple records in another table. For instance, a `User` can have many `Posts`, but each `Post` belongs to one `User`.

**Example**:
```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key to User

    user = db.relationship('User', back_populates='posts')
```

- In the above example, each `Post` is associated with one `User` (via `user_id`), and a `User` can have many `Posts`.

---

**Many-to-Many Relationship**:
- A **Many-to-Many** relationship exists when each record in one table can be associated with multiple records in another table, and vice versa. In the case of `User` and `Role`, each user can have many roles, and each role can be assigned to many users.

**Example (Many-to-Many)**:
```python
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='user_roles')  # Many-to-many relationship

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

user_roles = db.Table('user_roles',  # Association table
                      db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                      db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))
```

- **`user_roles`**: This is an **association table** that links `User` and `Role`. It doesn't have its own model; it simply holds the foreign keys that connect the `User` and `Role` models.
- **`roles = db.relationship('Role', secondary='user_roles')`**: This establishes the many-to-many relationship from the `User` model. It tells SQLAlchemy that the `roles` attribute of a `User` should be connected to the `Role` model via the `user_roles` association table.

---

### 5. **Using Flask-Security for User Authentication**

**Objective:** Learn how to handle user authentication securely using **Flask-Security**, which integrates user authentication, role management, password hashing, and more.

Here’s the setup:
1. **Install Flask-Security**:
   ```bash
   pip install flask-security
   ```

2. **Set Up User Registration and Authentication**:

```python
from flask_security import Security, SQLAlchemyUser

Datastore, UserMixin, RoleMixin
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SECURITY_PASSWORD_SALT'] = 'mysecretsalt'

db = SQLAlchemy(app)

# Define User and Role models
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')

user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                      db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

# Initialize user datastore
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

if __name__ == '__main__':
    app.run(debug=True)
```

---

### Key Concepts to Remember:
- **Flask-SQLAlchemy** provides a simple and effective way to work with relational databases in Flask apps.
- **Flask-Security** handles user authentication, password hashing, and role management.
- **`UserMixin` and `RoleMixin`** make it easy to manage user sessions and roles.
- **Many-to-Many and One-to-Many relationships** define how models (tables) are related in your database, making it easy to structure your application’s data.

---

This document provide a solid understanding of database models, relationships, and the configurations used in Flask-SQLAlchemy!