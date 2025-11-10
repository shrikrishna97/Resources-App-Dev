// --- Signup ---
document.getElementById("signupForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("signup-username").value;
  const password = document.getElementById("signup-password").value;

  const res = await fetch("/api/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json();
  showAlert("signup-alert", data);
});

// --- Login ---
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  const res = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json();

  if (data.status === "captcha_required") {
    sessionStorage.setItem("captcha_question", data.question);
    window.location.href = "/static/captcha.html";
  } else if (data.status === "success") {
    window.location.href = "/dashboard";
  } else {
    showAlert("login-alert", data);
  }
});

// --- Helper function ---
function showAlert(id, data) {
  const alertBox = document.getElementById(id);
  alertBox.classList.remove("d-none", "alert-danger", "alert-success");
  alertBox.classList.add(data.status === "success" ? "alert-success" : "alert-danger");
  alertBox.innerText = data.message;
}
