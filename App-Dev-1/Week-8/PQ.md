##### Q1. A server has a 16-core CPU, 64 GB RAM and 1 Gbps network connection. It can run a Python Flask application that can generate 500 HTML pages per second. Each page also has a 1 MB image that needs to be downloaded by the client. What will be the maximum number of requests per second that the server can handle?

---
##### Solution:

To find the maximum number of requests per second the server can handle, we need to evaluate the constraints imposed by the CPU, memory, and network bandwidth. Given the details:

1. **Server Specifications**:
   - **CPU**: 16-core
   - **RAM**: 64 GB (not likely to be a bottleneck in this scenario)
   - **Network**: 1 Gbps connection

2. **Application Performance**:
   - Can generate **500 HTML pages per second**.
   - Each page includes a **1 MB image** that the client downloads.

###### Step-by-step Analysis:

1. **CPU Capacity**:
   - The CPU can handle generating **500 HTML pages per second**, so CPU is not the bottleneck in this calculation.

2. **Method 1: Direct Conversion to MBps**:
   
   - **Network Bandwidth**:
     ```math
     1 \text{ Gbps} = \frac{1 \times 10^9 \text{ bits per second}}{8 \text{ bits per byte}} = 125 \text{ MBps}
     ```
     
   - **Network Requirement per Request**:
    ```math
     \frac{125 \text{ MBps}}{1 \text{ MB/request}} = 125 \text{ requests per second}
    ```
     
     
   
3. **Method 2: Using Mbps and Mb**:
   
   - **Network Bandwidth**:
    ```math 
     1 \text{ Gbps} = 1000 \text{ Mbps}
    ```
     
   - **Network Requirement per Request**:
     - Each request includes a 1 MB image, which is equal to **8 Mb** (megabits).
    ```math
       \frac{1000 \text{ Mbps}}{8 \text{ Mb/request}} = 125 \text{ requests per second}
     ```
       

###### Conclusion:
Both methods show that the **maximum number of requests per second** that the server can handle, based on the network constraint, is **125** requests per second. This is because the network bandwidth limits the number of 1 MB images that can be transferred per second, even though the CPU can generate more HTML pages.

---

#####  Q2. Asynchronous updates refer to: 
 1. loading part of a page in the background.
 2. operating without a system clock.
 3. using asynchronous circuit design for the processor in the data center.
 4. having separate files for HTML, CSS and JavaScript

##### Answer: 

The correct answer is:

**1. loading part of a page in the background.**

###### Explanation:
Asynchronous updates typically refer to web technologies like **AJAX (Asynchronous JavaScript and XML)**, where parts of a web page can be updated without reloading the whole page. This allows for a smoother user experience by loading data in the background and displaying it when ready. 

learn more: [AJAX W3School](https://www.w3schools.com/xml/ajax_intro.asp)

The other options are unrelated:
- **2. operating without a system clock** refers to asynchronous circuit design but not related to web page updates.
- **3. using asynchronous circuit design for the processor in the data center** relates to hardware design, not web updates.
- **4. having separate files for HTML, CSS and JavaScript** is a common practice in web development but does not relate to asynchronous updates.


##### One example of asynchronous updates:

Here's a simple example of how asynchronous updates can be implemented using **AJAX** in a web application to load data in the background without reloading the entire page:

**HTML, JavaScript and XML code**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asynchronous Update Example</title>
</head>
<body>
    <h1>Asynchronous Data Load</h1>
    <button onclick="loadData()">Load Data</button>
    <div id="dataContainer"></div>

    <script>
        function loadData() {
            const xhr = new XMLHttpRequest();
            xhr.open("GET", "https://jsonplaceholder.typicode.com/posts/1", true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    document.getElementById("dataContainer").innerHTML = xhr.responseText;
                }
            };
            xhr.send();
        }
    </script>
</body>
</html>
```

###### Explanation:
- **Button**: The `<button>` element triggers the `loadData()` function when clicked.
- **AJAX Request**: The `XMLHttpRequest` object is used to send an HTTP GET request to a placeholder API (`https://jsonplaceholder.typicode.com/posts/1`).
- **Asynchronous Loading**: The data is fetched asynchronously and displayed inside the `dataContainer` `<div>` when the request is successful.

**Output**:
When the button is clicked, the browser fetches the data in the background and displays it without reloading the page.

##### What is XMLHttpRequest ?

**`XMLHttpRequest` (XHR)** is an API in web development that allows a client (usually a web browser) to interact with a server and exchange data asynchronously. It is primarily used for making HTTP or HTTPS requests to a server without refreshing the entire web page. This is key for creating a dynamic user experience, as it enables parts of a web page to be updated without a full page reload.

###### Key Features of `XMLHttpRequest`:
- **Asynchronous Communication**: XHR allows data to be sent or retrieved in the background, so the user can continue interacting with the web page without interruption.
- **Flexible Data Formats**: You can send and receive data in various formats, including **text**, **XML**, **JSON**, and **HTML**.
- **HTTP Methods**: It supports HTTP methods such as `GET`, `POST`, `PUT`, `DELETE`, etc.

###### Basic Workflow:
1. **Create an instance** of `XMLHttpRequest`.
2. **Initialize a request** using `open()` method, specifying the HTTP method and URL.
3. **Set up a callback function** to handle the response when the request completes.
4. **Send the request** using the `send()` method.
5. **Process the response** when the `onreadystatechange` or `onload` event fires.

###### Example Code:
```javascript
// Create a new XMLHttpRequest object
var xhr = new XMLHttpRequest();

// Configure it: GET-request for the URL /data
xhr.open('GET', '/data', true);

// Set up a function to handle the response
xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        // Successful response; process the data
        console.log(xhr.responseText);
    }
};

// Send the request
xhr.send();
```

###### Explanation of `readyState`:
- **0**: `UNSENT` – The request has not been initialized.
- **1**: `OPENED` – The `open()` method has been called.
- **2**: `HEADERS_RECEIVED` – The request has been sent, and the headers and status are available.
- **3**: `LOADING` – The response body is being received.
- **4**: `DONE` – The operation is complete.

###### Common Uses:
- Loading new data for a section of a web page (e.g., updating user comments, loading search results).
- Sending form data to a server without reloading the page.
- Implementing auto-refresh features or polling data from a server.

**Note**: Modern web development often uses `Fetch API` or libraries like **Axios** for making HTTP requests, as they provide a more concise and powerful syntax compared to `XMLHttpRequest`.

---

##### Q3. DOM in the context of the web refers to:

document object model

document oriented meetings

data object mechanism

driver optional mode

##### Answer: 

In the context of the web, **DOM** refers to the **Document Object Model**. 

It is a programming interface for web documents, representing the structure of the document as a tree of nodes, where each node corresponds to a part of the document (such as an element or attribute). This allows programming languages like JavaScript to interact with and manipulate the structure, style, and content of web pages.

---

The **Document Object Model (DOM)** is a structured representation of a web page or document. Below are its key components:

###### 1. **Tree**
   - The DOM is structured as a **tree** of nodes. This hierarchical structure represents the page's content. The tree starts with a single **root node** and branches out to various other nodes, each representing elements, text, or attributes in the document.
   - At the top of this tree is the **document node**, which represents the entire HTML or XML document.
   - **Example**:  
     The HTML:
     ```html
     <html>
       <body>
         <div id="container">
           <p>Hello World!</p>
         </div>
       </body>
     </html>
     ```
     The DOM tree structure:
     ```
     Document
       ├── html
       │    └── body
       │         └── div (id="container")
       │              └── p (Text: "Hello World!")
     ```

###### 2. **Node**
   - A **node** is a single point in the DOM tree. There are different types of nodes, such as:
     - **Element nodes**: Represent HTML or XML elements (e.g., `<div>`, `<p>`, `<h1>`).
     - **Text nodes**: Represent the text within elements (e.g., the text inside a `<p>` tag).
     - **Attribute nodes**: Represent the attributes of elements (e.g., `class`, `id` in HTML).
     - **Comment nodes**: Represent comments within the document (e.g., `<!-- This is a comment -->`).
   - **Example**:  
     For the HTML:
     ```html
     <p>Hello World!</p>
     ```
     The `<p>` tag is an **element node** and the text `"Hello World!"` inside the `<p>` tag is a **text node**.

###### 3. **Element**
   - **Element nodes** are the building blocks of an HTML document, representing the HTML tags such as `<div>`, `<span>`, `<ul>`, etc.
   - Elements can contain other elements, text, or both. These are the actual content holders and can have attributes associated with them (like `class`, `id`, `style`, etc.).
   - **Example**:  
     In this HTML:
     ```html
     <div class="box">This is a box.</div>
     ```
     The `<div>` is an **element node**, and it has a `class` attribute. The `div` element can also contain text inside it ("This is a box.").

###### 4. **Attribute**
   - **Attributes** provide additional information about an element. They are usually name-value pairs. For example, in `<img src="image.jpg" alt="An image">`, `src` and `alt` are attributes of the `img` element.
   - In the DOM, attributes are considered as **attribute nodes** associated with their corresponding element nodes.
   - **Example**:  
     In the HTML:
     ```html
     <img src="image.jpg" alt="A beautiful image" />
     ```
     The `src` and `alt` are **attribute nodes** of the `img` element. The `src` attribute specifies the image file, and the `alt` attribute provides alternative text.

###### 5. **Text**
   - **Text nodes** contain the actual text inside an element. For example, in `<p>Hello, world!</p>`, the text node would be "Hello, world!".
   - Text nodes cannot contain HTML tags; they are simply the raw content within an element.
   - **Example**:  
     In this HTML:
     ```html
     <h1>Welcome to my website</h1>
     ```
     The **text node** is `"Welcome to my website"`, which is inside the `<h1>` element.

###### 6. **Event**
   - **Events** in the DOM are actions or occurrences that happen in the browser, often as a result of user interactions, such as clicks, key presses, mouse movements, etc.
   - Events are handled by event listeners, which are functions that are invoked when a specific event occurs. For example, `click`, `load`, `mouseover`, etc.
   - Events can be used to trigger actions on the page, like showing a popup, changing content, or submitting a form.
   - **Example** (Click Event):
     ```html
     <button id="myButton">Click Me!</button>
     <script>
       document.getElementById('myButton').addEventListener('click', function() {
         alert('Button clicked!');
       });
     </script>
     ```
     When the button is clicked, an event listener triggers the function, showing the alert "Button clicked!".

###### 7. **Document**
   - The **document node** represents the entire web page or document in the DOM. It's the entry point to access any part of the page via JavaScript.
   - It is the parent of all other nodes and serves as the root node from which everything else can be accessed. The `document` object in JavaScript allows you to query and modify the content of the page.
   - **Example**:
     ```javascript
     console.log(document.title);  // Prints the title of the current HTML document
     console.log(document.body);   // Prints the <body> element
     ```

###### 8. **Parent, Child, and Sibling Nodes**
   - **Parent node**: A node that contains other nodes. For example, in `<div><p>Hello</p></div>`, the `div` is the parent node of the `p` node.
   - **Child nodes**: Nodes that are contained within another node. The `p` node in the example above is a child of the `div` node.
   - **Sibling nodes**: Nodes that share the same parent. For example, if there were another `<p>` inside the `div`, both `p` nodes would be siblings.
   - **Example**:
     ```html
     <div>
       <p>First Paragraph</p>
       <p>Second Paragraph</p>
     </div>
     ```
     - The `div` is the **parent node** of the two `p` elements.
     - The two `p` elements are **child nodes** of the `div`.
     - The two `p` elements are **siblings** to each other.

###### 9. **Document Fragment**
   - A **document fragment** is a lightweight, in-memory tree of nodes that can be used to build up content without affecting the main DOM until it’s ready. This is useful for batch updates to the DOM as it reduces reflow and repainting costs.
   - **Example**:
     ```javascript
     var fragment = document.createDocumentFragment();
     var div = document.createElement('div');
     div.textContent = 'This is a new div element!';
     fragment.appendChild(div);
     document.body.appendChild(fragment);  // Adds the div to the body
     ```
     In this example, a new `div` element is added to a document fragment first, and then the fragment is appended to the body in one operation. This prevents multiple reflows and repaints.

###### 10. **DOM Manipulation**
   - DOM manipulation refers to the process of dynamically changing the content and structure of a web page by interacting with the DOM nodes using JavaScript methods like `createElement()`, `appendChild()`, `removeChild()`, `setAttribute()`, etc.
   - **Example**:
     ```html
     <div id="demo">Hello World</div>
     <script>
       document.getElementById('demo').textContent = 'Hello JavaScript';  // Modify text content
     </script>
     ```
     The text inside the `div` is changed from "Hello World" to "Hello JavaScript" using JavaScript to manipulate the DOM.

More information can be found in the [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model).

---

These components together form the DOM's core structure, enabling the web page to be programmatically accessed, modified, and interacted with by developers.

---

##### Q4. Using JavaScript for updating the DOM will generally

increase load on the server.

increase load on the client.

increase load on the network.

decrease load on the client

##### Answer:
The correct answer is:

**increase load on the client.**

Using JavaScript to update the DOM typically happens in the user's browser (the client side), so it increases the load on the client rather than the server or the network. The server and network are generally not affected by these DOM manipulations, unless new data is being fetched from the server using AJAX or similar methods.

---

##### Q5. DOM updates can be used to

add text to the page.

remove text from the page.

add new entries to the database.

all of the above

##### Answer:

The correct answer is:

**add text to the page.**

**remove text from the page.**

DOM updates can be used to add or remove text on the page (through manipulating elements and text nodes). However, DOM updates **cannot** directly interact with the database. To add new entries to a database, a server-side operation (such as an API request) is needed in addition to DOM manipulation. Therefore, "all of the above" is not the correct answer.

---

##### Q6. Which of the following is most secure?

static HTML web page

PHP script on server

JS with native mode access

JS with only basic API access

##### Answer:

The most secure option is:

**static HTML web page**

###### Explanation:
- **Static HTML web page**: This is the most secure option because it is a simple, non-interactive page that does not rely on dynamic content generation or user input processing. It doesn’t include server-side or client-side scripting that could introduce vulnerabilities.
  
- **PHP script on server**: While PHP scripts on the server can be secure if written properly, they can also be vulnerable to issues like SQL injection, cross-site scripting (XSS), and cross-site request forgery (CSRF) if not properly handled.

- **JS with native mode access**: JavaScript with native mode access typically refers to JavaScript interacting directly with the browser's system, which can expose the system to more security risks, such as potential exploits through browser vulnerabilities.

- **JS with only basic API access**: JavaScript with limited API access (such as working with the DOM and web APIs) is generally more secure than native mode access, but it still opens up security concerns, like XSS, if not handled properly.

Thus, **static HTML** is the most secure since it does not include the complexities and potential vulnerabilities associated with dynamic scripting languages like PHP or JavaScript.

---

##### Q7. Proper use of the constraint validation API can reduce the load on________.

client

server

network

all of the above

##### Answer: 
The **proper use of the constraint validation API** can reduce the load on both the **server** and the **network**.

Here's why:

- **Server**: By validating form inputs on the client side, the **constraint validation API** prevents invalid data from being sent to the server. This reduces unnecessary server-side processing because invalid submissions can be caught before they even reach the server.

- **Network**: Since invalid form submissions are blocked on the client side, there will be fewer requests made to the server. This reduces the network load by preventing unnecessary data transmission of invalid requests.

So, the correct answer is:
**Server and network**.


In addition to the **Constraint Validation API** (which is commonly used for form input validation), HTML5 provides other APIs and built-in mechanisms for validation:

 1. **Constraint Validation API** 
   - This API helps in validating form inputs against constraints like `required`, `min`, `max`, `pattern`, and more.
   - It's automatically used by the browser when the user tries to submit a form with invalid data.
   - **Example**: 
     ```html
     <form>
       <input type="email" required />
       <input type="submit" />
     </form>
     ```

 2. **FormData API**
   - The **FormData API** allows you to programmatically create and manipulate form data, and you can use it to validate form data before sending it to the server via AJAX requests.
   - This can be combined with custom JavaScript validation for more complex or custom form checks.
   - **Example**:
     ```javascript
     let formData = new FormData(form);
     if (formData.get('email') !== '') {
       // custom validation
     }
     ```

 3. **Custom Validation with JavaScript**
   - JavaScript allows you to implement custom validation logic beyond the built-in HTML5 form attributes. You can use JavaScript to create more sophisticated validation patterns or dynamic checks.
   - This is often used in conjunction with the **Constraint Validation API** to enhance the user experience and provide more detailed feedback.
   - **Example**:
     ```javascript
     const form = document.querySelector('form');
     form.addEventListener('submit', function(event) {
       if (!emailValid()) {
         event.preventDefault();  // Prevent form submission
         alert("Please enter a valid email.");
       }
     });
     
     function emailValid() {
       const email = document.querySelector('input[type="email"]').value;
       return /\S+@\S+\.\S+/.test(email);  // Simple regex for email validation
     }
     ```

 4. **Pattern Validation (HTML5 `pattern` attribute)**
   - The `pattern` attribute in HTML5 allows you to specify a regular expression for validating form input fields.
   - This is especially useful for fields that require specific formats, such as phone numbers or zip codes.
   - **Example**:
     ```html
     <input type="text" pattern="[A-Za-z]{3,}" title="Three or more letters">
     ```

 5. **HTML5 Input Types for Validation**
   - HTML5 introduced a variety of new input types, which automatically handle some common validation cases:
     - **`type="email"`**: Ensures the input is a valid email address format.
     - **`type="url"`**: Validates that the input is a valid URL.
     - **`type="number"`**: Ensures the input is a number, and can optionally be constrained with `min` and `max` attributes.
     - **`type="tel"`**: Allows phone number input and can be combined with custom validation using the `pattern` attribute.
     - **`type="date"`, `type="time"`, `type="range"`**: These input types allow users to input specific types of data that can be validated by the browser.
   - **Example**:
     ```html
     <input type="email" required />
     <input type="url" pattern="https?://.*" title="URL must start with http:// or https://">
     ```

 6. **HTML5 `required` Attribute**
   - The `required` attribute ensures that a form field must be filled out before the form is submitted.
   - **Example**:
     ```html
     <input type="text" required>
     ```

 7. **HTML5 `min` and `max` Attributes (for numeric fields)**
   - The `min` and `max` attributes can be used with input types like `number`, `range`, and `date` to specify the minimum and maximum allowable values.
   - **Example**:
     ```html
     <input type="number" min="18" max="100">
     ```

 8. **HTML5 `maxlength` and `minlength` Attributes**
   - The `maxlength` and `minlength` attributes allow you to specify the minimum and maximum number of characters for text input fields.
   - **Example**:
     ```html
     <input type="text" maxlength="10">
     ```

 9. **HTML5 `step` Attribute**
   - The `step` attribute allows for setting step increments for numeric inputs or date/time fields.
   - **Example**:
     ```html
     <input type="number" min="0" max="100" step="5">
     ```

 Summary of Common HTML5 Validation Methods:
1. **Constraint Validation API**: Built-in client-side validation.
2. **FormData API**: Allows programmatic manipulation and validation of form data.
3. **Pattern Validation**: Using regular expressions with the `pattern` attribute.
4. **Input Types**: Various input types like `email`, `url`, `number`, etc., come with built-in validation.
5. **Attributes**: `required`, `min`, `max`, `maxlength`, `minlength`, etc., allow for specifying validation rules directly in HTML.

Together, these methods provide a comprehensive set of tools for form validation in HTML5, ensuring that data entered by users meets the specified requirements before submission.

##### Q8.A Python flask application is given below.

```python 
from flask import Flask 

app = Flask(__name__) 

@app.route("/")
def hello(): 
    return "<P> Hello World </p>" 

if __name__ == "__main__": 
    app.run(debug=True) 

```
Which of the following options is true?
 1. It is an example of static web page being used.
 2. It is an example of dynamic web page being used.
 3. The browser will not render any output as a webpage.
 4. None of the above

##### Answer:
The correct answer is:

**2. It is an example of a dynamic web page being used.**

Explanation:
- The given Flask application sets up a web server that handles HTTP requests and returns a response dynamically generated by the Python code.
- When the route `"/"` is accessed, the `hello()` function returns the HTML content `"<P> Hello World </p>"`, which is rendered in the browser.
- This is considered **dynamic** because the content is served by a Python web application running on a server, as opposed to a static HTML file directly served by a web server.

Why the other options are incorrect:
1. **It is an example of a static web page being used**: Incorrect. A static web page is served directly as an HTML file without any server-side code execution.
3. **The browser will not render any output as a webpage**: Incorrect. The browser will render the output as a webpage displaying "Hello World".
4. **None of the above**: Incorrect. Option 2 is the correct answer.

Example for static pages:

```python 
from flask import Flask,render_template

app = Flask(__name__) 

@app.route("/")
def hello(): 
    return render_template("hello.html")

if __name__ == "__main__": 
    app.run(debug=True) 

```

##### Q9. Which of the following statements is/are true in the context of 'DOM' updates?

Generating a page completely through DOM updates is good for the accessibility of the page.

Generating a page completely through DOM updates will make the page almost inaccessible.

HTML is generated on client side and it cannot be done by browsers with limitations.

All of the above.

##### Answer:


The statement that is most accurate in the context of 'DOM' updates is:

**Generating a page completely through DOM updates will make the page almost inaccessible.**

##### Explanation:
- **Generating a page completely through DOM updates will make the page almost inaccessible**:
  - This can be true if the page relies heavily on JavaScript for rendering content. In such cases, users with JavaScript disabled or using older browsers may not be able to view or interact with the page properly, leading to accessibility issues.
  - Additionally, this could affect screen readers and other assistive technologies that rely on pre-rendered HTML for better accessibility.

- **HTML is generated on the client side and it cannot be done by browsers with limitations**:
  - This statement is partially correct. Client-side rendering (using JavaScript to generate the page content dynamically) may not be fully supported or perform well in older browsers or browsers with limited capabilities. Users with restricted environments may face difficulties when JavaScript-based content is required to render the page.

##### Why the Other Statements Are Incorrect:
- **Generating a page completely through DOM updates is good for the accessibility of the page**:
  - This is generally **false**. While modern JavaScript frameworks and libraries can improve accessibility if used correctly, generating the page purely through DOM updates can create challenges for users relying on assistive technologies.
  
- **All of the above**:
  - This option is incorrect because not all statements provided are true.

##### Conclusion:
The best choices are:
- **"Generating a page completely through DOM updates will make the page almost inaccessible."**
- **"HTML is generated on client side and it cannot be done by browsers with limitations."**

Both statements highlight the potential challenges of client-side rendering and dynamic content for accessibility and browser compatibility.

---

##### Q10.Which of the following is/are true for the web browsers?
Javascript is the only language that can be made available on web browsers.

Web browsers usually have JS engines to run Javascript.

It is quite possible to build some other browser that supports languages other than Javascript.

None of the above.

##### Answer:
The accepted answers are:

1. **Web browsers usually have JS engines to run Javascript.**
   - This statement is true because modern web browsers come with built-in JavaScript engines (e.g., V8 in Chrome, SpiderMonkey in Firefox, JavaScriptCore in Safari) to interpret and execute JavaScript code efficiently.

2. **It is quite possible to build some other browser that supports languages other than Javascript.**
   - This is also true. While JavaScript is the dominant language for client-side web development, it is technically possible to create a custom web browser or modify an existing one to support other languages, such as WebAssembly (which is already widely supported), or even custom plugins for different scripting languages. However, JavaScript remains the standard for web development.

##### Explanation:
- **“JavaScript is the only language that can be made available on web browsers”** is **false** because web browsers can also support WebAssembly (Wasm), which allows code written in other languages (such as C, C++, and Rust) to run in the browser alongside JavaScript.

---

##### Q12. Which of the following statements regarding WASM is/are true?

WASM is a compiled form of Javascript.

WASM is an instruction set that is supported on many browsers.

It is not limited to JS and can be generated from other languages also.

All of the above

##### Answer:
The accepted answers are:

1. **WASM is an instruction set that is supported on many browsers.**
   - This is true. WebAssembly (WASM) is a low-level, binary instruction format designed to run efficiently in web browsers. It is supported by all major modern browsers, enabling high-performance execution of code.

2. **It is not limited to JS and can be generated from other languages also.**
   - This is also true. WASM is not tied to JavaScript; it can be compiled from various programming languages, such as C, C++, Rust, Go, and many others, making it versatile for web and non-web applications.

Explanation:
- **“WASM is a compiled form of JavaScript”** is **false**. WASM is not a compiled form of JavaScript. Instead, it is an independent bytecode format that can be generated from languages other than JavaScript. It can work alongside JavaScript but is not derived from it.

Conclusion:
The correct statements are:
- **"WASM is an instruction set that is supported on many browsers."**
- **"It is not limited to JS and can be generated from other languages also."**

---
##### What is WSGI ?

**WSGI (Web Server Gateway Interface)** is a specification that defines how web servers communicate with web applications in the Python programming language. It acts as an interface between web servers and Python-based web applications or frameworks, facilitating a standard and consistent way to serve web content.

 Key Points About WSGI:
1. **Purpose**: WSGI was created to standardize the way Python web applications and web servers interact. Before WSGI, Python web frameworks and servers often had compatibility issues because each framework had its own method of communication.

2. **Specification**: It is not a library or a framework but a specification defined in [PEP 333](https://www.python.org/dev/peps/pep-0333/) and later updated in [PEP 3333](https://www.python.org/dev/peps/pep-3333/) to support Python 3.

3. **Components**:
   - **Web Server**: Receives HTTP requests and forwards them to the application via WSGI.
   - **WSGI Application**: Processes the request and returns a response back to the server.
   - **WSGI Middleware**: Optional layers that sit between the server and application, adding functionality such as request handling, authentication, or data compression.

4. **How It Works**:
   - The web server passes an environment dictionary and a callback function (start_response) to the WSGI application.
   - The application processes the request using the environment information and returns an iterable that contains the response body.
   - The `start_response` function is used by the application to send HTTP status and headers back to the server.

Example of a Simple WSGI Application:

```python
def simple_app(environ, start_response):
    # Status and response headers
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    
    # Response body
    return [b"Hello, WSGI World!"]
```

Why WSGI Is Important:
- **Framework Compatibility**: It allows various Python web frameworks (e.g., Flask, Django, Pyramid) to work with multiple web servers (e.g., Gunicorn, uWSGI, Apache with mod_wsgi).
- **Flexibility**: Enables developers to use middleware to handle common web application tasks like authentication, session management, and data compression.
- **Scalability**: WSGI allows for better handling of concurrent requests compared to basic Python server modules.

Common WSGI Servers:
- **Gunicorn**: A popular and efficient WSGI server used in production environments.
- **uWSGI**: Another powerful server with more extensive features and configurability.
- **mod_wsgi**: An Apache module for running WSGI applications.

---

### **Difference Between Synchronous and Asynchronous Updates in Frontend**  

In frontend development, **synchronous updates** and **asynchronous updates** define how the browser handles UI changes and communication with the backend.

---

### **1. Synchronous Updates**  
- The browser **waits** for an operation to complete before moving to the next step.  
- The UI **freezes** until the update is done.  
- This can make the application **slow and unresponsive** if the operation takes time.  

#### **Example (Synchronous)**
💡 Imagine you're ordering food at a restaurant:  
1. You **place an order** at the counter.  
2. You **stand there waiting** until the food is ready.  
3. Once the food is ready, you take it and leave.  

👉 In **frontend terms**, this means when you click a button, the whole page **freezes** until the request is completed.

#### **Code Example (Synchronous)**
```javascript
function fetchData() {
    let response = fetch('https://example.com/data'); // This blocks execution
    console.log("Data fetched!");
}

fetchData();
console.log("This message waits until data is fetched!");
```
👎 **Issue:** The browser **waits** for `fetch()` to complete before printing `"This message waits until data is fetched!"`. This can **freeze the UI**.

---

### **2. Asynchronous Updates**  
- The browser **doesn’t wait** for the operation to finish.  
- The UI **remains responsive** while the update happens in the background.  
- The page updates automatically when data arrives.  

#### **Example (Asynchronous)**
💡 Imagine you're ordering food at a restaurant with a **buzzer**:  
1. You **place an order** and get a **buzzer**.  
2. You **sit and relax** while waiting.  
3. When the food is ready, the **buzzer rings**, and you go to pick up your food.  

👉 In **frontend terms**, you can click a button, continue using the page, and get a notification when data arrives.

#### **Code Example (Asynchronous)**
```javascript
async function fetchData() {
    let response = await fetch('https://example.com/data'); // Fetch happens in background
    console.log("Data fetched!");
}

fetchData();
console.log("This message appears immediately!");
```
👍 **Advantage:** The `"This message appears immediately!"` is printed **before** data is fetched, meaning the UI **stays responsive**.

---

### **Key Differences**
| Feature | Synchronous | Asynchronous |
|---------|------------|--------------|
| **Execution** | One step at a time (blocking) | Multiple tasks at once (non-blocking) |
| **UI Freezing?** | Yes, if an operation is slow | No, UI remains responsive |
| **Example** | Waiting in line at a restaurant | Ordering food and waiting for a buzzer |
| **Best Used For** | Small, quick tasks | Network requests, animations, background updates |

**Conclusion:**  
Asynchronous updates make web apps **faster and more user-friendly**, especially when dealing with **API calls or background tasks**.



