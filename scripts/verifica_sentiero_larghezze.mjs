/**
 * Controlla la scheda di un sentiero a cinque larghezze.
 *
 * La fascia dei dati mette sei o sette numeri su una fila: su un telefono
 * devono impilarsi, non uscire dallo schermo. E la colonna delle condizioni
 * deve stare sotto il racconto, non affiancata.
 *
 * Uso:  node scripts/verifica_sentiero_larghezze.mjs [indirizzo]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const BASE = (process.argv[2] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');
const LARGHEZZE = [320, 375, 768, 1024, 1440];
const SLUG = 'orso-e-gallo';

const exe = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].find((p) => p && existsSync(p));

const browser = await chromium.launch({ executablePath: exe });
let problemi = 0;

for (const larghezza of LARGHEZZE) {
  const page = await browser.newPage({ viewport: { width: larghezza, height: 900 } });
  await page.goto(`${BASE}/sentieri/${SLUG}/`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(400);

  const d = await page.evaluate(() => {
    const fila = document.querySelector('.dati-sentiero__fila');
    const celle = fila ? [...fila.querySelectorAll('.dato')] : [];
    const aside = document.querySelector('aside[aria-labelledby="titolo-condizioni"]');
    const racconto = document.querySelector('section[aria-labelledby="titolo-percorso"] .md\\:col-span-6');

    // Su una riga o impilate? Si guarda quante righe occupa la fascia.
    const righe = new Set(celle.map((c) => Math.round(c.getBoundingClientRect().top))).size;

    return {
      celle: celle.length,
      righe,
      fuori: celle.filter((c) => c.getBoundingClientRect().right > window.innerWidth + 1).length,
      scorrimento: document.documentElement.scrollWidth > window.innerWidth + 1,
      larghezzaPagina: document.documentElement.scrollWidth,
      // Se l'aside sta sotto il racconto, il suo top è maggiore.
      sotto: aside && racconto ? aside.getBoundingClientRect().top >= racconto.getBoundingClientRect().bottom - 2 : null,
    };
  });

  const ok = d.fuori === 0 && !d.scorrimento;
  if (!ok) problemi++;

  console.log(
    `  [${ok ? 'OK  ' : 'FAIL'}] ${String(larghezza).padStart(4)}px  ` +
      `${d.celle} celle su ${d.righe} riga/e  pagina ${d.larghezzaPagina}px  ` +
      `condizioni ${d.sotto ? 'sotto il racconto' : 'affiancate'}`,
  );
  if (d.fuori) console.log(`         ${d.fuori} celle escono dallo schermo`);
  if (d.scorrimento) console.log('         la pagina scorre in orizzontale');

  await page.close();
}

console.log('');
console.log(problemi ? `PROBLEMI: ${problemi}` : 'la scheda regge a tutte le larghezze');

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(problemi ? 1 : 0);
