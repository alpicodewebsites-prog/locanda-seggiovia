/**
 * Verifica le micro-interazioni introdotte con la revisione del design.
 *
 * Non basta scrivere una transizione nel CSS: bisogna accertarsi che lo stato
 * cambi davvero al passaggio del mouse e al focus da tastiera, e che la durata
 * resti nella finestra 150-300 ms chiesta dal brief.
 *
 * Controlla:
 *   1. apertura: la freccia entra e l'etichetta cambia colore al passaggio;
 *   2. apertura: la stessa risposta arriva con il focus da tastiera;
 *   3. schede dei piatti: la linea sotto il nome si allunga;
 *   4. schede dei piatti: la freccia compare;
 *   5. foto dei piatti: l'immagine si ingrandisce;
 *   6. le durate sono fra 150 e 300 ms;
 *   7. con prefers-reduced-motion le transizioni si annullano.
 *
 * Uso:  node scripts/test_microinterazioni.mjs [indirizzo]
 */
import { chromium } from 'playwright';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);

const BASE = process.argv[2] ?? 'http://127.0.0.1:4340';

// Il browser di sistema: quello scaricato da Playwright qui non combacia.
const CANDIDATI = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].filter(Boolean);

const esiti = [];
const check = (nome, ok, dettaglio = '') => esiti.push([nome, Boolean(ok), dettaglio]);

/** Legge una proprietà calcolata di un elemento. */
const stile = (locator, proprieta) =>
  locator.evaluate((el, p) => getComputedStyle(el)[p], proprieta);

async function apri(browser, riduciMovimento = false) {
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    reducedMotion: riduciMovimento ? 'reduce' : 'no-preference',
  });
  const page = await context.newPage();
  return { context, page };
}

/** Durata in millisecondi della prima transizione dichiarata. */
function durataMs(valore) {
  const prima = String(valore).split(',')[0].trim();
  return prima.endsWith('ms') ? parseFloat(prima) : parseFloat(prima) * 1000;
}

async function main() {
  const browser = await chromium.launch({ executablePath: CANDIDATI[0] });

  /* --- 1-2. La biforcazione nell'apertura ------------------------------- */
  {
    const { context, page } = await apri(browser);
    await page.goto(`${BASE}/`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(600);

    const accesso = page.locator('.accesso').first();
    const freccia = accesso.locator('.accesso__freccia');
    const eyebrow = accesso.locator('.accesso__eyebrow');

    check('apertura: i due accessi esistono', (await page.locator('.accesso').count()) === 2);

    const opacitaPrima = await stile(freccia, 'opacity');
    const spostamentoPrima = await stile(freccia, 'transform');
    const colorePrima = await stile(eyebrow, 'color');

    await accesso.hover();
    await page.waitForTimeout(450);

    const opacitaDopo = await stile(freccia, 'opacity');
    const spostamentoDopo = await stile(freccia, 'transform');
    const coloreDopo = await stile(eyebrow, 'color');

    check(
      'apertura: al passaggio la freccia compare',
      parseFloat(opacitaPrima) === 0 && parseFloat(opacitaDopo) > 0.9,
      `${opacitaPrima} -> ${opacitaDopo}`,
    );
    check(
      'apertura: la freccia scorre dentro',
      spostamentoPrima !== spostamentoDopo,
      `${spostamentoPrima} -> ${spostamentoDopo}`,
    );
    check('apertura: l’etichetta cambia colore', colorePrima !== coloreDopo, `${colorePrima} -> ${coloreDopo}`);

    // Focus da tastiera: deve dare la stessa risposta del mouse
    await page.mouse.move(0, 0);
    await page.waitForTimeout(400);
    await accesso.focus();
    await page.waitForTimeout(450);
    check(
      'apertura: la stessa risposta arriva col focus da tastiera',
      parseFloat(await stile(freccia, 'opacity')) > 0.9,
    );
    check(
      'apertura: il focus è visibile',
      (await stile(accesso, 'outlineStyle')) !== 'none',
      await stile(accesso, 'outlineStyle'),
    );

    const durata = durataMs(await stile(freccia, 'transitionDuration'));
    check('apertura: durata fra 150 e 300 ms', durata >= 150 && durata <= 300, `${durata} ms`);

    await context.close();
  }

  /* --- 3-4. Le schede dei piatti sulla home ---------------------------- */
  {
    const { context, page } = await apri(browser);
    await page.goto(`${BASE}/`, { waitUntil: 'networkidle' });

    const scheda = page.locator('.scheda-piatto').first();
    await scheda.scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);

    const nome = scheda.locator('.scheda-piatto__nome');
    const freccia = scheda.locator('.scheda-piatto__freccia');

    // La linea è un ::after: si legge la trasformazione dichiarata
    const lineaPrima = await nome.evaluate(
      (el) => getComputedStyle(el, '::after').transform,
    );
    const opacitaPrima = await stile(freccia, 'opacity');
    const sfondoPrima = await stile(scheda, 'backgroundColor');

    await scheda.hover();
    await page.waitForTimeout(450);

    const lineaDopo = await nome.evaluate((el) => getComputedStyle(el, '::after').transform);
    const opacitaDopo = await stile(freccia, 'opacity');
    const sfondoDopo = await stile(scheda, 'backgroundColor');

    check(
      'scheda piatto: la linea sotto il nome si allunga',
      lineaPrima !== lineaDopo,
      `${lineaPrima} -> ${lineaDopo}`,
    );
    check(
      'scheda piatto: la freccia compare',
      parseFloat(opacitaPrima) === 0 && parseFloat(opacitaDopo) > 0.9,
      `${opacitaPrima} -> ${opacitaDopo}`,
    );
    check('scheda piatto: lo sfondo si scalda', sfondoPrima !== sfondoDopo);

    const durata = durataMs(await stile(scheda, 'transitionDuration'));
    check('scheda piatto: durata fra 150 e 300 ms', durata >= 150 && durata <= 300, `${durata} ms`);

    check(
      'scheda piatto: le informazioni restano sempre visibili',
      (await scheda.locator('.scheda-piatto__testo').isVisible()) &&
        (await scheda.locator('.scheda-piatto__etichetta').isVisible()),
    );

    await context.close();
  }

  /* --- 5. Lo zoom sulle foto dei piatti -------------------------------- */
  {
    const { context, page } = await apri(browser);
    await page.goto(`${BASE}/ristorante/`, { waitUntil: 'networkidle' });

    const figure = page.locator('.foto-piatto').first();
    const quante = await page.locator('.foto-piatto').count();

    if (quante === 0) {
      check('foto piatto: nessuna foto presente, controllo saltato', false, 'nessun elemento');
    } else {
      await figure.scrollIntoViewIfNeeded();
      await page.waitForTimeout(500);

      const img = figure.locator('img');
      const prima = await stile(img, 'transform');

      await figure.hover();
      await page.waitForTimeout(450);

      const dopo = await stile(img, 'transform');
      check('foto piatto: l’immagine si ingrandisce', prima !== dopo, `${prima} -> ${dopo}`);

      const durata = durataMs(await stile(img, 'transitionDuration'));
      check('foto piatto: durata fra 150 e 300 ms', durata >= 150 && durata <= 300, `${durata} ms`);

      // Il contenitore non deve cambiare dimensione: nessuno spostamento attorno
      const riquadroPrima = await figure.locator('.media').boundingBox();
      await page.mouse.move(0, 0);
      await page.waitForTimeout(400);
      const riquadroDopo = await figure.locator('.media').boundingBox();
      check(
        'foto piatto: il riquadro non si sposta',
        Math.abs(riquadroPrima.height - riquadroDopo.height) < 1,
        `${riquadroPrima.height} -> ${riquadroDopo.height}`,
      );
    }

    await context.close();
  }

  /* --- 7. Rispetto di prefers-reduced-motion --------------------------- */
  {
    const { context, page } = await apri(browser, true);
    await page.goto(`${BASE}/`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(500);

    const accesso = page.locator('.accesso').first();
    const durata = durataMs(await stile(accesso.locator('.accesso__freccia'), 'transitionDuration'));
    // Il browser riporta un valore minimo (0.001 ms) invece di zero esatto:
    // sotto il millisecondo la transizione è di fatto annullata.
    check('meno movimento: le transizioni si annullano', durata < 1, `${durata} ms`);

    const opacita = await stile(accesso.locator('.accesso__freccia'), 'opacity');
    check(
      'meno movimento: la freccia resta comunque visibile',
      parseFloat(opacita) > 0.9,
      opacita,
    );

    await context.close();
  }

  // La chiusura del browser in questo ambiente a volte non ritorna: si mette un
  // limite di tempo, altrimenti lo script resta appeso per sempre.
  await Promise.race([
    browser.close(),
    new Promise((risolvi) => setTimeout(risolvi, 4000)),
  ]).catch(() => {});

  /* --- Report ---------------------------------------------------------- */
  console.log('='.repeat(78));
  console.log('MICRO-INTERAZIONI');
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
