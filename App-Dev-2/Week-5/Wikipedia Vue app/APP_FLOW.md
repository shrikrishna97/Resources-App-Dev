# WikiVue — Application Flow & Architecture Guide

A simple, beginner-friendly explanation of how this Vue 2 Wikipedia Explorer app works.

---

## 1. Project Structure

```
Wikipedia Vue app/
├── components/
│   ├── SearchBar.js        # Search input + button component (uses v-model)
│   ├── SuggestionChips.js  # Quick topic button pills component
│   └── ArticleCard.js      # Displays article summary & link
├── app.js                  # Main Vue instance (state + fetch API call)
├── index.html              # Main HTML page & template
└── APP_FLOW.md             # This guide
```

---

## 2. Big Picture: How the Files Connect

1. **`index.html`** loads:
   - **Bootstrap (Litera Theme)** (via CDN — gives an elegant theme with zero custom CSS)
   - **Vue 2** (via CDN)
   - **`app.js`** as a module (`type="module"`)
2. **`app.js`** imports the three component files and registers them:
   ```javascript
   import SearchBar from './components/SearchBar.js';
   import ArticleCard from './components/ArticleCard.js';
   import SuggestionChips from './components/SuggestionChips.js';

   new Vue({
     el: '#app',
     components: { SearchBar, ArticleCard, SuggestionChips },
     ...
   });
   ```
3. Vue mounts on `<div id="app">` and controls the user interface based on data in `app.js`.

---

## 3. The Two Views of the App

The screen toggles between two views using Vue's `v-if`:

| View | When Shown | What is Displayed |
|---|---|---|
| **Home View** | `v-if="!article"` (No article loaded yet) | Title, big `<search-bar>`, and `<suggestion-chips>` |
| **Article View** | `v-if="article"` (Article data exists) | Compact `<search-bar>` and the `<article-card>` |

When the user clicks "Home" or the logo, `goHome()` clears `article`, `errorMessage`, and `searchQuery`. Vue reacts to the changed data and displays the Home View again.

---

## 4. Step-by-Step Data Flow

```
[ User Action ]
      │
      ├──> Types in SearchBar (v-model="query") & presses Enter / Search button
      │         └── Emits "search" with the query
      │
      └──> OR clicks a chip in <suggestion-chips>
                └── Emits "select" with the topic
      │
      ▼
[ Parent: app.js ]
      │
      ├──> Runs searchArticle(query)
      ├──> Trims and validates query (if empty, shows an error)
      │         └── Stops without making a request
      ├──> Encodes query with encodeURIComponent(q)
      ├──> Sets loading = true
      └──> Calls fetch(Wikipedia Summary API)
      │
      ▼
[ Request Result ]
      │
      ├──> If response.ok is false ➔ Shows an HTTP error message and clears article
      ├──> If response.ok is true  ➔ Parses JSON and builds article data
      └──> If fetch or JSON parsing fails ➔ Shows a connection error
      │
      ▼
[ UI Update (Vue Reactivity) ]
      │
      ├──> Sets loading = false
      ├──> v-if conditions select the Home or Article View
      └──> On success, passes article data down to <article-card>
```

---

## 5. Core Concepts Explained

### A. Two-Way Data Binding (`v-model`)
Inside `SearchBar.js`:
```html
<input v-model="query" @keyup.enter="submit" />
```
`query` is local component data. `v-model` keeps it in sync with the text input: typing updates `query`, and changing `query` updates the input. The `.enter` event modifier calls `submit` when the user presses Enter.

### B. Component Registration
In `app.js`, we write:
```javascript
components: { SearchBar, ArticleCard, SuggestionChips }
```
Vue automatically maps PascalCase names to kebab-case tags in HTML:
- `SearchBar` ➔ `<search-bar>`
- `ArticleCard` ➔ `<article-card>`
- `SuggestionChips` ➔ `<suggestion-chips>`

### C. Props (Parent to Child Communication)
Props pass data **down** from `app.js` to components:
- **Array syntax:** `props: ['article']` or `props: ['loading', 'compact']`
- In the template: `<article-card :article="article" :key="article.title"></article-card>`
- The `:` is shorthand for `v-bind`; it passes the parent's current value rather than a literal string. For example, `:loading="loading"` passes the Boolean loading state.
- Props are inputs from the parent. A child should not change a prop directly.

`SearchBar` receives `loading` and `compact`; it disables its button while loading and uses `compact` to choose its size and placeholder. `ArticleCard` receives the article object. `SuggestionChips` receives the topics array.

### D. Custom Events (Child to Parent Communication)
Events send messages **up** from components to `app.js`:
- `SearchBar` emits `this.$emit('search', this.query)`, and its parent listens with `@search="searchArticle"`.
- `SuggestionChips` emits `this.$emit('select', topic)`, and its parent listens with `@select="searchArticle"`.
- The emitted value is passed as the first argument to `searchArticle`. This lets the component report the user's action without owning the API request.

### E. Fetch, Promises, and Response Handling
`searchArticle` calls Wikipedia's Summary REST API. `fetch()` is asynchronous and returns a Promise. The first `.then()` receives the HTTP response; `response.json()` returns another Promise that parses the response body:
```javascript
fetch('https://en.wikipedia.org/api/rest_v1/page/summary/' + encodedQuery)
  .then(response => {
    if (!response.ok) {
      this.errorMessage = 'No article found for "' + q + '".';
      this.article = null;
      this.loading = false;
      return null;
    }
    return response.json();
  })
  .then(summary => {
    if (!summary) return;
    this.article = { ... };
    this.loading = false;
  })
  .catch(() => {
    this.errorMessage = 'Something went wrong. Please check your connection and try again.';
    this.loading = false;
  });
```

`response.ok` is `true` for successful HTTP status codes (200–299); it is not limited to status 200. `fetch()` does not reject its Promise just because the server returns an HTTP error such as 404, so the code checks `response.ok` explicitly. The `.catch()` handles failures such as a network error or invalid JSON. `loading` is set before the request and reset on each handled outcome.

The app maps the API response to only the fields it needs: title, description, extract, thumbnail, and article URL. Any non-success HTTP response (not just 404) is treated as an unsuccessful search: the app shows a “No article found” message, clears the current article, and returns to the Home View. If the request itself fails, it displays a connection error and resets loading; if an article was already on screen, it remains there, and the error alert is not shown in the Article View.

### F. URL Encoding (`encodeURIComponent`)
Spaces and other special characters should be encoded when placing a search term in a URL path. If a user searches for `"Quantum Physics"`, `encodeURIComponent("Quantum Physics")` transforms the space into `%20` so it can safely be used in the request URL.

### G. Optional Chaining (`?.`)
Inside `app.js`:
```javascript
url: summary.content_urls?.desktop?.page || ('https://en.wikipedia.org/wiki/' + encodedQuery)
```
Optional chaining safely reads nested properties. If `content_urls` or `desktop` is missing, the expression evaluates to `undefined` instead of throwing a `TypeError`; `||` then uses the Wikipedia URL fallback. The same pattern is used for the optional thumbnail, with `null` as its fallback.

### H. Template Directives and Event Bindings
Vue directives are attributes beginning with `v-`; `:` and `@` are their common shorthands:

- `v-if="article"` conditionally renders the Article View; `v-if="!article"` renders the Home View when there is no article.
- `v-for="topic in topics"` repeats the suggestion button for each topic. `:key="topic"` gives each repeated item a stable identity so Vue can update the list correctly.
- `<article-card :key="article.title">` gives the card a key based on the article title. When the title changes, Vue recreates the card, including its local image-error state.
- `{{ article.title }}` displays a value from Vue data or a prop in the template. Vue updates the displayed value when the data changes.
- `@click="submit"` listens for a click; `:disabled="loading"` binds the button's disabled state to data.
- `@click.prevent="goHome"` handles the click and prevents the anchor's default navigation to `#`.
- `:class="{ 'input-group-lg': !compact }"` conditionally applies a CSS class.

### I. Component State and UI Feedback
Each component's `data()` returns its own state object. For example, `SearchBar` stores its input in `query`, while `ArticleCard` stores `imageError`. Returning an object from a component's `data` function gives each component instance independent state.

The parent `loading` state is passed to `SearchBar` as a prop. The child uses it to disable the button and show a spinner while the request is in progress. In `ArticleCard`, `v-if` hides the thumbnail when none is available or when loading the image fails; the image's `@error` handler sets `imageError` to `true`.

The Home View's error alert is rendered only when `errorMessage` is non-empty. The Article View does not currently render that alert, which is why a network failure during a follow-up search leaves the previous article visible without showing the connection message.
