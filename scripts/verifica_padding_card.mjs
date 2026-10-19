/**
 * Controlla il padding interno delle card su tutte le pagine che le usano.
 *
 * Il padding orizzontale è stato aggiunto al componente `.card-accento`, che è
 * condiviso. Qui si verifica che le pagine che avevano già il loro padding non
 * ne abbiano ora il doppio.
 *
 * Uso:  node scripts/verifica_padding_card.mjs [indirizzo]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const BASE = (process.argv[2] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');
const exe = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].find((p) => p && existsSync(p));

const PAGINE = [
  { url: '/ristorante/', selettore: 'section[aria-labelledby="titolo-menu"] .card-accento', atteso: [28, 28] },
  { url: '/', selettore: '.scheda-piatto', atteso: [24, 24] },
  { url: '/gnocchi-con-la-fioreta/', selettore: '.card-accento', atteso: [32, 32] },
];

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });

let problemi = 0;

for (const { url, selettore, atteso } of PAGINE) {
  await page.goto(`${BASE}${url}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(400);

  const misure = await page.evaluate((sel) => {
    const el = document.querySelector(sel);
    if (!el) return null;
    const st = getComputedStyle(el);
    const h4 = el.querySelector('h4, h3');
    const r = el.getBoundingClientRect();
    const hr = h4?.getBoundingClientRect();
    return {
      sx: Math.round(parseFloat(st.paddingLeft)),
      dx: Math.round(parseFloat(st.paddingRight)),
      distanza: hr ? Math.round(hr.left - r.left) : null,
    };
  }, selettore);

  if (!misure) {
    console.log(`  [FAIL] ${url}: nessun elemento per «${selettore}»`);
    problemi++;
    continue;
  }

  const ok = misure.sx === atteso[0] && misure.dx === atteso[1];
  const segno = ok ? 'OK  ' : 'FAIL';
  if (!ok) problemi++;
  console.log(
    `  [${segno}] ${url.padEnd(26)} padding ${misure.sx}/${misure.dx}px ` +
      `(atteso ${atteso[0]}/${atteso[1]})  testo a ${misure.distanza}px`,
  );
}

console.log('');
if (problemi) {
  console.log(`PROBLEMI: ${problemi}`);
} else {
  console.log('padding delle card coerente: nessun doppione');
}

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(problemi ? 1 : 0);
