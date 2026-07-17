import AdminView from "../views/AdminView.vue";
import LandingPage from "../views/LandingPage.vue";
import UserView from "../views/UserView.vue";

import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/admin', component: AdminView }, 
  { path: '/user', component: UserView },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]




// const routes = [
//   { path: '/', component: LandingView },
//   { path: '/admin', component: AdminView }, 
//   { path: '/user', component: UserView },
//   { path: '/:pathMatch(.*)*', redirect: '/' }
// ]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router


