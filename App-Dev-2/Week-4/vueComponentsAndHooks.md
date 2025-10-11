# **Understanding Vue.js Components and Lifecycle Hooks (Vue 2)**

## 1. What is a Vue Component?

In Vue.js, a **component** is a **reusable block of code** that controls part of your web page.
It has its own **structure (HTML)**, **style (CSS)**, and **logic (JavaScript)**.

Think of components as **building blocks** — you build your web app by joining small reusable pieces.

---

### Without Components

If you don’t use components, your code becomes repetitive and hard to maintain.

```html
<!-- index.html -->
<div id="app">
  <h2>Welcome to My App</h2>
  <p>User Name: John</p>
  <p>User Age: 25</p>

  <h2>Welcome to My App</h2>
  <p>User Name: Mary</p>
  <p>User Age: 22</p>
</div>

<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
<script>
  new Vue({
    el: "#app"
  });
</script>
```

**Problem:**
Repeated markup and duplicated logic. Small changes require updates in many places.

---

### With Components

We can define a reusable `user-card` component and use it multiple times.

```html
<!-- index.html -->
<div id="app">
  <user-card name="John" age="25"></user-card>
  <user-card name="Mary" age="22"></user-card>
</div>

<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
<script>
  // Define a reusable component
  Vue.component('user-card', {
    // Props are like function parameters — they pass data from parent to child
    props: ['name', 'age'],
    template: `
      <div class="user-card">
        <h2>Welcome to My App</h2>
        <p>User Name: {{ name }}</p>
        <p>User Age: {{ age }}</p>
      </div>
    `
  });

  new Vue({
    el: '#app'
  });
</script>
```

**Note:**
`{{ name }}` is Vue’s syntax (this is Vue interpolation) for showing data dynamically — it displays the value of `name` inside the HTML.

---

### Output:

```
Welcome to My App
User Name: John
User Age: 25

Welcome to My App
User Name: Mary
User Age: 22
```

---

### Why Components Are Useful

* **Reusable:** Write once, use everywhere.
* **Readable:** Each component handles one part of the UI.
* **Maintainable:** Easy to change without breaking other parts.
* **Collaborative:** Multiple developers can work on different components.

---

### Try It Yourself

Add another `<user-card>` with your own name and age.
See how easily it appears without duplicating code.

---

### 1.1 `data` in components: Object vs. Function

* For the **root Vue instance** (the one you create with `new Vue({...})`), `data` can be a plain object.

```js
new Vue({
  el: '#app',
  data: {
    title: 'Hello World'
  }
});
```

* For **components**, `data` **must** be a function that returns an object. This ensures **each instance** of the component gets its own independent copy of the state.

```js
Vue.component('counter', {
  data: function () {
    return { count: 0 };
  },
  template: '<button @click="count++">Count: {{ count }}</button>'
});
```

If `data` were a shared object for components, multiple instances would share the same state, which causes bugs. By using a function, each component instance receives its own returned object.

**Try it:** Create two `<counter>` components and click buttons to confirm they maintain separate counts.

---

### 1.2 Parent and Child Components

* **Parent**: The Vue instance or component that uses a child component’s tag in its template.
* **Child**: The component defined separately that receives data via `props` and renders its template.

**Child component (declares props):**

```js
Vue.component('child-comp', {
  props: ['message'],
  template: '<p>Child says: {{ message }}</p>'
});
```

**Parent (passes props):**

```html
<div id="app">
  <!-- static string prop -->
  <child-comp message="Hello from Parent!"></child-comp>
  <!-- dynamic prop bound to parent data -->
  <child-comp :message="parentMsg"></child-comp>
</div>

<script>
new Vue({
  el: '#app',
  data: { parentMsg: 'Dynamic Hello!' }
});
</script>
```

**Notes on communication:**

* Data flows one-way: **parent → child** through props.
* Children should not directly mutate props (Vue warns against this). If a child needs to change parent state, it should emit an event that the parent listens to (this is the usual pattern: child `this.$emit('some-event', payload)`; parent uses `v-on` / `@some-event` to catch it).

**Try it:** Add a third `<child-comp>` and change `parentMsg` in the root data; observe the child update.

### 1.2.1 Child-to-Parent Communication (Using Events)

Props allow **data to flow from parent to child**, but sometimes the **child** also needs to send a message back to the **parent** — for example, when a button is clicked inside the child.

Since props are **one-way**, the child cannot directly modify parent data.
Instead, it uses **custom events** to “emit” messages upward.

**Example:**

```html
<div id="app">
  <parent-comp></parent-comp>
</div>

<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
<script>
  // Child component
  Vue.component('child-button', {
    template: `
      <button @click="notifyParent">Click Me (Child)</button>
    `,
    methods: {
      notifyParent() {
        // emit a custom event named 'child-clicked'
        this.$emit('child-clicked', 'Hello from Child!');
      }
    }
  });

  // Parent component
  Vue.component('parent-comp', {
    template: `
      <div>
        <h3>Parent Component</h3>
        <child-button @child-clicked="handleMessage"></child-button>
        <p>Message: {{ message }}</p>
      </div>
    `,
    data() {
      return { message: '' };
    },
    methods: {
      handleMessage(msg) {
        this.message = msg;
      }
    }
  });

  new Vue({ el: '#app' });
</script>
```

**Explanation:**

* The child triggers an event with `this.$emit('child-clicked', 'message')`.
* The parent listens for that event using `@child-clicked="handleMessage"`.
* When the event occurs, the parent’s method `handleMessage` receives the message from the child.

**In short:**

* **Parent → Child:** via `props`
* **Child → Parent:** via `$emit` (custom events)

This maintains a clear and predictable one-way data flow, ensuring components stay independent and easy to debug.


---

### 1.3 Slots (Content distribution)

A `<slot>` is a placeholder inside a child component where parent-provided content will be injected.

**Basic slot example:**

```js
Vue.component('alert-box', {
  template: `
    <div class="alert">
      <strong>Notice:</strong>
      <slot></slot>
    </div>`
});

new Vue({ el: '#app' });
```

```html
<div id="app">
  <alert-box>
    This is an important alert message.
  </alert-box>
</div>
```

**Fallback/default slot content:**

```js
Vue.component('submit-button', {
  template: '<button type="submit"><slot>Submit</slot></button>'
});
```

* `<submit-button></submit-button>` renders `<button>Submit</button>` (fallback used).
* `<submit-button>Save</submit-button>` renders `<button>Save</button>` (parent content overrides fallback).

**Named slots (simple example):**

```js
Vue.component('card-layout', {
  template: `
    <div class="card">
      <header><slot name="header">Default header</slot></header>
      <main><slot>Default body</slot></main>
      <footer><slot name="footer">Default footer</slot></footer>
    </div>`
});
```

```html
<card-layout>
  <template v-slot:header>
    <h4>Custom Header</h4>
  </template>
  <p>This is the body content (default slot).</p>
  <template v-slot:footer>
    <small>Custom Footer</small>
  </template>
</card-layout>
```

**Key points:** 
- Slot content is written in the parent and rendered inside the child’s template at the slot position. 

- Slot content has access to the parent’s scope. 

- Slots are often used to make layout or wrapper components flexible — for example, a modal, card, or alert box that displays custom inner content.

**Try it:** Change fallback texts and provide different content in the parent to observe how the slots render.


---

### 1.4 Alternative Ways to Define Components (Vue 2 CDN)

**Global registration with `Vue.component`** (already shown):

```js
Vue.component('my-component', {
  template: '<p>Global component</p>'
});
```

**Local registration using the `components` option:**

```js
var LocalChild = { template: '<p>I am local</p>' };
new Vue({
  el: '#app',
  components: { 'local-child': LocalChild }
});
```

Local registration keeps the global namespace clean and scopes components to the specific parent.



## 2. Vue Lifecycle Hooks

Every Vue component goes through a **lifecycle** — from creation to removal.
Vue provides **lifecycle hooks**, which are special functions that run automatically at specific stages.

---

### Lifecycle Stages Overview

| Stage           | Hook            | When It Runs                         |
| --------------- | --------------- | ------------------------------------ |
| **Creation**    | `beforeCreate`  | Before data and events are set up    |
|                 | `created`       | After data and methods are ready     |
| **Mounting**    | `beforeMount`   | Before template is added to the page |
|                 | `mounted`       | After template is on the page        |
| **Updating**    | `beforeUpdate`  | Before DOM updates after data change |
|                 | `updated`       | After DOM updates                    |
| **Destruction** | `beforeDestroy` | Before component is destroyed        |
|                 | `destroyed`     | After it’s removed from the DOM      |

---

### Real-Life Analogy

A Vue component’s lifecycle is similar to a plant’s life:

* **beforeCreate:** The seed exists but is not planted yet.
* **created:** The roots and data are ready.
* **mounted:** The plant appears in the soil (DOM/template).
* **updated:** The plant grows new leaves (data changes).
* **destroyed:** The plant is removed.

---

### Lifecycle Example in One File

```html
<!-- index.html -->
<div id="app">
  <lifecycle-demo></lifecycle-demo>
</div>

<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
<script>
  Vue.component('lifecycle-demo', {
    template: `
      <div>
        <h3>Lifecycle Hook Demo</h3>
        <p>Count: {{ count }}</p>
        <button @click="increaseCount">Increase</button>
      </div>
    `,
    data() {
      return { count: 0 }
    },
    methods: {
      increaseCount() {
        this.count++;
      }
    },
    beforeCreate() {
      console.log("beforeCreate: Data not yet available");
    },
    created() {
      console.log("created: Data and methods ready");
    },
    beforeMount() {
      console.log("beforeMount: Template not yet in DOM");
    },
    mounted() {
      console.log("mounted: Template added to DOM");
    },
    beforeUpdate() {
      console.log("beforeUpdate: DOM about to update");
    },
    updated() {
      console.log("updated: DOM updated");
    },
    beforeDestroy() {
      console.log("beforeDestroy: Component will be destroyed");
    },
    destroyed() {
      console.log("destroyed: Component destroyed");
    }
  });

  new Vue({
    el: '#app'
  });
</script>
```

Open your browser console and observe the messages printed in order.

---

### Try It Yourself

1. Click “Increase” and observe the `beforeUpdate` and `updated` hooks in the console.
2. To destroy the component manually, run these lines in the browser console:

   ```js
   vm = new Vue({ el: '#app' });
   vm.$children[0].$destroy();
   ```

   In vue 3 , the `destroyed` hook is renamed to `unmounted`, but in Vue 2 it remains `destroyed`.
---


## 3. Moving Component Logic to a Separate JS File

As your app grows, it is better to keep components in separate files for better organization and maintainability.
Let’s move our lifecycle component to a new JavaScript file.

---

### Step 1 — Create `lifecycleDemo.js`

```js
// lifecycleDemo.js
export const lifecycleDemo = {
  template: `
    <div>
      <h3>Lifecycle Hook Demo (External File)</h3>
      <p>Count: {{ count }}</p>
      <button @click="increaseCount">Increase</button>
    </div>
  `,
  data() {
    return { count: 0 }
  },
  methods: {
    increaseCount() {
      this.count++;
    }
  },
  beforeCreate() {
    console.log("beforeCreate (external): Data not yet available");
  },
  created() {
    console.log("created (external): Data and methods ready");
  },
  beforeMount() {
    console.log("beforeMount (external): Template not yet mounted");
  },
  mounted() {
    console.log("mounted (external): Template added to DOM");
  },
  beforeUpdate() {
    console.log("beforeUpdate (external): DOM about to change");
  },
  updated() {
    console.log("updated (external): DOM has been updated");
  },
  beforeDestroy() {
    console.log("beforeDestroy (external): Component will be destroyed");
  },
  destroyed() {
    console.log("destroyed (external): Component destroyed");
  }
};
```

---

### Step 2 — Import and Use It in `index.html`

```html
<!-- index.html -->
<div id="app">
  <lifecycle-demo></lifecycle-demo>
</div>

<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
<!-- 'type="module"' enables import/export syntax -->
<script type="module">
  import { lifecycleDemo } from './lifecycleDemo.js';

  Vue.component('lifecycle-demo', lifecycleDemo);

  new Vue({
    el: '#app'
  });
</script>
```

**Note:**

* `export` makes your component available for use in other files.
* `import` brings it into the current file.

---

## 4. Summary

| Concept                            | Description                                                               |
| ---------------------------------- | ------------------------------------------------------------------------- |
| **Component**                      | A reusable Vue instance that manages one part of the UI                   |
| **Props**                          | Allow parent-to-child data sharing (one-way data flow) ;Children can send messages to parents by emitting events; props should not be mutated by children.                                       |
| **Interpolation (`{{ }}`)**        | Displays dynamic data inside templates                                    |
| **Lifecycle Hooks**                | Functions that run automatically during creation, update, and destruction |
| **Modularization (export/import)** | Keeps code organized and reusable across files                            |
| **data**                           |  In the root Vue instance `data` can be an object; in component definitions `data` must be a function returning an object so each instance has independent state.                           |
| **slots**                          | `<slot>` allows parent-provided content to be injected into child templates; default and named slots help structure content insertion.                            |

---

## 5. What Happens If You Don’t Use Components

* Code duplication increases
* Debugging becomes difficult
* Hard to maintain or update
* No clear separation between logic and UI

---

## 6. Practice Exercises

1. **Create Your Own Component:**
   Create a `product-card` component that accepts `productName` and `price` as props.

2. **Add Lifecycle Hooks:**
   Log messages when your component is created, updated, and destroyed.

3. **Experiment with Data:**
   Add a button to update the price and observe which lifecycle hooks are triggered.

---

## 7. Final Takeaway

Vue components help you divide, reuse, and manage your web app efficiently.
Lifecycle hooks help you understand what happens and when in the life of a component.
Together, they make Vue a simple yet powerful framework for building dynamic applications.

---
