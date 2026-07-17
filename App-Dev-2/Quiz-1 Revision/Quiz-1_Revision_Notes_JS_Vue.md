# Quiz-1 Revision Notes (JavaScript & Vue.js)

> These notes are for quick revision before Quiz-1. They focus on concepts, syntax, and how everything works together.

---

# JavaScript

## 1. `typeof`
```js
let name = "Alice";
let age = 20;
let active = true;

console.log(typeof name);   // string
console.log(typeof age);    // number
console.log(typeof active); // boolean
```

`typeof` returns the type of a value as a string like `"number"`, `"string"`, or `"boolean"`.
It is useful for checking data types before performing operations or validations.

## 2. `document`
```html
<h2 id="title">Welcome</h2>

<script>
document.getElementById("title").innerText = "Quiz Revision";
</script>
```

`document` represents the full HTML page loaded in the browser.
You use it to select elements, update content, and respond to user actions.

## 3. Functions

```js
function greet(name){
    return "Hello " + name;
}

console.log(greet("Shri"));
```

Functions can also be stored in variables.

```js
const add = (a,b)=>a+b;
```

A function is a reusable block of code that runs when it is called.
Functions help organize logic, avoid repetition, and make code easier to test.

## 4. `let`, `var`, `const`

| Keyword | Scope | Redeclare | Reassign |
|---|---|---|---|
| var | Function | ✔ | ✔ |
| let | Block | ✘ | ✔ |
| const | Block | ✘ | ✘ |

These keywords declare variables, but they differ in scope and mutability rules.
`let` and `const` are block-scoped, while `var` is function-scoped and older.

## 5. `forEach()`

```js
let nums=[1,2,3];

nums.forEach(function(n){
    console.log(n);
});
```

`forEach()` executes a callback once for each element in an array.
It is best for side effects like printing or updating UI, not for creating new arrays.

## 6. `map()`

```js
let nums=[1,2,3];

let square=nums.map(n=>n*n);

console.log(square);
```

`map()` transforms each array element and returns a new array of the same length.
Use it when you want to convert data from one form to another.

## 7. `filter()`

```js
let nums=[10,25,40,50];

let result=nums.filter(n=>n>=30);

console.log(result);
```

`filter()` returns a new array containing only elements that satisfy a condition.
It is useful for search, selection, and removing unwanted items.

## 8. `sort()`

```js
let nums=[5,1,10,3];

nums.sort((a,b)=>a-b);

console.log(nums);
```

`sort()` rearranges array elements based on a compare function.
For numbers, use `(a, b) => a - b` to avoid default string-based sorting.

## 9. `slice()`

```js
let arr=["A","B","C","D"];

console.log(arr.slice(1,3));
```

Output

```json
["B","C"]
```

`slice(start, end)` returns a shallow copy of part of an array.
It does not modify the original array, so it is safe for non-destructive operations.

## 10. `length`

```js
let arr=[1,2,3];

console.log(arr.length);
```

`length` gives the number of elements in an array or characters in a string.
It is commonly used for loops, validations, and empty checks.

## 11. `setTimeout()`

```js
setTimeout(()=>{
    console.log("Executed after 2 seconds");
},2000);
```

`setTimeout()` schedules a function to run once after a delay in milliseconds.
It is used for delayed UI actions, simple async flow, or temporary waits.

## 12. Callback Function

```js
function process(callback){
    console.log("Processing...");
    callback();
}

process(()=>{
    console.log("Done");
});
```

A callback is a function passed as an argument to another function.
It allows custom behavior to run after a task is completed.

## 13. Event Listener

```html
<button id="btn">Click</button>

<script>
document.getElementById("btn")
.addEventListener("click",()=>{
    alert("Clicked");
});
</script>
```

An event listener waits for browser events like click, input, or keypress.
When the event happens, the attached callback function executes.

## 14. `apply()`

```js
function greet(city){
    console.log(this.name+" from "+city);
}

const user={name:"Alice"};

greet.apply(user,["Delhi"]);
```

`apply()` calls a function with a specific `this` value and arguments as an array.
It is useful when argument values are already stored as a list.

## 15. `bind()`

```js
function hello(){
    console.log(this.name);
}

const user={name:"Bob"};

const fn=hello.bind(user);

fn();
```

`bind()` creates a new function with `this` permanently set to a chosen object.
It is commonly used when passing methods as callbacks to preserve context.

## Calling JavaScript Functions

```js
sayHello();

function sayHello(){
    console.log("Hello");
}
```

or

```html
<button onclick="sayHello()">
Click
</button>
```

Functions can be called directly in code by writing their name with parentheses.
They can also be triggered from HTML events like `onclick` in browser pages.

---

# JavaScript Combined Example

```html
<input id="search" placeholder="Minimum Marks">
<button id="show">Show Students</button>

<ul id="students"></ul>

<script>
const students=[
    {name:"Alice",marks:80},
    {name:"Bob",marks:55},
    {name:"Charlie",marks:92},
    {name:"David",marks:45}
];

function render(data){
    const ul=document.getElementById("students");
    ul.innerHTML="";

    data
    .sort((a,b)=>b.marks-a.marks)
    .forEach(student=>{
        ul.innerHTML+=`<li>${student.name} - ${student.marks}</li>`;
    });
}

document.getElementById("show")
.addEventListener("click",()=>{

    let value=Number(document.getElementById("search").value);

    let filtered=students.filter(s=>s.marks>=value);

    console.log(typeof value);

    setTimeout(()=>{
        render(filtered);
    },500);

});

function done(){
    console.log("Finished rendering");
}

function execute(callback){
    callback();
}

execute(done);
</script>
```

**Concepts used:** document, function, callback, addEventListener, filter, sort, forEach, typeof, setTimeout.

---

# Vue.js

Vue is a progressive JavaScript framework for building user interfaces.

## Component

```js
app.component("student-card",{
    props:["student"],
    template:`<h3>{{student.name}}</h3>`
});
```

A component is a reusable, self-contained UI building block in Vue.
It helps split large interfaces into manageable and maintainable pieces.

## Props

```html
<student-card
    :student="student">
</student-card>
```

Props are custom inputs used to pass data from parent to child components.
They make child components dynamic while keeping data flow predictable.

## Emit

```js
this.$emit("delete",id);
```

`$emit` lets a child component send an event message to its parent.
This is the standard way for child-to-parent communication in Vue.

## `@click` / `v-on`

```html
<button @click="increment">
Add
</button>
```

Equivalent

```html
<button v-on:click="increment">
```

`@click` is shorthand for `v-on:click` to listen for click events.
It connects UI actions to methods so user interactions trigger logic.

## `v-for`

```html
<li
v-for="student in students"
:key="student.id">

{{student.name}}

</li>
```

`v-for` renders a list by repeating an element for each item in data.
A unique `:key` should be provided for better rendering performance and stability.

## `v-show`

```html
<p v-show="loggedIn">
Welcome
</p>
```

`v-show` toggles element visibility using CSS without removing it from the DOM.
It is efficient when visibility changes frequently.

## `v-bind`

```html
<img :src="image">
```

`v-bind` dynamically binds HTML attributes to Vue data.
Its shorthand `:` is widely used for props and attributes like `src` and `class`.

## `v-model`

```html
<input v-model="username">
```

`v-model` creates two-way binding between form input and component state.
When input changes, data updates automatically, and vice versa.

## Lifecycle Hooks

```js
created(){}

mounted(){}

updated(){}

beforeUnmount(){}
```

Lifecycle hooks are methods that run at specific stages of a component's life.
They are used for setup, DOM-related work, reactive updates, and cleanup.

- created → data ready
- mounted → DOM ready
- updated → reactive update
- beforeUnmount → cleanup

---

# Vue Combined Example (Notes App)

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vue Notes</title>
    <script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
  </head>
  <body>
    <div id="app">
      <h2>Notes</h2>

      <input v-model="newNote" placeholder="Enter note" />

      <button @click="addNote">Add</button>

      <p v-show="notes.length===0">No Notes Available</p>

      <ul>
        <li v-for="(note,index) in notes" :key="index">
          {{note}}

          <button @click="remove(index)">Delete</button>
        </li>
      </ul>
    </div>

    <script>
      new Vue({
        el: "#app",
        data() {
          return {
            newNote: "",
            notes: ["Learn JS", "Learn Vue"],
          };
        },

        methods: {
          addNote() {
            if (this.newNote.trim()) {
              this.notes.push(this.newNote);

              this.newNote = "";
            }
          },

          remove(index) {
            this.notes.splice(index, 1);
          },
        },

        mounted() {
          console.log("Application Mounted");
        },
      });

    </script>
  </body>
</html>

```

**Concepts used:** `v-model`, `@click`, `v-show`, `v-for`, lifecycle hook.

---

# Component + Props + Emit Example

```js
const Child = {
  props: ["name"],

  template: `
    <div>
        {{name}}
        <button @click="$emit('remove')">
            Delete
        </button>
    </div>
            `,
};

new Vue({
  el: "#app",
  components: { Child },

  data() {
    return {
      student: "Alice",
    };
  },

  methods: {
    deleteStudent() {
      this.student = "";
    },
  },
});

```

```html
<!doctype html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>Vue 2 Component Demo</title>
		<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<h2>Student Card</h2>

			<child v-if="student" :name="student" @remove="deleteStudent"></child>
			<p v-else>No student available</p>
		</div>

		<script src="./Component.js"></script>
	</body>
</html>
```

---

# Quick Revision

| Topic | Purpose |
|---|---|
| typeof | Find data type |
| document | Access HTML |
| function | Reusable code |
| forEach | Loop array |
| map | Transform array |
| filter | Select data |
| sort | Arrange data |
| slice | Copy part of array |
| length | Count elements |
| callback | Function passed to function |
| setTimeout | Delay execution |
| Event Listener | Browser events |
| apply | Call function with custom this |
| bind | Permanently bind this |
| Component | Reusable UI |
| Props | Parent → Child |
| Emit | Child → Parent |
| v-for | Loop |
| v-show | Show/Hide |
| v-bind | Bind attributes |
| v-model | Two-way binding |
| @click | Click event |
| Lifecycle | Component stages |

# Extra Resources

JavaScript
- https://developer.mozilla.org/docs/Web/JavaScript
- https://javascript.info

Vue
- https://vuejs.org/guide/introduction.html
