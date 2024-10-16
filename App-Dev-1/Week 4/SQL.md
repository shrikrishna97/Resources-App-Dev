

### Database Concepts

1. **Persistent Storage**:
   - Refers to storing data in a way that persists beyond the runtime of a program.
   - Example: Gradebook, storing details like students' names, IDs, and courses.
   - **Need for Persistence**: Ensures that data is not lost when a server is restarted or a program ends.

2. **Spreadsheets vs. Databases**:
   - **Spreadsheets**:
     - Organize data in rows and columns.
     - Good for small-scale data management.
     - Not suitable for complex relationships and large datasets.
     - Lookups and relationships are harder to manage.
   - **Relational Databases (SQL)**:
     - Store data in tables with rows (records) and columns (fields).
     - Efficient for complex queries using SQL (Structured Query Language).
     - Examples include MySQL, PostgreSQL, SQLite.
     - Concepts like **primary keys** (unique identifiers for records) and **foreign keys** (linking tables) manage relationships between data.

3. **Data Relationships**:

Three most used data relationships:
   - **One-to-One**: A unique relationship between two entities (e.g., a student and a unique ID).
   - **One-to-Many**: One entity can relate to multiple instances of another entity (e.g., one hostel with multiple students).
   - **Many-to-Many**: Both entities can relate to multiple instances of each other (e.g., students and courses).

4. **SQL Basics**:
   - **SQL Queries**: Used to interact with databases.
   - Common operations:
     - `SELECT`: Retrieve data.
     - `INNER JOIN` and `OUTER JOIN`: Combine rows from multiple tables based on related columns.
   - Example:
     ```sql
     SELECT Students.name, Hostels.name 
     FROM Students 
     INNER JOIN Hostels 
     ON Students.hostelID = Hostels.ID;
     ```
     This query retrieves student names alongside their hostels.

5. **NoSQL Databases**:
   - More flexible than relational databases, allowing for unstructured data.
   - Examples include **MongoDB** and **CouchDB**.
   - Suitable for dynamic schema or hierarchical data storage.

### Flask Basics

1. **Introduction to Flask**:
   - A micro web framework for Python, designed for simplicity.
   - Useful for building small to medium-sized web applications.
   - Requires minimal setup compared to larger frameworks like Django.

2. **Core Concepts in Flask**:
   - **Routes**: Define URL endpoints and how they are handled.
     - Example:
       ```python
       @app.route('/hello')
       def hello():
           return "Hello, World!"
       ```
   - **Templates**: Allow dynamic HTML generation using Jinja2.
     - Example:
       ```html
       <h1>Hello, {{ name }}!</h1>
       ```
       This dynamically displays a name passed from the Flask view.

3. **Database Integration with Flask**:
   - **Flask-SQLAlchemy**: An ORM (Object Relational Mapper) for integrating SQL databases with Flask.
     - Simplifies interaction with databases by using Python classes instead of SQL commands.
     - Example:
       ```python
       from flask_sqlalchemy import SQLAlchemy
       db = SQLAlchemy(app)
       
       class User(db.Model):
           id = db.Column(db.Integer, primary_key=True)
           name = db.Column(db.String(100))
       ```
   - **NoSQL with Flask**: Libraries like PyMongo allow MongoDB integration with Flask.

4. **Data Persistence in Flask**:
   - Persistent storage allows data to survive across multiple sessions and server restarts.
   - Can be managed using databases or file-based storage like CSV or JSON for simpler applications.

5. **RESTful APIs with Flask**:
   - Flask is often used to create APIs for CRUD operations (Create, Read, Update, Delete).
   - Example of a simple API route for adding a user:
     ```python
     @app.route('/add_user', methods=['POST'])
     def add_user():
         data = request.json
         new_user = User(name=data['name'])
         db.session.add(new_user)
         db.session.commit()
         return {"message": "User added successfully!"}
     ```

### Summary
- **Relational databases** (SQL) are best for structured data with complex relationships.
- **NoSQL databases** are more flexible but can sacrifice strict data validation.
- **Flask** is a lightweight framework ideal for building web apps and APIs.
- Integrating databases with Flask allows for dynamic web applications and persistent data storage.

This should provide a good understanding of the concepts around databases and using Flask for web development!