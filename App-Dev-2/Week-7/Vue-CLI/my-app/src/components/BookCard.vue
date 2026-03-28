<template>
  <div>
    <h3> {{ book.title }}</h3>
    <p>Author: {{ book.author }}</p>
    <p> Status: {{ book.read ? 'Read' : 'Not Read' }}</p>
    <button @click="$emit('toggle-read', book.id)"
      >{{ book.read ? 'Mark as Unread' : 'Mark as Read' }}</button>
      <button @click="$emit('delete', book.id)">Delete</button>
  </div>
</template>

<script>
export default {
  name: 'BookCard',
  props: {
    book: {
      type: Object,
      required: true
    },
    // emits: ['delete', 'toggle-read']
  }
}</script>
