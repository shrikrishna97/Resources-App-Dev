import SearchBar from './components/SearchBar.js';
import ArticleCard from './components/ArticleCard.js';
import SuggestionChips from './components/SuggestionChips.js';

new Vue({
  el: '#app',

  data() {
    return {
      searchQuery: '',
      loading: false,
      errorMessage: '',
      article: null,
      suggestedTopics: [
        'Quantum Physics',
        'Mars',
        'Renaissance',
        'Artificial Intelligence',
        'Black Holes',
        'Ancient Rome',
      ],
    };
  },

  components: { SearchBar, ArticleCard, SuggestionChips },

  methods: {
    searchArticle(query) {
      const q = query ? query.trim() : '';
      if (!q) {
        this.errorMessage = 'Please enter a topic to search.';
        return;
      }

      this.searchQuery = q;
      this.errorMessage = '';
      this.loading = true;

      const encodedQuery = encodeURIComponent(q);

      fetch('https://en.wikipedia.org/api/rest_v1/page/summary/' + encodedQuery)
        .then(response => {
          if (!response.ok) {
            this.errorMessage = 'No article found for "' + q + '". Try a different topic.';
            this.article = null;
            this.loading = false;
            return null;
          }
          return response.json();
        })
        .then(summary => {
          if (!summary) return;

          this.article = {
            title: summary.title,
            description: summary.description || '',
            extract: summary.extract || 'No overview available for this topic.',
            thumbnail: summary.thumbnail?.source || null,
            url: summary.content_urls?.desktop?.page || ('https://en.wikipedia.org/wiki/' + encodedQuery),
          };

          this.loading = false;
        })
        .catch(() => {
          this.errorMessage = 'Something went wrong. Please check your connection and try again.';
          this.loading = false;
        });
    },

    goHome() {
      this.article = null;
      this.errorMessage = '';
      this.searchQuery = '';
    },
  },
});
