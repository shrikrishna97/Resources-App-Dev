# Single File Components (SFC) with Vite + Vue 3 - Complete Beginner's Guide

A comprehensive guide to get started with Vite and Vue 3 Single File Components from scratch.

> **Note:** Vue CLI is no longer maintained. This guide uses **Vite** - the modern, faster build tool recommended for Vue projects.

> **About Vue 2:** Vite only scaffolds **Vue 3** projects. Vue 2 is not available as an option. Since Vue 3 is the current version and Vue 2 reached End of Life (Dec 2023), we use Vue 3.

---

## Table of Contents

1. [What is Vite?](#what-is-vite)
2. [Vue CLI vs Vite](#vue-cli-vs-vite)
3. [What are Single File Components?](#what-are-single-file-components)
4. [Prerequisites Installation](#prerequisites-installation)
5. [Creating Your First Project](#creating-your-first-project)
6. [Understanding Project Structure](#understanding-project-structure)
7. [Understanding Key JavaScript Concepts](#understanding-key-javascript-concepts)
8. [Single File Component Anatomy](#single-file-component-anatomy)
   - [Understanding `<script setup>`](#understanding-script-setup)
   - [Understanding `scoped` in `<style>`](#understanding-scoped-in-style)
9. [Example Project: Book Library Manager](#example-project-book-library-manager)
10. [Common Issues & Troubleshooting](#common-issues--troubleshooting)
11. [Useful Commands Reference](#useful-commands-reference)
12. [Vue Router](#vue-router)

---

## What is Vite?

**Vite** (French word for "fast", pronounced `/vit/`) is the next-generation build tool for modern web projects. It provides:

- Instant server start (no bundling during development)
- Lightning-fast Hot Module Replacement (HMR)
- Optimized production builds using Rollup
- Native ES modules support
- Much faster than Vue CLI/Webpack

---

## Vue CLI vs Vite

| Feature | Vue CLI (Old) | Vite (Modern) |
|---------|---------------|---------------|
| Status | ⚠️ No longer maintained | ✅ Actively maintained |
| Dev Server Start | Slow (bundles everything) | Instant (no bundling) |
| Hot Reload | Slower | Near-instant |
| Build Tool | Webpack | Rollup (optimized) |
| Configuration | Complex | Simple |

**Why use Vite?** Vue CLI is deprecated. Vite is the official recommendation from the Vue team.

---

## What are Single File Components?

**Single File Components (SFC)** are `.vue` files that contain three sections:

```vue
<template>
  <!-- HTML structure -->
</template>

<script>
// JavaScript logic
</script>

<style>
/* CSS styling */
</style>
```

**Benefits:**
- All component code in one file
- Scoped CSS (styles apply only to that component)
- Better organization and maintainability
- Syntax highlighting and IDE support

---

## Prerequisites Installation

### Step 1: Install Node.js and npm

Node.js includes npm (Node Package Manager). You need Node.js version **16.x or higher**.

---

### For Windows Users

**Option A: Direct Download (Recommended for Beginners)**

1. Go to [https://nodejs.org](https://nodejs.org)
2. Download the **LTS** (Long Term Support) version
3. Run the installer (.msi file)
4. Click "Next" through all steps (keep defaults)
5. Check "Automatically install necessary tools" if prompted
6. Click "Install" and wait for completion

**Option B: Using Chocolatey (Package Manager)**

```powershell
# First install Chocolatey (run PowerShell as Administrator)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Then install Node.js
choco install nodejs-lts
```

**Option C: Using winget (Windows 11)**

```powershell
winget install OpenJS.NodeJS.LTS
```

---

### For macOS Users

**Option A: Direct Download**

1. Go to [https://nodejs.org](https://nodejs.org)
2. Download the **LTS** version for macOS
3. Run the .pkg installer
4. Follow installation prompts

**Option B: Using Homebrew (Recommended)**

```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js
brew install node
```

**Option C: Using nvm (Node Version Manager)**

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart terminal, then install Node
nvm install --lts
nvm use --lts
```

---

### For Linux Users (Ubuntu/Debian)

**Option A: Using apt (Default repositories - may be older version)**

```bash
sudo apt update
sudo apt install nodejs npm
```

**Option B: Using NodeSource (Recommended - Latest LTS)**

```bash
# Download and run NodeSource setup script
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -

# Install Node.js
sudo apt install -y nodejs
```

**Option C: Using nvm (Most Flexible)**

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Close and reopen terminal, then:
nvm install --lts
nvm use --lts
```

---

### Step 2: Verify Installation

Open a **new terminal/command prompt** and run:

```bash
node --version
# Should show something like: v20.x.x

npm --version
# Should show something like: 10.x.x
```

If you see version numbers, you're ready to proceed!

---

## Creating Your First Project (Vite + Vue 3)

Unlike Vue CLI, Vite doesn't need global installation. You create projects directly with npm.

### Step 1: Create Project with Vite

```bash
npm create vite@latest my-vue-app
```

**Interactive prompts will appear:**

```
◇  Select a framework:
│  Vue
```

```
◇  Select a variant:
│  Official Vue Starter ↗    ← Select this (recommended!)
```

This launches `create-vue` which gives you more options:

```
◇  Use TypeScript?
│  No

◇  Select features to include in your project:
│  ◻ Router (SPA development)      ← Select if you need routing
│  ◻ Pinia (state management)
│  ◻ Vitest (unit testing)
│  ◻ End-to-End Testing
│  ◻ Linter (error prevention)     ← Recommended
│  ◻ Prettier (code formatting)    ← Recommended

◇  Select experimental features:
│  none

◇  Skip all example code and start with a blank Vue project?
│  No
```

**Recommended selections for beginners:**
- ✅ Router (if building multi-page app)
- ✅ Linter (helps catch errors)
- ✅ Prettier (auto-formats code)

### Step 2: Navigate and Install

```bash
cd my-vue-app
npm install
```

### Step 3: Format and Run

```bash
npm run format    # Format code with Prettier (if selected)
npm run dev       # Start development server
```

**Output:**

```
  VITE v5.x.x  ready in 300 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.1.5:5173/
  ➜  press h + enter to show help
```

Open `http://localhost:5173` in your browser!

**To stop the server:** Press `Ctrl + C`

---

## Quick Reference: All Commands

```bash
# Create project with Router, Linter, Prettier
npm create vite@latest my-vue-app
# Select: Vue → Official Vue Starter
# Select features: Router, Linter, Prettier

cd my-vue-app
npm install
npm run format
npm run dev
```

**Alternative (minimal setup without Router):**
```bash
npm create vite@latest my-vue-app
# Select: Vue → JavaScript

cd my-vue-app
npm install
npm run dev
```

---

## Understanding Project Structure (Official Vue Starter)

When you select **Router, ESLint, Prettier** during setup:

```
my-vue-app/
├── node_modules/        # Dependencies (don't touch)
├── public/              # Static assets (favicon.ico)
├── index.html           # Entry HTML (at root, not in public/)
├── vite.config.js       # Vite configuration
├── package.json         # Project dependencies & scripts
├── jsconfig.json        # JavaScript project config
├── eslint.config.js     # ESLint configuration
├── .prettierrc.json     # Prettier configuration
└── src/
    ├── assets/          # CSS files, images, logo.svg
    ├── components/      # Reusable Vue components
    │   ├── HelloWorld.vue
    │   └── icons/       # Icon components
    ├── router/          # Vue Router configuration
    │   └── index.js     # Route definitions
    ├── views/           # Page components (routed)
    │   ├── HomeView.vue
    │   └── AboutView.vue
    ├── App.vue          # Root component
    └── main.js          # Entry point
```

**Key Points:**
- `router/` folder contains route configurations
- `views/` folder contains page-level components
- `components/` folder for reusable components
- `index.html` is at project root (not in `public/`)

### Key Files Explained

**`vite.config.js`** - Vite configuration:

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()]  // Enable Vue 3 SFC support
})
```

**`index.html`** - Entry HTML file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Vue 3 + Vite App</title>
</head>
<body>
  <div id="app"></div>
  <!-- Note: type="module" is required for Vite -->
  <script type="module" src="/src/main.js"></script>
</body>
</html>
```

**`src/main.js`** - The entry point that mounts Vue with Router:

```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'   // Import router from router/index.js

const app = createApp(App)      // Create Vue application instance
app.use(router)                 // Register Router plugin
app.mount('#app')               // Mount to DOM element with id="app"
```

**Without Router (minimal setup):**
```javascript
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
```

**`src/App.vue`** - The root component that holds all other components.

---

## Understanding Key JavaScript Concepts

Before diving deeper, let's understand some important JavaScript/ES6 concepts used in Vue:

### `import` Statement

`import` is used to bring code from other files into your current file.

```javascript
// Import a named export (Vue 3 style)
import { createApp } from 'vue'

// Import the default export and name it "App"
import App from './App.vue'

// Import from a folder (looks for index.js inside)
import router from './router'

// Import specific named exports
import { createRouter, createWebHistory } from 'vue-router'
```

**Path types:**
- `'vue'` - From node_modules (installed package)
- `'./App.vue'` - Relative path (same folder)
- `'../views/Home.vue'` - Go up one folder, then into views

---

### `export default`

`export default` makes something available to other files. Each file can have **only one** default export.

```javascript
// In StudentCard.vue
export default {
  name: 'StudentCard',
  props: { ... },
  methods: { ... }
}

// Now another file can import it:
import StudentCard from './components/StudentCard.vue'
```

**Why use it?**
- Allows modular code (split into multiple files)
- Each component lives in its own .vue file
- Easy to reuse components across projects

---

### `app.use()` (Vue 3)

`app.use()` installs a Vue plugin. Plugins add global functionality.

```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// Install plugins
app.use(router)

app.mount('#app')

// Now you can use <router-view> and <router-link> in templates
```

> **Vue 2 vs Vue 3:**
> - Vue 2: `Vue.use(VueRouter)`
> - Vue 3: `app.use(router)`

---

### Router History Mode (Vue 3)

The router history mode controls how URLs look:

| Mode | URL Example | Description |
|------|-------------|-------------|
| `createWebHashHistory()` | `http://example.com/#/about` | Uses hash (#) - works everywhere, no server config |
| `createWebHistory()` | `http://example.com/about` | Clean URLs - needs server configuration |

```javascript
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),  // Clean URLs without #
  routes
})
```

**Note:** `createWebHistory()` requires server setup in production to redirect all routes to `index.html`.

---

### `createApp()` and `.mount()` (Vue 3)

Vue 3 uses a simpler mounting syntax:

```javascript
import { createApp } from 'vue'
import App from './App.vue'

// Create and mount in one line
createApp(App).mount('#app')

// Or with router/plugins:
import router from './router'

const app = createApp(App)
app.use(router)
app.mount('#app')  // Attach to <div id="app"></div>
```

> **Vue 2 vs Vue 3:**
> - Vue 2: `new Vue({ render: h => h(App) }).$mount('#app')`
> - Vue 3: `createApp(App).mount('#app')`

---

### Lazy Loading with `() => import()`

Loads a component only when needed (improves initial load time):

```javascript
const routes = [
  {
    path: '/',
    component: HomeView  // Loaded immediately
  },
  {
    path: '/about',
    // Lazy loaded - only downloads when user visits /about
    component: () => import('../views/AboutView.vue')
  }
]
```

---

## Single File Component Anatomy

Every `.vue` file has three optional sections:

```vue
<template>
  <!-- Required: HTML template -->
  <div class="my-component">
    <h1>{{ title }}</h1>
    <button @click="handleClick">Click Me</button>
  </div>
</template>

<script>
// Optional: JavaScript logic
export default {
  name: 'MyComponent',
  
  // Component data (reactive state)
  data() {
    return {
      title: 'Hello Vue!'
    }
  },
  
  // Methods (functions)
  methods: {
    handleClick() {
      alert('Button clicked!')
    }
  },
  
  // Computed properties
  computed: {
    // ...
  },
  
  // Lifecycle hooks
  mounted() {
    console.log('Component mounted!')
  }
}
</script>

<style scoped>
/* Optional: CSS styles */
/* "scoped" means styles only apply to this component */

.my-component {
  padding: 20px;
}

h1 {
  color: #42b983;
}
</style>
```

### Important Rules

1. **Vue 3: Multiple root elements allowed** (unlike Vue 2)
   ```vue
   <!-- Vue 3: Multiple roots OK! -->
   <template>
     <h1>Title</h1>
     <p>Content</p>
   </template>

   <!-- Also fine: single root -->
   <template>
     <div>
       <h1>Title</h1>
       <p>Content</p>
     </div>
   </template>
   ```

2. **`data` must be a function** (not an object):
   ```javascript
   // CORRECT
   data() {
     return {
       count: 0
     }
   }

   // WRONG
   data: {
     count: 0
   }
   ```

3. **Use `scoped` for component-specific styles**:
   ```vue
   <style scoped>
   /* Only affects this component */
   </style>
   ```

---

### Understanding `<script setup>`

Vue 3 introduced `<script setup>` as a simpler way to write components. It's **compile-time syntactic sugar** that makes code shorter and cleaner.

**Regular `<script>` (Options API):**
```vue
<script>
export default {
  data() {
    return {
      count: 0
    }
  },
  methods: {
    increment() {
      this.count++
    }
  }
}
</script>
```

**With `<script setup>` (Composition API):**
```vue
<script setup>
import { ref } from 'vue'

const count = ref(0)

function increment() {
  count.value++
}
</script>
```

**Key Differences:**

| Feature | `<script>` (Options API) | `<script setup>` |
|---------|--------------------------|------------------|
| Syntax | `export default { ... }` | Just write code directly |
| Variables | Inside `data()` return | Top-level `const` with `ref()` |
| Methods | Inside `methods: { ... }` | Regular functions |
| Access data | `this.count` | `count.value` |
| Imports | Must register in `components: {}` | Auto-registered |
| Code length | More boilerplate | Shorter, cleaner |

**When to use which:**
- **`<script>` (Options API)**: Easier for beginners, familiar structure
- **`<script setup>`**: Less code, better performance, preferred for new projects

**Example with imports:**
```vue
<!-- With <script setup>, imported components are auto-registered -->
<script setup>
import BookCard from './components/BookCard.vue'
import { ref } from 'vue'

const books = ref([])  // No need to register BookCard in components: {}
</script>

<template>
  <BookCard v-for="book in books" :key="book.id" :book="book" />
</template>
```

> **Note:** This guide uses Options API (`<script>`) for clarity. Both styles work in Vue 3.

---

### Understanding `scoped` in `<style>`

The `scoped` attribute makes CSS styles **apply only to the current component**. Without it, styles would be global and could affect other components.

**How it works:**

```vue
<!-- MyButton.vue -->
<template>
  <button class="btn">Click Me</button>
</template>

<style scoped>
.btn {
  background: blue;
  color: white;
}
</style>
```

Vue compiles this to:

```html
<button class="btn" data-v-7ba5bd90>Click Me</button>

<style>
.btn[data-v-7ba5bd90] {
  background: blue;
  color: white;
}
</style>
```

**What Vue does:**
1. Adds a unique attribute (`data-v-xxxx`) to all elements in the component
2. Adds the same attribute to CSS selectors
3. This ensures styles only match elements in THIS component

**Comparison:**

| Style Type | Scope | Use Case |
|------------|-------|----------|
| `<style>` | Global (entire app) | Base styles, resets |
| `<style scoped>` | Component only | Component-specific styles |

**Example showing the difference:**

```vue
<!-- ComponentA.vue -->
<template>
  <p class="text">I am Component A</p>
</template>
<style scoped>
.text { color: red; }  /* Only affects ComponentA */
</style>

<!-- ComponentB.vue -->
<template>
  <p class="text">I am Component B</p>
</template>
<style scoped>
.text { color: blue; }  /* Only affects ComponentB */
</style>
```

Both components use `.text` class but have different colors - no conflict!

**Best Practice:** Always use `<style scoped>` unless you intentionally want global styles.

---

## Example Project: Book Library Manager

Let's build a simple Book Library application to understand SFCs. **Focus is on Vue concepts, not styling.**

### Step 1: Create the Project

Follow the Vite + Vue 3 setup from earlier, naming your project `book-library`.

```bash
npm create vite@latest book-library
# Select: Vue → JavaScript
cd book-library
npm install
npm run dev
```

### Step 2: Replace `src/App.vue`

```vue
<template>
  <div id="app">
    <h1>Book Library</h1>
    
    <!-- Search Input -->
    <input 
      v-model="searchQuery" 
      placeholder="Search books..." 
    />
    <button @click="addBook">Add Book</button>
    
    <!-- Book Count -->
    <p>Total Books: {{ totalBooks }}</p>

    <!-- Book List -->
    <BookCard 
      v-for="book in filteredBooks" 
      :key="book.id"
      :book="book"
      @delete="deleteBook"
      @toggle-read="toggleRead"
    />

    <p v-if="filteredBooks.length === 0">No books found.</p>
  </div>
</template>

<script>
// Import the BookCard component
import BookCard from './components/BookCard.vue'

// Export this component so main.js can use it
export default {
  // Component name (useful for debugging)
  name: 'App',
  
  // Register child components
  components: {
    BookCard
  },

  // Reactive data - changes trigger re-render
  data() {
    return {
      searchQuery: '',
      nextId: 4,
      books: [
        { id: 1, title: 'The Alchemist', author: 'Paulo Coelho', isRead: true },
        { id: 2, title: 'Atomic Habits', author: 'James Clear', isRead: false },
        { id: 3, title: 'Deep Work', author: 'Cal Newport', isRead: false }
      ]
    }
  },

  // Computed properties - auto-update when dependencies change
  computed: {
    // Filter books based on search
    filteredBooks() {
      const query = this.searchQuery.toLowerCase()
      return this.books.filter(book => 
        book.title.toLowerCase().includes(query) ||
        book.author.toLowerCase().includes(query)
      )
    },
    
    // Count total books
    totalBooks() {
      return this.books.length
    }
  },

  // Methods - functions called from template
  methods: {
    addBook() {
      const title = prompt('Enter book title:')
      if (!title) return
      
      const author = prompt('Enter author name:') || 'Unknown'
      
      // Push new book to array (Vue detects this)
      this.books.push({
        id: this.nextId++,
        title: title,
        author: author,
        isRead: false
      })
    },

    // Called when child emits 'delete' event
    deleteBook(bookId) {
      this.books = this.books.filter(b => b.id !== bookId)
    },

    // Called when child emits 'toggle-read' event
    toggleRead(bookId) {
      const book = this.books.find(b => b.id === bookId)
      if (book) {
        book.isRead = !book.isRead
      }
    }
  }
}
</script>
```

**Code Explanation:**

| Part | Purpose |
|------|----------|
| `import BookCard from...` | Brings BookCard component into this file |
| `export default { }` | Makes this component available to other files |
| `name: 'App'` | Component name (shown in Vue DevTools) |
| `components: { BookCard }` | Registers BookCard so we can use `<BookCard />` in template |
| `data()` | Returns reactive state - Vue watches these for changes |
| `computed` | Cached values that auto-update when dependencies change |
| `methods` | Functions you can call from template or other methods |

### Step 3: Create BookCard Component

**Create `src/components/BookCard.vue`:**

```vue
<template>
  <div style="border: 1px solid #ccc; padding: 15px; margin: 10px 0;">
    <!-- Book Title -->
    <h3>{{ book.title }}</h3>
    <p>by {{ book.author }}</p>
    
    <!-- Read Status -->
    <p>
      Status: 
      <strong :style="{ color: book.isRead ? 'green' : 'red' }">
        {{ book.isRead ? 'Read' : 'Not Read' }}
      </strong>
    </p>
    
    <!-- Action Buttons -->
    <button @click="$emit('toggle-read', book.id)">
      {{ book.isRead ? 'Mark Unread' : 'Mark Read' }}
    </button>
    
    <button @click="$emit('delete', book.id)">
      Delete
    </button>
  </div>
</template>

<script>
export default {
  // Component name (shown in Vue DevTools)
  name: 'BookCard',
  
  // Props: Data received from parent component
  // Parent uses :book="bookObject" to pass data
  props: {
    book: {
      type: Object,      // Expected data type
      required: true     // Must be provided
    }
  },
  
  // Vue 3 best practice: declare emitted events
  emits: ['toggle-read', 'delete']
}
</script>
```

**Code Explanation:**

| Part | Purpose |
|------|----------|
| `props: { book: {...} }` | Declares what data this component expects from parent |
| `:book="book"` | Parent passes data using v-bind (`:` is shorthand) |
| `@click="$emit('delete', book.id)"` | Sends 'delete' event to parent with book.id |
| `@delete="deleteBook"` | Parent listens and calls deleteBook method |
| `:style="{ color: ... }"` | Dynamic inline style based on condition |

---

### Step 4: Run the Application

```bash
npm run dev
```

Open `http://localhost:5173` to see your Book Library!

---

## Parent-Child Communication Summary

```
┌─────────────────────────────────────────────────────────────┐
│                     PARENT (App.vue)                        │
│                                                             │
│  data: { books: [...] }                                    │
│  methods: { deleteBook(id) { ... } }                      │
│                                                             │
│  <BookCard                                                 │
│    :book="book"           ──────────► PROPS (data down)   │
│    @delete="deleteBook"   ◄────────── EVENTS (data up)    │
│  />                                                        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   CHILD (BookCard.vue)                     │
│                                                             │
│  props: { book: Object }                                   │
│                                                             │
│  <button @click="$emit('delete', book.id)">               │
│    Delete                                                  │
│  </button>                                                 │
└─────────────────────────────────────────────────────────────┘
```

**Key Points:**
- **Props** = Data flows DOWN (parent → child)
- **Events ($emit)** = Data flows UP (child → parent)
- Child cannot modify props directly (read-only)

---

## Common Issues & Troubleshooting

### Issue 1: "npm: command not found" or "'npm' is not recognized"

**Cause:** Node.js not installed or PATH not set.

**Solutions:**

```bash
# Check if Node.js is installed
node -v
npm -v
```

If not found:
1. Download from https://nodejs.org
2. Run installer with default options
3. **Windows:** Close and reopen terminal, or restart computer
4. **Mac/Linux:** Run `source ~/.bashrc` or `source ~/.zshrc`

---

### Issue 2: "npm ERR! EACCES permission denied"

**Linux/Mac Solution:**

```bash
# Option 1: Fix npm permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Option 2: Use sudo (not recommended for global installs)
sudo npm install package-name
```

---

### Issue 3: "Module not found: Error: Can't resolve..."

**Cause:** Missing import or incorrect path.

**Solution:**
- Check import path is correct
- Ensure file extension for .vue files
- Check component is registered:

```javascript
import MyComponent from './components/MyComponent.vue'

export default {
  components: {
    MyComponent  // Must register!
  }
}
```

---

### Issue 4: Port 8080 Already in Use

**Solution:**

```bash
# Use a different port (Vite will auto-select another, or specify)
npm run dev -- --port 3000
```

Or change in `vite.config.js`:
```javascript
export default defineConfig({
  plugins: [vue2()],
  server: {
    port: 3000
  }
})
```

---

### Issue 5: "ENOSPC: System limit for number of file watchers reached"

**Linux Solution:**

```bash
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

---

### Issue 6: Node Version Too Old

**Check version:**
```bash
node --version
```

**Update Node:**
- Windows: Download new installer from nodejs.org
- Mac: `brew upgrade node`
- Linux with nvm: `nvm install --lts`

---

### Issue 7: "Error: Cannot find module 'vue'"

**Solution:**

```bash
# Delete node_modules and reinstall
rm -rf node_modules
rm package-lock.json
npm install
```

**Windows:**
```powershell
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

---

### Issue 8: ESLint Errors Blocking Build

**Note:** Vite doesn't include ESLint by default. If you add ESLint and get:

**Common error:** `Component name should always be multi-word`

**Fix the warning properly:**
```javascript
// Use multi-word names
name: 'AppHeader'  // Good
name: 'Header'     // Bad (single word)
```

Or add to `.eslintrc.js`:
```javascript
rules: {
  'vue/multi-word-component-names': 'off'
}
```

---

### Issue 9: Hot Reload Not Working

**Solutions:**
1. Save the file (Ctrl+S)
2. Clear browser cache (Ctrl+Shift+R)
3. Restart dev server (Ctrl+C, then `npm run dev`)
4. Check file is inside `src/` folder
5. Make sure `vite.config.js` has the Vue plugin configured

---

### Issue 10: "digital envelope routines::unsupported" (Webpack only)

**Note:** This issue is specific to Webpack (Vue CLI). Vite uses esbuild and doesn't have this problem!

If you're migrating from Vue CLI and see this:
- Just switch to Vite (this guide) - problem solved!

---

## Useful Commands Reference

| Command | Description |
|---------|-------------|
| `npm run dev` | Start Vite development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build locally |
| `npm run format` | Format code with Prettier (if installed) |
| `npm run lint` | Check code with ESLint (if installed) |
| `npm install package-name` | Install a dependency |

---

## Vue Router

Vue Router lets you create multi-page applications with client-side routing.

### Option 1: Select Router During Project Creation (Recommended!)

When running `npm create vite@latest`, select:
- **Vue** → **Official Vue Starter**
- Check **Router (SPA development)**

This automatically creates:
- `src/router/index.js` - Router configuration
- `src/views/HomeView.vue` - Home page
- `src/views/AboutView.vue` - About page
- Updated `main.js` with router
- Updated `App.vue` with `<RouterView>` and `<RouterLink>`

**You're done!** Router is ready to use.

---

### Option 2: Add Router Manually (if not selected during setup)

If you didn't select Router during project creation:

#### Step 1: Install Vue Router

```bash
npm install vue-router@4
```

#### Step 2: Create Views

Create `src/views/HomeView.vue`:

```vue
<template>
  <div>
    <h1>Home Page</h1>
    <p>Welcome to the home page!</p>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>
```

Create `src/views/AboutView.vue`:

```vue
<template>
  <div>
    <h1>About Page</h1>
    <p>This is the about page.</p>
  </div>
</template>

<script>
export default {
  name: 'AboutView'
}
</script>
```

#### Step 3: Create Router Configuration

Create `src/router/index.js`:

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  { 
    path: '/', 
    name: 'home',
    component: HomeView 
  },
  { 
    path: '/about', 
    name: 'about',
    // Lazy loading - loads only when user visits /about
    component: () => import('../views/AboutView.vue') 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

#### Step 4: Update `src/main.js`

```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)
app.mount('#app')
```

#### Step 5: Update `src/App.vue`

```vue
<template>
  <header>
    <nav>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/about">About</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>
```

#### Step 6: Run and Test

```bash
npm run dev
```

Click the navigation links - the page content changes without full reload!

---

### Router Concepts Summary

| Concept | Description |
|---------|-------------|
| `<RouterLink to="/">` | Creates navigation links (no page reload) |
| `<RouterView />` | Placeholder where matched component renders |
| `app.use(router)` | Installs the router plugin |
| `createWebHistory()` | Clean URLs (`/about` instead of `/#/about`) |
| `() => import(...)` | Lazy loading - component loads only when needed |

---

## VS Code Extensions for Vue

Install these for better development experience:

1. **Vue - Official (Volar)** - Vue 3 language support (essential!)
2. **ESLint** - Code linting (included if you selected Linter)
3. **Prettier** - Code formatting (included if you selected Prettier)
4. **Path Intellisense** - Autocomplete file paths

---

## Project Commands Quick Reference

```bash
# Create project with Router, Linter, Prettier (Recommended)
npm create vite@latest my-app
# Select: Vue → Official Vue Starter
# Select features: Router, Linter, Prettier
cd my-app
npm install
npm run format
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## Summary

1. **Install Node.js** (includes npm) from nodejs.org
2. **Create project** with `npm create vite@latest`
   - Select **Vue** → **Official Vue Starter**
   - Select features: **Router**, **Linter**, **Prettier**
3. **Run** `npm install` then `npm run dev`
4. **Single File Components** have three sections: `<template>`, `<script>`, `<style scoped>`
5. **Vue 3 allows multiple root elements** in templates
6. **Components communicate** via props (parent → child) and events (child → parent)


