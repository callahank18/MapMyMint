/**
 * MapMyMint - Theme Manager
 * Handles theme switching and persistence
 */

const THEME_STORAGE_KEY = "mmmint-theme";
const DEFAULT_THEME = "light";

// Get the saved theme or use default
const getSavedTheme = () => {
    return localStorage.getItem(THEME_STORAGE_KEY) || DEFAULT_THEME;
};

// Apply theme to the document
const applyTheme = (theme) => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_STORAGE_KEY, theme);
    
    // Update theme switcher dropdown if it exists
    const switcher = document.getElementById("theme-switcher");
    if (switcher) {
        switcher.value = theme;
    }
};

// Initialize theme on page load
const initializeTheme = () => {
    const savedTheme = getSavedTheme();
    applyTheme(savedTheme);
};

// Set up theme switcher listener
const setupThemeSwitcher = () => {
    const switcher = document.getElementById("theme-switcher");
    if (switcher) {
        switcher.addEventListener("change", (e) => {
            applyTheme(e.target.value);
        });
    }
};

// Run on DOM ready
document.addEventListener("DOMContentLoaded", () => {
    initializeTheme();
    setupThemeSwitcher();
});

// Also apply theme immediately if DOM is already ready
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeTheme);
} else {
    initializeTheme();
    setupThemeSwitcher();
}
