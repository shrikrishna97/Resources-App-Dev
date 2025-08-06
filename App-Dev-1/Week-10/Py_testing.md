---

### **Session Objective**

To explore the essential features of Pytest in Python including fixtures, markers, parameterization, and organizing reusable code using `conftest.py`. By the end, students will understand how to write clear and maintainable tests using idiomatic Pytest practices.

---

#### **Introduction to Pytest**

* Pytest is a testing framework that makes it easy to write simple and scalable test code.
* Install: `pip install pytest`
* Test file format: `test_*.py` or `*_test.py`
* Test function naming: must start with `test_`

**Example:**

```python
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4
```

Run using: `pytest file.py`

---

#### **Fixtures**

Fixtures are functions that run before (and sometimes after) tests. They help set up test context.

**Analogy:** Think of a fixture like a butler who sets your table before every meal (test).

**Basic Fixture:**

```python
import pytest

@pytest.fixture
def sample_list():
    return [1, 2, 3]

def test_sum(sample_list):
    assert sum(sample_list) == 6
```
Run using: `pytest file.py`

**Scope:**

* `function` (default): New fixture for each test.
* `module`, `class`, `session`: Controls how often the fixture is run.

```python
@pytest.fixture(scope="module")
def connect_db():
    print("Connecting once for module")
    yield "db_connection"
    print("Disconnecting after module")
```

---

#### **Parameterization**

Allows you to run the same test with different inputs.

**Example:**

```python
import pytest

@pytest.mark.parametrize("a,b,result", [(1, 2, 3), (3, 4, 7), (5, 5, 10)])
def test_addition(a, b, result):
    assert a + b == result
```

**Analogy:** Like giving a quiz to multiple students with the same question but different answers.

---

#### **Skipping & Expected Failures**

```python
import pytest

@pytest.mark.skip(reason="Work in progress")
def test_login():
    assert False

@pytest.mark.xfail(reason="Bug #101")
def test_feature():
    assert 1 == 2
```

**Usage:**

* `@pytest.mark.skip`: Skip a test
* `@pytest.mark.xfail`: Expect it to fail (without breaking suite)

---

#### **Grouping with Markers & Filtering**

Markers allow grouping tests and selectively running them.

**Custom Marker:**

```python
import pytest

@pytest.mark.slow
def test_large_data():
    assert True
```

Run only slow tests: `pytest -m slow`

You can also use keyword filters:

```bash
pytest -k "addition"
```

---

#### **Shared Fixtures with conftest.py**

**Why?** To avoid duplicating fixtures across test files.

**Analogy:** Like placing shared utensils in a kitchen drawer (`conftest.py`) instead of repeating them at every table.

**Structure:**

```
project/
├── tests/
│   ├── test_math.py
│   ├── test_string.py
│   └── conftest.py
```

**conftest.py:**

```python
import pytest

@pytest.fixture
def fruit_basket():
    return ["apple", "banana", "cherry"]
```

**test\_math.py:**

```python
def test_banana_in_basket(fruit_basket):
    assert "banana" in fruit_basket
```

* Pytest automatically looks for fixtures in `conftest.py`
* No need to import `fruit_basket` manually


---



### **Post-Session Practice Resources**

* [https://docs.pytest.org](https://docs.pytest.org)
* [https://www.tutorialspoint.com/pytest/index.htm](https://www.tutorialspoint.com/pytest/index.htm)
* [https://realpython.com/pytest-python-testing/](https://realpython.com/pytest-python-testing/)

---

### **Unit Testing in Flask Using Pytest**

Unit testing is a core practice in Flask application development, allowing you to validate individual parts (units) of your application to ensure they behave as expected. `pytest` is a popular Python testing framework that works seamlessly with Flask.

---

### 1. **Setting Up the Project**

Make sure you have Flask and pytest installed:

```bash
pip install Flask pytest
```

**Project Structure:**

```
myapp/
├── app.py
├── test_app.py
```

---

### 2. **Minimal Flask App to Test**

#### app.py

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'This is the about page.'

@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'
```

---

### 3. **Writing Tests with Pytest**

#### test\_app.py

```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, World!' in response.data

def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'This is the about page.' in response.data

def test_greet(client):
    response = client.get('/greet/Alice')
    assert response.status_code == 200
    assert b'Hello, Alice!' in response.data
```

---

### 4. **Key Concepts Explained with Code**

####  Using `test_` Prefix

* All test functions must start with `test_` for pytest to detect them.

####  Using Fixtures

* The `client()` fixture provides a fresh Flask test client for every test, which simulates browser-like behavior.

####  Testing Routes

* `client.get('/some-url')` simulates a GET request.
* Use `assert` to check status codes and response content.

####  Byte Strings

* Flask’s `response.data` is in bytes, so compare using `b'Text'`.

---

### 5. **Running the Tests**

Navigate to the directory containing `test_app.py` and run:

```bash
pytest
```

You’ll see output like:

```
================== test session starts ==================
collected 3 items

test_app.py ...                                        [100%]

=================== 3 passed in 0.20s ===================
```

---

### 6. **Tips**

* Group related tests in classes using `class TestViews:` or `class TestAuth:`
* Use separate files like `test_models.py`, `test_forms.py`, etc. for modularity.
* Use temporary databases and mock data for more complex tests.

---

### Summary

* Minimal setup: Flask + Pytest
* Use `test_` prefix for all test functions
* Simulate requests using `client.get()` / `client.post()`
* Validate response with `assert`


---

### **Bonus Reference Table: Testing Types and Focus Areas**

| **Test Type**             | **Focus Area**                                         |
| ------------------------- | ------------------------------------------------------ |
| Unit Testing              | Smallest logical units (functions/methods)             |
| Integration Testing       | Multiple components/modules working together           |
| System Testing            | Whole app in full environment including server         |
| System Testing Automation | Simulated end-user browser-based interaction           |
| User Acceptance Testing   | Real-world verification by actual users before release |

---


