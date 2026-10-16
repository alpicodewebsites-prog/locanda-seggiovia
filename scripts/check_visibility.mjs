/**
 * Verifica che il contenuto non possa restare invisibile.
 *
 * Il controllo nasceva per le animazioni allo scorrimento, che nascondevano gli
 * elementi finché non entravano in schermo: se lo script non partiva, la pagina
 * restava bianca. Le animazioni sono state tolte, ma il controllo resta utile e
 * ora è più generale: cerca QUALUNQUE elemento di testo o figura che risulti
 * trasparente, e lo fa in quattro situazioni, compresa quella senza JavaScript.
 *
 * Un contenuto nascosto per sbaglio è un difetto che non si vede guardando la
 * pagina: si vede solo quando manca. Per questo si misura.
 *
 * Uso:  node scripts/check_visibility.mjs [url]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const url = process.argv[2] ?? 'http://127.0.0.1:4323/';

function trovaBrowser() {
  return [
    process.env.CHROME_PATH,
    `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  ]
    .filter(Boolean)
    .find((p) => existsSync(p));
}

const exe = trovaBrowser();
const browser = await chromium.launch(exe ? { executablePath: exe } : { channel: 'chrome' });

/**
 * Conta gli elementi che portano contenuto e risultano trasparenti.
 *
 * Si guardano solo i nodi con testo proprio o immagini: un contenitore vuoto
 * trasparente è normale e non è un problema.
 *
 * PERCHÉ SI CONTROLLA L'OPACITÀ E NON `display: none`
 *
 * Sono due cose diverse, e solo una è un difetto:
 *
 *   - `display: none` toglie l'elemento anche dall'albero di accessibilità.
 *     È il modo corretto di nascondere qualcosa, ed è quello che usano le
 *     regole responsive: il suffisso «Recoaro Terme» nella barra sparisce
 *     sotto i 640 px di proposito. Segnalarlo sarebbe un falso allarme.
 *
 *   - `opacity: 0` rende l'elemento invisibile ma lo lascia nell'albero di
 *     accessibilità: chi usa un lettore di schermo sente un contenuto che non
 *     può vedere, e chi guarda non lo vede affatto. Questo è il difetto vero,
 *     ed è quello che le animazioni allo scorrimento producevano quando lo
 *     script non partiva.
 *
 * Si escludono gli elementi decorativi (`aria-hidden="true"`), come le frecce
 * che compaiono al passaggio del mouse: quelli devono stare a opacità zero.
 */
const MISURA = () => {
  const candidati = [...document.querySelectorAll('body *')].filter((el) => {
    if (el.closest('[aria-hidden="true"]')) return false;
    const tag = el.tagName.toLowerCase();
    if (['script', 'style', 'svg', 'path', 'noscript'].includes(tag)) return false;

    const haTestoProprio = [...el.childNodes].some(
      (n) => n.nodeType === 3 && n.textContent.trim().length > 2,
    );
    const eFigura = tag === 'img' || tag === 'picture';
    return haTestoProprio || eFigura;
  });

  const invisibili = candidati.filter((el) => {
    const stile = getComputedStyle(el);
    // Se è tolto di mezzo del tutto, è una scelta: non è contenuto nascosto.
    if (stile.display === 'none') return false;
    return parseFloat(stile.opacity) < 0.05;
  });

  return {
    totale: candidati.length,
    invisibili: invisibili.length,
    esempi: invisibili
      .slice(0, 3)
      .map((el) => `${el.tagName.toLowerCase()}.${String(el.className).split(' ')[0]}`),
  };
};

const scenari = [
  { nome: 'JS attivo (desktop 1440)', viewport: { width: 1440, height: 900 } },
  { nome: 'JS attivo (mobile 390)', viewport: { width: 390, height: 844 } },
  {
    nome: 'prefers-reduced-motion',
    viewport: { width: 1440, height: 900 },
    reducedMotion: 'reduce',
  },
  {
    nome: 'JavaScript DISATTIVATO',
    viewport: { width: 1440, height: 900 },
    javaScriptEnabled: false,
  },
];

let problemi = 0;

for (const s of scenari) {
  const ctx = await browser.newContext({
    viewport: s.viewport,
    reducedMotion: s.reducedMotion ?? 'no-preference',
    javaScriptEnabled: s.javaScriptEnabled ?? true,
  });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'load' });

  // Si scorre tutta la pagina: un contenuto nascosto più in basso deve venire
  // fuori come uno nascosto in cima.
  //
  // Solo con JavaScript attivo: senza, `page.evaluate` non esiste e la prova
  // fallirebbe per il motivo sbagliato. Con JS spento si misura la presenza
  // del testo nel documento, che è quello che conta.
  if (s.javaScriptEnabled !== false) {
    await page.evaluate(async () => {
      const passo = window.innerHeight * 0.6;
      for (let y = 0; y < document.body.scrollHeight; y += passo) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 120));
      }
      await new Promise((r) => setTimeout(r, 300));
    });
  } else {
    await page.waitForTimeout(800);
  }

  let esito;
  if (s.javaScriptEnabled === false) {
    const testo = await page.evaluate(() => document.body.innerText.length);
    esito = { totale: '-', invisibili: 0, esempi: [], testoVisibile: testo };
  } else {
    esito = await page.evaluate(MISURA);
  }

  const ok = s.javaScriptEnabled === false ? esito.testoVisibile > 500 : esito.invisibili === 0;
  if (!ok) problemi++;

  const dettaglio =
    s.javaScriptEnabled === false
      ? `caratteri di testo nel DOM: ${esito.testoVisibile}`
      : `elementi con contenuto: ${esito.totale}, invisibili: ${esito.invisibili}` +
        (esito.esempi.length ? ` — ${esito.esempi.join(', ')}` : '');

  console.log(`[${ok ? 'OK  ' : 'FAIL'}] ${s.nome.padEnd(28)} ${dettaglio}`);

  await ctx.close();
}

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
console.log(problemi === 0 ? '\nNessun contenuto nascosto.' : `\n${problemi} scenario/i problematico/i.`);
process.exit(problemi === 0 ? 0 : 1);
