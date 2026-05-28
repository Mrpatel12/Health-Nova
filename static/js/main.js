document.addEventListener('DOMContentLoaded', function () {
    const dateFields = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    dateFields.forEach(field => field.setAttribute('min', today));

    const toggle = document.getElementById('themeToggle');
    const currentTheme = localStorage.getItem('healthNovaTheme') || 'light';
    document.documentElement.dataset.theme = currentTheme;
    updateThemeIcon(currentTheme);

    if (toggle) {
        toggle.addEventListener('click', function () {
            const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
            document.documentElement.dataset.theme = nextTheme;
            localStorage.setItem('healthNovaTheme', nextTheme);
            updateThemeIcon(nextTheme);
        });
    }
});

function updateThemeIcon(theme) {
    const toggle = document.getElementById('themeToggle');
    if (!toggle) return;

    const icon = toggle.querySelector('i');
    if (!icon) return;

    if (theme === 'dark') {
        icon.className = 'bi bi-sun-fill';
        toggle.title = 'Switch to light mode';
    } else {
        icon.className = 'bi bi-moon-stars-fill';
        toggle.title = 'Switch to dark mode';
    }
}
