/**
 * Controlla i due collegamenti in fondo all'apertura.
 *
 * Non basta guardare: si misura che stiano sulla STESSA riga e sotto la
 * colonna giusta — i sentieri sotto «Le camere», gli gnocchi sotto «Il
 * ristorante». Se la griglia non fosse allineata, i due sembrerebbero uno
 * attaccato all'altro invece di uno per colonna.
 *
 * Uso:  node scripts/verifica_hero_collegamenti.mjs [indirizzo]
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
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
await page.goto(`${BASE}/`, { waitUntil: 'networkidle' });
await page.waitForTimeout(900);

const d = await page.evaluate(() => {
  const nav = document.querySelector('nav[aria-label="Cosa vuoi esplorare"]');
  const accessi = [...nav.querySelectorAll('.accesso')].map((a) => {
    const r = a.getBoundingClientRect();
    return { titolo: a.querySelector('.accesso__titolo')?.textContent.trim(), x: Math.round(r.left), y: Math.round(r.top) };
  });
  const secondari = [...nav.querySelectorAll('.accesso-secondario')].map((a) => {
    const r = a.getBoundingClientRect();
    return {
      testo: a.textContent.trim().replace(/\s+/g, ' '),
      href: a.getAttribute('href'),
      x: Math.round(r.left),
      y: Math.round(r.top),
      colore: getComputedStyle(a).color,
    };
  });
  return { accessi, secondari };
});

console.log('  i due accessi:');
for (const a of d.accessi) console.log(`    ${(a.titolo ?? '').padEnd(16)} x=${a.x} y=${a.y}`);

console.log('  i due collegamenti in fondo:');
for (const a of d.secondari) console.log(`    ${a.testo.padEnd(56)} x=${a.x} y=${a.y}  -> ${a.href}`);

const problemi = [];
if (d.secondari.length !== 2) problemi.push(`attesi 2 collegamenti, trovati ${d.secondari.length}`);

const [s1, s2] = d.secondari;
if (s1 && s2) {
  if (s1.y !== s2.y) problemi.push(`non sono sulla stessa riga: y=${s1.y} contro y=${s2.y}`);
  if (s1.colore !== s2.colore) problemi.push(`colori diversi: ${s1.colore} contro ${s2.colore}`);
  if (s1.href !== '/sentieri') problemi.push(`il primo non porta ai sentieri: ${s1.href}`);
  if (s2.href !== '/gnocchi-con-la-fioreta') problemi.push(`il secondo non porta agli gnocchi: ${s2.href}`);
}
// Ciascuno deve cadere sotto la sua colonna.
if (s1 && d.accessi[0] && Math.abs(s1.x - d.accessi[0].x) > 2) {
  problemi.push(`i sentieri (x=${s1.x}) non sono sotto «Le camere» (x=${d.accessi[0].x})`);
}
if (s2 && d.accessi[1] && Math.abs(s2.x - d.accessi[1].x) > 2) {
  problemi.push(`gli gnocchi (x=${s2.x}) non sono sotto «Il ristorante» (x=${d.accessi[1].x})`);
}

// La vecchia fascia non deve più esistere.
const fascia = await page.locator('.tavolo').count();
if (fascia) problemi.push('la fascia .tavolo esiste ancora');

console.log('');
if (problemi.length) {
  for (const p of problemi) console.log('  [FAIL] ' + p);
} else {
  console.log('  [OK  ] stessa riga, sotto la propria colonna, stesso colore, fascia rimossa');
}

const nav = page.locator('nav[aria-label="Cosa vuoi esplorare"]');
await nav.screenshot({ path: 'hero-collegamenti.png' });
console.log('\n  fotogramma: hero-collegamenti.png');

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(problemi.length ? 1 : 0);
