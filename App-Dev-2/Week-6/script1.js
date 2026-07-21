import Home from "./components/Home.js";
import About from "./components/About.js";
import AboutUser from "./components/AboutUser.js";
import AboutPassword from "./components/AboutPassword.js";

const routes = [
  
  { path: "/home", component: Home },
  {
    path: "/about", component: About,
    children: [
      { path: "/about/:username", component: AboutUser },
      { path: "/about/:password/:username", component: AboutPassword },
    ]
    
  },
  {path: "*", redirect: "/" },
  // { path: "/about/:username", component: AboutUser },
];
const router = new VueRouter({
  // routes: routes,
  // mode: "history",
  routes,
});

const app = new Vue({
  el: "#app",
  data: {
    message: "Hello World",
  },
  components: {
    Home,
    About,
    AboutUser,
    AboutPassword,
  },
  router,
  // mounted() {
  // //   this.$router.push("/home");
  // //   this.$router.go(1);
  // }
});
