# Vuex Store with Vue 2 - CDN

* Introduction to Vuex
* Core concepts: State, Getters, Mutations, Actions
* CDN setup with Vue 2
* Basic working example using HTML + JS

---

## 1. What is Vuex?

Vuex is a state management library for Vue.js applications. It helps manage shared data (state) across multiple components in a predictable way.

### Why Vuex?

#### Without Vuex (Using Props and Emit)

In Vue 2, components communicate using:

* **Props** (Parent → Child)
* **Emit** (Child → Parent)

Example:

Parent:

```
<child-component :count="count" @increment="count++"></child-component>
```

Child:

```
props: ['count'],
methods: {
  updateCount() {
    this.$emit('increment')
  }
}
```

Problem:

* Works fine for small apps
* But in large apps, data has to pass through multiple components

Example issue (Props Drilling):
HomePage → ProductList → ProductCard → AddToCartButton (e-commerce cart example)

Even if only AddToCartButton needs data, all intermediate components must pass it.

This makes:

* Code harder to manage
* Debugging difficult
* Components tightly coupled

---

#### With Vuex

Instead of passing data manually:

* All components access a **central store**

Example:

```
this.$store.state.count
this.$store.commit('increment')
```

Benefits:

* No need for deep props passing
* Any component can access shared state directly
* Clear and predictable data flow
* Easier to debug and scale

---

#### Key Idea (Why this matters)

Let us understand with a clear situation.

Scenario:

* You have components: HomePage → ProductList → ProductCard → AddToCartButton
* Only **AddToCartButton** needs the cart count and should update it

Without Vuex (using props & emit):

Step 1: HomePage passes data to ProductList

```
<product-list :cartCount="cartCount" @add="cartCount++"></product-list>
```

Step 2: ProductList must pass it again (even if it does not use it)

```
<product-card :cartCount="cartCount" @add="$emit('add')"></product-card>
```

Step 3: ProductCard must pass it again

```
<add-to-cart-button :cartCount="cartCount" @add="$emit('add')"></add-to-cart-button>
```

Step 4: AddToCartButton finally uses it

Problem here:

* Parent and Child are **just forwarding data**
* They are not using it
* Code becomes messy and repetitive
* Hard to track where changes are happening

This is called **props drilling**

---

With Vuex:

Any component can directly access and update state:

AddToCartButton:

```
this.$store.state.count
this.$store.commit('increment')
```

No need for:

* Passing props through multiple levels
* Emitting events through multiple layers

---

Final Understanding:

Props/Emit:

* Best for **direct parent-child communication**

Vuex:

* Best when:

  * Many components need same data
  * Components are deeply nested
  * State needs to be shared globally

This is why Vuex is introduced in larger applications.

---

## 2. Core Concepts of Vuex

(Reference: [https://v3.vuex.vuejs.org/](https://v3.vuex.vuejs.org/))

### 2.1 State

(Reference: [https://v3.vuex.vuejs.org/guide/state.html](https://v3.vuex.vuejs.org/guide/state.html))

* The single source of truth
* Stores application data

Example:

```
state: {
  count: 0
}
```

---

### 2.2 Getters

(Reference: [https://v3.vuex.vuejs.org/guide/getters.html](https://v3.vuex.vuejs.org/guide/getters.html))

* Used to compute derived state
* Similar to computed properties

Example:

```
getters: {
  doubleCount: (state) => state.count * 2
}
```

---

### 2.3 Mutations

(Reference: [https://v3.vuex.vuejs.org/guide/mutations.html](https://v3.vuex.vuejs.org/guide/mutations.html))

* Only way to change state
* Must be synchronous

Example:

```
mutations: {
  increment(state) {
    state.count++
  }
}
```

---

### 2.4 Actions

(Reference: [https://v3.vuex.vuejs.org/guide/actions.html](https://v3.vuex.vuejs.org/guide/actions.html))

* Used for async operations
* Commit mutations

Example:

```
actions: {
  incrementAsync({ commit }) {
    setTimeout(() => {
      commit('increment')
    }, 1000)
  }
}
```

---

## 3. Vuex Flow

(Reference: [https://v3.vuex.vuejs.org/guide/actions.html#dispatching-actions](https://v3.vuex.vuejs.org/guide/actions.html#dispatching-actions))

Component -> Dispatch Action -> Commit Mutation -> Update State -> UI updates

---

## 4. Using Vuex with CDN (Vue 2)

### 4.1 Include CDN Links in HTML

```
<script src="https://cdn.jsdelivr.net/npm/vue@2"></script>
<script src="https://cdn.jsdelivr.net/npm/vuex@3"></script>
```

---

## 5. Project Structure

```
index.html
app.js
store.js
```

---

## 6. Creating the Store (store.js)

```
const store = new Vuex.Store({
  state: {
    count: 0
  },

  getters: {
    doubleCount(state) {
      return state.count * 2
    }
  },

  mutations: {
    increment(state) {
      state.count++
    },
    decrement(state) {
      state.count--
    }
  },

  actions: {
    incrementAsync({ commit }) {
      setTimeout(() => {
        commit('increment')
      }, 1000)
    }
  }
})
```

---

## 7. Using Store in Vue Instance (app.js)

```
new Vue({
  el: '#app',
  store,

  // data is still used, but only for local component state
  data() {
    return {
      message: 'Local UI state'
    }
  },

  computed: {
    // shared/global state comes from Vuex
    count() {
      return this.$store.state.count
    },
    doubleCount() {
      return this.$store.getters.doubleCount
    }
  },

  methods: {
    increment() {
      this.$store.commit('increment')
    },
    decrement() {
      this.$store.commit('decrement')
    },
    incrementAsync() {
      this.$store.dispatch('incrementAsync')
    }
  }
})
```

### Important Understanding

* `data()` is used for **local state** (only needed inside this component)
* Vuex `state` is used for **shared/global state** (used across multiple components)

Example:

* `message` → only this component needs it → use `data()`
* `count` (cart count) → many components need it → use Vuex

Why not use only data?

* If you keep `count` in `data()`, other components cannot access it easily
* You will again need props and emit (problem we discussed earlier)

So rule of thumb:

* Local UI state → `data()`
* Shared application state → Vuex store

---

### Computed vs Data

* `data()` → local state
* `computed` → reactive access to Vuex state

Wrong:

```
data() {
  return { count: this.$store.state.count }
}
```

(Not reactive)

Correct:

```
computed: {
  count() { return this.$store.state.count }
}
```

---

### Commit vs Dispatch

* `commit` → mutation (sync)
* `dispatch` → action (async → commit)

```
this.$store.commit('increment')
this.$store.dispatch('incrementAsync')
```

---

### Do we need computed?

* Not mandatory, but recommended
* Without it: not clean and less reactive in templates

Rule:

* Read → computed
* Update → commit / dispatch

---

## 8. HTML File (index.html)

```
<!DOCTYPE html>
<html>
<head>
  <title>Vuex CDN Example</title>
</head>
<body>

<div id="app">
  <h2>Count: {{ count }}</h2>
  <h3>Double: {{ doubleCount }}</h3>

  <button @click="increment">Increment</button>
  <button @click="decrement">Decrement</button>
  <button @click="incrementAsync">Increment Async</button>
</div>

<script src="https://cdn.jsdelivr.net/npm/vue@2"></script>
<script src="https://cdn.jsdelivr.net/npm/vuex@3"></script>

<script src="store.js"></script>
<script src="app.js"></script>

</body>
</html>
```

---

## 9. Teaching Flow (2 Hours Plan)

### Part 1 (30 mins)

* What is state management
* Problems without Vuex
* Introduction to Vuex concepts

### Part 2 (30 mins)

* Explain State, Getters, Mutations, Actions
* Dry run with examples

### Part 3 (30 mins)

* Setup using CDN
* Create store.js
* Explain each section

### Part 4 (20 mins)

* Connect store with Vue instance
* Explain computed and methods

### Part 5 (10 mins)

* Run and test example
* Ask students to modify (add reset button)

---

## 10. Practice Task for Students

1. Add a reset mutation
2. Create a getter for triple count
3. Add a button to reset count

---

## 11. Key Points to Emphasize

* Never modify state directly
* Always use mutations
* Actions are for async tasks
* Vuex helps in large-scale apps

---

## 12. What NOT to Do (Common Mistakes)

1. Directly modifying state

```
this.$store.state.count++
```

Wrong because it breaks Vuex flow

2. Using data() for shared state

```
data() {
  return { count: 0 }
}
```

Leads back to props/emit problem

3. Using commit for async logic

```
setTimeout(() => {
  this.$store.commit('increment')
}, 1000)
```

Async logic should go inside actions

4. Skipping computed for UI

* Makes code messy
* Reduces clarity and reusability

Keep it simple:

* Read → computed
* Update → commit / dispatch

---

## 12. Summary

Vuex provides a centralized store for managing application state. It ensures predictable state changes using mutations and supports async logic using actions. It is especially useful when multiple components need access to shared data.

---
