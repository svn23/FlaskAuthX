document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('createUserForm');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const ageInput = document.getElementById('age');
    const passwordInput = document.getElementById('password');
    const retypePasswordInput = document.getElementById('retypePassword');
    const messageDiv = document.getElementById('message');
    const passwordPolicyDiv = document.getElementById('passwordPolicy');

    const passwordRequirements = {
        length: document.getElementById('length'),
        uppercase: document.getElementById('uppercase'),
        lowercase: document.getElementById('lowercase'),
        number: document.getElementById('number'),
        special: document.getElementById('special')
    };

    // Function to display messages
    function showMessage(message, isError = false) {
        if (messageDiv) {
            messageDiv.textContent = message;
            messageDiv.className = isError ? 'error-message' : 'success-message';
            messageDiv.style.display = 'block';
        } else {
            alert(message);
        }
    }

    // Password validation function
    function validatePassword(password) {
        const minLength = password.length >= 6;
        const uppercase = /[A-Z]/.test(password);
        const lowercase = /[a-z]/.test(password);
        const numbers = /[0-9]/.test(password);
        const specialChar = /[!@#$%^&*()_+={}\[\]:;"'<>,.?/|\\`~]/.test(password);

        passwordRequirements.length.style.color = minLength ? 'green' : 'red';
        passwordRequirements.uppercase.style.color = uppercase ? 'green' : 'red';
        passwordRequirements.lowercase.style.color = lowercase ? 'green' : 'red';
        passwordRequirements.number.style.color = numbers ? 'green' : 'red';
        passwordRequirements.special.style.color = specialChar ? 'green' : 'red';

        return minLength && uppercase && lowercase && numbers && specialChar;
    }

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Clear any existing messages
        if (messageDiv) {
            messageDiv.style.display = 'none';
        }

        // Validate the form
        if (!validateForm()) {
            return;
        }

        // Prepare form data
        const formData = new FormData();
        formData.append('avatar', document.getElementById('avatar').files[0]);
        formData.append('name', nameInput.value.trim());
        formData.append('email', emailInput.value.trim());
        formData.append('age', ageInput.value);
        formData.append('role', document.getElementById('role').value);
        formData.append('password', passwordInput.value);
        formData.append('retypePassword', retypePasswordInput.value);

        try {
            // Send data to server
            const response = await fetch('/create-user', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                showMessage('User created successfully!');
                form.reset();

                // Redirect to the admin dashboard with the user's ID
                const userId = data.user_id;  // Get the user ID from the response
                setTimeout(() => window.location.href = `/admin_dash/${userId}`, 1500);
            } else {
                showMessage(data.error || 'User creation failed', true);
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('An error occurred while creating user. Please try again.', true);
        }
    });

    // Function to validate the form
    function validateForm() {
        if (!nameInput.value.trim()) {
            showMessage('Name is required', true);
            return false;
        }

        if (!emailInput.value.trim()) {
            showMessage('Email is required', true);
            return false;
        }

        if (!ageInput.value) {
            showMessage('Age is required', true);
            return false;
        }

        if (!validatePassword(passwordInput.value)) {
            showMessage('Password does not meet the required criteria', true);
            return false;
        }

        if (passwordInput.value !== retypePasswordInput.value) {
            showMessage('Passwords do not match', true);
            return false;
        }

        return true;
    }

    passwordInput.addEventListener('focus', function() {
        passwordPolicyDiv.style.display = 'block';
    });

    passwordInput.addEventListener('blur', function() {
        passwordPolicyDiv.style.display = 'none';
    });

    passwordInput.addEventListener('input', function() {
        validatePassword(passwordInput.value);
    });
});
