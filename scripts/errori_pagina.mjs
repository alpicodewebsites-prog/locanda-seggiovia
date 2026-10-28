/**
 * Cattura gli errori della pagina: console e pageerror.
 *
 * Uso:  node scripts/errori_pagina.mjs <percorso> [indirizzo]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const PERCORSO = process.argv[2] ?? '/';
const BASE = (process.argv[3] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');
const exe = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].find((p) => p && existsSync(p));

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

page.on('console', (msg) => {
  if (msg.type() === 'error' || msg.type() === 'warning') {
    console.log(`  [console.${msg.type()}] ${msg.text().slice(0, 300)}`);
  }
});
page.on('pageerror', (err) => {
  console.log(`  [pageerror] ${String(err).slice(0, 400)}`);
});
page.on('requestfailed', (req) => {
  console.log(`  [rete] ${req.url().slice(0, 120)} — ${req.failure()?.errorText ?? ''}`);
});

await page.goto(`${BASE}${PERCORSO}`, { waitUntil: 'networkidle' });
await page.waitForTimeout(4000);

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
