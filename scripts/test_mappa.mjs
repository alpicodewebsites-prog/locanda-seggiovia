/**
 * Verifica del caricamento differito della mappa.
 *
 * Controlla che, sulla pagina Contatti pubblicata, l'iframe di Google NON parta
 * da solo e che parta invece al clic: è il comportamento da cui dipende
 * l'assenza del banner cookie.
 *
 * Uso:  node scripts/test_mappa.mjs [baseUrl]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const base = (process.argv[2] ?? 'http://127.0.0.1:4330').replace(/\/$/, '');

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

/* --- 1. Senza clic: nessuna richiesta a Google --------------------------- */
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

const richiesteGoogle = [];
page.on('request', (r) => {
  if (/google\.[a-z.]+\/(maps|recaptcha)/.test(r.url())) richiesteGoogle.push(r.url());
});

await page.goto(`${base}/contatti/`, { waitUntil: 'load' });
await page.waitForTimeout(2500);

const statoIniziale = await page.evaluate(() => {
  const contenitore = document.getElementById('contenitore-mappa');
  return {
    esisteContenitore: Boolean(contenitore),
    srcDifferito: contenitore?.dataset.src ?? null,
    iframePresenti: document.querySelectorAll('#contenitore-mappa iframe').length,
    segnapostoPresente: Boolean(document.getElementById('segnaposto-mappa')),
    bottonePresente: Boolean(document.getElementById('carica-mappa')),
  };
});

check('il contenitore della mappa esiste', statoIniziale.esisteContenitore === true);
check('la sorgente è differita in data-src', Boolean(statoIniziale.srcDifferito), statoIniziale.srcDifferito ?? '');
check('nessun iframe prima del clic', statoIniziale.iframePresenti === 0, `trovati: ${statoIniziale.iframePresenti}`);
check('il segnaposto è visibile', statoIniziale.segnapostoPresente === true);
check('il pulsante «Carica la mappa» è presente', statoIniziale.bottonePresente === true);
check(
  'nessuna richiesta a Google prima del clic',
  richiesteGoogle.length === 0,
  richiesteGoogle.length ? richiesteGoogle[0] : 'nessuna',
);

/* --- 2. Dopo il clic: l'iframe compare ---------------------------------- */
if (statoIniziale.bottonePresente) {
  await page.click('#carica-mappa');
  await page.waitForTimeout(2500);

  const statoDopo = await page.evaluate(() => {
    const iframe = document.querySelector('#contenitore-mappa iframe');
    return {
      iframePresenti: document.querySelectorAll('#contenitore-mappa iframe').length,
      src: iframe?.getAttribute('src') ?? null,
      titolo: iframe?.getAttribute('title') ?? null,
      segnapostoRimosso: !document.getElementById('segnaposto-mappa'),
    };
  });

  check('dopo il clic l’iframe è presente', statoDopo.iframePresenti === 1, `trovati: ${statoDopo.iframePresenti}`);
  check('l’iframe punta a Google Maps', (statoDopo.src ?? '').includes('google.com/maps'), (statoDopo.src ?? '').slice(0, 80));
  check('l’iframe ha un titolo accessibile', Boolean(statoDopo.titolo), statoDopo.titolo ?? '');
  check('il segnaposto è stato rimosso', statoDopo.segnapostoRimosso === true);
  check(
    'dopo il clic parte la richiesta a Google',
    richiesteGoogle.length > 0,
    `${richiesteGoogle.length} richieste`,
  );
}

/* --- 3. Senza JavaScript: resta l'indirizzo e il link ------------------- */
const ctxNoJs = await browser.newContext({ javaScriptEnabled: false });
const pageNoJs = await ctxNoJs.newPage();
await pageNoJs.goto(`${base}/contatti/`, { waitUntil: 'load' });
const testo = await pageNoJs.evaluate(() => document.body.innerText);
check(
  'senza JavaScript resta l’indirizzo completo',
  testo.includes('Piazza A. Savoia Duca Aosta 7') && testo.includes('Recoaro Terme'),
);
check(
  'senza JavaScript resta il link a Google Maps',
  (await pageNoJs.$$('a[href*="google.com/maps"]')).length > 0,
);
await ctxNoJs.close();

/* --- Report -------------------------------------------------------------- */
await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});

console.log('='.repeat(72));
console.log('COLLAUDO MAPPA A CARICAMENTO DIFFERITO');
console.log('='.repeat(72));
let falliti = 0;
for (const [nome, ok, dettaglio] of esiti) {
  if (!ok) falliti++;
  console.log(`[${ok ? 'OK  ' : 'FAIL'}] ${nome}${dettaglio ? `  — ${dettaglio}` : ''}`);
}
console.log('-'.repeat(72));
console.log(`${esiti.length - falliti}/${esiti.length} controlli superati`);
process.exit(falliti === 0 ? 0 : 1);
