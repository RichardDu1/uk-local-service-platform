import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  site: 'https://approvedtilers.co.uk',
  integrations: [tailwind()],
  output: 'static',
  // Emit /services.html instead of /services/index.html so Cloudflare Pages serves
  // the slash-less URL (used in sitemap & canonical) with a 200 instead of a 308.
  trailingSlash: 'never',
  build: { format: 'file' }
});
