/**
 * Fotografa la pagina d'apertura così com'è quando arriva un visitatore nuovo.
 *
 * `localStorage` è vuoto in un contesto nuovo di zecca: è esattamente la
 * condizione del primo arrivo, che è quella che vogliamo vedere.
 *
 * Uso:  node scripts/scatta_apertura.mjs [indirizzo]
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

for (const [nome, lar] of [
  ['desktop', 1440],
  ['telefono', 390],
]) {
  const contesto = await browser.newContext({
    viewport: { width: lar, height: lar > 500 ? 900 : 844 },
  });
  const page = await contesto.newPage();
  await page.goto(`${BASE}/en/`, { waitUntil: 'networkidle' });

  // Il velo compare solo con JavaScript: si aspetta che lo faccia.
  await page.waitForSelector('.apertura.is-visibile', { timeout: 8000 }).catch(() => {
    console.log(`  [${nome}] il velo NON è comparso`);
  });
  await page.waitForTimeout(700);

  const dati = await page.evaluate(() => {
    const velo = document.querySelector('.apertura');
    const scelte = [...document.querySelectorAll('[data-scelta]')];
    const st = velo ? getComputedStyle(velo) : null;
    return {
      visibile: velo?.classList.contains('is-visibile') ?? false,
      fondo: st?.backgroundColor ?? null,
      larghezza: velo ? Math.round(velo.getBoundingClientRect().width) : 0,
      trabocca: document.documentElement.scrollWidth > window.innerWidth + 1,
      scelte: scelte.map((s) => s.textContent?.trim()),
      fuoco: document.activeElement?.textContent?.trim() ?? null,
    };
  });

  console.log(
    `  [${nome}] visibile=${dati.visibile} fondo=${dati.fondo} scelte=${dati.scelte.join(' / ')} fuoco=${dati.fuoco} trabocca=${dati.trabocca}`,
  );

  await page.screenshot({ path: `apertura-${nome}.png` });
  await contesto.close();
}

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
