document.addEventListener('DOMContentLoaded', () => {
    const userCard = document.getElementById('user-card');
    const userAvatar = document.getElementById('user-avatar');
    const userNameInput = document.getElementById('user-name');
    const userAgeInput = document.getElementById('user-age');
    const userEmail = document.getElementById('user-email');
    const userRole = document.getElementById('user-role');
    const saveChangesButton = document.querySelector('.save-btn');
    const logoutButton = document.querySelector('.logout-btn');

    // Fetch user data from the backend
    async function fetchUserData() {
        try {
            const response = await fetch('/api/user'); // Fetch data for the logged-in user

            if (!response.ok) {
                throw new Error('Failed to fetch user data');
            }

            const user = await response.json();

            // Dynamically update the user data
            if (user) {
                userAvatar.src = user.profile_picture || 'https://via.placeholder.com/80'; // default if no picture
                userNameInput.value = user.name;
                userEmail.textContent = user.email;
                userAgeInput.value = user.age || 'N/A'; // default if no age provided
                userRole.textContent = user.role;
            }
        } catch (error) {
            console.error('Error fetching user data:', error);
        }
    }

    // Save Changes (only avatar and age are editable)
    async function saveChanges() {
        const updatedUser = {
            name: userNameInput.value,  // Get updated name
            age: userAgeInput.value  // Get updated age
        };

        try {
            const response = await fetch('/update-user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updatedUser)
            });

            if (response.ok) {
                alert('Changes saved successfully!');
            } else {
                const error = await response.json();
                alert('Failed to save changes: ' + error.message);
            }
        } catch (error) {
            console.error('Error saving changes:', error);
            alert('An error occurred while saving changes.');
        }
    }

    // Logout functionality
    async function logout() {
        try {
            // Send a POST request to the backend to end the session
            const response = await fetch('/logout', { method: 'POST' });

            if (response.ok) {
                // On successful logout, redirect to the login page
                window.location.href = '/login'; // Redirect to login page
            } else {
                alert('Error logging out!');
            }
        } catch (error) {
            console.error('Logout failed:', error);
            alert('Error logging out!');
        }
    }

    // Attach event listeners
    saveChangesButton.addEventListener('click', saveChanges);
    logoutButton.addEventListener('click', logout);  // Attach logout functionality to the button

    // Initial data fetch
    fetchUserData();
});
