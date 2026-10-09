// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// Il dominio va aggiornato al go-live (usato da canonical, Open Graph, sitemap).
// Può essere sovrascritto senza toccare il codice: SITE_URL=... npm run build
export const SITE = process.env.SITE_URL ?? 'https://www.locandaseggiovia.com';

export default defineConfig({
  site: SITE,
  trailingSlash: 'ignore',

  // Sito statico: nessun server, nessun database (§ vincoli di progetto).
  output: 'static',

  integrations: [sitemap()],

  vite: {
    plugins: [tailwindcss()],
  },

  build: {
    // CSS inline quando è piccolo: una richiesta di rete in meno.
    inlineStylesheets: 'auto',
  },

  image: {
    // Le immagini passano da sharp in fase di build (nessun costo a runtime).
    service: { entrypoint: 'astro/assets/services/sharp' },
  },
});
