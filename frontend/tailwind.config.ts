import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          primary: '#05050B',
          secondary: '#0B0B16',
          card: '#12121F',
        },
        accent: {
          purple: '#7A3EFF',
          blue: '#4F8CFF',
        },
        text: {
          primary: '#FFFFFF',
          secondary: '#A1A1AA', // Tailwind zinc-400
          muted: '#71717A', // Tailwind zinc-500
        },
        border: {
          DEFAULT: 'rgba(255, 255, 255, 0.05)',
          hover: 'rgba(255, 255, 255, 0.1)',
        }
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'glow-purple': '0 0 40px -10px rgba(122, 62, 255, 0.4)',
        'glow-blue': '0 0 40px -10px rgba(79, 140, 255, 0.4)',
        'card': '0 8px 32px rgba(0, 0, 0, 0.4)',
        'btn-glow': '0 4px 20px rgba(122, 62, 255, 0.45)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'fade-in': 'fadeIn 0.5s ease-out forwards',
        'slide-up': 'slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
export default config
