/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      keyframes: {
        'bounce-delay': {
          '0%, 100%': { transform: 'translateY(0)' },
          '5%': { transform: 'translateY(-10px)' },
          '10%': { transform: 'translateY(0)' }
        }
      },
      animation: {
        'bounce-loop': 'bounce-delay 8s ease-in-out infinite',
      }
    },
  },
  plugins: [],
}

