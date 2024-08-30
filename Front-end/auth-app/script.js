const loginForm = document.getElementById('login-form');
const welcomeMessage = document.getElementById('welcome-message');
const errorMessage = document.getElementById('error-message');
const loadingGif = document.getElementById('loading-gif');
const linkToRegister = document.getElementById('link-to-register');

// Function to display the welcome message
function displayWelcomeMessage(name) {
    welcomeMessage.textContent = `Welcome, ${name}!`;
    welcomeMessage.style.display = 'block';
    loginForm.style.display = 'none';
    loadingGif.style.display = 'none';
}

// Function to handle login
async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    loadingGif.style.display = 'block'; // Show loading gif
    loginForm.style.display = 'none'; // Hide the form during the loading

    const response = await fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    loadingGif.style.display = 'none'; // Hide loading gif when done

    if (response.ok) {
        localStorage.setItem('token', data.token);
        getUserDetails(data.token);
    } else {
        loginForm.style.display = 'block'; // Show the form again if login fails
        errorMessage.textContent = data.detail || 'Login failed. Please check your credentials.';
    }
}

const logoutBtn = document.getElementById('logout-btn')

logoutBtn.style.display = 'none'; // Hide logout button if user is logged out


// Function to get user details using the token
async function getUserDetails(token) {
    loadingGif.style.display = 'block'; // Show loading gif
    loginForm.style.display = 'none'; // Hide the form during the loading
    linkToRegister.style.display = 'none'; // Hide the link to register

    const response = await fetch(`http://127.0.0.1:8000/secret?token=${token}`, {
        method: 'GET',
    });

    loadingGif.style.display = 'none'; // Hide loading gif when done
    
    if (response.ok) {
      const userData = await response.json();
      displayWelcomeMessage(userData.name);
      logoutBtn.style.display = 'block'; // Hide logout button if user is logged out

    } else {
        localStorage.removeItem('token');
        errorMessage.textContent = 'Failed to retrieve user details.';
        loginForm.style.display = 'block'; // Show the form again if fetching details fails
        logoutBtn.style.display = 'none'; // Show the form again if fetching details fails
    }
}


const logout = () =>{
  localStorage.removeItem('token');
  window.location.reload()
}

// Check if token is already available
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (token) {
        getUserDetails(token);
    }
});
