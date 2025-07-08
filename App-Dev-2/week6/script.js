// const Home = {
//     template: `<div>
//     <h2>Home</h2>
//     <p>Welcome to the home page!</p>
//     </div>`

// }

// const About = {
//     template: `<div>
//     <h2>About</h2>
//     <p>This is the about page.</p>
//     </div>`
// }

import Home from './components/Home.js'
import About from './components/About.js'
import NotFound from './components/NotFound.js'
import AboutUser from './components/AboutUser.js'
import AboutPassword from './components/AboutPassword.js'

const routes = [
    { path: '/', component: Home },
    // { path: '/about/:username/:password', component: About },
    {
        path: '/about',
        component: About,
        children: [
            {
                path: '/about/:username',
                component: AboutUser
            },
            {
                path: '/about/:password',
                component: AboutPassword
            },
        ]
    },
    
    { path: '*', component: NotFound }
]

const router = new VueRouter({
    routes: routes
})


const app = new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue!'
    },
    router: router,
    methods: {
        goBack: function () {
            // this.$router.push('/about');
            this.$router.go(-2);
        }
    }
})