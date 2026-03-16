/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        amex: {
          blue: "#006fcf",
          dark: "#0b1020",
          navy: "#121a2f",
          surface: "#0f172a",
        }
      }
    },
  },
  plugins: [],
}
