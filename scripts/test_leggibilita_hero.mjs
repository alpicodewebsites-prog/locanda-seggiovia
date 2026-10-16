/**
 * Verifica le aperture delle pagine dei sentieri.
 *
 * Controlla due cose distinte:
 *   1. che la fascia abbia davvero un'immagine di sfondo e che il testo
 *      alternativo dichiari che è un segnaposto, non una fotografia;
 *   2. che il velo scuro serva a rendere leggibile il testo SENZA cancellare
 *      l'immagine: il velo deve essere pesante in basso, dove c'è il testo, e
 *      leggero in alto, dove non c'è.
 *
 * Il contrasto vero fra testo e sfondo si misura sui pixel con
 * `scripts/misura_contrasto_hero.py`, che legge lo screenshot salvato qui.
 *
 * Uso:  node scripts/test_leggibilita_hero.mjs [indirizzo]
 */
import { mkdirSync, rmSync } from 'node:fs';
import { chromium } from 'playwright';

const BASE = (process.argv[2] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');
const USCITA = 'hero-misure';

const CANDIDATI = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].filter(Boolean);

const esiti = [];
const check = (nome, ok, dettaglio = '') => esiti.push([nome, Boolean(ok), dettaglio]);

/**
 * Estrae i valori di opacità dalle tappe del gradiente calcolato.
 *
 * Il formato non è uno solo: i browser moderni restituiscono
 * `color(srgb 0.1 0.1 0.09 / 0.85)` oppure `oklab(0.2 0 0 / 0.85)`, mentre i
 * più vecchi usano `rgba(28, 27, 25, 0.85)`. Si accettano entrambi, altrimenti
 * il controllo non trova niente e fallisce senza motivo.
 */
function opacitaGradiente(valore) {
  const testo = String(valore);
  const trovate = [];

  // Forma moderna: l'opacità sta dopo la barra.
  for (const m of testo.matchAll(/\/\s*([\d.]+)\s*\)/g)) {
    trovate.push({ posizione: m.index, valore: Number(m[1]) });
  }

  // Forma classica: è il quarto numero di rgba().
  for (const m of testo.matchAll(/rgba\([^)]*?,\s*([\d.]+)\s*\)/g)) {
    trovate.push({ posizione: m.index, valore: Number(m[1]) });
  }

  return trovate.sort((a, b) => a.posizione - b.posizione).map((t) => t.valore);
}

async function main() {
  rmSync(USCITA, { recursive: true, force: true });
  mkdirSync(USCITA, { recursive: true });

  const browser = await chromium.launch({ executablePath: CANDIDATI[0] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 760 } });

  const sentieri = ['gino-solda', 'sentiero-mole', 'grandi-alberi'];

  for (const slug of sentieri) {
    await page.goto(`${BASE}/sentieri/${slug}/`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(900);

    const dati = await page.evaluate(() => {
      const fascia = document.querySelector('section');
      const img = fascia.querySelector('img');
      const h1 = fascia.querySelector('h1');
      const velo = fascia.querySelector('[aria-hidden="true"].absolute.inset-0');
      const r = h1.getBoundingClientRect();
      const f = fascia.getBoundingClientRect();

      return {
        haImmagine: Boolean(img),
        alt: img?.alt ?? '',
        colore: getComputedStyle(h1).color,
        gradiente: getComputedStyle(velo).backgroundImage,
        riquadroTitolo: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) },
        fascia: { y: Math.round(f.y), h: Math.round(f.height) },
      };
    });

    check(`[${slug}] la fascia ha un'immagine di sfondo`, dati.haImmagine);
    check(
      `[${slug}] il testo alternativo dichiara che è un segnaposto`,
      /segnaposto/i.test(dati.alt),
      dati.alt.slice(0, 58),
    );

    const opacita = opacitaGradiente(dati.gradiente);
    check(
      `[${slug}] il velo non cancella l’immagine in alto`,
      opacita.length > 0 && opacita[opacita.length - 1] <= 0.25,
      `opacità in alto: ${opacita[opacita.length - 1] ?? 'n/d'}`,
    );
    check(
      `[${slug}] il velo è deciso in basso, dove c’è il testo`,
      opacita.length > 0 && Math.max(...opacita) >= 0.75,
      `opacità massima: ${opacita.length ? Math.max(...opacita) : 'n/d'}`,
    );

    /*
      Si salva DIRETTAMENTE la zona di sfondo da misurare, ritagliata dal
      browser. Così le coordinate sono calcolate in un posto solo.

      La zona sta a DESTRA del titolo, alla stessa altezza: lì non c'è testo e
      si è sicuri di essere dentro la fotografia. Il velo è un gradiente
      verticale, quindi alla stessa altezza lo sfondo è lo stesso che sta dietro
      alle lettere: la misura è fedele.

      Precedenti tentativi e perché sono stati scartati:
        - dentro il riquadro del titolo: il pixel più chiaro erano le lettere
          bianche, e il contrasto risultava 1:1;
        - striscia sopra il titolo: il ritaglio finiva in parte sul fondo della
          pagina, che è quasi bianco, e falsava il caso peggiore.
    */
    const r = dati.riquadroTitolo;
    const xInizio = Math.min(1240, Math.round(r.x + r.w + 24));
    const larghezzaZona = 1280 - xInizio;

    const zona = {
      x: xInizio,
      y: Math.max(0, Math.round(r.y) - 4),
      width: Math.max(40, larghezzaZona),
      height: Math.max(12, Math.round(r.h) + 8),
    };

    await page.screenshot({ path: `${USCITA}/${slug}-sfondo.png`, clip: zona });
    await page.screenshot({
      path: `${USCITA}/${slug}.png`,
      clip: { x: 0, y: Math.max(0, dati.fascia.y), width: 1280, height: Math.min(dati.fascia.h, 760) },
    });

    const fs = await import('node:fs');
    fs.writeFileSync(
      `${USCITA}/${slug}.json`,
      JSON.stringify({ colore: dati.colore, zona, titolo: r }, null, 2),
    );
  }

  await Promise.race([
    browser.close(),
    new Promise((r) => setTimeout(r, 4000)),
  ]).catch(() => {});

  console.log('='.repeat(78));
  console.log('APERTURE DEI SENTIERI');
  console.log('='.repeat(78));
  let falliti = 0;
  for (const [nome, ok, dettaglio] of esiti) {
    if (!ok) falliti++;
    console.log(`[${ok ? 'OK  ' : 'FAIL'}] ${nome}${dettaglio ? `  — ${dettaglio}` : ''}`);
  }
  console.log('-'.repeat(78));
  console.log(`${esiti.length - falliti}/${esiti.length} controlli superati`);
  console.log(`fotogrammi salvati in ${USCITA}/ per la misura sui pixel`);
  process.exit(falliti === 0 ? 0 : 1);
}

main().catch((e) => {
  console.error('errore:', e.message);
  process.exit(1);
});
