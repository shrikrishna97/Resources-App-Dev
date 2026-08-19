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
      form: { name: "", password: "" },
      errors: { name: "", password: "" },
    };
  },
  computed: {
    isFormValid() {
      return (
        this.form.name &&
        this.form.password &&
        !this.errors.name &&
        !this.errors.password
      );
    },
  },
  methods: {
    validateName() {
      this.errors.name = this.form.name.length < 3 ? "Min 3 chars" : "";
    },
    validatePassword() {
      this.errors.password = this.form.password.length < 6 ? "Min 6 chars" : "";
    },
    submitForm() {
      this.validateName();
      this.validatePassword();
      console.log(this.$route.params); // { id: '123' }
      console.log(this.$route.query); // { q: 'vue' }
      console.log(this.$route.path); // '/user/123'
      if (this.isFormValid) {
        // Send name & password to About page via route params
        this.$router.push(`/about/${this.form.password}/${this.form.name}`);
        this.form.name = "";
        this.form.password = "";
      }
    },
  },
};

export default Home;
