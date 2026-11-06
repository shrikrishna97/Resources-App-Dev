export default {
  props: ['article'],

  data() {
    return {
      imageError: false,
    };
  },

  methods: {
    onImageError() {
      this.imageError = true;
    },
  },

  template: `
    <div class="card col-md-8 mx-auto shadow-sm">
      <img
        v-if="article.thumbnail && !imageError"
        :src="article.thumbnail"
        :alt="article.title"
        class="card-img-top"
        style="max-height: 300px; object-fit: cover;"
        referrerpolicy="no-referrer"
        @error="onImageError"
      />

      <div class="card-body">
        <h2 class="card-title">{{ article.title }}</h2>
        <h6 class="card-subtitle text-muted mb-3" v-if="article.description">
          {{ article.description }}
        </h6>

        <p class="card-text fs-5">
          {{ article.extract }}
        </p>

        <a :href="article.url" target="_blank" class="btn btn-primary">
          Read on Wikipedia ↗
        </a>
      </div>
    </div>
  `,
};
