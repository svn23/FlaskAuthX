// Assuming the root theme is dark for this example. 
// You can change the colors as needed.

const root = document.documentElement;

// Set static theme
root.style.setProperty("--bg-color", "#36454F");  // Dark theme background
root.style.setProperty("--text-color", "#fff");   // Light text color for dark background
root.style.setProperty("--primary-color", "#faca2e");  // Primary color

// Set static sun/moon icon for the dark theme
const colorSwitcher = document.querySelector("[data-theme-color-switch]");
colorSwitcher.textContent = "\u{2600}";  // Sun symbol (or use Moon symbol if you prefer)
colorSwitcher.style.pointerEvents = "none";  // Disable interaction with the button

// Optionally, remove the event listener to ensure it cannot be toggled
colorSwitcher.removeEventListener("click", switchTheme);
