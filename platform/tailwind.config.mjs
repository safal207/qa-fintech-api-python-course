import typography from '@tailwindcss/typography';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        ink: '#07111f',
        panel: '#0d1728',
        line: '#22314f',
        glow: '#38bdf8',
        mint: '#34d399',
      },
      boxShadow: {
        soft: '0 24px 80px rgba(0, 0, 0, 0.24)',
      },
    },
  },
  plugins: [typography],
};
