document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');  // Renamed for clarity
    const passwordInput = document.getElementById('password');
    const messageDiv = document.getElementById('message');  // Display messages for login

    // Handle form submission
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();  // Prevent default form submission

        // Clear any existing messages
        if (messageDiv) {
            messageDiv.style.display = 'none';
        }

        // Get email and password values
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        if (!email || !password) {
            showMessage('Email and password are required', true);
            return;
        }

        // Send data to server
        const formData = {
            email: email,
            password: password  // Send plain password
        };

        try {
            const response = await fetch('http://localhost:5001/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)  // Send data as JSON
            });

            const data = await response.json();

            if (response.ok) {
                // Successful login - redirect
                showMessage('Login successful! Redirecting...', false);
                window.location.href = data.redirect_url;  // Redirect to dashboard or main page
            } else {
                // Show error message if login fails
                showMessage(data.error || 'Login failed', true);
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('An error occurred during login. Please try again.', true);
        }
    });

    // Function to display messages (similar to signup.js)
    function showMessage(message, isError = false) {
        if (messageDiv) {
            messageDiv.textContent = message;
            messageDiv.className = isError ? 'error-message' : 'success-message';
            messageDiv.style.display = 'block';
        } else {
            alert(message);
        }
    }
});