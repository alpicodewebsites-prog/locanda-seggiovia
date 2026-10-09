/**
 * Diagnostica: legge i valori calcolati dal browser per verificare che le
 * utility Tailwind v4 siano realmente applicate (non stima, misura).
 *
 * Uso: node scripts/diag.mjs [url]
 */
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
let playwright;
for (const c of ['playwright', ...(process.env.PLAYWRIGHT_PATHS ?? '').split(';').filter(Boolean)]) {
  try {
    playwright = require(c);
    break;
  } catch {
    /* continua */
  }
}
const { chromium } = playwright;

const url = process.argv[2] ?? 'http://127.0.0.1:4321/';
const browser = await chromium.launch({ channel: 'chrome' }).catch(() => chromium.launch());
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto(url, { waitUntil: 'load' });
await page.waitForTimeout(1200);

const dati = await page.evaluate(() => {
  const out = {};

  // 1. Token CSS generati da @theme?
  const cs = getComputedStyle(document.documentElement);
  out.tokens = {
    'color-forest-700': cs.getPropertyValue('--color-forest-700').trim(),
    'font-display': cs.getPropertyValue('--font-display').trim().slice(0, 40),
    'spacing-section': cs.getPropertyValue('--spacing-section').trim(),
    'ease-alpine': cs.getPropertyValue('--ease-alpine').trim(),
  };

  // 2. aspect-4/5 è applicato?
  const media = document.querySelector('.media');
  if (media) {
    const m = getComputedStyle(media);
    const r = media.getBoundingClientRect();
    out.media = {
      aspectRatio: m.aspectRatio,
      larghezza: Math.round(r.width),
      altezza: Math.round(r.height),
      rapportoReale: +(r.width / r.height).toFixed(3),
    };
  }

  // 3. Allineamento verticale della griglia della sezione "La Locanda".
  const griglia = document.querySelector('.section-y .grid');
  if (griglia) {
    const g = getComputedStyle(griglia);
    out.griglia = { alignItems: g.alignItems, gridTemplateColumns: g.gridTemplateColumns };
  }

  // 4. Il serif dei titoli è davvero Fraunces (caricato) o fallback?
  const h1 = document.querySelector('h1');
  if (h1) {
    const s = getComputedStyle(h1);
    out.h1 = {
      fontFamily: s.fontFamily.split(',')[0],
      fontSize: s.fontSize,
      fontWeight: s.fontWeight,
      fontVariationSettings: s.fontVariationSettings,
    };
  }

  // 5. Il background body ha il token giusto?
  out.body = { background: getComputedStyle(document.body).backgroundColor };

  // 6. AOS attivo?
  out.aos = {
    classi: document.documentElement.className,
    elementi: document.querySelectorAll('[data-aos]').length,
    animati: document.querySelectorAll('[data-aos].aos-animate').length,
  };

  // 7. Quali fogli di stile hanno caricato davvero.
  out.fogli = [...document.styleSheets].map((s) => {
    try {
      return { href: s.href ? s.href.split('/').pop() : 'inline', regole: s.cssRules.length };
    } catch {
      return { href: (s.href || 'inline').split('/').pop(), regole: 'bloccato' };
    }
  });

  return out;
});

console.log(JSON.stringify(dati, null, 2));
await browser.close();
process.exit(0);
