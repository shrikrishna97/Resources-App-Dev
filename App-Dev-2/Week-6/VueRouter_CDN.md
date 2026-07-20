# Basic Navigation and Introduction to Vue Router (Vue 2 CDN)

> **Goal:** Learn how to navigate between pages in a Vue application using **Vue Router** and reusable **Vue Components**.

---

# 1. What is Navigation?

Navigation means moving from one page (or view) to another without reloading the entire website.

Traditional websites:

```
Home → Browser reloads → About → Browser reloads
```

Vue Single Page Application (SPA):

```
Home → About → Contact
(No page reload)
```

Vue Router handles this navigation.

---

# 2. What is Vue Router?

**Vue Router** is the official routing library for Vue.js.

It allows us to:

* Navigate between pages
* Create Single Page Applications (SPA)
* Display different components based on URL
* Manage browser history

Example URLs:

```
/
```

```
/about
```

```
/contact
```

Each URL displays a different Vue component.

---

# 3. Include Vue Router (CDN)

```html
<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>

<script src="https://unpkg.com/vue-router@3/dist/vue-router.js"></script>
```

---

# 4. What is a Component?

A component is a reusable piece of UI.

Examples:

* Navbar
* Login Form
* Dashboard
* Profile Card
* Footer

Instead of writing everything inside one page, we divide the application into small reusable components.

Example:

```javascript
const Home = {
    template: `
        <div>
            <h2>Home Page</h2>
        </div>
    `
}
```

---

# 5. Creating Multiple Components

```javascript
const Home = {
    template: "<h2>Home Page</h2>"
}

const About = {
    template: "<h2>About Page</h2>"
}

const Contact = {
    template: "<h2>Contact Page</h2>"
}
```

Each component represents one page.

---

# 6. Creating Routes

Routes connect URLs to components.

```javascript
const routes = [

    {
        path: "/",
        component: Home
    },

    {
        path: "/about",
        component: About
    },

    {
        path: "/contact",
        component: Contact
    }

]
```

Meaning:

```
/          → Home Component

/about     → About Component

/contact   → Contact Component
```

---

# 7. Creating Router Object

```javascript
const router = new VueRouter({

    routes: routes

})
```

or

```javascript
const router = new VueRouter({

    routes

})
```

---

# 8. Router View

`<router-view>` is the place where the current page (component) is displayed.

```html
<div id="app">

    <router-view></router-view>

</div>
```

If URL is

```
/
```

Home component appears.

If URL is

```
/about
```

About component appears.

---

# 9. Router Link

Instead of using `<a>` tags, Vue Router provides `<router-link>`.

```html
<router-link to="/">Home</router-link>

<router-link to="/about">About</router-link>

<router-link to="/contact">Contact</router-link>
```

Generated HTML:

```html
<a href="/">Home</a>
```

But Vue Router prevents page reload.

---

# 10. Complete Example

```html
<!DOCTYPE html>
<html>

<head>

<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>

<script src="https://unpkg.com/vue-router@3/dist/vue-router.js"></script>

</head>

<body>

<div id="app">

    <h1>Vue Router Demo</h1>

    <router-link to="/">Home</router-link>

    |

    <router-link to="/about">About</router-link>

    |

    <router-link to="/contact">Contact</router-link>

    <hr>

    <router-view></router-view>

</div>

<script>

const Home = {

    template: "<h2>Welcome to Home Page</h2>"

}

const About = {

    template: "<h2>About Us</h2>"

}

const Contact = {

    template: "<h2>Contact Page</h2>"

}

const routes = [

    {
        path: "/",
        component: Home
    },

    {
        path: "/about",
        component: About
    },

    {
        path: "/contact",
        component: Contact
    }

]

const router = new VueRouter({

    routes

})

new Vue({

    el:"#app",

    router

})

</script>

</body>

</html>
```

---

# 11. Navigation Flow

```
Browser URL
      │
      ▼
Vue Router
      │
      ▼
Matches Route
      │
      ▼
Loads Component
      │
      ▼
Displays inside <router-view>
```

---

# 12. Summary

| Topic         | Description                                                                  |
| ------------- | ---------------------------------------------------------------------------- |
| Component     | Reusable Vue UI block                                                        |
| Vue Router    | Handles navigation between pages                                             |
| Route         | Maps a URL to a component                                                    |
| `router-link` | Creates navigation links without page reload                                 |
| `router-view` | Displays the matched component                                               |
| SPA           | Single Page Application where navigation happens without refreshing the page |

---

# Key Points to Remember

* Vue Router is the official routing library for Vue.js.
* Components help organize the application into reusable pieces.
* Each route maps a URL to a specific component.
* Use `<router-link>` instead of `<a>` for navigation.
* `<router-view>` is where the selected component is rendered.
* Vue Router enables **Single Page Application (SPA)** behavior by changing views without reloading the entire page.
