/**
 * Verifica delle animazioni di scorrimento.
 *
 * Non basta scrivere `data-aos` nel markup: bisogna accertarsi che l'elemento
 * parta davvero spostato e trasparente, che arrivi a posto quando entra nello
 * schermo, e che la durata sia quella voluta.
 *
 * Controlla:
 *   1. gli attributi vengano assegnati a molti elementi strutturali;
 *   2. l'apertura della home NON sia animata;
 *   3. un elemento fuori schermo parta con opacità 0 e spostato;
 *   4. dopo lo scorrimento arrivi a opacità 1 e senza spostamento;
 *   5. la durata sia 400 ms e la curva quella prevista;
 *   6. con «meno movimento» tutto resti visibile e senza transizioni;
 *   7. sotto i 768 px le animazioni non vengano assegnate;
 *   8. senza JavaScript il contenuto resti leggibile.
 *
 * Uso:  node scripts/test_animazioni.mjs [indirizzo]
 */
import { chromium } from 'playwright';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);

const BASE = (process.argv[2] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');

const CANDIDATI = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].filter(Boolean);

const esiti = [];
const check = (nome, ok, dettaglio = '') => esiti.push([nome, Boolean(ok), dettaglio]);

const stile = (locator, proprieta) =>
  locator.evaluate((el, p) => getComputedStyle(el)[p], proprieta);

/** Durata in millisecondi della prima transizione dichiarata. */
function durataMs(valore) {
  const prima = String(valore).split(',')[0].trim();
  return prima.endsWith('ms') ? parseFloat(prima) : parseFloat(prima) * 1000;
}

async function main() {
  const browser = await chromium.launch({ executablePath: CANDIDATI[0] });

  /* --- 1-5. Animazioni attive su schermo grande ------------------------- */
  {
    const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await context.newPage();
    await page.goto(`${BASE}/`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1200);

    const quanti = await page.evaluate(
      () => document.querySelectorAll('main [data-aos]').length,
    );
    check(
      'gli elementi animati sono numerosi (non solo qualcuno)',
      quanti >= 20,
      `${quanti} elementi con data-aos`,
    );

    const tipi = await page.evaluate(() => {
      const conteggio = {};
      document.querySelectorAll('main [data-aos]').forEach((el) => {
        const t = el.getAttribute('data-aos');
        conteggio[t] = (conteggio[t] ?? 0) + 1;
      });
      return conteggio;
    });
    check(
      'si usano animazioni diverse per tipo di elemento',
      Object.keys(tipi).length >= 2,
      Object.entries(tipi)
        .map(([t, n]) => `${t}:${n}`)
        .join(' '),
    );

    // L'apertura non deve comparire: è già a schermo quando la pagina si apre.
    const heroAnimato = await page.evaluate(
      () => document.querySelectorAll('.hero-apertura [data-aos]').length,
    );
    check('l’apertura non è animata', heroAnimato === 0, `${heroAnimato} elementi`);

    // Un elemento più in basso: deve partire nascosto e spostato.
    const bersaglio = page.locator('main [data-aos="fade-up"]').nth(3);
    const opacitaPrima = await stile(bersaglio, 'opacity');
    const trasformazionePrima = await stile(bersaglio, 'transform');

    check(
      'prima di entrare in schermo l’elemento è trasparente',
      parseFloat(opacitaPrima) < 0.2,
      opacitaPrima,
    );
    check(
      'prima di entrare in schermo l’elemento è spostato verso il basso',
      trasformazionePrima !== 'none',
      trasformazionePrima,
    );

    const durata = durataMs(await stile(bersaglio, 'transitionDuration'));
    check('durata 400 ms', durata === 400, `${durata} ms`);

    const curva = await stile(bersaglio, 'transitionTimingFunction');
    check(
      'curva morbida cubic-bezier',
      String(curva).includes('cubic-bezier'),
      String(curva),
    );

    const ritardo = durataMs(await stile(bersaglio, 'transitionDelay'));
    check('ritardo entro i 200 ms', ritardo <= 200, `${ritardo} ms`);

    // Scorrimento: l'elemento deve arrivare a posto.
    await bersaglio.scrollIntoViewIfNeeded();
    await page.waitForTimeout(1400);

    const opacitaDopo = await stile(bersaglio, 'opacity');
    const trasformazioneDopo = await stile(bersaglio, 'transform');

    check(
      'dopo lo scorrimento l’elemento è visibile',
      parseFloat(opacitaDopo) > 0.9,
      opacitaDopo,
    );
    check(
      'dopo lo scorrimento l’elemento è a posto',
      trasformazioneDopo === 'none' || trasformazioneDopo === 'matrix(1, 0, 0, 1, 0, 0)',
      trasformazioneDopo,
    );

    await context.close();
  }

  /* --- 6. Meno movimento ------------------------------------------------ */
  {
    const context = await browser.newContext({
      viewport: { width: 1280, height: 900 },
      reducedMotion: 'reduce',
    });
    const page = await context.newPage();
    await page.goto(`${BASE}/`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(800);

    const invisibili = await page.evaluate(
      () =>
        [...document.querySelectorAll('main [data-aos]')].filter(
          (el) => getComputedStyle(el).opacity !== '1',
        ).length,
    );
    check('con meno movimento nessun elemento resta nascosto', invisibili === 0, `${invisibili}`);

    await context.close();
  }

  /* --- 7. Schermo piccolo ----------------------------------------------- */
  {
    const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const page = await context.newPage();
    await page.goto(`${BASE}/`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(800);

    const assegnati = await page.evaluate(
      () => document.querySelectorAll('main [data-aos]').length,
    );
    check('sotto i 768 px le animazioni non vengono assegnate', assegnati === 0, `${assegnati}`);

    /*
      Nessun contenuto nascosto.
      Si guardano solo gli elementi che NASCONDONO contenuto per scelta del
      foglio di stile, non le frecce che compaiono al passaggio del mouse: quelle
      sono `opacity: 0` per progetto e non c'entrano con le animazioni. */
    const nascosti = await page.evaluate(() => {
      const candidati = document.querySelectorAll('main h2, main h3, main p, main figure, main dl');
      return [...candidati].filter((el) => getComputedStyle(el).opacity === '0').length;
    });
    check('su mobile nessun testo o figura resta nascosto', nascosti === 0, `${nascosti}`);

    const titoloVisibile = await page.locator('main h2').first().isVisible();
    check('su mobile i titoli sono visibili', titoloVisibile);

    await context.close();
  }

  /* --- 8. Senza JavaScript ---------------------------------------------- */
  {
    const context = await browser.newContext({
      viewport: { width: 1280, height: 900 },
      javaScriptEnabled: false,
    });
    const page = await context.newPage();
    await page.goto(`${BASE}/la-locanda/`, { waitUntil: 'load' });
    await page.waitForTimeout(400);

    const testo = await page.evaluate(() => document.body.innerText.length).catch(() => 0);
    check('senza JavaScript la pagina ha contenuto', testo > 500, `${testo} caratteri`);

    await context.close();
  }

  await Promise.race([
    browser.close(),
    new Promise((risolvi) => setTimeout(risolvi, 4000)),
  ]).catch(() => {});

  console.log('='.repeat(78));
  console.log('ANIMAZIONI DI SCORRIMENTO');
  console.log('='.repeat(78));
  let falliti = 0;
  for (const [nome, ok, dettaglio] of esiti) {
    if (!ok) falliti++;
    console.log(`[${ok ? 'OK  ' : 'FAIL'}] ${nome}${dettaglio ? `  — ${dettaglio}` : ''}`);
  }
  console.log('-'.repeat(78));
  console.log(`${esiti.length - falliti}/${esiti.length} controlli superati`);
  process.exit(falliti === 0 ? 0 : 1);
}

main().catch((errore) => {
  console.error('errore:', errore.message);
  process.exit(1);
});
