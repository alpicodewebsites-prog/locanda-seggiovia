/**
 * Fotogramma della colonna dei dati tecnici, con meteo e webcam.
 * Uso:  node scripts/scatta_meteo.mjs [slug] [indirizzo]
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
const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
await page.goto(`${BASE}/sentieri/${slug}/`, { waitUntil: 'networkidle' });

await page
  .waitForFunction(
    () => document.querySelector('[data-meteo] [data-meteo-corpo]')?.getAttribute('aria-busy') === 'false',
    { timeout: 20000 },
  )
  .catch(() => {});
await page.waitForTimeout(400);

const colonna = page.locator('[data-meteo]');
await colonna.scrollIntoViewIfNeeded();
await page.waitForTimeout(600);
await colonna.screenshot({ path: 'meteo.png' });

console.log(`  fotogramma: meteo.png  (${slug})`);

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
