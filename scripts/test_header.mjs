/**
 * Verifica della barra di navigazione trasparente.
 *
 * Controlla i valori calcolati dal browser a scroll zero e dopo lo scroll,
 * perché una schermata può ingannare: fotografare la pagina dopo averla
 * scorsa per attivare le animazioni cambia lo stato della barra.
 *
 * Uso:  node scripts/test_header.mjs [baseUrl]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const base = (process.argv[2] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');

/**
 * Dice se un colore `rgb(r, g, b)` è chiaro, cioè leggibile sopra una
 * fotografia scura.
 *
 * Si controlla la LUMINOSITÀ invece di confrontare valori esatti: la palette
 * cambia, e un test che pretende `rgb(250, 249, 246)` fallisce appena si
 * ritocca un tono — segnalando un problema che non esiste. Qui interessa una
 * proprietà vera: il testo è chiaro o scuro?
 */
function luminanza(colore) {
  const valori = String(colore).match(/\d+(\.\d+)?/g);
  if (!valori || valori.length < 3) return null;

  const [r, g, b] = valori.slice(0, 3).map((v) => {
    const n = Number(v) / 255;
    return n <= 0.04045 ? n / 12.92 : ((n + 0.055) / 1.055) ** 2.4;
  });

  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/** Il colore è chiaro? (soglia 0,5 su 1) */
const eChiaro = (colore) => {
  const l = luminanza(colore);
  return l !== null && l > 0.5;
};

/** Il colore è scuro? */
const eScuro = (colore) => {
  const l = luminanza(colore);
  return l !== null && l < 0.2;
};

function trovaBrowser() {
  return [
    process.env.CHROME_PATH,
    `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  ]
    .filter(Boolean)
    .find((p) => existsSync(p));
}

const esiti = [];
const check = (nome, ok, dettaglio = '') => esiti.push([nome, Boolean(ok), dettaglio]);

const exe = trovaBrowser();
const browser = await chromium.launch(exe ? { executablePath: exe } : { channel: 'chrome' });

const trasparente = (colore) =>
  colore === 'rgba(0, 0, 0, 0)' || colore === 'transparent' || /,\s*0\)$/.test(colore);

const leggi = () =>
  ({
    stato: (() => {
      const h = document.getElementById('header-sito');
      if (!h) return null;
      const s = getComputedStyle(h);
      return {
        classi: h.className,
        background: s.backgroundColor,
        bordo: s.borderBottomColor,
        coloreTitolo: getComputedStyle(h.querySelector('.site-header__wordmark')).color,
        posizione: s.position,
      };
    })(),
    scrollY: window.scrollY,
  });

/* --- HOME: deve partire trasparente -------------------------------------- */
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto(`${base}/`, { waitUntil: 'load' });
await page.waitForTimeout(1200); // webfont e primo frame

let s = await page.evaluate(leggi);
check('home: esiste un header con id', s.stato !== null);
check('home: a scroll zero lo scroll è 0', s.scrollY === 0, `scrollY=${s.scrollY}`);
check(
  'home: la barra NON ha sfondo in cima',
  trasparente(s.stato?.background ?? ''),
  s.stato?.background ?? '',
);
check(
  'home: il bordo inferiore è assente in cima',
  trasparente(s.stato?.bordo ?? ''),
  s.stato?.bordo ?? '',
);
check(
  'home: il wordmark è chiaro sopra la fotografia',
  eChiaro(s.stato?.coloreTitolo),
  s.stato?.coloreTitolo ?? '',
);
check('home: la classe di trasparenza è attiva', (s.stato?.classi ?? '').includes('site-header--trasparente'));
check(
  'home: la barra non è ancora solida',
  !(s.stato?.classi ?? '').includes('site-header--solido'),
);

/* --- HOME dopo lo scroll: deve diventare solida -------------------------- */
await page.evaluate(() => window.scrollTo(0, 400));
await page.waitForTimeout(700);

s = await page.evaluate(leggi);
check(
  'home dopo lo scroll: la barra diventa solida',
  (s.stato?.classi ?? '').includes('site-header--solido'),
  s.stato?.classi ?? '',
);
check(
  'home dopo lo scroll: la barra ha uno sfondo leggibile',
  !trasparente(s.stato?.background ?? ''),
  s.stato?.background ?? '',
);
check(
  'home dopo lo scroll: il wordmark torna scuro',
  eScuro(s.stato?.coloreTitolo),
  s.stato?.coloreTitolo ?? '',
);

// Tornando in cima deve tornare trasparente.
await page.evaluate(() => window.scrollTo(0, 0));
await page.waitForTimeout(700);
s = await page.evaluate(leggi);
check(
  'home: tornando in cima torna trasparente',
  !(s.stato?.classi ?? '').includes('site-header--solido'),
  s.stato?.classi ?? '',
);

/* --- PAGINA INTERNA: deve essere solida da subito ------------------------ */
const pageInt = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await pageInt.goto(`${base}/camere/`, { waitUntil: 'load' });
await pageInt.waitForTimeout(900);

const si = await pageInt.evaluate(leggi);
check(
  'pagina interna: nessuna classe di trasparenza',
  !(si.stato?.classi ?? '').includes('site-header--trasparente'),
  si.stato?.classi ?? '',
);
check(
  'pagina interna: sfondo leggibile in cima',
  !trasparente(si.stato?.background ?? ''),
  si.stato?.background ?? '',
);
check(
  'pagina interna: wordmark scuro',
  eScuro(si.stato?.coloreTitolo),
  si.stato?.coloreTitolo ?? '',
);

/* --- SENZA JavaScript: la barra deve restare leggibile ------------------- */
const ctx = await browser.newContext({ javaScriptEnabled: false });
const pageNoJs = await ctx.newPage();
await pageNoJs.goto(`${base}/`, { waitUntil: 'load' });
const noJs = await pageNoJs.evaluate(() => {
  const h = document.getElementById('header-sito');
  return h ? getComputedStyle(h).backgroundColor : null;
});
// Senza JS resta il CSS di base: sfondo chiaro e testo scuro, mai invisibile.
check(
  'senza JavaScript la barra resta con sfondo leggibile',
  noJs !== null && !trasparente(noJs),
  noJs ?? 'header non trovato',
);
await ctx.close();

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});

console.log('='.repeat(74));
console.log('VERIFICA BARRA DI NAVIGAZIONE');
console.log('='.repeat(74));
let falliti = 0;
for (const [nome, ok, dettaglio] of esiti) {
  if (!ok) falliti++;
  console.log(`[${ok ? 'OK  ' : 'FAIL'}] ${nome}${dettaglio ? `  — ${dettaglio}` : ''}`);
}
console.log('-'.repeat(74));
console.log(`${esiti.length - falliti}/${esiti.length} controlli superati`);
process.exit(falliti === 0 ? 0 : 1);
