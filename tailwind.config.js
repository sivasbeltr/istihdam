/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html",
        "./static/js/**/*.js",
    ],
    darkMode: 'class', // or 'media' for OS preference based dark mode
    theme: {
        extend: {
            colors: {
                'primary': '#e30613', // Sivas Kırmızı
                'secondary': '#004a93', // Sivas Lacivert
                'accent': '#f7b500', // Sivas Sarı/Altın
                'text-dark': '#333333',
                'text-light': '#ffffff',
                'bg-light': '#f8f9fa',
                'bg-dark': '#121212',
            },
            fontFamily: {
                sans: ['Inter', 'Poppins', 'system-ui', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
