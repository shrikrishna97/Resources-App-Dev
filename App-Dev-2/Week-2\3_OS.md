Prepared Based on: MAD 2 JavaScript week-3 Open Session

Target Audience: Beginners with Python background and Javascript basic understanding 

Prepared by: Shri Krishna 

Last term live session for reference: [Mad-2 week-3 open session](https://www.youtube.com/live/QYQWZhItGjQ?feature=shared)

# JavaScript Callback Functions and Timers

**Callback functions** are fundamental in JavaScript. A *callback* is simply a function passed as an argument into another function, so that it can be “called back” (invoked) later. In other words, the receiving function can execute the callback at the appropriate time to complete some task. Callbacks can run **synchronously** (immediately) or **asynchronously** (later, after some operation completes). 

For example, many array methods like `forEach` and `map` accept callbacks, and asynchronous APIs like `setTimeout()` or `fetch().then()` use callbacks when operations finish.

* **Use cases:** You use callbacks whenever one function needs to execute another after finishing work. For instance, passing a function to handle a server response, to run code after a click event, or to process each element in an array.
* **Example (plain JS):**

  ```js
  function greet(name, callback) {
    console.log("Hello, " + name + "!");
    callback();  // invoke the callback function
  }

  function sayGoodbye() {
    console.log("Goodbye!");
  }

  // Pass sayGoodbye as a callback to greet:
  greet("Alice", sayGoodbye);

  // Output:
  // Hello, Alice!
  // Goodbye!
  ```

  Here, `sayGoodbye` is the callback passed into `greet`. When `greet` finishes its work, it invokes the callback.

## `setTimeout`

The `setTimeout()` function schedules a one-time callback after a specified delay (in milliseconds). Its basic behavior is: *“set a timer, and when it expires, run the given function”*. 

For example, `setTimeout(fn, 1000)` will call `fn` after \~1000ms. Because it’s asynchronous, code after `setTimeout` continues running immediately – it does **not** pause the script. The function returns a timer ID (a number) which can be used to cancel the timeout before it fires.

* **Syntax:** `let timeoutId = setTimeout(callback, delay, [arg1, arg2, ...]);`
* **Key points:**

  * `callback` is the function to run after the delay.
  * `delay` is in milliseconds (1000ms = 1 second).
  * The returned ID (e.g. `timeoutId`) uniquely identifies this timer and can be passed to `clearTimeout()` to cancel it.
* **Use cases:** Delay execution of code (e.g. show a message after a pause, schedule a timeout on a network request, animate something after a wait). You cannot use `setTimeout` to synchronously pause code; it always runs the callback later.
* **Example (plain JS):**

  ```js
  function sayHello() {
    console.log("Hello after 1 second!");
  }
  let timerId = setTimeout(sayHello, 1000);
  // If needed, we could cancel with clearTimeout(timerId).
  ```
* **Vue.js example:** In a Vue component you might use `setTimeout` to update state after a delay. For example:

  ```js
  export default {
    data() {
      return { message: "Waiting...", visible: false, timeoutId: null };
    },
    mounted() {
      // Show message after 2 seconds
      this.timeoutId = setTimeout(() => {
        this.visible = true;
        this.message = "Hello from Vue!";
      }, 2000);
    },
    beforeUnmount() {
      // Always clear timers when the component is destroyed
      clearTimeout(this.timeoutId);
    }
  };
  ```

  In this Vue snippet, we schedule a change 2 seconds after mounting and store the ID (`timeoutId`). In the `beforeUnmount` hook we clear it so it won’t fire if the component is removed.

## `setInterval`

The `setInterval()` function repeatedly runs a callback at fixed time intervals. You pass it a function and a delay, and it will call that function every *delay* milliseconds until you stop it. Like `setTimeout`, it returns an interval ID that you can later use to clear the interval.

* **Syntax:** `let intervalId = setInterval(callback, delay, [arg1, arg2, ...]);`
* **Behavior:** Unlike `setTimeout` (once), `setInterval` keeps invoking the callback over and over. The first invocation happens after the initial delay, and then repeatedly after each delay.
* **Use cases:** Perfect for tasks that need repeating work – e.g. updating a timer or clock every second, polling a server periodically, animating a sequence (like a slideshow or blinking text), checking for conditions continuously, etc.
* **Example (plain JS):**

  ```js
  let count = 0;
  let intervalId = setInterval(() => {
    count++;
    console.log("Count is now " + count);
    if (count >= 5) {
      clearInterval(intervalId);  // stop after 5 iterations
    }
  }, 1000);
  ```

  This code logs the count every second and stops after reaching 5.
* **Vue.js example:** In Vue you might update component state every second (e.g. a timer). It’s important to clear the interval on destroy. For example:

  ```js
  export default {
    data() {
      return { seconds: 0, intervalId: null };
    },
    mounted() {
      // Increase seconds every second
      this.intervalId = setInterval(() => {
        this.seconds++;
      }, 1000);
    },
    beforeUnmount() {
      clearInterval(this.intervalId);
    }
  };
  ```

  Here `seconds` increments each second. By saving the ID and clearing it in `beforeUnmount`, we ensure the interval doesn’t keep running after the component is removed.

## `clearTimeout`

The `clearTimeout()` function stops a timeout scheduled by `setTimeout()`. You pass it the timer ID that `setTimeout` returned. If that timeout hasn’t fired yet, it gets cancelled and will never execute its callback. If you pass an invalid or already-cleared ID, `clearTimeout` does nothing.

* **Syntax:** `clearTimeout(timeoutId);`
* **Use case:** Cancel a pending delayed action. 

For example, if a user takes an action that makes the delayed callback irrelevant, you can call `clearTimeout` to prevent it from running.

* **Example:**

  ```js
  let timerId = setTimeout(() => {
    console.log("This won't run because we clear the timeout.");
  }, 5000);

  // Cancel the timeout before it fires:
  clearTimeout(timerId);
  ```

## `clearInterval`

The `clearInterval()` function stops a repeating action created by `setInterval()`. You give it the interval ID returned by `setInterval`, and it will cancel further executions of that callback. Like `clearTimeout`, if you pass an invalid ID it simply does nothing.

* **Syntax:** `clearInterval(intervalId);`
* **Use case:** Stop a repeated task when it is no longer needed. For instance, halt a clock update when leaving a page, or stop an animation when the user navigates away.
* **Example:**

  ```js
  let intervalId = setInterval(() => {
    console.log("This will run every second until cleared");
  }, 1000);

  // After 5 seconds, stop the interval:
  setTimeout(() => {
    clearInterval(intervalId);
    console.log("Interval stopped");
  }, 5000);
  ```

## Best Practices and Common Patterns

* **Asynchronous Nature:** Remember that `setTimeout` and `setInterval` **do not pause** the script. They schedule callbacks that run later, allowing other code to run immediately. For example, multiple timeouts may complete out of order if their delays differ.
* **Storing IDs:** Always save the IDs returned by `setTimeout`/`setInterval` if you may need to cancel them. In modern Vue.js (3.x), use the `onUnmounted` (or `beforeUnmount`) lifecycle hook to clear any active timers. This avoids “zombie” timers that fire after a component is gone.
* **Timing in Vue:** As shown above, a Vue component often sets timers in `mounted()` and clears them in `beforeUnmount()`. Neglecting to clear timers can lead to unexpected behavior or memory leaks (the timers will keep running even after the component is destroyed).
* **Practical scenarios:**

  * **Callbacks:** Used for event handling (e.g. `button.addEventListener("click", callback)`), array iteration (`arr.forEach(callback)`), network requests (`fetch(url).then(response => { ... })`), and more.
  * **setTimeout:** Delay showing a notification, auto-hiding alerts, debouncing rapid actions (e.g. delaying a search query), scheduling retries.
  * **setInterval:** Building a clock/timer UI, refreshing data periodically (polling), running animations (like cycling through images), checking conditions on a schedule.
  * **clearTimeout/clearInterval:** Often used for “cancel” buttons, cleanup on navigation away, or stopping animations after a certain time.

Each of these functions is part of standard Web APIs and works in browsers (and Node.js provides similar global functions). They are essential for controlling timing and flow in JavaScript, especially when working with asynchronous operations.

Great! I’ll add a beginner-friendly explanation of the difference between synchronous and asynchronous programming, including simple real-life analogies (like cooking or waiting in line) and JavaScript code examples to demonstrate the concept.

I’ll let you know once it's added to the notes.


# Synchronous vs Asynchronous Programming in JavaScript

**Synchronous** code runs one step at a time, in order. Each operation must finish before the next one starts. In other words, the program “steps through” each line sequentially, waiting on each to complete.  For example:

```js
console.log("Step 1");
console.log("Step 2");
console.log("Step 3");
// Output: Step 1, then Step 2, then Step 3 (in order)
```

In this code, each `console.log` waits for the previous one to finish before running. This sequential flow is simple and predictable, but if one step takes a long time (like loading a large file), it blocks everything else from running.

**Asynchronous** code, by contrast, allows tasks to be started and then run independently.  In asynchronous execution, you can initiate a long-running task and *then* move on to other work before that task finishes. The long task runs “in the background,” and when it’s done your code is notified (often via a callback). This non-blocking behavior keeps applications responsive. For example:

```js
console.log("Hi");

setTimeout(() => {
  console.log("Geek");
}, 2000);

console.log("End");
// Output: Hi, then End, then (after 2 seconds) Geek
```

In the above code, “Hi” and “End” are logged immediately, **before** the delayed “Geek” message. That’s because `setTimeout` is asynchronous: it hands off the callback to the browser’s timer system and immediately continues to the next lines. Only after 2000 ms does the callback run. This shows how asynchronous functions like `setTimeout` don’t block the main flow.

## Real-World Analogies

* **Waiting in Line (Synchronous):** Imagine standing in a coffee shop line. You must wait for all the people ahead of you to order and receive their drinks before it’s your turn. The whole line is blocked by each order. This is like synchronous code: each task waits its turn.
* **Dining with Friends (Asynchronous):** Now picture sitting at a restaurant. After you place your food order, you don’t sit silently at the table waiting – you chat, sip a drink, or play a game while the kitchen prepares your meal. When the food is ready, the server brings it to you. This is like asynchronous code: you start a task (the meal) and then do other things until it’s done.
* **Cooking a Meal:** Cooking can be synchronous or asynchronous. A synchronous approach is boiling water, **waiting** for it to boil, then cooking pasta, then chopping vegetables, all one after another. An asynchronous approach is boiling water **and at the same time** chopping vegetables or making sauce. While the water heats (a long task), you’re busy with other prep. You’re not standing around doing nothing – just like async code lets other work happen during delays.

These analogies illustrate how synchronous tasks block the flow (one at a time), whereas asynchronous tasks can overlap and improve efficiency.

## Synchronous vs Asynchronous: Key Points

* **Sequential vs Concurrent:** In synchronous programming, tasks run one after another. In asynchronous programming, tasks can begin and then proceed in the “background” while the main code continues.
* **Blocking vs Non-Blocking:** Synchronous functions *block* the main thread until they finish. Asynchronous functions (like timers or I/O) are *non-blocking*, so they hand off work and let your code keep running.
* **Event Loop:** JavaScript uses an event loop under the hood. When you call something like `setTimeout`, the callback is processed by the browser’s Web APIs and placed in a queue. The main thread doesn’t wait; when it’s free, the event loop pulls the callback from the queue and executes it.

## Code Examples

**Synchronous example:** Each line runs one after another:

```js
console.log("A");
console.log("B");
console.log("C");
// Output: A, then B, then C (in order)
```

**Asynchronous example with `setTimeout`:**

```js
console.log("Start");
setTimeout(() => {
  console.log("Inside timeout");
}, 1000);
console.log("Finish");
// Output: Start, then Finish, then (after ~1 second) Inside timeout
```

Here, “Finish” appears before “Inside timeout” even though the `setTimeout` call comes before it. That’s because the timer callback is deferred.

**Using Callbacks:** A *callback* is just a function you pass to another function to run later. For example, with `setTimeout` we give a callback to execute after a delay. Callbacks let you specify what to do when an async operation finishes. For instance:

```js
console.log("Before fetch");
setTimeout(() => {
  console.log("Data fetched!");
}, 2000);
console.log("After fetch");
// Output: Before fetch, After fetch, then (after 2s) Data fetched!
```

This shows that the code after `setTimeout` runs immediately; only later does the callback run, thanks to the event loop.

## Asynchronous Features: `setTimeout`, `setInterval`, and Callbacks

* **`setTimeout(callback, delay)`:** Schedules `callback` to run once after `delay` milliseconds. It does **not** pause your code. Your script keeps running; when the timer finishes, the callback is invoked.
* **`setInterval(callback, interval)`:** Schedules `callback` to run repeatedly every `interval` ms. Like `setTimeout`, it doesn’t block; it just sets up a recurring task that the event loop will execute. For example, `setInterval(() => console.log("Tick"), 1000);` will log “Tick” every second, while your main code continues immediately after calling it.
* **Callbacks:** A callback is a function passed into another function (for example, to `setTimeout` or an event handler) and expected to run later. In asynchronous code, callbacks execute after the current code finishes and when the event loop calls them. This is different from a normal function call, which runs immediately and blocks until it returns.

Because of these async features, code can be **non-sequential**. You might see the end of a function run before a callback or timer fires. This is normal: JavaScript is single-threaded but uses its event loop to handle async tasks without stopping the main thread.

**In summary:** Synchronous JavaScript does things in order, blocking each step (like a single queue). Asynchronous JavaScript starts tasks that run in the background and continues with other work, which keeps apps responsive. Timers (`setTimeout`, `setInterval`) and callbacks are core to this – they let you schedule code to run later without freezing the current flow.

**Sources:** Authoritative JavaScript docs and tutorials.



# Vue.js Examples and Setup

Below is an HTML example for **Vue 2** and **Vue 3** that implements the given component (showing “Waiting…” and then “Hello from Vue!” after 2 seconds).  The examples use a CDN script so you can simply open the HTML file in a browser to run it.  We then discuss the differences between Vue 2 vs Vue 3 (including renamed lifecycle hooks and API changes) and the various ways to run Vue (CDN, CLI, or Vite).

## Vue 2 Example (with CDN)

In Vue 2, you include the Vue 2.x script via a `<script>` tag, and then create a Vue instance with `new Vue(...)`.  For example:

```html
<!-- index.html for Vue 2 -->
<div id="app">
  <!-- Only show the message when visible is true -->
  <p v-if="visible">{{ message }}</p>
</div>

<!-- Include Vue 2 from CDN -->
<script src="https://cdn.jsdelivr.net/npm/vue@2.7.16/dist/vue.js"></script>
<script>
// Create a new Vue 2 instance
new Vue({
  el: '#app',
  data: {
    message: 'Waiting...',
    visible: false,
    timeoutId: null
  },
  mounted() {
    // After 2 seconds, show the message
    this.timeoutId = setTimeout(() => {
      this.visible = true;
      this.message = 'Hello from Vue!';
    }, 2000);
  },
  beforeDestroy() {
    // Clear timer when component is destroyed
    clearTimeout(this.timeoutId);
  }
});
</script>
```

* We use `<script src="...vue@2.7.16/dist/vue.js"></script>` to load Vue 2 (latest 2.x) from a CDN.
* The `new Vue({ el: '#app', data: {...}, mounted(), beforeDestroy() })` creates the Vue 2 instance (using the *Options API*). Note the lifecycle hook is called `beforeDestroy` in Vue 2.
* Simply open this HTML file in a browser. No build step is needed when using a CDN script.

## Vue 3 Example (with CDN)

In Vue 3, the API has changed: you use `Vue.createApp()` instead of `new Vue`, and the destroy hooks were renamed.  Here is the equivalent example in Vue 3:

```html
<!-- index.html for Vue 3 -->
<div id="app">
  <p v-if="visible">{{ message }}</p>
</div>

<!-- Include Vue 3 from CDN -->
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
<script>
// Use the global Vue object to create the app
const { createApp } = Vue;
createApp({
  data() {
    return {
      message: 'Waiting...',
      visible: false,
      timeoutId: null
    };
  },
  mounted() {
    // After 2 seconds, show the message
    this.timeoutId = setTimeout(() => {
      this.visible = true;
      this.message = 'Hello from Vue!';
    }, 2000);
  },
  beforeUnmount() {
    // Clear timer when component is unmounted
    clearTimeout(this.timeoutId);
  }
}).mount('#app');
</script>
```

* The `<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>` loads Vue 3’s global build from a CDN.
* We call `const { createApp } = Vue; createApp({...}).mount('#app')` (Vue 3’s new app-mount API).  The `beforeUnmount` hook replaces `beforeDestroy` in Vue 3.
* As with Vue 2, this HTML can be opened directly in a browser with no build step.  (Note: using `vue.global.js` exposes Vue on the global `Vue` object.)

## Key Differences (Vue 2 vs Vue 3)

* **Lifecycle Hooks Renamed:** In Vue 3 the destroy hooks were renamed – `beforeDestroy` → `beforeUnmount`, `destroyed` → `unmounted`. In our example we use `beforeUnmount` for Vue 3 and `beforeDestroy` for Vue 2.
* **App Creation:** Vue 2 uses `new Vue({ ... })` (or `new Vue().$mount('#app')`), whereas Vue 3 uses `createApp({...}).mount('#app')`.  The migration guide notes that the global API now uses an application instance in Vue 3.
* **Mount Behavior:** In Vue 2, mounting replaces the target element. In Vue 3, the app’s DOM is appended inside the mount element (Vue 3 wraps the content but does not remove the element).
* **Composition API:** Vue 3 introduced the **Composition API** (using `setup()` and `ref()` etc.) alongside the Options API.  This offers more flexible code organization and better TypeScript support. (Our example still uses the Options API for simplicity.)
* **Performance & Size:** Vue 3 has a rewritten reactivity system and supports better tree-shaking, resulting in faster rendering and smaller bundles.  Many sources note Vue 3 is generally faster and has new features (Teleport, Suspense, multiple root elements) not in Vue 2.
* **Tooling:** The official docs now recommend using **Vite** (via `npm create vue@latest`) for new projects, since Vue CLI is in maintenance mode. Vue 2 projects commonly used Vue CLI (Webpack-based) or simple CDN inclusion.

## Running Vue: CDN vs CLI vs Vite

* **CDN (script tag):**  Simply include Vue via `<script>` as above.  This is the easiest way to try Vue or add it to an existing site without a build process. There’s no compilation step – your code runs directly in the browser. However, you cannot use `.vue` single-file components or advanced features that require a build. (You also load the entire Vue library at runtime.)
* **Vue CLI (Legacy Tool):**  The official Vue CLI (webpack-based) scaffolds full projects with hot-reload and bundling. In a Vue CLI project, you typically run `npm run serve` (or `yarn serve`) to start a dev server. Vue CLI handles compiling `.vue` files, modern JS, CSS preprocessors, etc., and outputs optimized builds. Note that as of Vue 3, the Vue team recommends using Vite instead of Vue CLI for new projects.
* **Vite (Recommended):**  Vite is a modern build tool that provides an extremely fast dev server and HMR for Vue projects.  To start a new Vue 3 app with Vite, you can run `npm create vue@latest` and follow prompts. Then install and run `npm run dev` in the project folder. Vite will bundle your Vue files and assets, but unlike CDN mode, it allows using single-file components, modern syntax, and build optimizations (tree-shaking, minification, etc.). The Vue docs note that for new projects, Vite (via `create-vue`) is the best choice.
* **Summary:**  Using a CDN is great for simple demos or adding Vue to a server-rendered page. For larger or production apps, you’d use a build setup: Vue CLI or Vite. Build tools automatically bundle and optimize your code (compiling `.vue` components, handling dependencies, etc.). The end result is still HTML/JS/CSS, but build tools improve developer experience and performance. In short: CDN = quick prototyping (no build); CLI/Vite = full app development with tooling.


