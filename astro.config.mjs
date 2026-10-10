// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// Il dominio arriva da src/data/site.ts, così esiste in un posto solo.
// Può essere sovrascritto senza toccare il codice: SITE_URL=... npm run build
import { SITE_URL } from './src/data/site.ts';

export default defineConfig({
  site: SITE_URL,
  trailingSlash: 'ignore',

  // Sito statico: nessun server, nessun database (§ vincoli di progetto).
  output: 'static',

  // La sitemap deve contenere solo le pagine che ha senso far indicizzare.
  // Le pagine di utilità (/grazie, /404) sono noindex: annunciarle in sitemap
  // sarebbe una contraddizione, e Search Console le segnalerebbe come errore.
  integrations: [
    sitemap({
      filter: (page) => !['/grazie/', '/404/', '/404.html'].some((p) => page.endsWith(p)),
    }),
  ],

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
