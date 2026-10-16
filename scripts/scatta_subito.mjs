/**
 * Fotogramma di verifica: la pagina subito dopo il caricamento, senza scorrere.
 * Uso:  node scripts/scatta_subito.mjs [indirizzo] [percorso] [file]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const BASE = (process.argv[2] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');
const PAGINA = process.argv[3] ?? '/camere/';
const FILE = process.argv[4] ?? 'z-subito.png';

const exe = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].find((p) => p && existsSync(p));

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
await page.goto(`${BASE}${PAGINA}`, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(200);
await page.screenshot({ path: FILE });
console.log(`  fotogramma salvato: ${FILE} (${PAGINA}, 200 ms dopo il caricamento)`);

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
