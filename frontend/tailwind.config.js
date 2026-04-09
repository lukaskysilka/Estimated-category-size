export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        movit: {
          orange: '#F97316',
          dark: '#0F172A',
          card: '#1E293B',
          accent: '#FB923C',
        }
      },
      fontFamily: {
        display: ['"Syne"', 'sans-serif'],
        body: ['"DM Sans"', 'sans-serif'],
      }
    }
  }
}
