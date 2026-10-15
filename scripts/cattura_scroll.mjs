/**
 * Cattura i fotogrammi delle animazioni di scorrimento, per farne un GIF.
 *
 * Si scorre una pagina a piccoli passi e si salva un fotogramma a ogni passo:
 * mettendoli in sequenza si vede il contenuto che entra mentre si scorre, che è
 * esattamente quello che un'immagine ferma non può mostrare.
 *
 * I fotogrammi vanno poi uniti in un GIF da scripts/crea_gif.py.
 *
 * Uso:  node scripts/cattura_scroll.mjs <pagina> <cartella> [passi] [passo]
 */
import { mkdirSync, rmSync } from 'node:fs';
import { chromium } from 'playwright';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);

const BASE = (process.env.BASE_URL ?? 'http://127.0.0.1:4340').replace(/\/$/, '');

const CANDIDATI = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].filter(Boolean);

const pagina = process.argv[2] ?? '/camere/';
const cartella = process.argv[3] ?? 'frames';
const passi = Number(process.argv[4] ?? 22);
const passo = Number(process.argv[5] ?? 130);

// Finestra più piccola della norma: il GIF resta leggero e leggibile.
const LARGHEZZA = 900;
const ALTEZZA = 560;

async function main() {
  rmSync(cartella, { recursive: true, force: true });
  mkdirSync(cartella, { recursive: true });

  const browser = await chromium.launch({ executablePath: CANDIDATI[0] });
  const page = await browser.newPage({ viewport: { width: LARGHEZZA, height: ALTEZZA } });

  await page.goto(BASE + pagina, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1200);

  // Si parte dall'alto: le animazioni devono avvenire DURANTE la cattura.
  await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
  await page.waitForTimeout(600);

  for (let i = 0; i < passi; i++) {
    await page.evaluate(
      ({ y }) => window.scrollTo({ top: y, behavior: 'instant' }),
      { y: i * passo },
    );
    // Si aspetta meno della durata dell'animazione, così nei fotogrammi si
    // vede il movimento a metà invece del solo stato finale.
    await page.waitForTimeout(220);

    const nome = `${cartella}/frame-${String(i).padStart(3, '0')}.png`;
    await page.screenshot({ path: nome });
  }

  console.log(`  ${passi} fotogrammi salvati in ${cartella}/`);

  await Promise.race([
    browser.close(),
    new Promise((risolvi) => setTimeout(risolvi, 4000)),
  ]).catch(() => {});
  process.exit(0);
}

main().catch((errore) => {
  console.error('errore:', errore.message);
  process.exit(1);
});
