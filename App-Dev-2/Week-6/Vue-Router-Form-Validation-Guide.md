# Vue Router & Form Validation - Quick Guide

## 1. History Mode

### Hash Mode (Default) vs History Mode

| Mode | URL | When to Use |
|------|-----|-----------|
| Hash | `#/home` | Development, GitHub Pages |
| History | `/home` | Production, when you control server |

### Enable History Mode
```javascript
const router = new VueRouter({
  mode: 'history',  // Clean URLs
  routes
})
```

### ⚠️ Important: Server Configuration
History mode needs server to serve `index.html` for all unknown routes:

```javascript
// Express example
app.get('*', (req, res) => {
  res.sendFile('index.html')
})
```

Without this, direct URL visits will 404.

---

## 2. Form Validation

### Basic Validation Example
```javascript
const Home = {
    template: `
    <div>
        <h3>Home Component - User Registration Form</h3>
        <form @submit.prevent="submitForm">
            <div>
                <label>Name:</label>
                <input v-model="form.name" @blur="validateName" placeholder="Enter name (min 3 chars)">
                <span v-if="errors.name" style="color: red;">{{ errors.name }}</span>
            </div>
            
            <div>
                <label>Password:</label>
                <input v-model="form.password" @blur="validatePassword" type="password" placeholder="Enter password (min 6 chars)">
                <span v-if="errors.password" style="color: red;">{{ errors.password }}</span>
            </div>
            
            <button type="submit" :disabled="!isFormValid">Submit</button>
        </form>
    </div>
    `,
    data() {
        return {
            form: { name: '', password: '' },
            errors: { name: '', password: '' }
        }
    },
    computed: {
        isFormValid() {
            return this.form.name && this.form.password && 
                   !this.errors.name && !this.errors.password
        }
    },
    methods: {
        validateName() {
            this.errors.name = this.form.name.length < 3 ? 'Min 3 chars' : ''
        },
        validatePassword() {
            this.errors.password = this.form.password.length < 6 ? 'Min 6 chars' : ''
        },
        submitForm() {
            this.validateName()
            this.validatePassword()
            if (this.isFormValid) {
                // Send name & password to About page via route params
                this.$router.push(`/about/${this.form.password}/${this.form.name}`)
                this.form.name = ''
                this.form.password = ''
            }
        }
    }
}
```

**Key Points:**
- `@blur="validateName"` - Validates when user leaves field
- `v-if="errors.name"` - Shows error message if validation fails
- `:disabled="!isFormValid"` - Disables submit button until form is valid
- `submitForm()` - Validates all fields before submission

### What is `computed` doing here?

```javascript
computed: {
    isFormValid() {
        return this.form.name && this.form.password && 
               !this.errors.name && !this.errors.password
    }
}
```

`computed` is a special Vue option that defines **reactive derived values** — values that are automatically recalculated whenever the data they depend on changes.

**Why not just use a method?**

| | `computed` | `method` |
|--|--|--|
| Re-runs when? | Only when `form.name`, `form.password`, `errors` change | Every time the template re-renders |
| Cached? | ✅ Yes | ❌ No |
| Usage in template | `{{ isFormValid }}` | `{{ isFormValid() }}` |

**What `isFormValid` checks:**
```javascript
this.form.name          // name field is not empty
&& this.form.password   // password field is not empty
&& !this.errors.name    // no name validation error
&& !this.errors.password // no password validation error
```

All 4 must be `true` for the button to be enabled. As soon as user types or clears a field, `isFormValid` **automatically updates** — you don't call it manually.

This is why the button reacts live:
```html
<button :disabled="!isFormValid">Submit</button>
<!-- disabled = true  → when form is invalid -->
<!-- disabled = false → when all fields valid -->
```

---

## 3. Nested Routes

### Structure
```javascript
const routes = [
  {
    path: '/about',
    component: About,
    children: [
      { path: '/about/:username', component: AboutUser },
      { path: '/about/:password/:username', component: AboutPassword }
    ]
  }
]
```

### Parent Component (About.js)
```javascript
const About = {
  template: `
    <div>
      <h1>About Page</h1>
      <!-- router-links use the received name & password from Home form -->
      <router-link :to="'/about/' + $route.params.username">About User</router-link>
      <router-link :to="'/about/' + $route.params.password + '/' + $route.params.username">About Password</router-link>
      <router-view></router-view>
    </div>
  `
}
```

**Flow:**
1. User fills form in Home → hits Submit
2. `submitForm()` calls `this.$router.push('/about/secret123/john')`
3. About page receives: `$route.params.username = 'john'`, `$route.params.password = 'secret123'`
4. Router-links in About dynamically build URLs using these params
5. Child components display the data

### Child Components
```javascript
// AboutUser.js
export default {
  template: `<div>User: {{ $route.params.username }}</div>`
}

// AboutPassword.js
export default {
  template: `<div>Password: {{ $route.params.password }}</div>`
}
```

---

## 4. Route Parameters

### Path Parameters
```javascript
// Route: { path: '/user/:id', component: User }
// URL: /user/123
{{ $route.params.id }}  // Output: 123
```

### Query Parameters
```javascript
// URL: /search?q=vue&sort=new
{{ $route.query.q }}     // Output: vue
{{ $route.query.sort }}  // Output: new
```

### Access in Code
```javascript
console.log(this.$route.params)  // { id: '123' }
console.log(this.$route.query)   // { q: 'vue' }
console.log(this.$route.path)    // '/user/123'
```

---

## 5. Quick Cheat Sheet

| Task | Code |
|------|------|
| Link navigation | `<router-link to="/path">Link</router-link>` |
| Display component | `<router-view/>` |
| Go to route | `this.$router.push('/path')` |
| Get param | `this.$route.params.id` |
| Get query | `this.$route.query.search` |
| Nested routes | `children: [{ path: '...', component: ... }]` |
| Validate form | `@blur="validate"` + `v-if="errors.field"` |
| Enable history | `mode: 'history'` + server config |

---

## Common Issues & Fixes

### Issue: Validation not triggering
✅ Add `@blur` or `@input` event to input
✅ Make sure method is inside `methods: {}`

### Issue: Form not submitting
✅ Add `@submit.prevent="submit"` to form
✅ Check if `isFormValid` computed property is correct

### Issue: Nested route not showing
✅ Add `<router-view></router-view>` in parent component
✅ Check route path matches exactly

### Issue: History mode 404 errors
✅ Configure server to serve `index.html` for all routes
✅ Or keep using hash mode (#/path)
