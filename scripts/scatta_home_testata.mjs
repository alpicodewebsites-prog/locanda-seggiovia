/**
 * Fotogramma dell'apertura della home: logo nell'header, dettagli rossi,
 * pulsanti stondati.
 *
 * Uso:  node scripts/scatta_home_testata.mjs [indirizzo]
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

const misure = await page.evaluate(() => {
  const logo = document.querySelector('.site-header__logo');
  const bottone = document.querySelector('.btn--primary');
  const barretta = document.querySelector('.accesso__eyebrow');
  const freccia = document.querySelector('.accesso-secondario');
  const st = (el, prop) => (el ? getComputedStyle(el)[prop] : null);
  return {
    logoPresente: !!logo,
    logoVisibile: logo ? getComputedStyle(logo).display !== 'none' : false,
    logoAltezza: logo ? Math.round(logo.getBoundingClientRect().height) : null,
    raggioBottone: st(bottone, 'borderRadius'),
    barrettaColore: barretta ? getComputedStyle(barretta, '::before').backgroundColor : null,
    barrettaLarghezza: barretta ? getComputedStyle(barretta, '::before').width : null,
    coloreFreccia: st(freccia, 'color'),
  };
});

console.log('  logo nell\'header  : ' + (misure.logoPresente ? 'presente' : 'ASSENTE') + ' · ' + misure.logoAltezza + ' px · visibile: ' + misure.logoVisibile);
console.log('  raggio dei pulsanti: ' + misure.raggioBottone);
console.log('  barretta rossa     : ' + misure.barrettaColore + ' · ' + misure.barrettaLarghezza);
console.log('  link apertura      : ' + misure.coloreFreccia);

await page.screenshot({ path: 'home-testata.png', clip: { x: 0, y: 0, width: 1440, height: 760 } });
console.log('\n  fotogramma: home-testata.png');

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
