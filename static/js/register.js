document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signupForm');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const ageInput = document.getElementById('age');
    const passwordInput = document.getElementById('password');
    const retypePasswordInput = document.getElementById('retypePassword');
    const messageDiv = document.getElementById('message');
    const passwordPolicyDiv = document.getElementById('passwordPolicy');

    // Remove the first submit event listener (lines 11-44)
    // Keep only the more complete submit event listener that includes form validation
    
    // Fix the password requirements block that was outside any function
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

    // Function to validate email format
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Function to validate if age is a valid integer and in the correct range
    function isValidAge(age) {
        return Number.isInteger(age) && age >= 10 && age <= 99;
    }

    // Password validation function
    function validatePassword(password) {
        const minLength = password.length >= 6;
        const uppercase = /[A-Z]/.test(password);
        const lowercase = /[a-z]/.test(password);
        const numbers = /[0-9]/.test(password);
        const specialChar = /[!@#$%^&*()_+={}\[\]:;"'<>,.?/|\\`~]/.test(password);

        // Update the UI based on password validation
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
        const formData = {
            name: nameInput.value.trim(),
            email: emailInput.value.trim(),
            age: parseInt(ageInput.value),
            password: passwordInput.value,
            retypePassword: retypePasswordInput.value
        };

        try {
            // Send data to server
            const response = await fetch('/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                showMessage('Registration successful!');
                // Clear form
                form.reset();
                // Redirect to login page after successful registration
                if (data.redirect_url) {
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 1500);
                }
            } else {
                showMessage(data.error || 'Registration failed', true);
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('An error occurred during registration. Please try again.', true);
        }
    });

    // Function to validate the form (name, email, age, password)
    function validateForm() {
        if (!nameInput.value.trim()) {
            showMessage('Name is required', true);
            return false;
        }

        if (!emailInput.value.trim()) {
            showMessage('Email is required', true);
            return false;
        }

        if (!isValidEmail(emailInput.value.trim())) {
            showMessage('Please enter a valid email address', true);
            return false;
        }

        if (!ageInput.value) {
            showMessage('Age is required', true);
            return false;
        }

        const age = parseInt(ageInput.value);
        if (!isValidAge(age)) {
            showMessage('Age must be between 10 and 99', true);
            return false;
        }

        if (!passwordInput.value) {
            showMessage('Password is required', true);
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

    // Function to clear message when user starts typing
    const inputs = [nameInput, emailInput, ageInput, passwordInput, retypePasswordInput];
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (messageDiv) {
                messageDiv.style.display = 'none';
            }
        });
    });

    // Display password policy when password field is focused
    passwordInput.addEventListener('focus', function() {
        passwordPolicyDiv.style.display = 'block';
    });

    // Hide password policy when password field is blurred
    passwordInput.addEventListener('blur', function() {
        passwordPolicyDiv.style.display = 'none';
    });

    // Real-time password validation
    passwordInput.addEventListener('input', function() {
        validatePassword(passwordInput.value);
    });
});
