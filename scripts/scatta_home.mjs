/**
 * Scatta la home: apertura, carosello, e cambio diapositiva.
 *
 * Serve a vedere davvero com'è, non a dedurlo dall'HTML: il carosello è fatto di
 * posizioni e animazioni, e solo uno scatto dice se sta in piedi.
 *
 * Uso:  node scripts/scatta_home.mjs [indirizzo]
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

for (const [nome, larghezza, altezza] of [
  ['desktop', 1440, 900],
  ['telefono', 390, 844],
]) {
  const page = await browser.newPage({ viewport: { width: larghezza, height: altezza } });
  await page.goto(`${BASE}/`, { waitUntil: 'networkidle' });

  // Si sceglie l'italiano nell'apertura, come farebbe una persona.
  const scelta = page.locator('[data-scelta="it"]');
  if (await scelta.count()) {
    await scelta.first().click();
    await page.waitForLoadState('networkidle');
  }

  const carosello = page.locator('[data-carosello]');
  await carosello.scrollIntoViewIfNeeded();
  await page.waitForTimeout(700);

  await page.screenshot({ path: `home-carosello-${nome}.png` });

  // Stato del carosello: quale diapositiva è visibile, e i comandi ci sono?
  const stato = await page.evaluate(() => {
    const radice = document.querySelector('[data-carosello]');
    if (!radice) return null;
    const visibili = Array.from(radice.querySelectorAll('[data-diapositiva]')).filter(
      (d) => getComputedStyle(d).display !== 'none',
    );
    const immagini = Array.from(radice.querySelectorAll('img')).map((img) => ({
      naturalWidth: img.naturalWidth,
      reso: img.currentWidth ?? img.clientWidth,
    }));
    return {
      attivo: radice.getAttribute('data-carosello'),
      visibili: visibili.length,
      titolo: visibili[0]?.querySelector('h3')?.textContent?.trim() ?? '',
      altezza: Math.round(radice.getBoundingClientRect().height),
      immagini,
    };
  });

  console.log(
    `  [${nome}] diapositive visibili=${stato?.visibili} · altezza=${stato?.altezza}px · «${stato?.titolo}»`,
  );
  console.log(
    `            immagini: ${stato?.immagini.map((i) => i.naturalWidth).join(', ')} px di sorgente`,
  );

  // Si preme «avanti» e si guarda se cambia.
  await page.locator('[data-avanti]').click();
  await page.waitForTimeout(700);
  const dopo = await page.evaluate(() => {
    const visibile = Array.from(
      document.querySelectorAll('[data-carosello] [data-diapositiva]'),
    ).find((d) => getComputedStyle(d).display !== 'none');
    return visibile?.querySelector('h3')?.textContent?.trim() ?? '';
  });
  console.log(`            dopo «avanti»: «${dopo}»`);

  await page.screenshot({ path: `home-carosello-${nome}-2.png` });
  await page.close();
}

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
