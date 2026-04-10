# MAD-2 Recap Quiz-2

---

## 1. Reading Data from DOM

### You might know what is getAttribute? but do you know what is dataset?

`dataset` is a built-in DOM property that gives you access to all `data-*` attributes on an element as a key-value object.

```html
<button id="btn" data-id="x" data-action="y">Delete</button>

<script>
  const btn = document.getElementById('btn');

  // Using dataset (modern way)
  console.log(btn.dataset.id);       // "x"
  console.log(btn.dataset.action);   // "y"

  // Using getAttribute (older, explicit way)
  console.log(btn.getAttribute('data-id'));      // "x"
  console.log(btn.getAttribute('data-action'));  // "y"
</script>
```

> **Note:** `dataset` values are always strings. Convert with `Number(btn.dataset.id)` if you need a number.

### Common Ways to Get Data from DOM

| Method | What it does |
|---|---|
| `getElementById('id')` | Select by id |
| `querySelector('.class')` | Select first match (CSS selector) |
| `querySelectorAll('li')` | Select all matches (returns NodeList) |
| `element.value` | Get value of input/select |
| `element.innerText` | Get visible text content |
| `element.dataset.key` | Get data-* attribute |

```js
// Read input value
const name = document.querySelector('#username').value;

// Read text
const msg = document.querySelector('#msg').innerText;

// Loop through list items
document.querySelectorAll('li').forEach(item => {
  console.log(item.innerText);
});
```

---

## 2. Reference vs Shallow Copy vs Deep Copy

In JavaScript, objects are stored by **reference**. Assigning an object to a new variable does NOT create a new object - both variables point to the same place in memory.

### Three Ways to "Copy" an Object

| Method | Type | Nested objects? |
|---|---|---|
| `b = a` | Reference | Fully shared - same object |
| `{ ...a }` or `Object.assign({}, a)` | Shallow Copy | Top level copied, nested still shared |
| Spread each level manually | Deep Copy | Fully independent |

```js
const original = { title: "Alice", address: { city: "Delhi" } };

const ref     = original;                                            // REFERENCE
const shallow = { ...original };                                     // SHALLOW COPY
const deep    = { title: original.title, address: { ...original.address } }; // DEEP COPY

ref.title = "Bob";           // original.title is now "Bob"   (same object!)
shallow.address.city = "Mumbai"; // original.address.city changes too! (nested shared)
deep.address.city = "Pune";  // original is NOT affected       (own copy of address)

console.log(original.title);        // "Bob"     changed via ref
console.log(original.address.city); // "Mumbai"  changed via shallow (trap!)
console.log(deep.address.city);     // "Pune"    independent
```

### The Shallow Copy Trap

`{ ...original }` looks like a full copy but nested objects are still shared references:

```
original --> { title: "Alice",  address: --> { city: "Delhi" } }
                                   ^
shallow  --> { title: "Alice",  address: --+  points to the SAME address object!

// So changing shallow.address.city also changes original.address.city
```

Fix: spread the nested object too:

```js
const deep = { ...original, address: { ...original.address } };
// Now deep.address is a brand new object - changes won't affect original
```

> **Quick rule:** `{ ...obj }` only copies the top level. Nested objects are still shared links. Spread every level for a true independent copy - or use `JSON.parse(JSON.stringify(obj))` for a quick deep clone of plain data.

```js
// Quick deep clone (works for plain data - no functions, no Date objects)
const deepClone = JSON.parse(JSON.stringify(original));
```

---

## 3. Normal Function vs Arrow Function (Strict Mode)

In strict mode, `this` depends on **how** the function is called. Arrow functions do not create their own `this`; they capture it from outer scope.

| Type | `this` behavior | Good for |
|---|---|---|
| Normal function | Set at call time | Methods that need dynamic `this` |
| Arrow function | Lexical (from parent scope) | Callbacks, preserving outer `this` |

### One Example with `fn()()`

```js
'use strict';

const accountBox = {
  owner: 'Riya',

  buildNormal: function () {
    console.log('outer normal this.owner =', this ? this.owner : undefined);

    return function () {
      console.log('inner normal this =', this); // strict mode: undefined in plain call
    };
  },

  buildArrow: function () {
    console.log('outer normal this.owner =', this ? this.owner : undefined);

    return () => {
      console.log('inner arrow this.owner =', this ? this.owner : undefined);
    };
  }
};

// Direct method call, then returned function call
accountBox.buildNormal()();
accountBox.buildArrow()();

// Detach method into variable, then call fn()()
const detachedNormal = accountBox.buildNormal;
const detachedArrow = accountBox.buildArrow;

detachedNormal()();
detachedArrow()();
```

### What Happens

```
1) accountBox.buildNormal()()
   - First call: method call, so outer this = accountBox
   - Returned inner normal is called as plain function, so this = undefined (strict mode)

2) accountBox.buildArrow()()
   - First call: outer this = accountBox
   - Returned arrow keeps outer this, so it still sees accountBox

3) detachedNormal()() and detachedArrow()()
   - Method is detached from object
   - First call is plain function, so outer this = undefined (strict mode)
   - Arrow also captures that undefined outer this
```

> **Quick rule:** In strict mode, extracting a method into a variable usually loses object binding. If object context is required, use `bind` (for example: `const safeFn = obj.method.bind(obj)`).

---

## 4. Promise Behaviour

A **Promise** represents a value that will be available in the future (async result). It has 3 states:

| State | Meaning |
|---|---|
| Pending | Still waiting (e.g. API call in progress) |
| Fulfilled | Success — `.then()` runs |
| Rejected | Error — `.catch()` runs |

```js
// Basic Promise
const p = new Promise((resolve, reject) => {
  const ok = true;
  if (ok) resolve("Data ready");
  else reject("Something failed");
});

p.then(data => console.log(data))   // "Data ready"
 .catch(err => console.error(err))
 .finally(() => console.log("Done")); // runs always
```

```js
// async / await (cleaner syntax for the same thing)
async function loadUser() {
  try {
    const res = await fetch('/api/user/1');
    const data = await res.json();
    console.log(data);
  } catch (err) {
    console.error('Error:', err);
  }
}
```

> **Remember:** `await` only works inside an `async` function. It pauses that function until the promise settles.

---

## 5. Async and Await

`async` and `await` are a cleaner way to work with Promises. They do not replace Promises; they are just easier syntax for reading async code.

| Keyword | Meaning |
|---|---|
| `async` | Makes a function return a Promise automatically |
| `await` | Pauses that async function until the Promise settles |

### How Promise Resolve / Reject Works

```js
const task = new Promise((resolve, reject) => {
  const finished = true;

  if (finished) {
    resolve('Work completed');
  } else {
    reject('Work failed');
  }
});

task
  .then(result => console.log(result))   // runs if resolved
  .catch(error => console.log(error));   // runs if rejected
```

**One-line rule:** In `new Promise((resolve, reject) => { ... })`, the first parameter is resolve and the second is reject; whichever one is called first settles the Promise.

A Promise has 3 states:

```
pending   = still waiting
resolved  = success, value goes to .then()
rejected  = error, value goes to .catch()
```

### Same Idea with async / await

```js
function fetchReport(statusOk) {
  return new Promise((resolve, reject) => {
    if (statusOk) {
      resolve('Report loaded');
    } else {
      reject('Server error');
    }
  });
}

async function loadReport() {
  try {
    const message = await fetchReport(true);
    console.log(message); // 'Report loaded'
  } catch (error) {
    console.log(error);   // runs if Promise is rejected
  }
}
```

### How It Works Step by Step

```
1) async function starts
2) await sees a Promise
3) JavaScript pauses only that function, not the whole program
4) If Promise resolves, await gives back the resolved value
5) If Promise rejects, control jumps to catch block
```

### Which Console Log Prints First? (then/catch vs await)

In both styles, handlers run in the **microtask queue**. If both Promises are already settled, the callback that is queued first runs first.

```js
function compareOrder(thenState, awaitState) {
  const pThen  = thenState  === 'resolve' ? Promise.resolve('THEN OK')  : Promise.reject('THEN ERR');
  const pAwait = awaitState === 'resolve' ? Promise.resolve('AWAIT OK') : Promise.reject('AWAIT ERR');

  // 1) Queue then/catch handler first
  pThen
    .then(v => console.log('then:', v))
    .catch(e => console.log('catch:', e));

  // 2) Then call async function (await continuation is queued after this starts)
  (async function () {
    try {
      const c = await pAwait;
      console.log('await:', c);
    } catch (e) {
      console.log('await catch:', e);
    }
  })();
}

// Case A: then resolve, await resolve
compareOrder('resolve', 'resolve');
// Output order:
// then: THEN OK
// await: AWAIT OK

// Case B: then reject, await resolve
compareOrder('reject', 'resolve');
// Output order:
// await: AWAIT OK
// catch: THEN ERR

// Case C: then resolve, await reject
compareOrder('resolve', 'reject');
// Output order:
// then: THEN OK
// await catch: AWAIT ERR

// Case D: then reject, await reject
compareOrder('reject', 'reject');
// Output order:
// await catch: AWAIT ERR
// catch: THEN ERR
```

> **Important:** In this example, output order depends on microtask scheduling, so `then(...).catch(...)` may log before or after `await` depending on how handlers are queued.

**One-line tip:** `then(success, error)` attaches the reject handler directly to the same Promise, while `then(...).catch(...)` handles rejection on the next chained Promise.

> **Quick rule:** Use `try...catch` with `await`. A resolved Promise gives a value; a rejected Promise throws an error.

---

## 6. Vue Directives: v-if and v-show

Vue directives are special attributes that start with `v-`. They tell Vue to do something in the template.

| Directive | What it does | Main difference |
|---|---|---|
| `v-if` | Adds or removes element from DOM | Element may not exist at all |
| `v-show` | Shows or hides with CSS | Element stays in DOM |

### One Toggle Example

```html
<div id="app">
  <button @click="togglePanel">Toggle</button>

  <p v-if="isVisible">This text uses v-if</p>
  <p v-show="isVisible">This text uses v-show</p>
</div>

<script>
new Vue({
  el: '#app',
  data: {
    isVisible: true
  },
  methods: {
    togglePanel() {
      this.isVisible = !this.isVisible;
    }
  }
});
</script>
```

### What Happens on Toggle

```
If isVisible = true:
  - v-if element is created and shown
  - v-show element is shown

If isVisible = false:
  - v-if element is removed from DOM
  - v-show element stays in DOM but becomes hidden (display: none)
```

> **Quick rule:** Use `v-if` when the condition changes less often. Use `v-show` when you need to show/hide frequently, because it only changes CSS.

---

## 7. Vue: data vs computed vs watch

Use this simple rule:

| Option | Use it for | Should have side effects? |
|---|---|---|
| `data` | Raw state you store and change | No (just values) |
| `computed` | Derived value from existing state | No (must return a value) |
| `watch` | Run logic when a value changes | Yes (API calls, timers, localStorage, etc.) |

### One Example (Search Box)

```js
new Vue({
  el: '#app',
  data: {
    keyword: '',           // data: actual user input
    products: ['Apple', 'Banana', 'Mango', 'Grapes'],
    typingMessage: ''
  },

  computed: {
    filteredProducts() {
      // computed: value derived from data
      const k = this.keyword.toLowerCase();
      return this.products.filter(p => p.toLowerCase().includes(k));
    }
  },

  watch: {
    keyword(newValue, oldValue) {
      // watch: reacts to change and performs side effect
      if (newValue !== oldValue) {
        this.typingMessage = 'Searching for: ' + newValue;
        // Example side effect: could call API here
        // fetch('/api/search?q=' + encodeURIComponent(newValue))
      }
    }
  }
});
```

### How to Think About It

```
data     = source (input values, arrays, flags)
computed = formula/result (auto recalculates, cached)
watch    = reaction ("when this changes, do something")
```

> **Exam tip:** If you need a value for template display, prefer `computed`. If you need to trigger an action because a value changed, use `watch`.

---

## 8. Vue Lifecycle Hooks

Lifecycle hooks are special methods Vue calls at different stages of a component's life.

| Hook | When it runs | Common Use |
|---|---|---|
| `beforeCreate` | Before data & events are set up | Rarely used |
| `created` | After data is ready, before DOM | API calls, set initial data |
| `beforeMount` | Before HTML is inserted | Rarely used |
| `mounted` | After HTML is in the page | DOM manipulation, third-party libs |
| `beforeUpdate` | Before re-render on data change | Capture old DOM state |
| `updated` | After re-render | React to DOM changes |
| `beforeDestroy` | Before component is removed | Clean up timers, listeners |
| `destroyed` | After component is removed | Final cleanup |

> **Analogy (easy memory trick):** Think of child component like a student entering and leaving a classroom.
> `beforeCreate`/`created` = student is being registered,
> `beforeMount`/`mounted` = student enters and sits in class,
> `beforeUpdate`/`updated` = student is already in class and changes notebook/work,
> `beforeDestroy`/`destroyed` = student leaves class.
> If student is outside (component removed with `v-if="false"`), no update can happen. That is why `updated` does not run when child is not visible via `v-if`.

```js
new Vue({
  data: { message: '' },

  created() {
    // Good place for API calls — data is ready
    fetch('/api/hello')
      .then(r => r.json())
      .then(d => { this.message = d.text; });
  },

  mounted() {
    // DOM is available here
    console.log(this.$el); // the root element
  },

  beforeDestroy() {
    // Clean up (e.g. clear setInterval)
    clearInterval(this.timer);
  }
});
```

> **Most used:** `created` (fetch data) and `mounted` (touch the DOM).

---

## 9. Vuex Store

Vuex is a **central state management** library for Vue 2. Think of it as a shared data container all components can read from and write to.

### 4 Core Concepts

| Concept | Role | Rule |
|---|---|---|
| `state` | Holds the data | Read-only directly |
| `getters` | Computed values from state | Like computed properties |
| `mutations` | Change the state | Must be synchronous |
| `actions` | Call mutations, can be async | Use for API calls |

```js
const store = new Vuex.Store({
  state: {
    count: 0,
    users: []
  },
  getters: {
    doubleCount: state => state.count * 2
  },
  mutations: {
    INCREMENT(state) { state.count++; },
    SET_USERS(state, users) { state.users = users; }
  },
  actions: {
    fetchUsers({ commit }) {
      fetch('/api/users')
        .then(res => res.json())
        .then(data => commit('SET_USERS', data));
    }
  }
});

// Inside a Vue component:
this.$store.state.count          // read state
this.$store.getters.doubleCount  // read getter
this.$store.commit('INCREMENT')  // call mutation
this.$store.dispatch('fetchUsers') // call action
```

**Where to use commit and dispatch:** Use `this.$store.commit(...)` inside component methods/watch/hooks when you want to change state using a mutation. Use `this.$store.dispatch(...)` inside component methods/watch/hooks when you want to run an action (usually async), which then commits a mutation.

**Template usage tip:** You can read Vuex state directly in template using `{{ $store.state.count }}` and getters using `{{ $store.getters.doubleCount }}`. For bigger components, many teams prefer mapping state/getters into computed properties for cleaner templates.

> **Rule of thumb:** Never mutate state directly. Always go through mutations (or actions -> mutations).

---

## 10. Props, Emit, RouterLink, RouterView

These four concepts are often used together in Vue apps:

| Concept | Direction | Use |
|---|---|---|
| `props` | Parent -> Child | Pass data down |
| `emit` | Child -> Parent | Send event up |
| `<router-link>` | Navigation | Move between routes without page reload |
| `<router-view>` | Rendering area | Shows the component matched by current route |

### One Connected Example

```html
<div id="app">
  <!-- router-link creates SPA navigation links -->
  <router-link to="/home">Home</router-link>
  <router-link to="/profile">Profile</router-link>

  <!-- router-view is where current route component appears -->
  <router-view></router-view>
</div>

<script>
// Child component
const UserCard = {
  props: ['displayName'], // receive data from parent
  template: `
    <div>
      <p>User: {{ displayName }}</p>
      <button @click="$emit('rename', 'Updated Name')">Rename</button>
    </div>
  `
};

// Route component (acts as parent for UserCard)
const ProfilePage = {
  components: { UserCard },
  data() {
    return {
      currentName: 'First Name'
    };
  },
  methods: {
    onRename(newName) {
      this.currentName = newName;
    }
  },
  template: `
    <div>
      <h3>Profile Page</h3>
      <user-card
        :display-name="currentName"
        @rename="onRename"
      ></user-card>
    </div>
  `
};

const HomePage = { template: '<h3>Home Page</h3>' };

const router = new VueRouter({
  routes: [
    { path: '/home', component: HomePage },
    { path: '/profile', component: ProfilePage },
    { path: '*', redirect: '/home' }
  ]
});

new Vue({
  el: '#app',
  router
});
</script>
```

### Flow in Simple Words

```
1) Click Profile router-link -> route changes to /profile
2) router-view renders ProfilePage
3) ProfilePage passes currentName to UserCard via prop (displayName)
4) Child button triggers $emit('rename', 'Updated Name')
5) Parent catches @rename and runs onRename(newName)
6) Parent state updates, UI re-renders with new name
```

> **Quick rule:** Data goes down with props, events go up with emit. `router-link` changes route; `router-view` displays the matched component.

---

## 11. Security with JWT

JWT (JSON Web Token) is used for **stateless authentication**. The server issues a token; the client sends it back with every request to prove identity.

### JWT Structure

A JWT looks like: `xxxxx.yyyyy.zzzzz` — three Base64-encoded parts joined by dots.

| Part | Contains |
|---|---|
| Header | Algorithm type (e.g. HS256) |
| Payload | User data (id, role, expiry) — *not secret!* |
| Signature | Hash of header+payload using a secret key — *tamper-proof* |

### Typical Flow

```js
// 1. User logs in -> server returns a JWT
POST /api/login  ->  { token: "eyJ..." }

// 2. Client stores the token
localStorage.setItem('token', data.token);

// 3. Client sends token with every protected request
fetch('/api/profile', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('token')
  }
});

// 4. Server verifies the token - if valid, returns data
//    If expired or tampered -> 401 Unauthorized
```

### Key Security Rules Overall Based on Token/Session

| Rule | Why |
|---|---|
| Always use HTTPS | Prevent token interception |
| Set short expiry (`exp`) | Limit damage if token is stolen |
| Never put passwords in payload | Payload is Base64 - readable by anyone |
| Use `httpOnly` cookie over localStorage (when possible) | Protects against XSS attacks |
| Validate token on every request (server-side) | Ensures token is genuine |

> **Remember:** JWT proves *who* the user is, but the payload is not encrypted — do not store sensitive data in it.

### Simple Analogy

> **JWT is like a signed ID card.**
> Anyone can read what is written on it (payload is Base64, not encrypted).
> But only the server (the issuer) can verify if the signature is genuine.
> If someone tampers with the card, the signature will not match and the server will reject it.

**Key points in plain words:**

1. JWT is not bad — it is safe for identity, just not for secrets
2. Payload is readable by anyone (just Base64-decode it) — never put passwords or sensitive data there
3. Security comes from the server **verifying the signature**, not from hiding the payload
4. If you must store a token on the client, prefer an `httpOnly` cookie over `localStorage` — `httpOnly` cookies cannot be read by JavaScript, which protects against XSS attacks
5. Always set a short expiry (`exp`) — if a token is stolen, it becomes useless quickly
