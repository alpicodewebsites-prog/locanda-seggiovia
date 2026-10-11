/**
 * Diagnostica dell'impaginazione della pagina Ristorante e dell'ingombro
 * dell'header sulla home.
 *
 * Serve a capire DA COSA dipende un problema di layout, invece di dedurlo
 * da una schermata: misura colonne, altezze e sovrapposizioni reali.
 *
 * Uso:  node scripts/diag_layout.mjs [baseUrl]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const base = (process.argv[2] ?? 'http://127.0.0.1:4340').replace(/\/$/, '');

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
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

/* --- 1. Ristorante: struttura delle sezioni ------------------------------ */
await page.goto(`${base}/ristorante/`, { waitUntil: 'load' });
await page.waitForTimeout(1200);

const rist = await page.evaluate(() => {
  const sezioni = [...document.querySelectorAll('main > section')];

  return sezioni.map((s, i) => {
    const griglie = [...s.querySelectorAll('*')].filter((el) => {
      const d = getComputedStyle(el).display;
      return d === 'grid';
    });

    return {
      indice: i + 1,
      classi: s.className.slice(0, 70),
      altezza: Math.round(s.getBoundingClientRect().height),
      griglie: griglie.map((g) => {
        const cs = getComputedStyle(g);
        const figli = [...g.children];
        return {
          classi: g.className.slice(0, 70),
          colonne: cs.gridTemplateColumns.split(' ').length,
          righe: cs.gridTemplateRows.split(' ').length,
          nFigli: figli.length,
          altezzeFigli: figli.map((f) => Math.round(f.getBoundingClientRect().height)),
        };
      }),
    };
  });
});

console.log('=== STRUTTURA PAGINA RISTORANTE ===\n');
for (const s of rist) {
  console.log(`Sezione ${s.indice} — h=${s.altezza}px — ${s.classi}`);
  for (const g of s.griglie) {
    if (g.colonne > 1 || g.nFigli > 1) {
      console.log(
        `   griglia ${g.colonne}col x ${g.righe}rig, ${g.nFigli} figli ` +
          `[${g.altezzeFigli.join(', ')}]`,
      );
      console.log(`      ${g.classi}`);
    }
  }
}

// Quanti piatti sono "specialità"?
const specialita = await page.$$eval('main section li', (els) =>
  els.filter((e) => e.className.includes('bg-forest-900')).length,
);
console.log(`\nSpecialità in evidenza: ${specialita}`);

/* --- 2. Home: ingombro header e posizione del testo ---------------------- */
await page.goto(`${base}/`, { waitUntil: 'load' });
await page.waitForTimeout(1200);

const home = await page.evaluate(() => {
  const header = document.getElementById('header-sito');
  const eyebrow = [...document.querySelectorAll('main p')].find((p) =>
    p.textContent.includes('Valle dell’Agno'),
  );
  const h1 = document.querySelector('main h1');
  const hero = document.querySelector('main > section');

  const r = (el) => {
    if (!el) return null;
    const b = el.getBoundingClientRect();
    return { top: Math.round(b.top), bottom: Math.round(b.bottom), h: Math.round(b.height) };
  };

  return {
    header: r(header),
    hero: r(hero),
    eyebrow: r(eyebrow),
    h1: r(h1),
    heroPaddingTop: hero ? getComputedStyle(hero).paddingTop : null,
    heroMinHeight: hero ? getComputedStyle(hero).minHeight : null,
    heroMarginTop: hero ? getComputedStyle(hero).marginTop : null,
  };
});

console.log('\n=== HOME: ingombro header vs testo ===\n');
console.log('header      ', JSON.stringify(home.header));
console.log('hero        ', JSON.stringify(home.hero), `margin-top=${home.heroMarginTop}`);
console.log('eyebrow     ', JSON.stringify(home.eyebrow));
console.log('h1          ', JSON.stringify(home.h1));
if (home.header && home.eyebrow) {
  const sovrapposto = home.eyebrow.top < home.header.bottom;
  console.log(
    `\n>>> eyebrow inizia a ${home.eyebrow.top}px, header finisce a ${home.header.bottom}px`,
  );
  console.log(`>>> SOVRAPPOSIZIONE: ${sovrapposto ? 'SÌ' : 'no'}`);
}

/* --- 3. Forma delle immagini -------------------------------------------- */
const forme = await page.evaluate(() => {
  const out = [];
  for (const el of document.querySelectorAll('.media, main img')) {
    const cs = getComputedStyle(el);
    if (cs.borderRadius !== '0px') {
      out.push({ classe: el.className.slice(0, 40), raggio: cs.borderRadius });
    }
  }
  return out;
});
console.log(`\n=== Immagini con angoli arrotondati: ${forme.length} ===`);
for (const f of forme.slice(0, 5)) console.log(`   ${f.raggio} — ${f.classe}`);

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});
process.exit(0);
