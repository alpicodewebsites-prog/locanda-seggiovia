/**
 * Fotogramma della sezione «Il menù» della pagina ristorante.
 * Uso:  node scripts/scatta_menu.mjs [indirizzo]
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
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
await page.goto(`${BASE}/ristorante/`, { waitUntil: 'networkidle' });
await page.waitForTimeout(1000);

const sezione = page.locator('section[aria-labelledby="titolo-menu"]');
await sezione.scrollIntoViewIfNeeded();
await page.waitForTimeout(800);

const d = await sezione.evaluate((el) => {
  const schede = [...el.querySelectorAll('.card-accento')].slice(0, 4).map((s) => {
    const r = s.getBoundingClientRect();
    const h4 = s.querySelector('h4');
    const hr = h4?.getBoundingClientRect();
    const st = getComputedStyle(s);
    return {
      nome: h4?.textContent.trim(),
      larghezza: Math.round(r.width),
      altezza: Math.round(r.height),
      // Distanza fra il bordo sinistro della scheda e l'inizio del testo.
      distanzaTesto: hr ? Math.round(hr.left - r.left) : null,
      paddingSx: st.paddingLeft,
    };
  });
  const colonna = el.querySelector('.md\\:col-span-8') ?? el.querySelector('[class*="col-span-8"]');
  return {
    schede,
    larghezzaColonna: colonna ? Math.round(colonna.getBoundingClientRect().width) : null,
  };
});

console.log('  larghezza colonna dei piatti: ' + d.larghezzaColonna + 'px');
console.log('  schede:');
for (const s of d.schede) {
  console.log(
    `    ${(s.nome ?? '').padEnd(30)} ${s.larghezza}x${s.altezza}  ` +
      `testo a ${s.distanzaTesto}px dal bordo (padding ${s.paddingSx})`,
  );
}

await sezione.screenshot({ path: 'menu.png' });
console.log('\n  fotogramma: menu.png');

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
