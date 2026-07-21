const About = {
    template: `
        <div>
            <h1>About Page</h1>
            {{}}
             <router-link to="/about/xyz"> About User</router-link>
             <router-link to="/about/yes/xyz">About Password</router-link>
            <p>This is not the about page of our Vue.js application.</p>
            <router-view></router-view>
        </div>
    `
};

export default About

// index1 (router view) -> about (router view )-> aboutuser