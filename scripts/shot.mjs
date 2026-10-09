/**
 * Cattura screenshot del sito per revisione visiva.
 * Strumento di sviluppo, non fa parte del sito.
 *
 * Uso:  node scripts/shot.mjs [url] [outDir]
 */
import { mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const url = process.argv[2] ?? 'http://127.0.0.1:4322/';
const outDir = process.argv[3] ?? 'screenshots';
await mkdir(outDir, { recursive: true });

const log = (...a) => console.log(`[${new Date().toISOString().slice(11, 19)}]`, ...a);

/** Sceglie un browser già presente, senza scaricare nulla. */
function trovaBrowser() {
  const candidati = [
    process.env.CHROME_PATH,
    `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
    `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium_headless_shell-1243\\chrome-headless-shell-win64\\chrome-headless-shell.exe`,
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  ].filter(Boolean);
  return candidati.find((p) => existsSync(p));
}

const viewports = [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'mobile', width: 390, height: 844 },
];

const exe = trovaBrowser();
log('browser:', exe ?? 'predefinito');
const browser = await chromium.launch(exe ? { executablePath: exe } : { channel: 'chrome' });
log('browser avviato');

for (const vp of viewports) {
  const page = await browser.newPage({
    viewport: { width: vp.width, height: vp.height },
    deviceScaleFactor: 1,
  });

  await page.goto(url, { waitUntil: 'load', timeout: 30000 });
  log(`${vp.name}: pagina caricata`);

  // Prima si scorre (le immagini lazy partono solo quando entrano nel viewport),
  // poi si aspetta che abbiano dimensioni reali. Sondaggio con tetto di tempo:
  // un'immagine che non carica non deve bloccare lo script.
  await page.evaluate(async () => {
    const passo = window.innerHeight * 0.7;
    for (let y = 0; y < document.body.scrollHeight; y += passo) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 120));
    }
    window.scrollTo(0, 0);
    await document.fonts.ready;

    const scadenza = Date.now() + 8000;
    while (Date.now() < scadenza) {
      const mancanti = [...document.querySelectorAll('img')].filter(
        (img) => img.naturalWidth === 0,
      );
      if (mancanti.length === 0) return;
      await new Promise((r) => setTimeout(r, 100));
    }
  });
  log(`${vp.name}: immagini pronte`);

  // Le animazioni AOS si sono già attivate durante lo scroll; attesa di assestamento.
  await page.waitForTimeout(400);
  log(`${vp.name}: assestato`);

  await page.screenshot({ path: `${outDir}/${vp.name}-hero.png` });
  log(`${vp.name}: hero salvato`);

  await page.screenshot({ path: `${outDir}/${vp.name}-full.png`, fullPage: true });
  log(`${vp.name}: full salvato`);

  // Dettaglio delle sezioni, per valutare tipografia e spaziature.
  const sezioni = await page.$$('main > section');
  for (let i = 0; i < sezioni.length; i++) {
    const box = await sezioni[i].boundingBox();
    if (!box || box.height < 40) continue;
    await sezioni[i].screenshot({ path: `${outDir}/${vp.name}-sez${i + 1}.png` });
  }
  log(`${vp.name}: ${sezioni.length} sezioni salvate`);

  await page.close();
  log(`${vp.name}: pagina chiusa`);
}

log('fatto');
// In alcuni ambienti Windows la chiusura del browser resta appesa:
// i file sono già scritti, quindi non si attende oltre.
Promise.race([browser.close(), new Promise((r) => setTimeout(r, 5000))]).finally(() => process.exit(0));
