# Revision Week 1 - 4

---

### **Week 1: Basics of Web**

**Content:**
- **Apps in General**
- **Types of Apps/Platforms**
- **Components of an App**
- **Web Architectures**
  - Client-Server
- **Design Patterns**
  - MVC (Model-View-Controller)

**Things to Know:**
1. **[What are Protocols?](https://www.youtube.com/watch?v=gPrRv4Fh04U&list=PLZ2ps__7DhBZGVuyXs2l3KJtiHs0KMVE7&t=16s)**
2. **[HTTP/HTTP Verbs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)**
3. **Request/Response Mechanism**
4. **[What is curl and how to make a curl request?](https://curl.se/docs/httpscripting.html)**
5. **[Performance Parameters](https://www.youtube.com/watch?v=kJ9QYXs8jtE&list=PLZ2ps__7DhBYpzo7wVqvvV9OZulyGZVjA)**
   - Latency
   - Bandwidth
   - Round Trip Time

---

### **Week 2: Basics of HTML and CSS**

**Content:**
- **Information Representation**
- **Efficiency in Web Development**
- **Markups and Its Types:** HTML
- **Basic DOM (Document Object Model)**
- **Styling and Aesthetics:** CSS
- **Responsive Design**

**Things to Know:**
1. **[Basics of Number Systems](https://www.youtube.com/watch?v=zDHXpOZxaYs&t=6047s)**
   - Binary
   - Octal
   - Decimal
   - Hexadecimal
2. **[Unicode to UTF-8 Conversion](https://www.youtube.com/watch?v=evaJCiwmFeg&list=PLZ2ps__7DhBaavCDmD5YWSo9QnY_mpTpY&t=4573s)**
3. **[HTML Tags](https://www.youtube.com/live/oJhPmB5waEg?feature=shared&t=420)**
4. **CSS: Inline, Internal, External**
5. **Developer Tools**

---

### **Week 3: Presentation Layer: View**

**Content:**
- **User Interface vs. User Interaction**
- **Types of Views**
- **User Interface Design:** Aesthetics, Accessibility
- **Jakob Nielsen’s Heuristics**

**Things to Know:**
1. **Template Creation Using:**
   - [PyHTML](https://www.youtube.com/watch?v=SbVDz1P4AMg&list=PLZ2ps__7DhBZGVuyXs2l3KJtiHs0KMVE7&t=18s)
   - [Python String Module](https://www.youtube.com/watch?v=SbVDz1P4AMg&list=PLZ2ps__7DhBZGVuyXs2l3KJtiHs0KMVE7&t=832s)
   - [Jinja2](https://www.youtube.com/watch?v=SbVDz1P4AMg&list=PLZ2ps__7DhBZGVuyXs2l3KJtiHs0KMVE7&t=925s)
2. **[Template Designer Documentation](https://jinja.palletsprojects.com/en/stable/templates/)**
3. **[Jinja Filters](https://jinja.palletsprojects.com/en/stable/templates/#filters)**
4. **Template Inheritance**

---

### **Week 4: Database Layer: Model**

**Content:**
- **Persistent Storage**
- **Mechanisms for Persistent Storage**
- **Relational Databases (SQL) vs. Unstructured Databases (NoSQL)**
- **Relationships and Their Types**
- **Entity-Relationship (ER) Diagrams**

**Things to Know:**
1. **Basic SQL Queries**
2. **Setting Up SQLite Database**
3. **ER Diagrams**
4. **[Basic Wildcards in SQL](https://learn.microsoft.com/en-us/previous-versions/troubleshoot/visualstudio/foxpro/use-wildcard-characters-sql-statement)**
5. **Object-Relational Mappings (ORMs)**

---

### **Bonus: Basics of Flask Application and GET/POST Methods**

**Content:**
- **Introduction to Flask:** A micro web framework for Python
- **Setting Up a Basic Flask Application**
- **Creating Routes**
  - **GET Method**: Used to retrieve data from the server.
  - **POST Method**: Used to send data to the server for creating or updating resources.
- **Flask Application Structure**
- **Handling Forms with Flask**

**Example Code:**

```python
from flask import Flask, request

app = Flask(__name__)

# GET Method Example
@app.route('/hello', methods=['GET','POST'])
def hello():
    return "Hello, World!"

# POST Method Example
@app.route('/submit', methods=['POST'])
def submit_data():
    if request.method == 'POST':
    	data = request.form['data']
    	return f"Data received: {data}"

if __name__ == '__main__':
    app.run(debug=True)
```

---

