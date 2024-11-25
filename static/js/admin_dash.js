document.addEventListener('DOMContentLoaded', () => {
    const userList = document.getElementById('user-list');
    const logoutButton = document.querySelector('.logout-btn');
    const saveChangesButton = document.querySelector('.save-btn');

    // Render user cards dynamically
    async function renderUsers() {
        const users = await fetchUserData();
        if (users.length > 0) {
            userList.innerHTML = users.map(user => `
                <div class="user-card" id="user-card-${user.id}">
                    <img src="${user.profilePicture || 'https://via.placeholder.com/80'}" alt="${user.name}">
                    <h3><input type="text" class="editable" id="name-${user.id}" value="${user.name}" /></h3>
                    <p>Email: <input type="email" class="editable" id="email-${user.id}" value="${user.email}" /></p>
                    <p>Age: <input type="number" class="editable" id="age-${user.id}" value="${user.age}" /></p>
                    <p>Role: 
                        <span class="roles" id="role-${user.id}">${user.role}</span>
                    </p>
                    <div class="user-actions">
                        <button class="action-btn delete-btn" data-id="${user.id}">Delete</button>
                        <button class="action-btn reset-btn" data-id="${user.id}">Reset Password</button>
                        <select class="role-dropdown" id="role-select-${user.id}" onchange="updateRole(${user.id}, this.value)">
                            <option value="Admin" ${user.role === 'Admin' ? 'selected' : ''}>Admin</option>
                            <option value="Standard" ${user.role === 'Standard' ? 'selected' : ''}>Standard</option>
                        </select>
                    </div>
                </div>
            `).join('');
        } else {
            userList.innerHTML = '<p>No users found.</p>';
        }

        // Add event listeners for delete and reset actions
        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                const userId = e.target.getAttribute('data-id');
                deleteUser(userId);
            });
        });

        document.querySelectorAll('.reset-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                const userId = e.target.getAttribute('data-id');
                resetPassword(userId);
            });
        });
    }

    // Function to fetch user data from the backend
    async function fetchUserData() {
        try {
            const response = await fetch('/api/users'); // Make sure this endpoint returns all users
            const users = await response.json();
            return users;
        } catch (error) {
            console.error('Error fetching users:', error);
            return [];
        }
    }

    // Save changes for the roles and other user data
    async function saveChanges() {
        const updatedUsers = [];

        const userCards = document.querySelectorAll('.user-card');
        userCards.forEach(card => {
            const userId = card.id.split('-')[2];
            const userName = card.querySelector(`#name-${userId}`).value;
            const userEmail = card.querySelector(`#email-${userId}`).value;
            const userAge = card.querySelector(`#age-${userId}`).value;
            const userRole = card.querySelector('.role-dropdown').value;

            updatedUsers.push({ userId, userName, userEmail, userAge, userRole });
        });

        try {
            const response = await fetch('/update-users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedUsers),
            });

            if (response.ok) {
                alert('Users data updated successfully!');
                renderUsers(); // Re-render the updated user list
            } else {
                const error = await response.json();
                alert('Failed to update user data: ' + error.message);
            }
        } catch (error) {
            console.error('Error updating user data:', error);
            alert('An error occurred while updating user data.');
        }
    }

    // Logout function
    function logout() {
        fetch('/logout', { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/login'; // Redirect to login page
                } else {
                    alert('Error logging out!');
                }
            })
            .catch(error => {
                console.error('Logout failed:', error);
                alert('Error logging out!');
            });
    }

    // Delete user function
    async function deleteUser(userId) {
        try {
            const response = await fetch(`/delete-user/${userId}`, { method: 'DELETE' });

            if (response.ok) {
                alert('User deleted successfully');
                renderUsers(); // Re-render after deletion
            } else {
                const error = await response.json();
                alert('Failed to delete user: ' + error.message);
            }
        } catch (error) {
            console.error('Error deleting user:', error);
            alert('An error occurred while deleting the user.');
        }
    }

    // Reset password function
    async function resetPassword(userId) {
        try {
            const response = await fetch(`/reset-password/${userId}`, { method: 'POST' });

            if (response.ok) {
                alert('Password reset email sent to user.');
            } else {
                const error = await response.json();
                alert('Failed to reset password: ' + error.message);
            }
        } catch (error) {
            console.error('Error resetting password:', error);
            alert('An error occurred while resetting password.');
        }
    }

    // Update role in the UI
    function updateRole(userId, newRole) {
        document.getElementById(`role-${userId}`).textContent = newRole;
        console.log(`Role for user ID ${userId} updated to ${newRole}`);
    }

    // Attach event listener for save changes button
    saveChangesButton.addEventListener('click', saveChanges);

    // Attach event listener for logout button
    logoutButton.addEventListener('click', logout);

    // Initial render
    renderUsers(); 
});
