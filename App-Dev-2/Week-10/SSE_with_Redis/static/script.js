const app = new Vue({
  el: "#app",
  data: {
    message: "",
  },
  mounted() {this.loadEventSource()},
  methods: {
    loadEventSource() {
      const eventSource = new EventSource("/stream");

      eventSource.addEventListener("notify", function (event) {
        const data = JSON.parse(event.data);
          console.log("Received data:", data);
          const container = document.getElementById("notification")
          const n1 = document.createElement("div");
          n1.textContent = data.message;
          container.prepend(n1);
      });
    },
    textToBackend() {
      fetch("/send_notification", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: this.message }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success == "success") {
            console.log("Notification sent successfully");
          }
          this.message = "";
        });
    },
  },
});
