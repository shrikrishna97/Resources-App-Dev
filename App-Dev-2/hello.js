new Vue({
    el: '#app',
    data: {       
        message: 'Waiting...',
        visible: false,
        timeoutId: null
    },
    methods: {
        showMessage() {
            this.visible = true;
            this.message = 'Hello from Vue!';
        }
    },
})    
