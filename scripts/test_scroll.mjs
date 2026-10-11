/**
 * Verifica che le pagine scorrano.
 *
 * Il blocco dello scroll è un difetto invisibile in una schermata statica ma
 * grave nell'uso reale: questa diagnostica confronta l'altezza del documento
 * con quella della finestra e prova a scorrere davvero.
 *
 * Uso:  node scripts/test_scroll.mjs [baseUrl]
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

const esiti = [];
const check = (nome, ok, dettaglio = '') => esiti.push([nome, Boolean(ok), dettaglio]);

const exe = trovaBrowser();
const browser = await chromium.launch(exe ? { executablePath: exe } : { channel: 'chrome' });

const pagine = ['/', '/la-locanda/', '/camere/', '/ristorante/', '/gnocchi-con-la-fioreta/',
  '/sentieri/', '/sentieri/gino-solda/', '/contatti/', '/privacy/', '/cookie/'];

for (const percorso of pagine) {
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(`${base}${percorso}`, { waitUntil: 'load' });
  await page.waitForTimeout(700);

  const dati = await page.evaluate(() => {
    const doc = document.documentElement;
    const csDoc = getComputedStyle(doc);

    return {
      scrollHeight: doc.scrollHeight,
      clientHeight: doc.clientHeight,
      scrollabile: doc.scrollHeight - doc.clientHeight,
      overflowHtml: csDoc.overflow,
      scrollBehavior: csDoc.scrollBehavior,
    };
  });

  /*
   * Lo scroll va misurato con calma: il sito usa `scroll-behavior: smooth`,
   * quindi la posizione si assesta con un'animazione. Misurandola subito dopo
   * averla impostata si legge sempre 0, e si scambia un'animazione per un blocco.
   */
  await page.evaluate(() => window.scrollTo({ top: 800, behavior: 'instant' }));
  await page.waitForTimeout(500);
  const posizione = await page.evaluate(() => Math.round(window.scrollY));

  const atteso = dati.scrollHeight - dati.clientHeight;
  const scorre = posizione > 100 || atteso <= 4;

  check(
    `${percorso}: la pagina scorre`,
    scorre,
    `atteso ${atteso}px di scorrimento, raggiunti ${posizione}px ` +
      `(scrollHeight=${dati.scrollHeight}, viewport=${dati.clientHeight})`,
  );

  await page.close();
}

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});

console.log('='.repeat(78));
console.log('VERIFICA SCROLL DELLE PAGINE');
console.log('='.repeat(78));
let falliti = 0;
for (const [nome, ok, dettaglio] of esiti) {
  if (!ok) falliti++;
  console.log(`[${ok ? 'OK  ' : 'FAIL'}] ${nome}`);
  console.log(`         ${dettaglio}`);
}
console.log('-'.repeat(78));
console.log(`${esiti.length - falliti}/${esiti.length} controlli superati`);
process.exit(falliti === 0 ? 0 : 1);
