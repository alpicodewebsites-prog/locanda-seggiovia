/**
 * Verifica che l'header non copra mai il testo dell'apertura.
 *
 * Il difetto compare solo ad alcune altezze di finestra: su schermi bassi il
 * contenuto dell'hero sale e finisce sotto la barra. Va quindi provato a più
 * altezze, non solo a 900px.
 *
 * Uso:  node scripts/test_overlap.mjs [baseUrl]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const base = (process.argv[2] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');

function trovaBrowser() {
  return [
    process.env.CHROME_PATH,
    `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  ]
    .filter(Boolean)
    .find((p) => existsSync(p));
}

/** Altezze di finestra realistiche: portatile basso, tablet, desktop, schermo alto. */
const altezze = [560, 620, 700, 800, 900, 1000, 1200];
const larghezze = [1440, 1024, 768, 390];

const esiti = [];
const check = (nome, ok, dettaglio = '') => esiti.push([nome, Boolean(ok), dettaglio]);

const exe = trovaBrowser();
const browser = await chromium.launch(exe ? { executablePath: exe } : { channel: 'chrome' });

for (const larghezza of larghezze) {
  for (const altezza of altezze) {
    const page = await browser.newPage({ viewport: { width: larghezza, height: altezza } });
    await page.goto(`${base}/`, { waitUntil: 'load' });
    await page.waitForTimeout(500);

    const r = await page.evaluate(() => {
      const header = document.getElementById('header-sito');
      const hb = header.getBoundingClientRect().bottom;

      // Tutti i blocchi di testo dell'apertura che non devono finire sotto la barra.
      const hero = document.querySelector('main > section');
      const elementi = hero
        ? [...hero.querySelectorAll('h1, p, a, .btn')]
        : [];

      let peggiore = null;
      for (const el of elementi) {
        const b = el.getBoundingClientRect();
        if (b.height === 0) continue;
        const coperto = Math.round(hb - b.top);
        if (coperto > 0 && (!peggiore || coperto > peggiore.coperto)) {
          peggiore = {
            coperto,
            testo: (el.textContent || '').trim().slice(0, 42),
            top: Math.round(b.top),
          };
        }
      }

      return { headerBottom: Math.round(hb), peggiore };
    });

    check(
      `${larghezza}x${altezza}: nessun testo sotto la barra`,
      r.peggiore === null,
      r.peggiore
        ? `"${r.peggiore.testo}" coperto di ${r.peggiore.coperto}px (top=${r.peggiore.top}, barra fino a ${r.headerBottom})`
        : `barra fino a ${r.headerBottom}px`,
    );

    await page.close();
  }
}

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});

console.log('='.repeat(80));
console.log('VERIFICA SOVRAPPOSIZIONE HEADER / TESTO DI APERTURA');
console.log('='.repeat(80));
let falliti = 0;
for (const [nome, ok, dettaglio] of esiti) {
  if (!ok) falliti++;
  console.log(`[${ok ? 'OK  ' : 'FAIL'}] ${nome}${ok ? '' : `\n         ${dettaglio}`}`);
}
console.log('-'.repeat(80));
console.log(`${esiti.length - falliti}/${esiti.length} controlli superati`);
process.exit(falliti === 0 ? 0 : 1);
