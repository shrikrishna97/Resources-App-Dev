### **Day 1: Introduction to Flask, Jinja2, HTML/CSS, and Setup**

**Coding (2 PM - 4 PM)**

- **Create Project Structure**:

  - **app.py**: Main entry point for the Flask app.
  - **models.py**: Where database models will reside.
  - **templates/**: Create `index.html` as a base template.
  - **static/**: Store your CSS and JS files (use Bootstrap CDN for styling).

  **Explanation of Code and Structure**

  **app.py**:
  ```python
  from flask import Flask, render_template  # Importing Flask and render_template to create the app and render templates

  app = Flask(__name__)  # Creating the Flask app instance

  @app.route('/')  # Route decorator that maps the function to the root URL ('/')
  def home():
      return render_template('index.html', title='Home Page', username='John Doe')  # Rendering the template and passing data

  if __name__ == "__main__":  # Ensures code runs only when executed directly
      app.run(debug=True)  # Runs the app in debug mode for easier development
  ```

  **Explanation**:
  - **`from flask import Flask, render_template`**: Imports the necessary modules to create the Flask app and render HTML templates.
  - **`app = Flask(__name__)`**: Initializes the Flask app, with `__name__` indicating the root path.
  - **`@app.route('/')`**: Specifies the route for the homepage.
  - **`return render_template('index.html', title='Home Page', username='John Doe')`**: Calls `render_template()` to load `index.html` from the `templates/` folder and passes `title` and `username` to be used in the template.
  - **`if __name__ == "__main__"`**: Ensures the script runs as the main program.
  - **`app.run(debug=True)`**: Starts the Flask development server with debug mode enabled.

  **Why the `templates` Folder?**
  - Flask expects to find HTML templates in a directory named `templates` by default. This is where you should place all the HTML files that need to be rendered by `render_template()`.
  - The connection is established when `render_template('index.html')` is called, prompting Flask to look for `index.html` in the `templates/` folder.

- **Create a Simple HTML Template** in `templates/index.html`:

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{{ title }}</title>  <!-- Dynamic title passed from app.py -->
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body>
      <div class="container">
          <h1>Welcome, {{ username }}!</h1>  <!-- Dynamic username passed from app.py -->
      </div>
  </body>
  </html>
  ```

  **Explanation of `index.html`**:
  - **`{{ title }}`** and **`{{ username }}`** are Jinja2 placeholders. Flask replaces them with the values passed from `app.py`.
  - This template is stored in the `templates/` directory and rendered when the `home()` function in `app.py` is called.

Here's why we used Bootstrap over traditional CSS and information on how to get and use CDN links:

### Why Use Bootstrap Instead of Traditional CSS?
Bootstrap is a popular CSS framework that provides pre-designed components and a responsive grid system. Here are the key reasons for using Bootstrap in this context:

- **Ease of Use**: Bootstrap offers a collection of ready-to-use styles and components, such as navigation bars, buttons, and modals, that reduce the amount of custom CSS you need to write.
- **Consistency**: It ensures a consistent design across different parts of your application and across different projects.
- **Responsiveness**: Bootstrap's grid system allows you to build responsive web pages that adapt seamlessly to various screen sizes without writing extensive CSS.
- **Community Support**: Being widely used, Bootstrap has excellent documentation and community support, which is helpful for learners.

### What is a CDN?
CDN stands for **Content Delivery Network**. It is a system of distributed servers that deliver web content, like CSS or JavaScript libraries, based on the user's geographic location. The main benefits include:

- **Faster Load Times**: CDNs store content in multiple locations worldwide, so users can download assets from the nearest server, leading to quicker load times.
- **Reduced Server Load**: Your server doesn’t need to handle the load of serving static files, as CDNs take care of that.
- **Automatic Updates**: When using the latest version of a library via a CDN, updates are managed by the service.

### How to Get a CDN Link for Bootstrap?
1. **Visit the Bootstrap website**: Go to [getbootstrap.com](https://getbootstrap.com/).
2. **Navigate to the "Get Started" section**: Copy the CSS and JavaScript links provided for quick integration.
3. **Insert the CDN link in your HTML `<head>`**: This allows your page to pull Bootstrap directly from the web.

### Example of Including Bootstrap via a CDN:
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
```

This link loads the Bootstrap CSS directly from a CDN, so you don’t need to download and host it locally.

### What is Jinja2?
Jinja2 is a template engine used in Flask for rendering dynamic web pages. It allows you to embed Python-like expressions in HTML, making it easier to generate complex HTML structures.

### Why Use Jinja2?
Jinja2 has several advantages over other template engines:

- **Dynamic Content**: Jinja2 allows you to insert Python expressions into HTML templates, making it easy to generate dynamic content.
- **Template Inheritance**: It supports template inheritance, allowing you to reuse common sections of HTML across multiple templates.
- **Extensibility**: Jinja2 is extensible, making it easy to add custom filters, macros, and functions to your templates.

### How to Use Jinja2 in Flask?
1. **Import Jinja2**: Import the `render_template` function from the `flask` module.
2. **Render Templates**: Call `render_template()` to load and render templates.
3. **Pass Data**: Pass data to the template using keyword arguments.
4. **Template Variables**: Jinja2 allows you to use variables in your templates. You can access the data passed from `app.py` using the `{{ }}` syntax.



**Prep/Doubt Clearing (4 PM - 5 PM)**

- Discuss the Flask structure, routing, and templates or problem statements discussion.
- If any doubts, clear them.

Here are some excellent HTML and CSS resources for beginners:

### **HTML Resources:**

1. **[W3Schools - HTML Tutorial](https://www.w3schools.com/html/)**  
   - A beginner-friendly resource that covers all the basic concepts of HTML with interactive examples and exercises.

2. **[MDN Web Docs - HTML Basics](https://developer.mozilla.org/en-US/docs/Web/HTML/Introduction)**  
   - Mozilla’s comprehensive documentation, starting with an overview of HTML and progressing to more advanced topics. It’s great for both learning and referencing.

3. **[freeCodeCamp - HTML and HTML5](https://www.freecodecamp.org/learn/responsive-web-design/#basic-html-and-html5)**  
   - Offers a free interactive course covering HTML basics and advanced concepts. It’s practical and allows you to build projects.

4. **[HTML.com](https://html.com/)**  
   - A simple, straightforward resource with tutorials that break down HTML concepts in an easy-to-understand manner.

---

### **CSS Resources:**

1. **[W3Schools - CSS Tutorial](https://www.w3schools.com/css/)**  
   - A great resource for beginners that covers all CSS properties and concepts with examples and exercises.

2. **[MDN Web Docs - CSS Basics](https://developer.mozilla.org/en-US/docs/Web/CSS/Introduction_to_CSS)**  
   - MDN offers in-depth documentation with examples on CSS properties, selectors, and layouts, perfect for learners of all levels.

3. **[freeCodeCamp - CSS](https://www.freecodecamp.org/learn/responsive-web-design/basic-css/)**  
   - Another free, interactive course that helps you learn CSS, starting from the basics and advancing to responsive design techniques.

4. **[CSS-Tricks](https://css-tricks.com/guides/)**  
   - Provides a series of guides and articles on various CSS topics, ranging from beginner to advanced. Includes practical examples and tips.

5. **[The Net Ninja - CSS Tutorials (YouTube)](https://www.youtube.com/playlist?list=PL4cUxeGkcC9iIi6d_UlD6w2Edo0W9Jz-K)**  
   - A YouTube playlist with clear and concise CSS tutorials for beginners. Great if you prefer video tutorials.

---

### **Interactive Learning:**

1. **[CodePen](https://codepen.io/)**  
   - A platform where you can write and experiment with HTML, CSS, and JavaScript. It's a great way to practice and see your changes in real-time.

2. **[CSS Diner](https://flukeout.github.io/)**  
   - A fun game to learn and practice CSS selectors, perfect for beginners who want to engage with the learning process.

3. **[Flexbox Froggy](https://flexboxfroggy.com/)**  
   - A fun way to learn CSS Flexbox, a layout model that’s very useful in modern web design.

4. **[Grid Garden](https://cssgridgarden.com/)**  
   - Similar to Flexbox Froggy, but for learning CSS Grid layout. It’s an interactive way to master CSS Grid.

---

### **Books for Beginners:**

1. **"HTML and CSS: Design and Build Websites" by Jon Duckett**  
   - A visually appealing and easy-to-follow book for beginners, offering clear explanations and practical examples.

2. **"Learning Web Design" by Jennifer Niederst Robbins**  
   - A comprehensive guide to HTML and CSS, starting with the basics and advancing to more complex topics. Perfect for new learners.

By exploring these resources, you'll gain a solid foundation in HTML and CSS, and you’ll be ready to apply your skills in web development projects.




