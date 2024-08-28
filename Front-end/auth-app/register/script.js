const registerForm = document.getElementById('register-form');
const welcomeMessage = document.getElementById('welcome-message');
const errorMessage = document.getElementById('error-message');
const loadingGif = document.getElementById('loading-gif');

// Function to display the welcome message
function displayWelcomeMessage(name) {
    welcomeMessage.textContent = `Welcome, ${name}!`;
    welcomeMessage.style.display = 'block';
    registerForm.style.display = 'none';
    loadingGif.style.display = 'none';
}

// Function to handle User Sign up
async function register() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    loadingGif.style.display = 'block'; // Show loading gif
    registerForm.style.display = 'none'; // Hide the form during the loading

    const response = await fetch('http://127.0.0.1:8000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name,email, password, role:'SUPER_USER' }),
    });

    const data = await response.json();

    loadingGif.style.display = 'none'; // Hide loading gif when done

    // if (response.ok) {
    //     localStorage.setItem('token', data.token);
    //     getUserDetails(data.token);
    // } else {
    //     registerForm.style.display = 'block'; // Show the form again if login fails
    //     errorMessage.textContent = data.detail || 'Login failed. Please check your credentials.';
    // }
}

// Function to get user details using the token
// async function getUserDetails(token) {
//     loadingGif.style.display = 'block'; // Show loading gif
//     registerForm.style.display = 'none'; // Hide the form during the loading

//     const response = await fetch(`http://127.0.0.1:8000/secret?token=${token}`, {
//         method: 'GET',
//     });

//     loadingGif.style.display = 'none'; // Hide loading gif when done
    
//     if (response.ok) {
//       const userData = await response.json();
//       displayWelcomeMessage(userData.name);
//       logoutBtn.style.display = 'block'; // Hide logout button if user is logged out

//     } else {
//         localStorage.removeItem('token');
//         errorMessage.textContent = 'Failed to retrieve user details.';
//         registerForm.style.display = 'block'; // Show the form again if fetching details fails
//         logoutBtn.style.display = 'none'; // Show the form again if fetching details fails
//     }
// }


// const logout = () =>{
//   localStorage.removeItem('token');
//   window.location.reload()
// }

// Check if token is already available
// document.addEventListener('DOMContentLoaded', () => {
//     const token = localStorage.getItem('token');
//     if (token) {
//         getUserDetails(token);
//     }
// });
