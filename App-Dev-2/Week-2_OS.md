Prepared Based on: MAD 2 Introductory JavaScript Open Session

Target Audience: Beginners with Python background

Prepared by: Shri Krishna 

Last term live session for reference: [Mad-2 week-2 open session](https://www.youtube.com/live/dNGVCIAB0rU)

---

## 1. Introduction

JavaScript is a versatile language that runs in multiple environments. To get started with JavaScript development, here are the main methods:

### A. Running JavaScript in the Browser

All modern browsers come with built-in JavaScript engines. You can:

1. **Use the Browser Console**

   * Open DevTools (F12 or right-click → Inspect → Console tab).
   * Type JavaScript directly and run it.

2. **Include JavaScript in HTML**

   ```html
   <script>
     alert("Hello from HTML script tag!");
   </script>
   ```

   Or link an external file:

   ```html
   <script src="script.js"></script>
   ```

### B. Running JavaScript with Node.js

Node.js allows you to run JavaScript outside the browser.

1. **Install Node.js**

   * Download from [https://nodejs.org](https://nodejs.org) and install.

2. **Run a script**

   ```bash
   node filename.js
   ```

3. **Use REPL (Read-Eval-Print Loop)**

   ```bash
   node
   > console.log("Hello from Node.js");
   ```

### C. Using Online Editors

1. **JSFiddle / CodePen / Replit**

   * No installation needed.
   * Code and share directly in the browser.

### D. Using Integrated Development Environments (IDEs)

* **Visual Studio Code** (recommended)

  * Install extensions like ESLint, Prettier, and Live Server.
  * Use built-in terminal to run `node`.

the difference between a **JavaScript engine** and a **JavaScript runtime**, using **Chrome** and **VS Code** as examples:

---

##  1. JavaScript Engine

A **JavaScript engine** is the **core program that parses and executes JavaScript code**. It knows only how to understand and execute JavaScript, nothing more.

###  Example: Chrome uses **V8**

* V8 is a high-performance JavaScript engine developed by Google.
* It reads JavaScript, optimizes it, and turns it into fast machine code.
* It knows only about JavaScript syntax and internal data types — not about the DOM or `fetch()` or `setTimeout()`.

> **Think of V8 as the "brain" that knows JavaScript — but not how to interact with the browser or OS.**

---

##  2. JavaScript Runtime

A **JavaScript runtime** is a **full environment** that uses a JavaScript engine (like V8) and provides additional tools/APIs that JS alone can't offer — like:

* The DOM (in browsers)
* `setTimeout`, `console`, `fetch`
* Event loop and callback queue

###  Example: Chrome’s JavaScript runtime

* Engine: V8
* Runtime: Adds DOM access, timers, `console.log`, `alert`, `window`, etc.

###  Example: VS Code running Node.js

* Engine: V8 (same as Chrome!)
* Runtime: Node.js runtime adds `fs`, `http`, `process`, `require`, etc. (but no DOM)

>  **Think of the runtime as a kitchen: the engine is the chef, the runtime includes the fridge, oven, ingredients, and tools.**

---

## 🔍 Side-by-Side: Chrome vs. VS Code (with Node)

| Feature                        | Chrome (Browser Runtime) | VS Code + Node.js (Server Runtime) |
| ------------------------------ | ------------------------ | ---------------------------------- |
| JS Engine                      | V8                       | V8                                 |
| Has DOM                        | ✅ Yes                   | ❌ No                             |
| Has `setTimeout()`             | ✅ Yes                   | ✅ Yes (provided by Node)         |
| Has `fs` module                | ❌ No                    | ✅ Yes (Node's file system module)|
| Has `document.querySelector()` | ✅ Yes                   | ❌ No                             |
| Common use case                | Web apps, frontend       | Server-side scripting, backend     |

---

## Summary

| Concept     | JavaScript Engine     | JavaScript Runtime                         |
| ----------- | --------------------- | ------------------------------------------ |
| What it is  | Core JS interpreter   | Full environment to run JS                 |
| Knows about | JS syntax & semantics | JS + APIs (DOM, timers, file system, etc.) |
| Example     | V8                    | Chrome runtime (browser), Node.js runtime  |

[ JavaScript Runtime ]
  ├── JS Engine (V8) ← The core interpreter (like car engine)
  ├── Timers (setTimeout, setInterval)
  ├── Console (console.log)
  ├── APIs (DOM in browser / fs in Node)
  └── Event Loop (handles async stuff)

---

## 2. JavaScript Basics

### 2.1 Syntax Overview

JavaScript syntax is similar to C-style languages. Statements end with semicolons (optional but recommended), and blocks are enclosed in curly braces.

```javascript
let name = "Alice";
const age = 25;
console.log(name + " is " + age + " years old.");
```

This code declares two variables and prints a message using string concatenation.

### 2.2 Variable Declarations

JavaScript provides `var`, `let`, and `const` for declaring variables:

```javascript
var x = 10;      // function scoped, hoisted
let y = 20;      // block scoped
const z = 30;    // block scoped, immutable
```

* `var` is function-scoped and can lead to unexpected bugs due to hoisting.
* `let` is block-scoped and should be used when reassignment is needed.
* `const` is also block-scoped but prevents reassignment; prefer `const` by default.

---

## 3. Data Types

JavaScript has two main categories: primitives and objects.

### 3.1 Primitive Types

```javascript
let str = "Hello";   // string
let num = 42;        // number
let bool = true;     // boolean
let empty = null;    // null (intentional empty)
let undef;           // undefined (not assigned)
```

### 3.2 Objects

Objects are key-value pairs like Python dictionaries.

```javascript
let person = {
  name: "Alice",
  age: 25
};
console.log(person.name);  // Accessing properties using dot notation
```

You can dynamically add or delete properties:

```javascript
person.gender = "female";
delete person.age;
```

---

## 4. Control Flow

### 4.1 If-Else Statement

```javascript
if (age > 18) {
  console.log("Adult");
} else {
  console.log("Minor");
}
```

This is used for conditional branching.

### 4.2 Loops

#### For Loop

```javascript
for (let i = 0; i < 5; i++) {
  console.log(i);
}
```

#### While Loop

```javascript
let count = 0;
while (count < 3) {
  console.log(count);
  count++;
}
```

## `for...in` and `for...of` Loops

JavaScript provides two distinct looping constructs for iterating over data structures: `for...in` and `for...of`. Understanding their differences is crucial for effective coding.

### `for...in` Loop

**Purpose:**
Iterates over the enumerable property keys of an object, including inherited properties.

**Syntax:**

```javascript
for (let key in object) {
  // code block to be executed
}

```

**Example:**

```javascript
const person = { name: "Alice", age: 30 };

for (let key in person) {
  console.log(key);         // Outputs: name, age
  console.log(person[key]); // Outputs: Alice, 30
}

```

**Behavior:**

* Returns keys (property names) as strings.
* Includes enumerable properties from the object's prototype chain.
* Not recommended for arrays due to potential unexpected results, especially when the array is extended with custom properties.

**Use Case:**
Best suited for iterating over object properties.

### `for...of` Loop

**Purpose:**
Iterates over the values of iterable objects like arrays, strings, maps, sets, etc.

**Syntax:**

```javascript
for (let value of iterable) {
  // code block to be executed
}

```

**Example:**

```javascript
const fruits = ["apple", "banana", "cherry"];

for (let fruit of fruits) {
  console.log(fruit); // Outputs: apple, banana, cherry
}

```

**Behavior:**

* Returns the values of the iterable.
* Does not include properties added to the object (e.g., custom properties on arrays).
* Maintains the order of iteration as defined by the iterable.

**Use Case:**
Ideal for iterating over arrays, strings, maps, sets, and other iterable collections.

### 12.3 Comparison Table

|           Feature             |             `for...in`               |                `for...of`                |
| ----------------------------- | ------------------------------------ | ---------------------------------------- |
| Iterates Over                 | Enumerable property keys             | Iterable values                          |
| Return Value                  | Strings (keys)                       | Actual values                            |
| Applicable To                 | Objects (also arrays, but not ideal) | Arrays, strings, maps, sets, etc.        |
| Includes Inherited Properties | Yes                                  | No                                       |
| Iteration Order               | Not guaranteed                       | Follows the order of the iterable        |
| Use Case                      | Accessing object properties          | Accessing values in iterable collections |

**Note:**
When iterating over arrays, it's recommended to use `for...of` or traditional `for` loops instead of `for...in` to avoid unexpected behaviors, especially if the array has custom properties or methods.

## 5. Arrays and Objects

### 5.1 Arrays

```javascript
let fruits = ["apple", "banana", "cherry"];
fruits.push("date");  // Adds to end
console.log(fruits[0]);  // "apple"
```

### 5.2 Objects

```javascript
let car = {
  make: "Toyota",
  model: "Corolla"
};
car.year = 2020;       // Dynamic property addition
delete car.model;      // Property deletion
console.log(car);
```

---

## 6. Execution Environments

JavaScript operates in various environments, primarily the browser and Node.js. Each environment provides a global object that serves as the top-level context for code execution.

### 6.1 Global Object in Different Environments

* **Browser Environment:**
  In browsers, the global object is `window`. It represents the browser window and provides methods and properties for interacting with the browser.
* **Node.js Environment:**
  In Node.js, the global object is `global`. It provides access to global variables and functions specific to the Node.js environment.
* **Universal Access with:**
  To write environment-agnostic code, JavaScript introduces `globalThis` as a standardized way to access the global object across different environments.

### 6.2 Use Cases and Examples

#### 6.2.1 Using `window` in the Browser

The `window` object allows interaction with the browser window and its components.

**Example: Accessing Global Variables and Functions**

```javascript
// Declaring a global variable
var siteName = "ExampleSite";

// Accessing the global variable via window
console.log(window.siteName); // Output: "ExampleSite"

// Defining a global function
function greetUser() {
  alert("Welcome to " + siteName);
}

// Invoking the global function via window
window.greetUser(); // Displays alert: "Welcome to ExampleSite"

```

**Example: Using Browser-Specific Methods**

```javascript
// Displaying an alert dialog
window.alert("This is an alert box!");

// Opening a new browser window
window.open("https://www.example.com", "_blank");

```

#### 6.2.2 Using `global` in Node.js

In Node.js, the `global` object provides access to globally available variables and functions.

**Example: Defining and Accessing Global Variables**

```javascript
// Defining a global variable
global.appVersion = "1.0.0";

// Accessing the global variable
console.log(global.appVersion); // Output: "1.0.0"

```

**Example: Using Global Functions**

```javascript
// Using setTimeout, a global function in Node.js
setTimeout(() => {
  console.log("Executed after 2 seconds");
}, 2000);

```

#### 6.2.3 Using `globalThis` for Cross-Environment Compatibility

The `globalThis` object provides a standard way to access the global object, regardless of the environment.

**Example: Defining a Global Variable**

```javascript
// Defining a global variable using globalThis
globalThis.config = {
  appName: "UniversalApp",
  version: "2.0.0"
};

// Accessing the global variable
console.log(globalThis.config.appName); // Output: "UniversalApp"

```

By using `globalThis`, developers can write code that is compatible across different JavaScript environments without worrying about the specific global object name.

---

## 7. Debugging Techniques

### 7.1 Console Methods

```javascript
console.log("Info");
console.warn("Warning");
console.error("Error");
```

The browser console helps test and debug code.

---

## 8. Functions

### 8.1 Function Declaration

```js
function greet() {
  console.log("Hello");
}
```

* Classic function syntax.
* Hoisted (can be called before it is defined).
* Has its own this context.
* Hoisted and available before declaration.

### 8.2 Function Expression

```javascript
const greet = function() {
  console.log("Hello");
};
greet();
```

Not hoisted—must be declared before use.

### 8.3 Arrow Function

```javascript
const greet = () => {
  console.log("Hello");
};
greet();
```

* Arrow functions use lexical `this` and are often more concise.
* More concise.
* Not hoisted (must be declared before use).
* Does NOT have its own this.

---

## 9. The `this` Keyword

###  Regular Function:

```js
const user = {
  name: "Alice",
  greet: function() {
    console.log("Hi " + this.name);
  }
};
user.greet(); // Output: Hi Alice
```

* Here, this refers to the object user because it's called as user.greet().
* Regular functions dynamically bind this depending on how they're called.

###  Arrow Function:

```js
const user = {
  name: "Alice",
  greet: () => {
    console.log("Hi " + this.name);
  }
};
user.greet(); // Output: Hi undefined (in browsers, likely "Hi " or "Hi undefined")
```

* Arrow functions do not have their own this.
* They inherit this from the surrounding lexical scope (e.g., the window/global object if declared at the top level).
* So this.name is undefined.

✅ Use arrow functions when:

* You want to preserve the outer this (e.g., in callbacks).
* You don’t need your own this, arguments, or super.

❌ Avoid arrow functions when:

* You need to access object-specific this (e.g., methods on objects or classes).

---

## Summary Table

| Feature                    | Regular Function    | Arrow Function               |
| -------------------------- | ------------------- | ---------------------------- |
| Syntax                     | function greet() {} | const greet = () => {}       |
| Hoisting                   | ✅ Yes               | ❌ No                         |
| Own this                   | ✅ Yes               | ❌ No (lexical this)          |
| Use as constructor         | ✅ Yes               | ❌ No                         |
| Suitable for object method | ✅ Yes               | ❌ No (usually not preferred) |
| Suitable for callbacks     | ✅ Sometimes         | ✅ Often preferred            |

---

## 10. Hoisting and Temporal Dead Zone (TDZ)

What is Hoisting? Hoisting is JavaScript's default behavior of moving declarations to the top of the current scope during the compilation phase. This means that:

* Variable declarations (using var) are hoisted and initialized with undefined.
* Function declarations are hoisted entirely — both their name and body.
* Variables declared with let and const are hoisted too, but not initialized. Accessing them before declaration results in a ReferenceError due to the Temporal Dead Zone.

Examples:

**var example:**

This demonstrates hoisting of variables declared with `var`. The declaration is hoisted, but the assignment is not, so `a` is `undefined` when logged:

```javascript
console.log(a); // undefined
var a = 5;
```

**let/const example:**

Variables declared with `let` and `const` are hoisted but not initialized. Trying to access them before declaration results in a `ReferenceError` due to the Temporal Dead Zone (TDZ):

```javascript
console.log(b); // ReferenceError
let b = 10;
```

**function declaration:**

Function declarations are fully hoisted, so you can call them before the declaration appears in the code:

```javascript
greet(); // "Hello"
function greet() {
  console.log("Hello");
}
```

**function expression (not hoisted):**

Function expressions assigned to variables (even with `var`) are not hoisted with their assigned function. Only the variable is hoisted and initialized to `undefined`, so calling it before the assignment results in a `TypeError`:

```javascript
console.log(greet); // undefined
// console.log(greet()); // TypeError: greet is not a function
var greet = function() {
  return "Hello";
};
console.log(greet()); // "Hello"
```

With `let` or `const`, the variable is hoisted but not initialized. Trying to access it before declaration results in a `ReferenceError` due to the Temporal Dead Zone (TDZ):

```javascript
// console.log(greetLet); // ReferenceError
const greetLet = function() {
  return "Hi there";
};
console.log(greetLet()); // "Hi there"
```

So while function declarations are fully hoisted, function expressions are only hoisted with their variable declaration — not the function assignment. This is important to understand for debugging and code structure.

Function expressions assigned to variables (even with `var`) are not hoisted with their assigned function. Only the variable is hoisted and initialized to `undefined`, so calling it before the assignment results in a `TypeError`:

```javascript
greet(); // TypeError: greet is not a function
var greet = function() {
  console.log("Hello");
};
```

```javascript
console.log(a); // undefined
var a = 5;
```

---

## 11. Scope in JavaScript

### Definitions

* **Global Scope:** Variables accessible from anywhere in the program. Declared outside functions.
* **Function Scope:** Variables accessible only within the function where they are declared. `var` is function-scoped.
* **Block Scope:** Variables accessible only within a specific block (`{}`), typically defined using `let` or `const`.
* **Lexical Scope:** Scope determined by the position of functions and blocks during code definition. Inner functions can access variables from their outer functions.

### 11.1 Global Scope

Variables declared outside functions are accessible everywhere.

```javascript
var globalVar = "I'm global";
let globalLet = "I'm a global let";
const globalConst = "I'm a global const";

function printGlobal() {
  console.log(globalVar);
  console.log(globalLet);
  console.log(globalConst);
}
printGlobal();
```

### 11.2 Function Scope

Variables declared with `var` inside a function are only available inside that function. `let` and `const` behave similarly but are scoped more strictly to blocks.

```javascript
function example() {
  var localVar = "I'm a function-scoped var";
  let localLet = "I'm a function-scoped let";
  const localConst = "I'm a function-scoped const";
  console.log(localVar);
  console.log(localLet);
  console.log(localConst);
}
example();
// console.log(localVar); // ReferenceError
// console.log(localLet); // ReferenceError
// console.log(localConst); // ReferenceError
```

### 11.3 Block Scope

`let` and `const` are block-scoped, meaning they only exist within `{}`. `var` does not respect block scope.

```javascript
if (true) {
  var a = 1;       // Accessible outside the block
  let b = 2;       // Block-scoped
  const c = 3;     // Block-scoped
  console.log(a, b, c); // 1 2 3
}

console.log(a);    // 1
// console.log(b); // ReferenceError
// console.log(c); // ReferenceError
```

### 11.4 Lexical Scope

Functions remember the scope in which they were defined.

```javascript
function outer() {
  let name = "Alice";
  function inner() {
    console.log(name); // Alice
  }
  inner();
}
outer();
```

###

## 12. Best Practices

* Prefer `const` over `let` unless reassignment is needed.
* Avoid `var` unless maintaining legacy code.
* Use strict comparison (`===`) instead of loose (`==`).

```javascript
const MAX_USERS = 100;
let userCount = 0;

function addUser() {
  if (userCount < MAX_USERS) {
    userCount++;
  }
}
```

---

## 13. Summary

This session covered JavaScript syntax, data types, control flows, arrays, objects, function types, the `this` keyword, hoisting, execution environments, scoping, and best practices.

Practice Recommendations:

* Convert Python programs into JavaScript.

* Practice writing functions using all three declaration styles.

  **Function Declaration:**([Medium](https://mayanovarini.medium.com/functions-in-javascript-declaration-expression-arrow-d6f907dc850a?utm_source=chatgpt.com "Functions in Javascript (Declaration, Expression, Arrow) | by RM"))

  **Function Expression:**([Medium](https://mayanovarini.medium.com/functions-in-javascript-declaration-expression-arrow-d6f907dc850a?utm_source=chatgpt.com "Functions in Javascript (Declaration, Expression, Arrow) | by RM"))

  **Arrow Function:**([W3Schools](https://www.w3schools.com/js/js_arrow_function.asp?utm_source=chatgpt.com "JavaScript Arrow Function - W3Schools"))

* Experiment with `this` in different contexts.

* Use browser dev tools and Node.js to debug and test code.

* Practice hoisting and scope scenarios.
