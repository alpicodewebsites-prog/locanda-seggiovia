/**
 * Entra nella voce «Home Page» e legge i campi, con le fotografie che ognuno
 * vede nella propria cartella. SOLA LETTURA.
 *
 * Uso:  GITHUB_TOKEN=... node scripts/ispeziona_campi.mjs [indirizzo]
 */
import { existsSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const BASE = (process.argv[2] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');
const TOKEN = process.env.GITHUB_TOKEN;
const USCITA = process.env.USCITA ?? 'campi.txt';

const righe = [];
const scrivi = (t = '') => {
  righe.push(t);
  console.log(t);
};

const exe = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].find((p) => p && existsSync(p));

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1500, height: 1100 } });

// --- Accesso ---------------------------------------------------------------
await page.goto(`${BASE}/admin/`, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3500);
await page.getByRole('button', { name: /Accedi con Token/i }).first().click();
await page.waitForTimeout(1200);
await page.locator('input[type="text"], input[type="password"]').first().fill(TOKEN);
await page.locator('input[type="text"], input[type="password"]').first().press('Enter');
await page.waitForTimeout(15000);
scrivi(`accesso effettuato: ${page.url()}`);

// --- Si entra nella voce della Home ----------------------------------------
const voce = page.getByText('Testi, paragrafi e foto', { exact: false }).first();
if (await voce.count()) {
  await voce.click();
  await page.waitForTimeout(6000);
  scrivi(`voce aperta: ${page.url()}`);
} else {
  scrivi('voce «Testi, paragrafi e foto» non trovata');
}

// --- I campi presenti ------------------------------------------------------
const campi = await page.evaluate(() => {
  const etichette = [...document.querySelectorAll('label, [class*="label"]')]
    .map((e) => e.textContent.trim())
    .filter((t) => t && t.length > 3 && t.length < 90);
  return [...new Set(etichette)];
});
scrivi('\n=== campi della voce «Home Page» ===');
for (const c of campi) scrivi(`  - ${c}`);

// --- Le anteprime delle fotografie -----------------------------------------
const foto = await page.evaluate(() =>
  [...document.querySelectorAll('img')]
    .map((i) => ({ alt: i.alt || '', src: (i.currentSrc || i.src || '').split('/').pop() }))
    .filter((f) => f.src && !f.src.startsWith('data:')),
);
scrivi('\n=== immagini mostrate nella schermata ===');
for (const f of foto.slice(0, 20)) scrivi(`  ${f.src}   alt="${f.alt.slice(0, 60)}"`);

const contenuto = await page.evaluate(() => document.body.innerText.replace(/\n{2,}/g, '\n').slice(0, 2500));
scrivi('\n=== testo della schermata ===');
scrivi(contenuto);

await page.screenshot({ path: 'pannello-home.png', fullPage: true });
writeFileSync(USCITA, righe.join('\n'), 'utf-8');
scrivi(`\n  resoconto in ${USCITA}`);

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
