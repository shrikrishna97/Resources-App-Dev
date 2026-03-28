<template>
  <div id="app">
    <h1>Book Library</h1>
    <input v-model="searchQuery" placeholder="Search books..." />
    <button @click="addBook">Add Book</button>

    <BookCard
      v-for="book in filteredBooks"
      :key="book.id"
      :book="book"
      @delete="deleteBook"
      @toggle-read="toggleRead"
    />

    <p v-if="filteredBooks.length === 0">no books</p>
    <div>
      <p>Total Books: {{ totalBooks }}</p>
    </div>
  </div>
</template>

<script>
import BookCard from './components/BookCard.vue'
export default {
  name: 'App',
  components: {
    BookCard,
  },
  data() {
    return {
      searchQuery: '',
      nextId: 4,
      books: [
        { id: 1, title: 'The Great Gatsby', author: 'F. Scott Fitzgerald', read: false },
        { id: 2, title: 'To Kill a Mockingbird', author: 'Harper Lee', read: true },
        { id: 3, title: '1984', author: 'George Orwell', read: false },
      ],
    }
  },
  computed: {
    totalBooks() {
      return this.books.length
    },
    filteredBooks() {
      const query = this.searchQuery.toLowerCase()
      return this.books.filter(
        (book) =>
          book.title.toLowerCase().includes(query) || book.author.toLowerCase().includes(query),
      )
    },
  },
  methods: {
    addBook() {
      const title = prompt('Enter book title:')
      if (!title) return

      const author = prompt('Enter book author:') || 'Unknown Author'

      this.books.push({
        id: this.nextId++,
        title: title,
        author: author,
        read: false,
      })
    },
    deleteBook(bookId) {
      this.books = this.books.filter((book) => book.id !== bookId)
    },
    toggleRead(bookId) {
      const books = this.books.find((book) => book.id === bookId)

      if (books) {
        books.read = !books.read
      }
    },
  },
}
</script>
