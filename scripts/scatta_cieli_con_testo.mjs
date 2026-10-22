/**
 * Fotografa lo stesso riquadro meteo con cieli diversi, testo compreso.
 *
 * Serve a controllare che le forme (nuvole, sole, fiocchi) si vedano davvero e
 * che il testo resti leggibile sopra di esse. `fotografa_cieli.mjs` nasconde il
 * testo perché deve misurare solo il fondo; questo invece lo lascia, perché
 * guarda un'altra cosa.
 *
 * Uso:  node scripts/scatta_cieli_con_testo.mjs [indirizzo]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const BASE = (process.argv[2] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');
const CIELI = ['nuvoloso', 'pioggia', 'neve'];
const exe = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].find((p) => p && existsSync(p));

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
await page.goto(`${BASE}/sentieri/campogrosso/`, { waitUntil: 'networkidle' });

await page
  .waitForFunction(
    () => document.querySelector('[data-meteo] [data-meteo-corpo]')?.getAttribute('aria-busy') === 'false',
    { timeout: 20000 },
  )
  .catch(() => {});

const riquadro = page.locator('[data-meteo]');

for (const cielo of CIELI) {
  await page.evaluate((valore) => {
    const el = document.querySelector('[data-meteo]');
    if (el) el.dataset.cielo = valore;
  }, cielo);
  await page.waitForTimeout(200);
  await riquadro.screenshot({ path: `cielo-${cielo}.png` });
  console.log(`  cielo-${cielo}.png`);
}

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
