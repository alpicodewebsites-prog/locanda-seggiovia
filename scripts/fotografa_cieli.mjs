/**
 * Fotografa il fondo di ogni cielo del meteo, senza testo.
 *
 * Serve al controllo dei contrasti: un gradiente non si può leggere da
 * `getComputedStyle` — quella restituisce solo il colore di ripiego. Qui si
 * svuota il riquadro e si fotografa il fondo vero, così il controllo misura i
 * pixel che l'occhio vede davvero.
 *
 * Uso:  node scripts/fotografa_cieli.mjs [indirizzo]
 */
import { existsSync, mkdirSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const BASE = (process.argv[2] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');
const CIELI = ['sereno', 'poco-nuvoloso', 'nuvoloso', 'nebbia', 'pioggia', 'rovesci', 'neve', 'temporale'];
const exe = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].find((p) => p && existsSync(p));

const USCITA = 'cieli';
if (!existsSync(USCITA)) mkdirSync(USCITA);

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
await page.goto(`${BASE}/sentieri/campogrosso/`, { waitUntil: 'networkidle' });

// Si rende INVISIBILE tutto ciò che non è fondo: testo, filetti, bordi.
//
// Due errori precedenti, entrambi trovati perché i numeri non tornavano:
//   1. svuotando il riquadro collassava e la fotografia non misurava niente;
//   2. lasciando i bordi, il pixel più scuro era il filetto sopra i tre giorni
//      (un grigio scuro al 20%), non il cielo — e tutti i cieli risultavano
//      sotto soglia.
// Qui resta visibile SOLO il fondo, che è quello che il testo deve reggere.
await page.addStyleTag({
  content: `
    .meteo, .meteo * {
      color: transparent !important;
      text-shadow: none !important;
      border-color: transparent !important;
      box-shadow: none !important;
    }
  `,
});
await page.waitForTimeout(300);

const riquadro = page.locator('[data-meteo]');

for (const cielo of CIELI) {
  await page.evaluate((valore) => {
    const el = document.querySelector('[data-meteo]');
    if (el) el.dataset.cielo = valore;
  }, cielo);
  await page.waitForTimeout(120);
  await riquadro.screenshot({ path: `${USCITA}/${cielo}.png` });
  console.log(`  ${USCITA}/${cielo}.png`);
}

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
