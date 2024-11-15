// Function to toggle mobile navigation
function mobilenav() {
    const overlay = document.getElementById('overlay');
    overlay.style.display = (overlay.style.display === 'flex') ? 'none' : 'flex';
}

// Function to close the menu when a link is clicked
function navigation() {
    document.getElementById('overlay').style.display = 'none';
}
