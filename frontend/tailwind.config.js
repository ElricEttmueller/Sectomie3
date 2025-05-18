module.exports = {
  purge: ['./src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: false,
  theme: {
    extend: {
      colors: {
        'cultivation-gold': '#d4af37',
        'cultivation-brown': '#8b4513',
        'scroll-bg': '#fff8dc',
      },
      fontFamily: {
        'cultivation': ['"Ma Shan Zheng"', 'cursive'],
        'sect': ['"Noto Serif SC"', 'serif'],
      },
      boxShadow: {
        'scroll': '0 10px 30px rgba(0, 0, 0, 0.5)',
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
