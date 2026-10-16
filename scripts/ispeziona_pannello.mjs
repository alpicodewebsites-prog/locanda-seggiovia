/**
 * Ispezione del pannello Sveltia con un token, in SOLA LETTURA.
 *
 * Percorso: si preme «Accedi con Token di Accesso», si incolla il token, e si
 * legge quello che il pannello mostra. NON SALVA NULLA: non compila contenuti,
 * non preme Salva, non carica file.
 *
 * Il token arriva da una variabile d'ambiente e non viene mai scritto su disco.
 *
 * Uso:  GITHUB_TOKEN=... node scripts/ispeziona_pannello.mjs [indirizzo]
 */
import { existsSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const BASE = (process.argv[2] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');
const TOKEN = process.env.GITHUB_TOKEN;
const USCITA = process.env.USCITA ?? 'pannello.txt';

const righe = [];
const scrivi = (t = '') => {
  righe.push(t);
  console.log(t);
};

const exe = [
  process.env.PW,
  `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
].find((p) => p && existsSync(p));

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });

const errori = [];
page.on('console', (m) => {
  if (m.type() === 'error') errori.push(m.text().slice(0, 180));
});

await page.goto(`${BASE}/admin/`, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3500);

// --- 1. Si apre la schermata del token -------------------------------------
const apriToken = page.getByRole('button', { name: /Accedi con Token/i }).first();
if (await apriToken.count()) {
  await apriToken.click();
  await page.waitForTimeout(1500);
  scrivi('  premuto «Accedi con Token di Accesso»');
} else {
  scrivi('  pulsante del token non trovato');
}

const campi = await page.evaluate(() =>
  [...document.querySelectorAll('input')].map((i) => ({
    tipo: i.type,
    nome: i.name || i.id || '',
    segnaposto: i.placeholder || '',
  })),
);
scrivi(`  campi di input: ${campi.length}`);
for (const c of campi) scrivi(`    tipo=${c.tipo} nome="${c.nome}"`);

// --- 2. Si incolla il token e si entra -------------------------------------
const campo = page.locator('input[type="password"], input[type="text"]').first();
if (await campo.count()) {
  await campo.fill(TOKEN);
  const avanti = page.getByRole('button', { name: /^Accedi$|^Continua$|^Sign in$|^Login$/i }).first();
  if (await avanti.count()) {
    await avanti.click();
  } else {
    await campo.press('Enter');
  }
  scrivi('  token inserito, attesa del caricamento del repository');
  await page.waitForTimeout(14000);
} else {
  scrivi('  NESSUN campo dove incollare il token');
}

scrivi(`\n  indirizzo dopo l'accesso: ${page.url()}`);

// --- 3. Che cosa mostra il pannello ----------------------------------------
const contenuto = await page.evaluate(() => document.body.innerText.replace(/\n{2,}/g, '\n').slice(0, 2200));
scrivi('\n=== schermata del pannello ===');
scrivi(contenuto);

// --- 4. Le voci delle collezioni -------------------------------------------
const voci = await page.evaluate(() => {
  const sel = 'nav a, nav button, aside a, aside button, [class*="sidebar"] a, [class*="sidebar"] button';
  return [...new Set([...document.querySelectorAll(sel)].map((e) => e.textContent.trim()).filter((t) => t && t.length < 50))];
});
scrivi('\n=== voci del pannello ===');
for (const v of voci) scrivi(`  - ${v}`);

if (errori.length) {
  scrivi('\n=== errori in console ===');
  for (const e of errori.slice(0, 12)) scrivi(`  ${e}`);
} else {
  scrivi('\n  nessun errore in console');
}

await page.screenshot({ path: 'pannello.png' });
writeFileSync(USCITA, righe.join('\n'), 'utf-8');
scrivi(`\n  resoconto in ${USCITA}, fotogramma in pannello.png`);

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
