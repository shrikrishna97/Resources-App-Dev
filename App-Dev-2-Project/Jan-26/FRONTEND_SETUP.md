# Frontend Setup Guide - Vue 3 with Vite + Bootstrap

Simple frontend setup using Vue 3, Vite, and Bootstrap 5 (no custom CSS complexity).

---

## Prerequisites

Complete `PREREQUISITES_AND_SETUP.md` first.

---

## Step 1: Create Vue 3 Project

```bash
npm create vite@latest vehicle-parking-frontend
cd vehicle-parking-frontend
```

Select: **Vue** → **Official Vue Starter** → **Router (SPA)**

## Step 2: Install Dependencies

```bash
npm install axios bootstrap
npm run dev
```

---

## Step 3: Update main.js (Entry Point)

```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
```

---

## Step 4: Update App.vue (Root Component)

```vue
<template>
  <router-view />
</template>

<script>
export default {
  name: 'App'
}
</script>
```

---

## Step 5: Create router/index.js

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import AdminView from '../views/AdminView.vue'
import UserView from '../views/UserView.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/admin', component: AdminView },
  { path: '/user', component: UserView },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

---

## Step 6: Create Views

### views/LandingPage.vue

Select Admin or User portal.

```vue
<template>
  <div class="container-fluid d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="text-center">
      <h1 class="mb-4">Parking Management System</h1>
      <div class="row g-3">
        <div class="col-md-6">
          <div class="card cursor-pointer" @click="$router.push('/admin')">
            <div class="card-body">
              <h2 class="card-title">Admin Portal</h2>
              <p class="card-text">Manage parking lots and reservations</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card cursor-pointer" @click="$router.push('/user')">
            <div class="card-body">
              <h2 class="card-title">User Portal</h2>
              <p class="card-text">Make and manage reservations</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default { name: 'LandingPage' }
</script>

<style scoped>
.min-vh-100 { min-height: 100vh; }
.cursor-pointer { cursor: pointer; }
.card:hover { transform: translateY(-4px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
</style>
```

### views/AdminView.vue

Admin login + dashboard with tabs.

```vue
<template>
  <div>
    <AdminLogin v-if="!isLoggedIn" @login-success="handleLoginSuccess" />
    
    <div v-else>
      <div class="bg-white border-bottom px-4 py-3 d-flex justify-content-between align-items-center">
        <h2>Admin Dashboard</h2>
        <button class="btn btn-danger btn-sm" @click="logout">Logout</button>
      </div>
      
      <ul class="nav nav-tabs bg-white px-4">
        <li class="nav-item">
          <a href="#" class="nav-link" :class="{ active: activeTab === 'dashboard' }" @click.prevent="activeTab = 'dashboard'">Dashboard</a>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link" :class="{ active: activeTab === 'lots' }" @click.prevent="activeTab = 'lots'">Parking Lots</a>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link" :class="{ active: activeTab === 'users' }" @click.prevent="activeTab = 'users'">Users</a>
        </li>
      </ul>
      
      <div class="p-4">
        <div v-if="activeTab === 'dashboard'" class="card">
          <div class="card-body"><p>Dashboard content...</p></div>
        </div>
        <div v-if="activeTab === 'lots'" class="card">
          <div class="card-body"><p>Parking lots list...</p></div>
        </div>
        <div v-if="activeTab === 'users'" class="card">
          <div class="card-body"><p>Users list...</p></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminLogin from '../components/AdminLogin.vue'
import axios from 'axios'

export default {
  components: { AdminLogin },
  data() {
    return {
      isLoggedIn: !!localStorage.getItem('adminToken'),
      activeTab: 'dashboard'
    }
  },
  methods: {
    handleLoginSuccess() {
      this.isLoggedIn = true
    },
    logout() {
      localStorage.removeItem('adminToken')
      localStorage.removeItem('adminUser')
      this.isLoggedIn = false
    }
  }
}
</script>
```

### views/UserView.vue

User registration/login + dashboard with tabs.

```vue
<template>
  <div>
    <div v-if="!isLoggedIn">
      <AdminLogin v-if="!showRegister" @login-success="handleLoginSuccess" @switch-to-register="showRegister = true" />
      <UserRegister v-else @register-success="handleRegisterSuccess" @switch-to-login="showRegister = false" />
    </div>
    
    <div v-else>
      <div class="bg-white border-bottom px-4 py-3 d-flex justify-content-between align-items-center">
        <h2>User Dashboard</h2>
        <button class="btn btn-danger btn-sm" @click="logout">Logout</button>
      </div>
      
      <ul class="nav nav-tabs bg-white px-4">
        <li class="nav-item">
          <a href="#" class="nav-link" :class="{ active: activeTab === 'dashboard' }" @click.prevent="activeTab = 'dashboard'">Dashboard</a>
        </li>
        <li class="nav-item">
          <a href="#" class="nav-link" :class="{ active: activeTab === 'reservations' }" @click.prevent="activeTab = 'reservations'">My Reservations</a>
        </li>
      </ul>
      
      <div class="p-4">
        <div v-if="activeTab === 'dashboard'" class="card">
          <div class="card-body"><p>Dashboard content...</p></div>
        </div>
        <div v-if="activeTab === 'reservations'" class="card">
          <div class="card-body"><p>Your reservations...</p></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminLogin from '../components/AdminLogin.vue'
import UserRegister from '../components/UserRegister.vue'

export default {
  components: { AdminLogin, UserRegister },
  data() {
    return {
      isLoggedIn: !!localStorage.getItem('userToken'),
      showRegister: false,
      activeTab: 'dashboard'
    }
  },
  methods: {
    handleLoginSuccess() {
      this.isLoggedIn = true
    },
    handleRegisterSuccess() {
      this.showRegister = false
    },
    logout() {
      localStorage.removeItem('userToken')
      localStorage.removeItem('userData')
      this.isLoggedIn = false
    }
  }
}
</script>
```

---

## Step 7: Create Components

### components/AdminLogin.vue

```vue
<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <div class="card shadow" style="max-width: 400px; width: 100%;">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">Admin Login</h2>
        
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input v-model="form.username" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="form.password" type="password" class="form-control" required />
          </div>
          <button type="submit" class="btn btn-primary w-100" :disabled="loading">
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>
        
        <div v-if="error" class="alert alert-danger mt-3 mb-0">{{ error }}</div>
        <p class="text-center mt-3 mb-0">
          <router-link to="/" class="text-decoration-none">← Back</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminLogin',
  emits: ['login-success'],
  data() {
    return {
      form: { username: '', password: '' },
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      try {
        const res = await axios.post('http://localhost:5000/api/auth/login', this.form)
        localStorage.setItem('adminToken', res.data.access_token)
        localStorage.setItem('adminUser', JSON.stringify(res.data.user))
        this.$emit('login-success')
      } catch (err) {
        this.error = err.response?.data?.error || 'Login failed'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
```

### components/UserLogin.vue

```vue
<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100" style="background: linear-gradient(135deg, #42b983 0%, #359268 100%);">
    <div class="card shadow" style="max-width: 400px; width: 100%;">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">User Login</h2>
        
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input v-model="form.username" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="form.password" type="password" class="form-control" required />
          </div>
          <button type="submit" class="btn btn-success w-100" :disabled="loading">
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>
        
        <div v-if="error" class="alert alert-danger mt-3 mb-0">{{ error }}</div>
        
        <p class="text-center mt-3 mb-2">
          Don't have account? <a href="#" @click.prevent="$emit('switch-to-register')" class="text-decoration-none">Register</a>
        </p>
        <p class="text-center mb-0">
          <router-link to="/" class="text-decoration-none">← Back</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserLogin',
  emits: ['login-success', 'switch-to-register'],
  data() {
    return {
      form: { username: '', password: '' },
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      try {
        const res = await axios.post('http://localhost:5000/api/auth/login', this.form)
        localStorage.setItem('userToken', res.data.access_token)
        localStorage.setItem('userData', JSON.stringify(res.data.user))
        this.$emit('login-success')
      } catch (err) {
        this.error = err.response?.data?.error || 'Login failed'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
```

### components/UserRegister.vue

```vue
<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100" style="background: linear-gradient(135deg, #42b983 0%, #359268 100%);">
    <div class="card shadow" style="max-width: 400px; width: 100%;">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">Register</h2>
        
        <form @submit.prevent="handleRegister">
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input v-model="form.username" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="form.email" type="email" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="form.password" type="password" class="form-control" required />
          </div>
          <button type="submit" class="btn btn-success w-100" :disabled="loading">
            {{ loading ? 'Registering...' : 'Register' }}
          </button>
        </form>
        
        <div v-if="error" class="alert alert-danger mt-3 mb-0">{{ error }}</div>
        
        <p class="text-center mt-3 mb-0">
          Have account? <a href="#" @click.prevent="$emit('switch-to-login')" class="text-decoration-none">Login</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserRegister',
  emits: ['register-success', 'switch-to-login'],
  data() {
    return {
      form: { username: '', email: '', password: '' },
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true
      this.error = ''
      try {
        await axios.post('http://localhost:5000/api/auth/register', this.form)
        this.$emit('register-success')
      } catch (err) {
        this.error = err.response?.data?.error || 'Registration failed'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
```

---

## Step 8: Update vite.config.js

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: { port: 5173, open: true }
})
```

---

## Step 9: Run Development Server

```bash
npm run dev
```

Visit `http://localhost:5173` and select Admin or User portal.

---

## API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/login` | POST | Admin/User authentication |
| `/api/auth/register` | POST | User registration |
| `/api/parking-lots` | GET | List parking lots |
| `/api/reservations` | GET/POST | User reservations |
| `/api/admin/users` | GET | All users (admin only) |
| `/api/admin/reservations` | GET | All reservations (admin only) |

---

## Storage Keys

- `adminToken` - Admin JWT token
- `adminUser` - Admin user JSON data
- `userToken` - User JWT token
- `userData` - User JSON data

---

## Troubleshooting

**Port 5173 in use?** Change in vite.config.js `server.port`

**CORS errors?** Backend must have CORS enabled

**Login fails?** Check backend is running (`python app.py` on `http://localhost:5000`)

**API URL wrong?** Update in each component from `http://localhost:5000/api` if needed
