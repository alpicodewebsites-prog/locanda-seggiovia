/**
 * Trova gli elementi più larghi della finestra.
 *
 * Un `scrollWidth` maggiore della larghezza della finestra significa che la
 * pagina scorre in orizzontale, e su un telefono è sempre un difetto. Qui si
 * elenca CHI lo causa, invece di tirare a indovinare.
 *
 * Uso:  node scripts/diagnostica_larghezza.mjs [indirizzo] [larghezza]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const BASE = (process.argv[2] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');
const LARGHEZZA = Number(process.argv[3] ?? 390);
const exe = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].find((p) => p && existsSync(p));

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: LARGHEZZA, height: 844 } });
await page.goto(`${BASE}/en/`, { waitUntil: 'networkidle' });
await page.waitForTimeout(900);

const dati = await page.evaluate(() => {
  const larghezza = window.innerWidth;
  const colpevoli = [];

  for (const el of document.querySelectorAll('*')) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    if (r.right > larghezza + 1 || r.left < -1) {
      const id = `${el.tagName.toLowerCase()}${el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 3).join('.') : ''}`;
      colpevoli.push(`${id}  left=${Math.round(r.left)} right=${Math.round(r.right)} larghezza=${Math.round(r.width)}`);
    }
  }

  return {
    finestra: larghezza,
    documento: document.documentElement.scrollWidth,
    corpo: document.body.scrollWidth,
    colpevoli: colpevoli.slice(0, 15),
  };
});

console.log(`  finestra: ${dati.finestra}px · documento: ${dati.documento}px · body: ${dati.corpo}px`);
console.log(`  elementi fuori misura: ${dati.colpevoli.length}`);
for (const c of dati.colpevoli) console.log(`    ${c}`);

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
