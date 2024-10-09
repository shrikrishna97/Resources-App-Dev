Open Session Week 3

## f-strings and Comments

### 1. **Using f-strings for Formatting**
```python
name = "Shiv"
place = "Chennai"
profession = "Data Analyst"

text = f"My name is {name}, I live in {place} and I am {profession}."
print(text)
```
- **f-strings**: This is a concise and efficient way of embedding variables directly inside a string. The syntax is `f"some text {variable}"`, where everything inside the curly braces (`{}`) is evaluated and inserted into the string.

- In this case, three variables are defined:
  - `name = "Shiv"`
  - `place = "Chennai"`
  - `profession = "Data Analyst"`

- The **formatted string** `f"My name is {name}, I live in {place} and I am {profession}."` will insert the values of these variables in the corresponding positions inside the string. So, when you print it out, it will look like this:
  ```plaintext
  My name is Shiv, I live in Chennai and I am Data Analyst.
  ```

### 2. **Commented Code**
```python
# text = "Today is sunday"
# print(text)
```
- The lines are commented out using the `#` symbol, so they won’t be executed.
- If uncommented, the code would create a string `text = "Today is sunday"` and print it. However, because it's commented, it doesn’t affect the current output.

### Key Points:
- **f-strings**: These are a very handy way of inserting values into strings in Python, introduced in Python 3.6. They allow you to insert the value of any variable inside a string by using curly braces `{}`.
- **Comments**: Lines starting with `#` are ignored by the Python interpreter. They are useful for leaving notes or temporarily disabling code.

## **Jinja2** 

### 1. **Defining Variables**
```python
name = "Shiv"
place = "Chennai"
profession = "Data Analyst"
```
- Three variables are created:
  - `name` with the value `"Shiv"`
  - `place` with the value `"Chennai"`
  - `profession` with the value `"Data Analyst"`
These will be used to fill in placeholders in the template.

### 2. **Step 1: Create Template Text with Placeholders**
```python
temp = "My name is {{name}}, I live in {{place}} and I am a {{profession}}"
```
- A **template string** is defined here. The double curly braces `{{ }}` are placeholders that will later be filled with the values of the corresponding variables.
  - `{{name}}` will be replaced with the value of the variable `name`.
  - `{{place}}` will be replaced with the value of `place`.
  - `{{profession}}` will be replaced with the value of `profession`.

This step essentially creates the structure of the output you want.

### 3. **Step 2: Convert Text to a Template**
```python
made_temp = Template(temp)
```
- **`Template(temp)`**: This converts the `temp` string into a Jinja2 **template object**. Now, this `made_temp` can be used to fill the placeholders with actual data.

### 4. **Step 3: Render the Template with Data**
```python
output = made_temp.render(name=name, place=place, profession=profession)
```
- **Rendering**: The `.render()` method takes the template and substitutes the placeholders with the actual values.
  - `name=name`: This passes the value of the `name` variable into the template's `{{name}}` placeholder.
  - `place=place`: This passes the value of `place` to `{{place}}`.
  - `profession=profession`: This passes the value of `profession` to `{{profession}}`.
  
- The **left-hand side** (`name`, `place`, `profession`) refers to the placeholders in the template, while the **right-hand side** refers to the actual data being passed.

This will generate the following string:
```plaintext
My name is Shiv, I live in Chennai and I am a Data Analyst
```

### 5. **Output the Result**
```python
print(output)
```
- Finally, the `output` (which is the rendered string with the variable values inserted) is printed.

### Summary:
- A template with placeholders (`{{name}}`, `{{place}}`, and `{{profession}}`) is defined.
- The **Jinja2 `Template`** object is created from the string.
- The `.render()` method is used to pass the actual data (`name`, `place`, `profession`) to the template.
- The resulting string, with the placeholders replaced by their values, is printed out.

This method allows you to dynamically generate text (in this case, HTML or simple strings) by inserting data at runtime.

## Jinja2 and HTML

### 1. **Defining Variables**
```python
name = "Divya"
place = "Delhi"
```
- Two variables are created:
  - `name` with the value `"Divya"`
  - `place` with the value `"Delhi"`
These variables will be used to fill in the placeholders inside the HTML template.

---

### 2. **Step 1: Creating the HTML Template with Placeholders**
```python
temp = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        </head>
        <body>
            <h2>My name is {{name}}</h2>
            <h2>I live in {{place}}</h2>
        </body>
        </html>
"""
```
- **HTML Template**: This is a simple HTML document stored as a string, and it includes two placeholders inside curly braces (`{{ }}`):
  - `{{name}}`: This placeholder will later be filled with the value of the `name` variable.
  - `{{place}}`: This placeholder will be filled with the value of the `place` variable.

This template forms a structure of a basic HTML page, with two headings displaying a person's name and place of residence.

---

### 3. **Step 2: Converting Text to a Jinja2 Template**
```python
made_temp = Template(temp)
```
- **`Template(temp)`**: The `temp` string is converted into a Jinja2 **template object**. This prepares the template for dynamic content insertion (substituting placeholders with real values).
  - `made_temp` is the template object created from the `temp` string, which will be rendered with actual data in the next step.

---

### 4. **Step 3: Rendering the Template with Data**
```python
out = made_temp.render(name=name, place=place)
```
- **Rendering the template**: The `.render()` method is used to pass data into the template, filling the placeholders with the corresponding values.
  - `name=name`: This replaces `{{name}}` in the template with the value `"Divya"`.
  - `place=place`: This replaces `{{place}}` in the template with the value `"Delhi"`.

The final rendered HTML string will look like this:
```html
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <h2>My name is Divya</h2>
    <h2>I live in Delhi</h2>
</body>
</html>
```

---

### 5. **Printing the Output**
```python
print(out)
```
- This prints the rendered HTML content to the terminal, showing the final HTML structure with the inserted data.

### Summary:
1. **Template Creation**: You define a template (in this case, an HTML structure) with placeholders for the variables.
2. **Converting to a Template**: The template string is converted into a Jinja2 `Template` object.
3. **Rendering**: The `.render()` method substitutes the placeholders (`{{name}}`, `{{place}}`) with the actual data values (`"Divya"` and `"Delhi"`).
4. **Output**: The final HTML with the substituted values is printed out.

This technique is useful when you want to dynamically generate HTML or text-based content using data provided at runtime.

## Jinja2 and for loop

### 1. **Defining a List**
```python
data = ["Programmer", "Analyst", "Scientist"]
```
- A list named `data` is created with three elements: `"Programmer"`, `"Analyst"`, and `"Scientist"`. These are the values that will be inserted into the template in the upcoming steps.

---

### 2. **Step 1: Creating the Template with a For Loop**
```python
temp = "My data is: {%for i in Data %} {{i}} {% endfor %}"
```
- This is a Jinja2 template string with a **for loop** that iterates over the variable `Data` (which will be passed during rendering).
- The Jinja2 syntax:
  - `{%for i in Data %}`: This starts a loop that goes through each element of `Data`. The variable `i` represents each item during the iteration.
  - `{{i}}`: This prints the current value of `i` (each item from the `Data` list).
  - `{% endfor %}`: This ends the for loop.
  
When rendered, this loop will iterate over the list `Data` and insert each value into the final output.

---

### 3. **Step 2: Converting the String into a Jinja2 Template**
```python
made_temp = Template(temp)
```
- **`Template(temp)`**: This converts the `temp` string into a **Jinja2 template object**. Now, the string can be rendered with dynamic data passed into it.
- `made_temp` holds the template object.

---

### 4. **Step 3: Rendering the Template with Data**
```python
out = made_temp.render(Data=data)
```
- **`.render()`**: This method is used to pass data into the template. In this case:
  - `Data=data`: The list `data` (which contains `["Programmer", "Analyst", "Scientist"]`) is passed to the template as `Data`.
  
The for loop inside the template will iterate over this list and print each value.

When rendered, the result will be:
```plaintext
My data is: Programmer Analyst Scientist 
```

---

### 5. **Printing the Output**
```python
print(out)
```
- This will print the final rendered string to the console, which looks like:
```plaintext
My data is: Programmer Analyst Scientist 
```
It displays each item from the list `data` on the same line, separated by spaces.

---

### Summary:
1. **Template Creation**: A template string is created with a for loop to iterate over the list `Data`.
2. **Converting to a Template**: The template string is converted into a Jinja2 template object.
3. **Rendering**: The `.render()` method substitutes the list `data` for `Data` and loops over it, inserting each element into the final string.
4. **Output**: The final rendered string (with the list elements inserted) is printed.

This method allows you to dynamically generate strings by looping over data using Jinja2 templates.

## Jinja2 and for loop with if condition


### 1. **Defining the List**
```python
data = ["Programmer", "Analyst", "Scientist"]
```
- You define a list named `data` containing three strings: `"Programmer"`, `"Analyst"`, and `"Scientist"`. This list will be passed into the template and checked for certain conditions later.

---

### 2. **Creating the Template**
```python
temp = """
      {% for i in data %}
         {% if "z" in i %}
            {{i}}
         {% endif %}
         
      {% endfor %}
      No data found   
      """
```
- This is the **Jinja2 template** that you are going to render. It contains:
  - `{% for i in data %}`: A **for loop** that iterates over the list `data`.
  - `{% if "z" in i %}`: Inside the loop, an **if statement** checks if the letter `"z"` exists in the current string (`i`). If `"z"` is found, it will print that string using `{{i}}`.
  - `{% endif %}`: Closes the if statement.
  - `{% endfor %}`: Closes the for loop.
  
If no string in the list contains the letter `"z"`, the template will not print any of the list items. After the loop, the string `"No data found"` will always be printed.

---

### 3. **Converting to a Template Object**
```python
made_temp = Template(temp)
```
- **`Template(temp)`**: This converts the `temp` string into a **Jinja2 template object**, which can now be rendered with actual data.

---

### 4. **Rendering the Template**
```python
out = made_temp.render(data=data)
```
- **`.render(data=data)`**: The `.render()` method is used to pass the list `data` into the template under the name `data`. This allows the for loop to iterate over the list.
  - Since none of the strings `"Programmer"`, `"Analyst"`, or `"Scientist"` contain the letter `"z"`, the if condition `if "z" in i` will never be true.
  
Therefore, no strings from the list will be printed.

---

### 5. **Printing the Output**
```python
print(out)
```
- Since none of the strings in the list satisfy the condition (having a `"z"` in them), the output will be:
```plaintext
No data found
```

### Explanation Summary:
1. **Template Creation**: You define a template that loops over a list and checks whether each string contains the letter `"z"`. If it does, the string is printed.
2. **Converting to a Template Object**: The template string is converted into a Jinja2 `Template` object.
3. **Rendering the Template**: You render the template by passing the `data` list, but no strings match the condition (having a `"z"`).
4. **Output**: Since no list items meet the condition, the final output will be `"No data found"`.

This template structure is useful when you want to filter data dynamically based on certain conditions.

## Jinja2 and for loop with if , elif and else condition

### 1. **Defining the Variable**
```python
subject = "MAD 1"
```
- A variable named `subject` is defined with the value `"MAD 1"`. This string will be used in the template to determine the output based on certain conditions.

---

### 2. **Creating the Template**
```python
temp = """
      {% if "2" in sub %}
        {{sub}}
      {% else %}
      Required subject not found
      {% endif %}
"""
```
- This is a **Jinja2 template** string that contains a conditional statement:
  - `{% if "2" in sub %}`: This checks if the character `"2"` is present in the variable `sub` (which will later be assigned the value of `subject`).
  - `{{sub}}`: If `"2"` is found in `sub`, this line will print the value of `sub` (which is `"MAD 1"`).
  - `{% else %}`: If `"2"` is not found, the code inside this block will execute.
  - `Required subject not found`: This string will be printed if `"2"` is not present in `sub`.
  - `{% endif %}`: This ends the if-else block.

---

### 3. **Converting to a Template Object**
```python
made_temp = Template(temp)
```
- **`Template(temp)`**: This converts the `temp` string into a **Jinja2 template object** named `made_temp`, allowing for dynamic content rendering based on the conditions specified.

---

### 4. **Rendering the Template**
```python
out = made_temp.render(sub=subject)
```
- **`.render(sub=subject)`**: This method is called on the template object to pass the `subject` variable to the template as `sub`.
  - Since the value of `subject` is `"MAD 1"`, the template checks if `"2"` is present in this string.
  - Since `"2"` is **not** in `"MAD 1"`, the condition will evaluate to `False`.

---

### 5. **Printing the Output**
```python
print(out)
```
- Because the condition is false, the output of the template will be:
```plaintext
Required subject not found
```

### Summary:
1. **Template Creation**: A Jinja2 template is defined that checks for the presence of the character `"2"` in the `sub` variable.
2. **Converting to a Template Object**: The template string is converted into a Jinja2 `Template` object.
3. **Rendering**: The template is rendered by passing the variable `subject` (with the value `"MAD 1"`) as `sub`.
4. **Output**: Since `"2"` is not found in `"MAD 1"`, the output is `"Required subject not found"`.

This example demonstrates how to use Jinja2 for conditional rendering based on the content of a variable.