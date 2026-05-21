import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [mdx(), tailwind()],
  site: 'https://safal207.github.io',
  base: '/qa-fintech-api-python-course/',
});
