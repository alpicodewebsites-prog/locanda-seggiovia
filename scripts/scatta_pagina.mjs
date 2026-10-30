/**
 * Scatta l'intestazione di una pagina, e la striscia della home.
 *
 * Uso:  node scripts/scatta_pagina.mjs <percorso> <file> [indirizzo]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const PERCORSO = process.argv[2] ?? '/';
const FILE = process.argv[3] ?? 'pagina.png';
const BASE = (process.argv[4] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');
const exe = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].find((p) => p && existsSync(p));

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1440, height: 950 } });
await page.goto(`${BASE}${PERCORSO}`, { waitUntil: 'networkidle' });

// Sulla home c'è la scelta della lingua: si sceglie, come farebbe una persona.
const scelta = page.locator('[data-scelta="it"]');
if (await scelta.count()) {
  await scelta.first().click();
  await page.waitForLoadState('networkidle');
}

await page.waitForTimeout(700);
await page.screenshot({ path: FILE });
console.log(`  ${PERCORSO} -> ${FILE}`);

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
