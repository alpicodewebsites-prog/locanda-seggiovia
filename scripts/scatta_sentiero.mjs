/**
 * Fotogramma a piena pagina della scheda di un sentiero.
 * Uso:  node scripts/scatta_sentiero.mjs [slug] [indirizzo]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const slug = process.argv[2] ?? 'campogrosso';
const BASE = (process.argv[3] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');
const exe = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].find((p) => p && existsSync(p));

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
await page.goto(`${BASE}/sentieri/${slug}/`, { waitUntil: 'networkidle' });

await page
  .waitForFunction(
    () => document.querySelector('[data-meteo] [data-meteo-corpo]')?.getAttribute('aria-busy') === 'false',
    { timeout: 20000 },
  )
  .catch(() => {});
await page.waitForTimeout(700);

const misure = await page.evaluate(() => {
  const h = (sel) => {
    const el = document.querySelector(sel);
    return el ? Math.round(el.getBoundingClientRect().height) : null;
  };
  const dati = document.querySelector('.dati-sentiero__fila');
  return {
    fasciaDati: h('.dati-sentiero'),
    celleDati: dati ? dati.querySelectorAll('.dato').length : 0,
    cielo: document.querySelector('[data-meteo]')?.dataset.cielo ?? null,
    colonnaRacconto: h('section[aria-labelledby="titolo-percorso"] > .shell > div'),
    colonnaCondizioni: h('aside[aria-labelledby="titolo-condizioni"]'),
    altezzaPagina: document.documentElement.scrollHeight,
  };
});

console.log('  fascia dei dati : ' + misure.fasciaDati + ' px, ' + misure.celleDati + ' celle');
console.log('  cielo del meteo : ' + misure.cielo);
console.log('  colonna racconto: ' + misure.colonnaRacconto + ' px');
console.log('  colonna condizioni: ' + misure.colonnaCondizioni + ' px');
console.log('  altezza pagina  : ' + misure.altezzaPagina + ' px');

await page.screenshot({ path: 'sentiero.png', fullPage: true });
console.log('\n  fotogramma: sentiero.png');

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
