/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f8f9ff',
          100: '#e8eaff',
          200: '#d1d4ff',
          300: '#a7adff',
          400: '#7c84ff',
          500: '#5158ff',
          600: '#2f35ff',
          700: '#0006ff',
          800: '#0005cc',
          900: '#000499',
        },
      },
    },
  },
  plugins: [],
}