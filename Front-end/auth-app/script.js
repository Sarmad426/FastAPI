const loginForm = document.getElementById("login-form");
const welcomeMessage = document.getElementById("welcome-message");
const errorMessage = document.getElementById("error-message");

// Function to display the welcome message
function displayWelcomeMessage(name) {
  welcomeMessage.textContent = `Welcome, ${name}!`;
  welcomeMessage.style.display = "block";
  loginForm.style.display = "none";
}

// Function to handle login
async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  console.log(email, password);
  const response = await fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (response.ok) {
    localStorage.setItem("token", data.token);
    getUserDetails(data.token);
  } else {
    errorMessage.textContent =
      data.detail || "Login failed. Please check your credentials.";
  }
}

// Function to get user details using the token

async function getUserDetails(token) {
  const response = await fetch(
    `http://127.0.0.1:8000/secret?token=${token}`,
    {
      method: "GET",
    }
  );

  if (response.ok) {
    const userData = await response.json();
    displayWelcomeMessage(userData.name);
  } else {
    localStorage.removeItem("token");
    errorMessage.textContent = "Failed to retrieve user details.";
  }
}

// Check if token is already available
document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  if (token) {
    getUserDetails(token);
  }
});