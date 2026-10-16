/**
 * Fotogramma della fascia «tavolo» della home.
 * Uso:  node scripts/scatta_tavolo.mjs [indirizzo]
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

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
await page.goto(`${BASE}/`, { waitUntil: 'networkidle' });
await page.waitForTimeout(1200);

const sezione = page.locator('.tavolo');
await sezione.scrollIntoViewIfNeeded();
await page.waitForTimeout(1200);

const d = await sezione.evaluate((el) => {
  const r = el.getBoundingClientRect();
  const tessere = [...el.querySelectorAll('.ingrediente')].map((t) => ({
    nome: t.querySelector('.ingrediente__nome')?.textContent.trim(),
    quantita: t.querySelector('.ingrediente__quantita')?.textContent.trim(),
    numero: t.querySelector('.ingrediente__numero')?.textContent.trim(),
    larghezza: Math.round(t.getBoundingClientRect().width),
    altezza: Math.round(t.getBoundingClientRect().height),
  }));
  return {
    altezza: Math.round(r.height),
    sfondo: getComputedStyle(el).backgroundColor,
    coloreTesto: getComputedStyle(el).color,
    tessere,
  };
});

console.log('  altezza della fascia : ' + d.altezza + 'px');
console.log('  fondo                : ' + d.sfondo);
console.log('  testo                : ' + d.coloreTesto);
console.log('  ingredienti (' + d.tessere.length + '):');
for (const t of d.tessere) {
  console.log(`    ${t.numero}  ${(t.nome ?? '').padEnd(32)} ${(t.quantita ?? '').padEnd(12)} tessera ${t.larghezza}x${t.altezza}`);
}

await sezione.screenshot({ path: 'tavolo.png' });
console.log('\n  fotogramma: tavolo.png');

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
