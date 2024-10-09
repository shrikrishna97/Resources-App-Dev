
1. **What is `sys` and how to import it in Python?**
2. **How to handle files in Python?**
3. **How to read command-line values in Python?**

### 1. What is `sys` and how to import it in Python?

The `sys` module in Python provides access to system-specific parameters and functions. It allows you to interact with the Python interpreter and provides a way to manipulate the runtime environment.

#### Importing `sys`:

To use the `sys` module, you need to import it at the beginning of your Python script:

```python
import sys
```

You can also import specific parts of the `sys` module, but usually, it's more common to import the whole module. Example of importing a specific function (not usually done with `sys`):

```python
from sys import argv
```

### Key Features of `sys`:

- `sys.argv`: A list of command-line arguments passed to your script.
- `sys.exit()`: Allows you to exit the program with a specified exit status.
- `sys.stdin`, `sys.stdout`, `sys.stderr`: File objects that represent the standard input, output, and error streams.
  
### Example:

```python
import sys

print("Python version:", sys.version)
print("Platform:", sys.platform)
```

### 2. How to Handle Files in Python?

In Python, handling files is straightforward. You can open, read, write, and close files using built-in functions like `open()`, `read()`, `write()`, and `close()`.

#### Opening a File:

```python
file = open("example.txt", "r")  # Open file in read mode
```

#### Reading a File:

You can read files in various ways:
- **Read the whole content**:
  ```python
  content = file.read()
  print(content)
  ```
  
- **Read line by line**:
  ```python
  for line in file:
      print(line.strip())  # strip() removes extra newlines
  ```

#### Writing to a File:

To write to a file, you open it in write (`'w'`) or append (`'a'`) mode:

```python
file = open("example.txt", "w")  # Open file in write mode
file.write("Hello, World!")
file.close()
```

- **Note**: If the file already exists, opening it in write mode (`'w'`) will overwrite its contents.

#### Closing a File:

Always close files after you’re done to free up system resources:

```python
file.close()
```

#### Using `with` to handle files:

A better way to handle files is to use the `with` statement. This automatically closes the file for you, even if an error occurs:

```python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
```

### 3. How to Read Command-Line Values in Python?

Command-line arguments can be accessed using `sys.argv`. This is a list where:
- `sys.argv[0]` is the script name.
- `sys.argv[1]` and onward are the actual command-line arguments passed.

#### Example:

Create a Python script `example.py`:

```python
import sys

if len(sys.argv) != 3:
    print("Usage: python example.py <arg1> <arg2>")
else:
    print("Argument 1:", sys.argv[1])
    print("Argument 2:", sys.argv[2])
```

To run the script from the command line with arguments:

```bash
$ python example.py hello world
```

Output:

```
Argument 1: hello
Argument 2: world
```

### Additional Examples:


Let's explore more examples in each of the areas we discussed: using `sys`, handling files, and reading command-line arguments.

### 1. **Using `sys` Module**

#### Example 1: Checking the Python Version
You can check the version of Python being used by accessing `sys.version`.

```python
import sys

print("Python Version:", sys.version)
```

#### Example 2: Exiting the Program with `sys.exit()`
The `sys.exit()` function can terminate a script early.

```python
import sys

age = input("Enter your age: ")

if not age.isdigit():
    print("Invalid input. Exiting.")
    sys.exit(1)  # Exits with an error code
else:
    print(f"Your age is {age}.")
```

#### Example 3: Using `sys.stdin` for Input
You can use `sys.stdin.read()` to read input directly from the console.

```python
import sys

print("Enter something:")
input_data = sys.stdin.read()
print(f"You entered: {input_data}")
```

### 2. **Handling Files in Python**

#### Example 1: Reading a File

Let's say you have a file called `data.txt` with the following content:

```
Hello, this is line 1.
This is line 2.
```

You can read the entire content of the file:

```python
with open("data.txt", "r") as file:
    content = file.read()
    print(content)
```

Output:

```
Hello, this is line 1.
This is line 2.
```

#### Example 2: Writing to a File
This example demonstrates how to write to a file.

```python
with open("output.txt", "w") as file:
    file.write("This is the first line.\n")
    file.write("This is the second line.\n")
```

This creates a file called `output.txt` with the content:

```
This is the first line.
This is the second line.
```

#### Example 3: Appending to a File
You can append to an existing file without overwriting its content:

```python
with open("output.txt", "a") as file:
    file.write("This is the third line.\n")
```

This will add a new line to `output.txt`:

```
This is the first line.
This is the second line.
This is the third line.
```

#### Example 4: Reading Line by Line
You can read a file line by line using a loop:

```python
with open("data.txt", "r") as file:
    for line in file:
        print(line.strip())  # Use strip() to remove any extra newline characters
```

Output:

```
Hello, this is line 1.
This is line 2.
```

### 3. **Reading Command-Line Arguments**

#### Example 1: Simple Script Using Command-Line Arguments
Here's a simple script that accepts two command-line arguments.

```python
import sys

# Check if the user provided enough arguments
if len(sys.argv) < 3:
    print("Usage: python script.py <name> <age>")
    sys.exit(1)

# Access the arguments
name = sys.argv[1]
age = sys.argv[2]

# Print them
print(f"Hello, {name}. You are {age} years old.")
```

To run this script from the command line:

```bash
$ python script.py Alice 30
```

Output:

```
Hello, Alice. You are 30 years old.
```

#### Example 2: Reading Multiple Arguments
If you want to process multiple arguments from the command line, you can loop through `sys.argv`.

```python
import sys

print("You provided the following arguments:")

for arg in sys.argv:
    print(arg)
```

If you run the script as follows:

```bash
$ python script.py first second third
```

The output would be:

```
You provided the following arguments:
script.py
first
second
third
```

#### Example 3: Handling Missing Command-Line Arguments
You can check the number of arguments and handle missing values gracefully.

```python
import sys

if len(sys.argv) != 4:
    print("Usage: python script.py <first name> <last name> <age>")
else:
    first_name = sys.argv[1]
    last_name = sys.argv[2]
    age = sys.argv[3]

    print(f"Hello {first_name} {last_name}, you are {age} years old.")
```

If you don't pass enough arguments, the script will print the usage instructions:

```bash
$ python script.py John
```

Output:

```
Usage: python script.py <first name> <last name> <age>
```

But if you provide the correct number of arguments:

```bash
$ python script.py John Doe 25
```

Output:

```
Hello John Doe, you are 25 years old.
```

### Additional Notes:

- **File Modes**: When working with files, you'll use different modes:
  - `'r'`: Read (default mode).
  - `'w'`: Write (overwrites the file).
  - `'a'`: Append (adds to the end of the file).
  - `'r+'`: Read and write.
  
- **Error Handling with Files**: It's a good idea to handle errors when working with files.
  
```python
try:
    with open("nonexistent.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("The file does not exist.")
```

### Summary of New Examples:
1. **`sys` Module**:
   - `sys.version` for checking Python version.
   - `sys.exit()` for terminating the script early.
   - `sys.stdin.read()` for reading input from the console.

2. **File Handling**:
   - Read file content with `read()`, write to a file with `write()`, and append content with `'a'`.
   - Use `with` to automatically close the file after reading or writing.

3. **Command-Line Arguments**:
   - `sys.argv` allows you to access command-line arguments.
   - Handle cases where arguments are missing using `len(sys.argv)`.

