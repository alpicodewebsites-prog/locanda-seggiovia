/**
 * Controlla che i due collegamenti dell'apertura non sbordino a nessuna
 * larghezza. Il testo degli gnocchi è lungo: su un telefono stretto potrebbe
 * uscire dallo schermo e creare scorrimento orizzontale.
 *
 * Uso:  node scripts/verifica_hero_larghezze.mjs [indirizzo]
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

const LARGHEZZE = [320, 375, 768, 1024, 1440];

const browser = await chromium.launch({ executablePath: exe });
let problemi = 0;

for (const larghezza of LARGHEZZE) {
  const page = await browser.newPage({ viewport: { width: larghezza, height: 900 } });
  await page.goto(`${BASE}/`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);

  const d = await page.evaluate(() => {
    const nav = document.querySelector('nav[aria-label="Cosa vuoi esplorare"]');
    const collegamenti = [...nav.querySelectorAll('.accesso-secondario')].map((a) => {
      const r = a.getBoundingClientRect();
      return { testo: a.textContent.trim().replace(/\s+/g, ' ').slice(0, 24), destra: Math.round(r.right) };
    });
    return {
      collegamenti,
      scorrimentoOrizzontale: document.documentElement.scrollWidth > window.innerWidth + 1,
      larghezzaPagina: document.documentElement.scrollWidth,
    };
  });

  const fuori = d.collegamenti.filter((c) => c.destra > larghezza);
  const ok = !fuori.length && !d.scorrimentoOrizzontale;
  if (!ok) problemi++;

  console.log(
    `  [${ok ? 'OK  ' : 'FAIL'}] ${String(larghezza).padStart(4)}px  ` +
      `collegamenti a destra: ${d.collegamenti.map((c) => c.destra).join(', ')}  ` +
      `pagina larga ${d.larghezzaPagina}`,
  );
  if (fuori.length) {
    for (const f of fuori) console.log(`         esce: «${f.testo}…» a ${f.destra}px`);
  }
  if (d.scorrimentoOrizzontale) console.log('         la pagina scorre in orizzontale');

  await page.close();
}

console.log('');
console.log(problemi ? `PROBLEMI: ${problemi}` : 'nessun trabocco a nessuna larghezza');

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(problemi ? 1 : 0);
