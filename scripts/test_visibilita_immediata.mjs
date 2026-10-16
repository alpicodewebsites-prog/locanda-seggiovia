/**
 * Verifica che il contenuto sia visibile SUBITO, senza scorrere e senza attesa.
 *
 * Dopo la rimozione delle animazioni allo scorrimento questa è la prova che
 * conta: prima il contenuto partiva a opacità zero e compariva entrando in
 * schermo, ora deve essere presente al primo fotogramma.
 *
 * Uso:  node scripts/test_visibilita_immediata.mjs [indirizzo]
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

const esiti = [];
const check = (nome, ok, dettaglio = '') => esiti.push([nome, Boolean(ok), dettaglio]);

const browser = await chromium.launch({ executablePath: exe });

for (const pagina of ['/camere/', '/sentieri/', '/la-locanda/']) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto(`${BASE}${pagina}`, { waitUntil: 'domcontentloaded' });

  // Il punto è proprio questo: si guarda SUBITO, senza scorrere.
  await page.waitForTimeout(150);

  const d = await page.evaluate(() => {
    const elementi = [...document.querySelectorAll('main p, main h1, main h2, main h3, main img, main li')];
    const opacita = elementi.map((el) => parseFloat(getComputedStyle(el).opacity));
    const spostati = [...document.querySelectorAll('main *')].filter((el) => {
      const t = getComputedStyle(el).transform;
      return t !== 'none' && t !== 'matrix(1, 0, 0, 1, 0, 0)';
    }).length;
    return {
      quanti: elementi.length,
      minimo: opacita.length ? Math.min(...opacita) : 1,
      spostati,
      classiHtml: document.documentElement.className,
    };
  });

  check(`[${pagina}] il contenuto è visibile subito`, d.minimo === 1, `opacità minima ${d.minimo}`);
  check(
    `[${pagina}] nessun elemento è spostato in attesa di animarsi`,
    d.spostati === 0,
    `${d.spostati} spostati su ${d.quanti}`,
  );
  check(
    `[${pagina}] nessuna classe residua delle animazioni su <html>`,
    !d.classiHtml.includes('aos'),
    d.classiHtml ? `<html class="${d.classiHtml}">` : 'nessuna',
  );

  await page.close();
}

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});

console.log('='.repeat(74));
console.log('CONTENUTO VISIBILE SUBITO (senza scorrere)');
console.log('='.repeat(74));
let falliti = 0;
for (const [nome, ok, dettaglio] of esiti) {
  if (!ok) falliti++;
  console.log(`[${ok ? 'OK  ' : 'FAIL'}] ${nome}${dettaglio ? `  — ${dettaglio}` : ''}`);
}
console.log('-'.repeat(74));
console.log(`${esiti.length - falliti}/${esiti.length} controlli superati`);
process.exit(falliti === 0 ? 0 : 1);
