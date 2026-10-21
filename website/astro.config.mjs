import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { unified } from '@astrojs/markdown-remark';
import { documentationLinks } from './src/lib/documentation.mjs';

export default defineConfig({
  site: 'https://holycow.neuralherd.dev',
  output: 'static',
  trailingSlash: 'always',
  integrations: [sitemap()],
  markdown: {
    processor: unified({ remarkPlugins: [documentationLinks] }),
    shikiConfig: { theme: 'github-light' },
  },
});
