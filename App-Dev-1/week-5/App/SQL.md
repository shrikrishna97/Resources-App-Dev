# Flask and SQLAlchemy Guide

### Pre-requisite:  Download VS Code, python, pip.

[App Github link](https://github.com/shrikrishna97/Resources-App-Dev/tree/main/App-Dev-1/week-5/App)

**NOTE: This document might get updated multiple times till last session.**

## **[Session 1: Introduction to Flask and Jinja Templates](https://www.youtube.com/live/wBI5SZjaAD8?feature=shared)**

### **1. Introduction to Flask**

- Flask is a lightweight Python web micro framework for building web applications.
- It follows the WSGI (Web Server Gateway Interface) standard.
- Provides flexibility and simplicity with minimal setup.

### **2. Setting Up a Flask Application**

#### **Installation**

```sh
pip install flask
```

#### **Basic Flask Application**

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
```

- Run `python app.py` and visit `http://127.0.0.1:5000/`.

### **3. Jinja Templates**

- Jinja2 is a templating engine used in Flask for rendering dynamic HTML.
- Supports variables, loops, and conditionals.

#### **Example Template (templates/index.html)**

```html
<!DOCTYPE html>
<html>
<head><title>Flask App</title></head>
<body>
    <h1>Welcome, {{ name }}</h1>
    {% if items %}
        <ul>
            {% for item in items %}
                <li>{{ item }}</li>
            {% endfor %}
        </ul>
    {% else %}
        <p>No items found.</p>
    {% endif %}
</body>
</html>
```

#### **Flask Route to Render Template**

```python
from flask import render_template

@app.route('/items')
def items():
    return render_template('index.html', name="User", items=["Apple", "Banana", "Cherry"])
```

### **4. Why SQLAlchemy Over SQLite?**

- SQLite is good for small applications but lacks scalability and advanced querying.
- SQLAlchemy provides an ORM (Object-Relational Mapping) for better maintainability and flexibility.
- SQLAlchemy has easier(english) queries than SQLite(SQL).

---

## **[Session 2: Database Models and CRUD Operations](https://www.youtube.com/live/e1F621aPDKw?feature=shared)**

### **1. Recap of Flask & Jinja**

- A quick recap of Flask routing, templates, and rendering data dynamically.

### **2. Setting Up SQLAlchemy**

#### **Installation**

```sh
pip install flask-sqlalchemy
```

#### **Configuring the Database**

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.sqlite3'
db = SQLAlchemy(app)
```

### **[3. Creating a Model (User Table)](https://www.youtube.com/live/IZf7aW8S-zM?feature=shared)**

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

with app.app_context():
    db.create_all()
```

### **4. Adding Data to the Database**

```python
with app.app_context():
    user = User(username="JohnDoe")
    db.session.add(user)
    db.session.commit()
```

### **5. Fetching and Displaying Data**

#### **Flask Route**

```python
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)
```

#### **Jinja Template (templates/users.html)**

```html
<ul>
    {% for user in users %}
        <li>{{ user.username }}</li>
    {% endfor %}
</ul>
```

---

## **Session 3: Relationships and Advanced SQLAlchemy**

### **1. Recap of Models and CRUD Operations**

- Brief discussion on database setup, creating models, and performing CRUD operations.

### **2. One-to-Many Relationship (User and Class)**

#### **Creating Models with Relationships**

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    classes = db.relationship('Class', backref='creator', lazy=True)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

### **3. Querying Related Data**

```python
user = User.query.get(1)
for class in user.classes:
    print(class.title)
```

### **4. Many-to-Many Relationship (User and Class Participants)**

#### **Creating an Association Table**

```python
class_participants = db.Table('class_participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True)
)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    participants = db.relationship('User', secondary=class_participants, backref='participated_classes')
```

### **5. Final Recap and Q&A**

- Best practices with SQLAlchemy.
- How to integrate authentication and role-based access.
- Discuss future enhancements like migrations and API integrations.



------

### **Understanding `__name__` in Flask**

When creating a **Flask application**, we usually initialize it like this:

```python
from flask import Flask

app = Flask(__name__)  # Here __name__ is passed
```

#### **Why Do We Pass `__name__`?**

- `__name__` represents the **module name** of the script that is being executed.
- If the script is run **directly**, `__name__` is set to `"__main__"`.
- If the script is **imported** into another module, `__name__` is set to the **module's name**.
- **Flask uses this to locate resources** like templates and static files.

------

### **Counter-Example: Without Using `__name__`**

You **can** create a Flask app without passing `__name__`, but you have to manually specify configurations.

#### **Example:**

```python
from flask import Flask

app = Flask("custom_app")  # Instead of __name__, using a custom string

# Manually set the template folder
app.template_folder = "my_templates"

@app.route('/')
def home():
    return "Hello, Flask without __name__!"

if __name__ == "__main__":
    app.run(debug=True)
```

#### **How is this different?**

1. Flask won't automatically detect templates and static files
   - You must **manually specify** `app.template_folder = "my_templates"` and `app.static_folder = "my_static"`.
2. If the script is imported, Flask might not behave correctly
   - Some features like relative imports may break.

------

### **When NOT to Use `__name__`**

- If you have a **custom module structure** and don't rely on Flask's default behavior.
- If you're manually configuring everything (templates, static files, etc.).
- If you're **embedding Flask into a larger system** where module resolution is handled differently.

------

### **Best Practice?**

Using `Flask(__name__)` is still **recommended** unless you have a **strong reason to override it**. It ensures Flask correctly locates templates, static files, and configurations automatically.

### **Why Do We Use `if __name__ == "__main__":` in Flask?**

In **Python**, the special variable `__name__` helps determine **how a script is being run**:

- If the script is **run directly**, `__name__` is set to `"__main__"`.
- If the script is **imported into another module**, `__name__` is set to the **module name** instead.

### **How It Works in Flask**

When writing a Flask app, we typically include:

```python
if __name__ == "__main__":
    app.run(debug=True)
```

This ensures that the Flask server **only starts when the script is run directly**.

------

### **What Happens If We Don't Use It?**

#### **Example Without `if __name__ == "__main__":`**

```python
#filename: my_flask_app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

app.run(debug=True)  # This runs even when the module is imported!
```

**Problem:**
 If another script **imports this file**, Flask will **automatically start the server**, even if you don't want it to.

------

### **When Importing This Module**

Consider another file importing this script:

```python
import my_flask_app  # my_flask_app.py contains Flask code
```

- If **`if __name__ == "__main__":` is missing**, the Flask app will **start running automatically**.
- With `if __name__ == "__main__":`, the server **only starts when explicitly executed**, not when imported.

------

### **When Can We Skip It?**

If you’re using a **Flask app factory pattern**, you often don’t need `if __name__ == "__main__":`.

#### **Example: Using `flask run` Instead**

Instead of:

```sh
python my_flask_app.py
```

You can use:

```sh
flask run
```

In this case, Flask automatically finds the app, and `if __name__ == "__main__":` is not needed.

------

### **Conclusion**

-   **Prevents unintended execution when importing the module**
-   **Ensures the Flask app runs only when executed as a script**
-   **Good practice for maintainability and modularity**

### **Is `"__main__"` Important, or Can We Write Something Else?**

Yes, `__main__` is **important** because it's a special Python identifier. You **cannot** replace it with something else.

------

### **Why Is `__main__` Special?**

When Python executes a script, it sets the special variable `__name__` based on how the script is being run:

- If the script is **executed directly**, Python sets `__name__ = "__main__"`.
- If the script is **imported as a module**, `__name__` is set to the script's filename (without `.py`).

#### **Example**

```python
# my_script.py
print(f"__name__ is: {__name__}")

if __name__ == "__main__":
    print("Running directly")
```

**Running directly:**

```sh
python my_script.py
```

**Output:**

```
__name__ is: __main__
Running directly
```

**Importing into another script:**
```python
import my_script
```

**Output:**
```
__name__ is: my_script
```

*(Notice `"Running directly"` does **not** appear.)*

------

### **What If We Change `"__main__"`?**

You **cannot** replace `"__main__"` with a different string. If you do this:

```python
if __name__ == "custom_name":
    print("This will never run")
```

It **will never execute**, because Python will never set `__name__` to `"custom_name"`.

------

### **Conclusion**

-  **You MUST use `"__main__"` because it's predefined by Python.**
-  **It ensures the script runs only when executed directly, not when imported.**
-  **If you replace `"__main__"` with something else, the condition will never be `True`!**

------
### **Understanding the Difference: Script vs. Module vs. Python File vs. Flask App**  

To fully understand `__name__ == "__main__"`, let's break it down into four key concepts:  

| Term | Definition | Example |
|------|------------|---------|
| **Python File** | A `.py` file that contains Python code. It can be a script, a module, or a Flask app. | `my_script.py`, `my_module.py` |
| **Script** | A Python file that is meant to be executed directly (not imported). | `python my_script.py` |
| **Module** | A Python file that is designed to be **imported** into another script. | `import my_module` |
| **Flask App** | A Python file that runs a Flask application, typically with `__name__ == "__main__"` to ensure correct execution. | `app.py` (Flask entry point) |

---

## **1️⃣ `__name__` in Scripts (`__name__ == "__main__"`)**
A **script** is a Python file intended to be run directly. If we print `__name__` inside a script:

```python
# my_script.py
print(f"Script executed, __name__ = {__name__}")
```

### **Running the Script Directly**
```sh
python my_script.py
```
 **Output:**
```
Script executed, __name__ = __main__
```
✅ Since it was run directly, Python sets `__name__ = "__main__"`.

---

## **2️⃣ `__name__` in Modules (`__name__ == "module_name"`)**
A **module** is a Python file meant to be imported into another script.

```python
# my_module.py
print(f"Module loaded, __name__ = {__name__}")
```

### **Importing the Module**
```python
# another_script.py
import my_module
```

 **Output:**
```
Module loaded, __name__ = my_module
```
✅ Since `my_module.py` was **imported**, `__name__` is set to `"my_module"` instead of `"__main__"`.

---

## **3️⃣ Python File That Can Be Both a Script and a Module**
If you want a file to be **both runnable and importable**, use:
```python
if __name__ == "__main__":
    print("Running as a script")
else:
    print("Imported as a module")
```

### **Running Directly**
```sh
python my_file.py
```
 **Output:**
```
Running as a script
```

### **Importing in Another File**
```python
import my_file
```
 **Output:**
```
Imported as a module
```

✅ This is useful when you want a Python file to behave **differently** based on how it's executed.

---

## **4️⃣ `__name__` in Flask Apps**
Flask uses `__name__` to locate resources (templates, static files) and correctly configure the app.

```python
from flask import Flask

app = Flask(__name__)  # Uses module name

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":  
    app.run(debug=True)  # Runs only when script is executed directly
```

### **Why use `__name__`?**
1. ✅ If **run directly** (`python app.py`), `__name__ == "__main__"` → Flask starts normally.  
2. ✅ If **imported** (`from app import app`), `__name__ == "app"` → It won’t start automatically.  

This prevents unnecessary execution when the app is imported elsewhere (e.g., for testing or deployment).

---

## **Key Differences Summarized**
| Type | Purpose | `__name__` Value |
|------|---------|-----------------|
| **Script** | A file meant to be executed directly | `"__main__"` |
| **Module** | A file meant to be imported | `"module_name"` |
| **Python File** | General Python code (can be script or module) | Depends on how it's used |
| **Flask App** | Web application that runs with Flask | `"__main__"` when executed, `"app"` when imported |

---

### ** Can I Use Something Other Than `"__main__"`?**
No, `__main__` is a **special keyword** defined by Python.  
However, you can create your own main function and call it inside `if __name__ == "__main__"`:

```python
def main():
    print("Hello from main function!")

if __name__ == "__main__":
    main()
```
This keeps the code **clean** while still ensuring proper execution.

---

## **Final Takeaways**
✔ **Use `__name__ == "__main__"` to prevent unintended execution when importing a script.**  
✔ **Flask uses `__name__` to correctly load templates and static files.**  
✔ **Scripts run with `"__main__"`, modules run with their filename.**  
✔ **For Flask, always use `if __name__ == "__main__": app.run(debug=True)` to control execution.**
 

------

### **Differences Between RDBMS (SQL) → SQLite → SQLite3 → SQLAlchemy → Flask-SQLAlchemy**

| **Concept**                 | **What It Is**                                               |                       **Key Features**                       | **Use Case**                                              |
| --------------------------- | ------------------------------------------------------------ | :----------------------------------------------------------: | --------------------------------------------------------- |
| **RDBMS (SQL)**             | A **Relational Database Management System** that stores data in tables using SQL | Supports structured queries (SQL), relations (tables), transactions, indexing, etc. | MySQL, PostgreSQL, SQLite, Oracle, etc.                   |
| **SQLite**                  | A lightweight, file-based **SQL database engine** (subset of RDBMS) | Self-contained, serverless, zero configuration, stores database as a single `.db` file | Ideal for small-scale apps, embedded systems, mobile apps |
| **sqlite3 (Python module)** | Python’s **built-in library** for working with SQLite databases | Provides a **direct interface** to SQLite, executes SQL queries using Python | Direct SQL execution in Python scripts                    |
| **SQLAlchemy**              | A **Python ORM (Object-Relational Mapper)** for working with databases | Provides an abstraction layer over SQL, supports multiple RDBMSs (SQLite, MySQL, PostgreSQL, etc.), allows object-oriented DB operations | Large-scale applications needing DB flexibility           |
| **Flask-SQLAlchemy**        | A **Flask extension** integrating SQLAlchemy with Flask      | Simplifies SQLAlchemy setup in Flask, provides Flask-specific features like `app.config['SQLALCHEMY_DATABASE_URI']` | Web applications using Flask with a database backend      |

------

## **Detailed Explanation of Each**

### **1. RDBMS (SQL)**

- A **Relational Database Management System** that follows **SQL (Structured Query Language)** to manage data.
- Examples: **MySQL, PostgreSQL, SQLite, Oracle, SQL Server**.
- Uses **tables, rows, and columns** for structured data storage.

------

### **2. SQLite**

- A **lightweight, embedded SQL database**.
- Stores the entire database in a **single file** (`.db`).
- **No separate server** is required—everything runs in the application itself.
- Limited in concurrency (can handle multiple reads but has issues with multiple writes).

------

### **3. sqlite3 (Python Module)**

- Python’s **built-in module** for interacting with SQLite.

- Provides methods like:

  ```python
  import sqlite3
  
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  
  cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
  cursor.execute("INSERT INTO users (name) VALUES ('John Doe')")
  
  conn.commit()
  conn.close()
  ```

- **Raw SQL** is required; no ORM (Object-Relational Mapping) support.

------

### **4. SQLAlchemy (Python ORM)**

- A **powerful ORM (Object-Relational Mapper)** for Python.

- Supports multiple databases **(MySQL, PostgreSQL, SQLite, etc.)**.

- Allows database interactions using Python **classes and objects** instead of raw SQL.

- Example:

  ```python
  from sqlalchemy import create_engine, Column, Integer, String
  from sqlalchemy.orm import declarative_base, sessionmaker
  
  engine = create_engine('sqlite:///database.db')
  Base = declarative_base()
  
  class User(Base):
      __tablename__ = 'users'
      id = Column(Integer, primary_key=True)
      name = Column(String)
  
  Base.metadata.create_all(engine)
  
  Session = sessionmaker(bind=engine)
  session = Session()
  
  user = User(name="Alice")
  session.add(user)
  session.commit()
  ```

------

### **5. Flask-SQLAlchemy**

- A Flask **extension** that integrates SQLAlchemy seamlessly with Flask applications.

- **Simplifies configuration** and initialization of SQLAlchemy within Flask.

- Example:

  ```python
  from flask import Flask
  from flask_sqlalchemy import SQLAlchemy
  
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
  db = SQLAlchemy(app)
  
  class User(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(100), nullable=False)
  
  with app.app_context():
      db.create_all()
  ```

------

## **Summary**

| **Concept**                 | **Key Role**                        | **Raw SQL Required?** | **Use Case**                                     |
| --------------------------- | ----------------------------------- | --------------------- | ------------------------------------------------ |
| **RDBMS (SQL)**             | General SQL databases               | ✅ Yes                 | Large-scale applications needing structured data |
| **SQLite**                  | Lightweight embedded database       | ✅ Yes                 | Small-scale applications, mobile apps            |
| **sqlite3 (Python module)** | Direct SQLite access in Python      | ✅ Yes                 | Python scripts working with SQLite               |
| **SQLAlchemy (ORM)**        | Object-oriented database management | ❌ No                  | Large-scale applications needing DB flexibility  |
| **Flask-SQLAlchemy**        | SQLAlchemy for Flask apps           | ❌ No                  | Flask applications needing DB integration        |



### **Which One Should You Use?**

- **For small projects** → SQLite (`sqlite3` if using raw SQL, `SQLAlchemy` for ORM).
- **For Flask apps** → `Flask-SQLAlchemy` (simplifies database management in web applications).
- **For large applications** → Use `SQLAlchemy` with a full RDBMS like PostgreSQL or MySQL for scalability.

------

### **Final Thoughts**

-   **Use `sqlite3` if you only need raw SQL queries in Python.**
-   **Use `SQLAlchemy` if you want an ORM to manage database operations with Python objects.**
-   **Use `Flask-SQLAlchemy` if you're building a Flask app and need an easy way to integrate SQLAlchemy.**

### **Practical Example: Transitioning from `sqlite3` to `Flask-SQLAlchemy`**

Below, we will first create a **database using `sqlite3` (raw SQL)** and then **convert it to use Flask-SQLAlchemy (ORM approach).**

------

## **Step 1: Using `sqlite3` (Raw SQL Approach)**

This method uses direct SQL queries to create a database, insert data, and fetch results.

```python
import sqlite3

# Connect to SQLite (creates 'database.db' if not exists)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create 'users' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

# Insert data
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 30))

# Commit and close connection
conn.commit()
conn.close()

# Fetch and display data
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

print("Users from sqlite3:")
for user in users:
    print(user)

conn.close()
```

### **Problems with `sqlite3`:**

- Writing raw SQL queries manually.
- No object-oriented access to data.
- Harder to maintain as the project grows.

------

## **Step 2: Using `Flask-SQLAlchemy` (ORM Approach)**

Now, we **convert** the above SQLite logic into **Flask-SQLAlchemy** for a cleaner, object-oriented approach.

### **1️⃣ Install Flask-SQLAlchemy**

```sh
pip install flask flask-sqlalchemy
```

### **2️⃣ Convert to Flask-SQLAlchemy**

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define ORM Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Insert Data
with app.app_context():
    user1 = User(name="Alice", age=25)
    user2 = User(name="Bob", age=30)

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

# Fetch and display data
with app.app_context():
    users = User.query.all()
    print("Users from Flask-SQLAlchemy:")
    for user in users:
        print(user.id, user.name, user.age)
```

------

## **Key Differences & Benefits of Flask-SQLAlchemy**

| Feature         | `sqlite3` (Raw SQL)                                          | `Flask-SQLAlchemy` (ORM)                     |
| --------------- | ------------------------------------------------------------ | -------------------------------------------- |
| Querying        | Manual SQL statements                                        | Pythonic Object-Oriented Queries             |
| Insert Data     | `cursor.execute("INSERT INTO users VALUES (?, ?)", (name, age))` | `db.session.add(User(name="Alice", age=25))` |
| Fetch Data      | `cursor.execute("SELECT * FROM users")`                      | `User.query.all()`                           |
| Maintainability | Difficult for large apps                                     | Clean & Scalable                             |

------

## **When to Use Each?**

| **Use Case**                | **sqlite3** | **Flask-SQLAlchemy** |
| --------------------------- | ----------- | -------------------- |
| Small scripts               | ✅ Yes       | ❌ No                 |
| Flask Web Apps              | ❌ No        | ✅ Yes                |
| Large Databases             | ❌ No        | ✅ Yes                |
| Object-Oriented DB Handling | ❌ No        | ✅ Yes                |

------

### **Final Takeaway**

If you're just running a quick script, **sqlite3** works fine. But for **Flask applications, Flask-SQLAlchemy is the way to go** because it offers cleaner, more maintainable, and scalable database handling.

------

Here are all the common SQLAlchemy queries categorized by CRUD (Create, Read, Update, Delete) operations.  

---

### **1. Setting Up SQLAlchemy**

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

with app.app_context():
    db.create_all()
```

---

## **CRUD Operations in SQLAlchemy**

### **2. Create (Insert) Data**

```python
# Adding a single user
new_user = User(username="JohnDoe", email="john@example.com")
db.session.add(new_user)
db.session.commit()

# Adding multiple users
users = [
    User(username="Alice", email="alice@example.com"),
    User(username="Bob", email="bob@example.com")
]
db.session.add_all(users)
db.session.commit()
```

---

### **3. Read (Select) Data**

#### **3.1 Get all users**

```python
users = User.query.all()  
for user in users:
    print(user.username, user.email)
```

#### **3.2 Get a single user by ID**

```python
user = User.query.get(1)  # Fetches the user with id = 1
print(user.username, user.email)
```

#### **3.3 Filter users by condition**

```python
user = User.query.filter_by(username="Alice").first()  # Fetch first user with username Alice
print(user.id, user.email)

users = User.query.filter(User.email.like('%@example.com')).all()  # Fetch all users with email ending in @example.com
```

#### **3.4 Query using multiple filters**

```python
users = User.query.filter(User.username == "Alice", User.email.like("%@example.com")).all()
```

#### **3.5 Order and Limit Query Results**

```python
users = User.query.order_by(User.username.desc()).limit(5).all()  # Get the latest 5 users
```

#### **3.6 Count number of users**

```python
user_count = User.query.count()
print(user_count)
```

---

### **4. Update Data**

#### **4.1 Update a single record**

```python
user = User.query.get(1)
user.username = "JohnUpdated"
db.session.commit()
```

#### **4.2 Update multiple records**

```python
User.query.filter(User.email.like('%@example.com')).update({"email": "newemail@example.com"})
db.session.commit()
```

---

### **5. Delete Data**

#### **5.1 Delete a single user**

```python
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
```

#### **5.2 Delete multiple users**

```python
User.query.filter(User.username == "Alice").delete()
db.session.commit()
```

---
## Flask-SQLAlchemy Relationships: One-to-One, One-to-Many, and Many-to-Many

## 1. One-to-One Relationship
A **one-to-one** relationship ensures that each record in one table is linked to exactly one record in another table. This can be useful when storing additional details about a user, like a profile.

### Example:
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False, cascade="all, delete-orphan")

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
```
- Each **User** has only one **Profile**.
- `uselist=False` ensures that a single object is returned instead of a list.

---
## 2. One-to-Many Relationship
A **one-to-many** relationship is where a record in one table can be associated with multiple records in another table. For example, a **user can create multiple classes**.

### Example:
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    classes = db.relationship('Class', backref='creator', lazy=True)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```
- A **User** can create multiple **Class** entries.
- The `backref='creator'` makes it easy to access the user who created the class.

---
## 3. Many-to-Many Relationship
A **many-to-many** relationship occurs when multiple records in one table are related to multiple records in another table. This is useful when **students enroll in multiple classes**.

### Example:
```python
class_participants = db.Table('class_participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    classes = db.relationship('Class', secondary=class_participants, backref='participants')

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
```
- A **User** can enroll in multiple **Class** instances, and a **Class** can have multiple **Users**.
- The `secondary=class_participants` defines the join table for this relationship.

---
## Example Usage in Flask Routes
Adding users and enrolling them in classes:
```python
@appp.route('/enroll_user/<int:user_id>/<int:class_id>')
def enroll_user(user_id, class_id):
    user = User.query.get(user_id)
    class_instance = Class.query.get(class_id)
    
    if user and class_instance:
        class_instance.participants.append(user)
        db.session.commit()
        return f"User {user.username} enrolled in {class_instance.title}"
    return "User or Class not found"
```
- This route allows users to enroll in a class.

---
## Summary
| Relationship | Example Use Case | Implementation |
|-------------|----------------|----------------|
| **One-to-One** | User & Profile | `db.relationship(..., uselist=False)` |
| **One-to-Many** | User & Created Classes | `db.relationship(..., backref='creator')` |
| **Many-to-Many** | Students & Classes | `db.relationship(..., secondary=table_name, backref='participants')` |

This guide provides a structured approach to handling relationships in Flask-SQLAlchemy.



---

## **Advanced Queries**

### **6. Aggregate Functions**

```python
from sqlalchemy import func

# Get the number of users
user_count = db.session.query(func.count(User.id)).scalar()

# Get the maximum user ID
max_id = db.session.query(func.max(User.id)).scalar()
```

### **7. Many-to-Many Relationship Query**

```python
# Example Many-to-Many association
user = User.query.get(1)
print(user.participated_classes)  # Prints all classes the user participated in
```

---

## **8. Many-to-Many Relationship Query Using `append()`**

When dealing with a **many-to-many** relationship, we use `append()` to associate objects instead of `db.session.add()`.  

### **Example: User & Class Many-to-Many Relationship**

```python
# Association table
class_participants = db.Table('class_participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    classes = db.relationship('Class', secondary=class_participants, back_populates="participants")

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    participants = db.relationship('User', secondary=class_participants, back_populates="classes")

with app.app_context():
    db.create_all()
```

### **Adding a User to a Class**

```python
# Fetch existing user and class
user = User.query.get(1)
class = Class.query.get(1)

# Use append() to associate the user with the class
class.participants.append(user)

# Commit changes
db.session.commit()
```

### **Fetching All Classes a User Participated In**

```python
user = User.query.get(1)
for class in user.classes:
    print(class.title)
```

---

### **Key Difference Between `append()` and `db.session.add()`**

- `db.session.add()` is used to **add new objects** to the database.
- `append()` is used to **add relationships** between existing objects in a **many-to-many** or **one-to-many** relationship.

---

`and_` in SQLAlchemy is used for combining multiple conditions in a query using **logical AND**. It comes from `sqlalchemy import and_` and is especially useful when filtering with multiple conditions.

---

## **9. Using `and_` for Multiple Filters**

`and_` allows you to apply multiple filter conditions in queries.

### **Example: Using `and_` to Filter Queries**

```python
from sqlalchemy import and_

# Fetch users with username "Alice" AND email ending with "@example.com"
users = User.query.filter(and_(User.username == "Alice", User.email.like("%@example.com"))).all()

for user in users:
    print(user.username, user.email)
```

### **Alternative Without `and_`**

You can also write the same query like this:

```python
users = User.query.filter(User.username == "Alice", User.email.like("%@example.com")).all()
```

SQLAlchemy automatically treats multiple arguments in `.filter()` as an AND condition.

---

### **10. Using `or_` for OR Conditions**

For OR conditions, use `or_` instead of `and_`:

```python
from sqlalchemy import or_

# Fetch users who have username "Alice" OR email ending with "@example.com"
users = User.query.filter(or_(User.username == "Alice", User.email.like("%@example.com"))).all()
```

---

### **11. Combining `and_` and `or_`**

For complex queries, you can combine `and_` and `or_`:

```python
users = User.query.filter(and_(User.username != "Bob", or_(User.email.like("%@gmail.com"), User.email.like("%@yahoo.com")))).all()
```

This query:

- Excludes users with username `"Bob"`
- Includes users with emails ending in `"@gmail.com"` or `"@yahoo.com"`

---

### **Summary**

| Function             | Usage                                                    |
| -------------------- | -------------------------------------------------------- |
| `and_(cond1, cond2)` | Returns records that satisfy **both conditions**.        |
| `or_(cond1, cond2)`  | Returns records that satisfy **at least one condition**. |

### **Difference Between `backref` and `back_populates` in SQLAlchemy**

Both `backref` and `back_populates` are used to define **bidirectional relationships** in SQLAlchemy, but they work in slightly different ways.

------

## **1️⃣ `backref` (Automatic Back Population)**

- **Single-sided declaration** (only in one model).
- **SQLAlchemy automatically creates** the reverse relationship.
- Less explicit, but more concise.

### **Example Using `backref`**

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    classes = db.relationship('Class', backref='creator')  # Creates 'creator' in Class

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

### **How It Works?**

- In `User`, we define `classes = db.relationship('Class', backref='creator')`
- SQLAlchemy **automatically creates** `creator` in `Class`, so we can do:

```python
user = User.query.get(1)
print(user.classes)  # List of classes created by the user

classs = Class.query.get(1)
print(classs.creator)  # User who created the class (automatically available)
```

------

## **2️⃣ `back_populates` (Explicit Two-Sided Definition)**

- **Manually defined on both models.**
- Used when more control is needed.

### **Example Using `back_populates`**

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    classes = db.relationship('Class', back_populates='creator')  # Explicit

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', back_populates='classes')  # Explicit
```

### **How It Works?**

- We explicitly define the relationship **on both sides** using `back_populates`.
- This means:

```python
user = User.query.get(1)
print(user.classes)  # Works as expected

classs = Class.query.get(1)
print(classs.creator)  # Also works because of explicit back_populates
```

------

## **Key Differences:**

| Feature         | `backref`                                                    | `back_populates`                                             |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Definition**  | Defined on **one model only**                                | Defined on **both models**                                   |
| **Automatic?**  | Yes, SQLAlchemy **automatically** creates the reverse relationship | No, you must **explicitly define** both sides                |
| **Use Case**    | When you want a **quick** bidirectional relationship         | When you need **more control** over the relationship         |
| **Flexibility** | Less flexible                                                | More flexible (e.g., setting additional relationship parameters) |

------

## **When to Use What?**

- **Use `backref`** when you want **quick bidirectional access** without writing redundant code.
- **Use `back_populates`** when you need **more control** (e.g., when adding additional parameters like lazy loading or cascade behavior).

### **Can We Use `backref` in a Many-to-Many Relationship?**

Yes, we can use `backref` in a **many-to-many relationship**, but there are some nuances.

In **many-to-many relationships**, we usually define an **association table** (without an explicit model) using `db.Table`, and `backref` works in this case.

------

## **Example: Many-to-Many with `backref`**

```python
class_participants = db.Table('class_participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    classes = db.relationship('Class', secondary=class_participants, backref='participants')

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
```

### **How `backref` Works Here**

- **In `User`**: We define `classes = db.relationship('Class', secondary=class_participants, backref='participants')`
- **In `Class`**: SQLAlchemy **automatically creates** `participants`, allowing us to access users from the `Class` model.

### **Querying the Data**

```python
user = User.query.get(1)
print(user.classes)  # List of classes the user participated in

classs = Class.query.get(1)
print(classs.participants)  # List of users who participated in this class
```

------

## **What If We Use an Association Model?**

If we use an **explicit association model** (instead of `db.Table`), `backref` **cannot be used directly**. Instead, we must use **`back_populates`**.

### **Example: Many-to-Many Using an Explicit Model**

```python
class ClassParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Extra column makes it an association model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

    user = db.relationship('User', back_populates='class_associations')
    classs = db.relationship('Class', back_populates='class_associations')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    class_associations = db.relationship('ClassParticipant', back_populates='user')  # Use back_populates

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    class_associations = db.relationship('ClassParticipant', back_populates='class')  # Use back_populates
```

### **Key Differences**

| Scenario                                        | Can We Use `backref`?       | Alternative                  |
| ----------------------------------------------- | --------------------------- | ---------------------------- |
| **Using `db.Table` for Many-to-Many**           | ✅ Yes, with `secondary=...` | Works perfectly              |
| **Using an Association Model (Explicit Table)** | ❌ No                        | Use `back_populates` instead |

------

## **Conclusion**

- ✅ **Yes, `backref` can be used** in a **many-to-many relationship** **if** using `db.Table` for the association.
- ❌ If you have an **explicit association model**, use **`back_populates`** instead of `backref`.

