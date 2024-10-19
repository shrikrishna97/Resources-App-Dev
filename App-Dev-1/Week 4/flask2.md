
---

### Introduction to Flask

**Flask** is a Python framework designed for building web applications. It's known for being:
- **Small**, **lightweight**, and **simple** compared to other frameworks like Django.
- Ideal for beginners and small to medium-sized projects due to its minimal setup requirements.

### Flask Setup

To start working with Flask, you need to:
1. **Create a Project Directory**:
   - Create a new folder where you will store all your Flask projects, for example:
     ```
     Documents/python/flask
     ```
   - Change into that directory:
     ```bash
     cd Documents/python/flask
     ```

2. **Install Flask**:
   -  install Flask using pip:
     ```bash
     pip install Flask
     ```

### Testing Flask

1. **Check Flask Version**:
   - Before running your Flask application, check the installed Flask version to ensure it is 2.0 or higher:
     ```bash
     flask --version
     ```
   - If Flask is not installed or is an older version, install or upgrade Flask using:
     ```bash
     pip install --upgrade Flask
     ```

2. **Create a Simple Flask App**:
   - Create a file named `hello.py` in your project directory and copy the following code:
     ```python
     from flask import Flask
     app = Flask(__name__)
     
     @app.route('/')
     def hello():
         return 'Hello World!'
     ```

3. **Run the Flask App**:
   - At the command prompt, run the following commands:

     - **Mac OS**:
       ```bash
       export FLASK_APP=hello.py
       flask run
       ```

     - **PowerShell**:
       ```powershell
       $env:FLASK_APP = "hello.py"
       flask run
       ```

     - **Command Prompt (CMD)**:
       ```cmd
       set FLASK_APP=hello.py
       flask run
       ```

   - **Using the `--app` Option**:
     - You can also run your app using the `--app` option, which is particularly useful for Flask versions 2.2 and later:
       ```bash
       flask --app hello.py run --debug
       ```
     - The `--debug` flag enables the debug mode, which provides detailed error messages and automatically reloads the server when code changes are made. This is especially helpful during development.

4. **View the Web App**:
   - Open a browser and navigate to `http://localhost:5000`. You should see `Hello World!` displayed on the screen.
   - If you encounter a port conflict, try running the server on a different port:
     ```bash
     flask run --port 4999
     ```
   - Then, visit `http://localhost:4999`.

5. **Stopping the Server**:
   - To shut down the server, press `Control+C` in the terminal.

### Understanding Flask Code

1. **Importing Flask**:
   - The `Flask` class is imported from the `flask` library, and an instance of this class represents your web application:
     ```python
     from flask import Flask
     app = Flask(__name__)
     ```
   - `app = Flask(__name__)` creates an application object using the current Python module. This object handles all the operations of the web app.

2. **Creating Routes**:
   - A **route** in Flask determines how URLs are handled by the application. It is defined using a decorator:
     ```python
     @app.route('/')
     def hello():
         return 'Hello World!'
     ```
   - The **decorator** `@app.route('/')` tells Flask that the function `hello()` should be called when the home page (`/`) is accessed.
   - The `hello()` function returns the string `'Hello World!'`, which is then displayed in the browser.

3. **Adding Additional Routes**:
   - You can add multiple routes to a Flask app. For example:
     ```python
     @app.route('/foobar')
     def foobar():
         return '<h1>Hi there, foobar!</h1>'
     ```
   - After adding this, running the server and navigating to `http://localhost:5000/foobar` will display `Hi there, foobar!` in the browser.

<b>The ` __name__ ` Variable </b>

- In Python, `__name__` is a special built-in variable that represents the name of the current module. 
- When a Python script is run directly, the `__name__` variable is set to `"__main__"`. 
- When a script is imported as a module in another script, `__name__` is set to the name of that module.

### Using 
```python 
if __name__ == "__main__":
```

- This construct is used to determine if a script is being run directly or being imported:
  ```python
  if __name__ == "__main__":
      app.run()
  ```
- If the script is executed directly, the code inside this block will run (like starting the Flask application).
- If the script is imported into another module, the code inside this block will not run. This is useful for writing code that should only execute when the file is run as the main program, such as starting a web server or executing test cases.

### Key Concepts Recap

- **Flask Application Object**: Created with `app = Flask(__name__)`, it brings in all the capabilities of the Flask framework.
- **Routes**: Determine which URLs are handled by which functions. Defined using the `@app.route()` decorator.
- **Functions in Flask**: Define the actions to be taken when a specific URL is accessed.
- **Development Server**: Flask includes a built-in server that is useful for testing but should not be used in a production environment.

---
