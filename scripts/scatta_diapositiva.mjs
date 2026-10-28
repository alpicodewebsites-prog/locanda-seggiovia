/**
 * Scatta una diapositiva precisa del carosello.
 *
 * Serve a guardare il caso peggiore: la fotografia più piccola ingrandita nel
 * riquadro. Se tiene quella, tengono tutte.
 *
 * Uso:  node scripts/scatta_diapositiva.mjs <indice> [indirizzo]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const INDICE = Number(process.argv[2] ?? 2);
const BASE = (process.argv[3] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');
const exe = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].find((p) => p && existsSync(p));

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto(`${BASE}/`, { waitUntil: 'networkidle' });

const scelta = page.locator('[data-scelta="it"]');
if (await scelta.count()) {
  await scelta.first().click();
  await page.waitForLoadState('networkidle');
}

await page.locator('[data-carosello]').scrollIntoViewIfNeeded();
await page.locator(`[data-punto="${INDICE}"]`).click();
await page.waitForTimeout(900);

const info = await page.evaluate(() => {
  const attiva = Array.from(document.querySelectorAll('[data-carosello] [data-diapositiva]')).find(
    (d) => getComputedStyle(d).display !== 'none',
  );
  const img = attiva?.querySelector('img');
  return {
    titolo: attiva?.querySelector('h3')?.textContent?.trim() ?? '',
    naturale: img?.naturalWidth ?? 0,
    css: Math.round(img?.getBoundingClientRect().width ?? 0),
  };
});

console.log(
  `  diapositiva ${INDICE}: «${info.titolo}» — sorgente ${info.naturale} px, mostrata a ${info.css} px`,
);
await page.screenshot({ path: `diapositiva-${INDICE}.png` });

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
