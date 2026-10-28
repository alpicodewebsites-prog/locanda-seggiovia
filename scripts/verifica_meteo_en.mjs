/**
 * Il meteo sulla scheda inglese: deve disegnarsi in inglese.
 *
 * Le etichette statiche si vedono nell'HTML, ma «Oggi», «Domani», «Vento» e le
 * condizioni sono scritte dallo script: senza questo controllo si potrebbe
 * avere un riquadro con l'intestazione in inglese e i dati in italiano.
 *
 * Uso:  node scripts/verifica_meteo_en.mjs [indirizzo]
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
await page.goto(`${BASE}/en/trails/gino-solda/`, { waitUntil: 'networkidle' });

await page
  .waitForFunction(
    () => document.querySelector('[data-meteo] [data-meteo-corpo]')?.getAttribute('aria-busy') === 'false',
    { timeout: 20000 },
  )
  .catch(() => {});

const dati = await page.evaluate(() => {
  const el = document.querySelector('[data-meteo]');
  const corpo = el?.querySelector('[data-meteo-corpo]');
  return {
    testo: corpo?.textContent?.replace(/\s+/g, ' ').trim() ?? '',
    cielo: el?.dataset.cielo ?? null,
    lingua: el?.dataset.lingua ?? null,
  };
});

let problemi = 0;
const controlla = (nome, ok, nota = '') => {
  console.log(`  [${ok ? 'OK  ' : 'FAIL'}] ${nome}${nota ? ` — ${nota}` : ''}`);
  if (!ok) problemi++;
};

controlla('il riquadro dichiara la lingua inglese', dati.lingua === 'en', dati.lingua ?? '');
controlla('il meteo si è caricato', dati.testo.length > 0 && !dati.testo.includes('Loading'), dati.testo.slice(0, 40));
controlla('usa «Today»', dati.testo.includes('Today'));
controlla('usa «Wind»', dati.testo.includes('Wind'));
for (const italiano of ['Oggi', 'Domani', 'Vento', 'Sereno', 'Nuvoloso']) {
  controlla(`non contiene «${italiano}»`, !dati.testo.includes(italiano));
}
controlla('il cielo è stato scelto', Boolean(dati.cielo), dati.cielo ?? '');

console.log('');
console.log(problemi ? `PROBLEMI: ${problemi}` : 'il meteo è in inglese');

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(problemi ? 1 : 0);
