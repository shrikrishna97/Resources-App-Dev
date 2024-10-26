# Revision Notes Quiz-1

#### 1. **Size = characters × bits required to store each character**
#### 2. **ASCII (7-bit old)**
   - **7-bit ASCII** example: The character `'A'` is represented by **65** in decimal (binary: `1000001`).
#### 3. **ASCII (8-bit new)**

#### 4. **UCS (8 bits)**

#### 5. **UCS-2 (2 bytes, i.e., 16 bits)**

#### 6. **UCS-4 (4 bytes)**

#### 7. **UTF-8 (8 bits)**

#### 8. **Bandwidth = no of requests × size of request**
#### 9. **Unit Balancing:**
   - **Mbps to MBps** conversion:
   ```js
   let Mbps = 100; // Megabits per second
   let timeInSeconds = 10;
   let totalDataInMegabits = Mbps * timeInSeconds; // Total data in Mb
   let totalDataInMegabytes = totalDataInMegabits / 8;  // Convert to MB
   console.log(`Total data transferred: ${totalDataInMegabytes} MB`);
   ```

   - **Speed = distance / time**:
   ```js
   let distance = 100; // meters
   let time = 10; // seconds
   let speed = distance / time;
   console.log(`Speed: ${speed} m/s`);  // Output: 10 m/s
   ```

#### 10. **Styling:**
   - **Inline CSS:**
   ```html
   <p style="color: red;">This is red text</p>
   ```

   - **Internal CSS:**
   ```html
   <style>
     p { color: blue; }
   </style>
   <p>This is blue text</p>
   ```

   - **External CSS:** (Linking to an external stylesheet)
   ```html
   <link rel="stylesheet" href="styles.css">
   ```

#### 11. **Selectors:**
   - **ID selector:**
   ```html
   <style>
     #myDiv { color: red; }
   </style>
   <div id="myDiv">This is red text</div>
   ```

   - **Class selector:**
   ```html
   <style>
     .myClass { color: green; }
   </style>
   <div class="myClass">This is green text</div>
   ```

#### 12. **String:**
   - **Substitute:**
   ```python
   from string import Template
   t = Template('Hello, $name!')
   print(t.substitute(name='Ravi'))  # Output: Hello, Ravi!
   ```

   - **Safe substitute** (to avoid errors with missing variables):
   ```python
   print(t.safe_substitute())  # Output: Hello, $name!
   ```

#### 13. **Jinja (Template Rendering):**
   ```python
   from jinja2 import Template
   template = Template('Hello {{ name }}!')
   print(template.render(name='Ravi'))  # Output: Hello Ravi!
   ```

#### 14. **Display:**
   - **Inline:**
   ```html
   <span style="background-color: yellow;">Text 1</span>
   <span style="background-color: green;">Text 2</span>
   ```

   - **Block:**
   ```html
   <div style="background-color: yellow;">Block 1</div>
   <div style="background-color: green;">Block 2</div>
   ```

   - **Inline-block:**
   ```html
   <div style="display: inline-block; background-color: yellow;">Block 1</div>
   <div style="display: inline-block; background-color: green;">Block 2</div>
   ```

#### 15. **MVC (Model-View-Controller):**
   - **Model** (Handles data, typically interacting with a database):
   ```python
   class UserModel:
       def __init__(self, name, age):
           self.name = name
           self.age = age
   ```

   - **View** (Renders data to the user):
   ```html
   <p>User Name: {{ user.name }}</p>
   <p>User Age: {{ user.age }}</p>
   ```

   - **Controller** (Handles logic and interacts with the model):
   ```python
   def get_user():
       user = UserModel('Ravi', 25)
       return render_template('user_view.html', user=user)
   ```

#### 16. **Response:**
   - **Response header and body using `curl`:**
   ```bash
   curl -I https://www.google.com  # Fetches only the headers
   ```
   - **GET request (retrieves header and body):**
   ```bash
   curl https://jsonplaceholder.typicode.com/posts/1
   ```

#### 17. **GET/HEAD:**
   - **GET request example:**
   ```bash
   curl -X GET https://api.example.com/data
   ```

   - **HEAD request (fetches header without body):**
   ```bash
   curl -I https://api.example.com/data
   ```

#### 18. **curl -X (method) URL (sending request)**
   - **Example POST request with data:**
   ```bash
   curl -X POST https://api.example.com/users -d '{"name":"Ravi"}' -H "Content-Type: application/json"
   ```

#### 19. **python -m http.server**
   - **Start a simple HTTP server to serve files:**
   ```bash
   python -m http.server 8000
   ```
   - After running this command, visit `http://localhost:8000` in your browser to view the served files.

#### 20. **HTTP Status Codes:**
   - **Common Status Codes:**
   - **200 OK**
   - **400 Bad Request**
   - **404 Not Found**
   -  **1xx informational response** – the request was received, continuing process
   - **2xx successful** – the request was successfully received, understood, and
     accepted
   - **3xx redirection** – further action needs to be taken in order to complete the
     request
   - **4xx client error** – the request contains bad syntax or cannot be fulfilled
   -  **5xx server error** – the server failed to fulfil an apparently valid request

[HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
       

**SQL Extra resource:** https://subenduonlinedegre.github.io/DBMS-WIKI/ 