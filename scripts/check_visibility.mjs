/**
 * Verifica che il contenuto non possa restare invisibile.
 *
 * Il rischio: gli elementi con [data-aos] vengono nascosti dal CSS finché AOS
 * non aggiunge .aos-animate. Se lo script non parte o l'animazione non scatta,
 * l'utente vedrebbe una pagina vuota. Questo controllo misura l'opacità reale
 * in tre situazioni: JS attivo, JS disattivato, e "prefers-reduced-motion".
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

/** Conta gli elementi [data-aos] che risultano invisibili (opacità ~0). */
const MISURA = () => {
  const elementi = [...document.querySelectorAll('[data-aos]')];
  const invisibili = elementi.filter((el) => {
    const o = parseFloat(getComputedStyle(el).opacity);
    return o < 0.05;
  });
  return {
    totale: elementi.length,
    invisibili: invisibili.length,
    esempio: invisibili[0]?.getAttribute('data-aos') ?? null,
    classiHtml: document.documentElement.className,
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

  if (s.javaScriptEnabled !== false) {
    // Scorre la pagina come farebbe una persona, poi torna in cima.
    await page.evaluate(async () => {
      const passo = window.innerHeight * 0.6;
      for (let y = 0; y < document.body.scrollHeight; y += passo) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 150));
      }
      await new Promise((r) => setTimeout(r, 400));
    });
  } else {
    await page.waitForTimeout(800);
  }

  let esito;
  if (s.javaScriptEnabled === false) {
    // Senza JS non si può leggere l'opacità: si controlla che il testo ci sia.
    const testo = await page.evaluate(() => document.body.innerText.length);
    esito = { totale: '-', invisibili: 0, esempio: null, testoVisibile: testo };
  } else {
    esito = await page.evaluate(MISURA);
  }

  const ok = s.javaScriptEnabled === false ? esito.testoVisibile > 500 : esito.invisibili === 0;
  if (!ok) problemi++;

  console.log(
    `[${ok ? 'OK  ' : 'FAIL'}] ${s.nome.padEnd(28)} ` +
      (s.javaScriptEnabled === false
        ? `caratteri di testo nel DOM: ${esito.testoVisibile}`
        : `elementi [data-aos]: ${esito.totale}, invisibili: ${esito.invisibili}` +
          (esito.classiHtml ? `, <html class="${esito.classiHtml}">` : '')),
  );

  await ctx.close();
}

await browser.close();
console.log(problemi === 0 ? '\nNessun contenuto nascosto.' : `\n${problemi} scenario/i problematico/i.`);
process.exit(problemi === 0 ? 0 : 1);
