/**
 * Verifica che il meteo si carichi davvero, in un browser vero.
 *
 * Non basta che il blocco esista nell'HTML: quello che conta è che lo script
 * chiami Open-Meteo, riceva i dati e li scriva. Un blocco che resta in
 * «Caricamento del meteo…» è peggio di nessun blocco.
 *
 * Controlla anche i casi che si rompono facilmente:
 *   - il riquadro esce da «in caricamento» (aria-busy torna a false)
 *   - compare una temperatura vera, non un segnaposto
 *   - la località dichiarata è accanto ai dati
 *   - se la rete è bloccata, compare un messaggio leggibile invece di un vuoto
 *
 * Uso:  node scripts/verifica_meteo.mjs [indirizzo]
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
const problemi = [];

function check(nome, ok, dettaglio = '') {
  console.log(`  [${ok ? 'OK  ' : 'FAIL'}] ${nome}${dettaglio ? '  — ' + dettaglio : ''}`);
  if (!ok) problemi.push(nome);
}

// ---------------------------------------------------------------------------
// 1. Il meteo si carica su ogni scheda che lo dichiara
// ---------------------------------------------------------------------------
const SLUG = ['gino-solda', 'grandi-alberi', 'strada-52-gallerie', 'ponte-tibetano', 'campogrosso', 'sentiero-mole'];

const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });

for (const slug of SLUG) {
  await page.goto(`${BASE}/sentieri/${slug}/`, { waitUntil: 'networkidle' });

  const riquadro = page.locator('[data-meteo]');
  const quanti = await riquadro.count();
  if (quanti !== 1) {
    check(`${slug}: un solo riquadro meteo`, false, `trovati ${quanti}`);
    continue;
  }

  // Si aspetta che il caricamento finisca: aria-busy passa a false.
  await page
    .waitForFunction(
      () => document.querySelector('[data-meteo] [data-meteo-corpo]')?.getAttribute('aria-busy') === 'false',
      { timeout: 20000 },
    )
    .catch(() => {});

  const stato = await page.evaluate(() => {
    const el = document.querySelector('[data-meteo]');
    const corpo = el?.querySelector('[data-meteo-corpo]');
    const giorni = corpo?.querySelector('.meteo__giorni');
    const dati = corpo?.querySelector('.meteo__dati');
    return {
      occupato: corpo?.getAttribute('aria-busy'),
      testo: (corpo?.textContent ?? '').replace(/\s+/g, ' ').trim(),
      gradi: corpo?.querySelector('.meteo__gradi')?.textContent?.trim() ?? null,
      luogo: el?.dataset.luogo ?? null,
      luogoVisibile: el?.querySelector('.meteo__luogo')?.textContent?.trim() ?? null,
      giorni: corpo?.querySelectorAll('.meteo__giorni li').length ?? 0,
      gradiVisibili: !!corpo?.querySelector('.meteo__gradi'),
      // Gli stili devono arrivare ANCHE al contenuto creato da JavaScript.
      // Astro, con gli stili "con scopo", lo lascerebbe senza: qui si controlla
      // che la griglia dei giorni sia davvero una griglia e non testo impilato.
      displayGiorni: giorni ? getComputedStyle(giorni).display : null,
      displayDati: dati ? getComputedStyle(dati).display : null,
    };
  });

  const ok = stato.occupato === 'false' && stato.gradiVisibili && /-?\d+°/.test(stato.gradi ?? '');
  check(`${slug}: meteo caricato`, ok, `${stato.gradi ?? '—'} · ${stato.giorni} giorni · ${stato.luogo}`);

  check(
    `${slug}: gli stili arrivano al contenuto iniettato`,
    stato.displayGiorni === 'grid' && stato.displayDati === 'flex',
    `giorni=${stato.displayGiorni} dati=${stato.displayDati}`,
  );

  if (!ok) console.log(`         contenuto: «${stato.testo.slice(0, 120)}»`);
}

// ---------------------------------------------------------------------------
// 2. Senza rete resta un messaggio leggibile, non un riquadro vuoto
//
// Serve un CONTESTO NUOVO, non basta bloccare la rete: la pagina mette i dati
// in sessionStorage per 15 minuti, e su una scheda già visitata il riquadro
// mostrerebbe quelli invece di provare a chiedere. È il comportamento giusto
// — ma allora il guasto non si vedrebbe, e il test passerebbe per il motivo
// sbagliato (o fallirebbe, come è successo la prima volta).
// ---------------------------------------------------------------------------
const contestoPulito = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
const paginaOffline = await contestoPulito.newPage();

await paginaOffline.route('**/api.open-meteo.com/**', (route) => route.abort());
await paginaOffline.goto(`${BASE}/sentieri/strada-52-gallerie/`, { waitUntil: 'domcontentloaded' });

await paginaOffline
  .waitForFunction(
    () => document.querySelector('[data-meteo] [data-meteo-corpo]')?.getAttribute('aria-busy') === 'false',
    { timeout: 20000 },
  )
  .catch(() => {});

const guasto = await paginaOffline.evaluate(() => {
  const corpo = document.querySelector('[data-meteo] [data-meteo-corpo]');
  return {
    occupato: corpo?.getAttribute('aria-busy'),
    testo: (corpo?.textContent ?? '').replace(/\s+/g, ' ').trim(),
  };
});

check(
  'rete bloccata: messaggio leggibile',
  guasto.occupato === 'false' && guasto.testo.length > 20 && /non è disponibile/i.test(guasto.testo),
  guasto.testo.slice(0, 80),
);

await contestoPulito.close();

// ---------------------------------------------------------------------------
// 3. La località dichiarata è accanto ai dati
// ---------------------------------------------------------------------------
await page.goto(`${BASE}/sentieri/gino-solda/`, { waitUntil: 'networkidle' });
const luogo = await page.evaluate(() => {
  const el = document.querySelector('[data-meteo]');
  return {
    dichiarato: el?.dataset.luogo,
    mostrato: el?.querySelector('.meteo__luogo')?.textContent?.trim(),
  };
});
check(
  'la località del meteo è dichiarata in pagina',
  Boolean(luogo.mostrato) && luogo.mostrato.includes(luogo.dichiarato ?? '###'),
  luogo.mostrato,
);

console.log('');
console.log(problemi.length ? `PROBLEMI: ${problemi.length}` : 'meteo funzionante su tutte le schede');

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(problemi.length ? 1 : 0);
