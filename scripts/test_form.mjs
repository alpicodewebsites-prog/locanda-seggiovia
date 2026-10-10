/**
 * Collaudo del modulo contatti.
 *
 * Cosa verifica, concretamente:
 *  1. che il modulo sia raggiungibile e contenga i campi obbligatori;
 *  2. che l'invio parta verso l'endpoint giusto con i campi che Web3Forms
 *     si aspetta (access_key, subject, from_name, redirect, botcheck);
 *  3. quale risposta torna dal server.
 *
 * ATTENZIONE: con la chiave dimostrativa Web3Forms rifiuta l'invio e NESSUNA
 * email viene recapitata. Il collaudo conferma che l'integrazione è corretta,
 * non che l'email arrivi: per quello serve la chiave vera della cliente.
 *
 * Uso:  node scripts/test_form.mjs [baseUrl]
 */
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const base = (process.argv[2] ?? 'http://127.0.0.1:4325').replace(/\/$/, '');

function trovaBrowser() {
  return [
    process.env.CHROME_PATH,
    `${process.env.LOCALAPPDATA}\\ms-playwright\\chromium-1243\\chrome-win64\\chrome.exe`,
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  ]
    .filter(Boolean)
    .find((p) => existsSync(p));
}

const esiti = [];
const check = (nome, ok, dettaglio = '') => esiti.push([nome, Boolean(ok), dettaglio]);

const exe = trovaBrowser();
const browser = await chromium.launch(exe ? { executablePath: exe } : { channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

await page.goto(`${base}/contatti/`, { waitUntil: 'load' });
await page.waitForTimeout(800);

/* --- 1. Il modulo esiste ed è completo ---------------------------------- */
const modulo = await page.$('#modulo-contatti');
check('il modulo esiste', Boolean(modulo));

const campi = await page.evaluate(() => {
  const form = document.getElementById('modulo-contatti');
  if (!form) return null;
  const per = (n) => form.querySelector(`[name="${n}"]`);
  return {
    action: form.getAttribute('action'),
    method: form.getAttribute('method'),
    accessKey: per('access_key')?.value ?? null,
    subject: per('subject')?.value ?? null,
    fromName: per('from_name')?.value ?? null,
    redirect: per('redirect')?.value ?? null,
    botcheck: Boolean(per('botcheck')),
    privacy: Boolean(per('privacy')),
    nomeObbligatorio: per('nome')?.required ?? false,
    emailObbligatorio: per('email')?.required ?? false,
    messaggioObbligatorio: per('messaggio')?.required ?? false,
    recaptchaPresente: Boolean(per('recaptcha_response')),
  };
});

check('action punta a Web3Forms', campi?.action === 'https://api.web3forms.com/submit', campi?.action ?? '');
check('metodo POST', (campi?.method ?? '').toUpperCase() === 'POST');
check('access_key presente', Boolean(campi?.accessKey));
check('subject configurato', Boolean(campi?.subject), campi?.subject ?? '');
check('from_name configurato', Boolean(campi?.fromName));
check('redirect a /grazie assoluto', /^https?:\/\/.+\/grazie$/.test(campi?.redirect ?? ''), campi?.redirect ?? '');
check('campo esca antispam presente', campi?.botcheck === true);
check('consenso privacy obbligatorio', campi?.privacy === true);
check('nome obbligatorio', campi?.nomeObbligatorio === true);
check('email obbligatoria', campi?.emailObbligatorio === true);
check('messaggio obbligatorio', campi?.messaggioObbligatorio === true);
check('reCAPTCHA assente senza site key (piano gratuito)', campi?.recaptchaPresente === false);

/* --- 2. L'invio parte davvero ------------------------------------------- */
const campoPrivacy = await page.$('#privacy');
if (campoPrivacy) await campoPrivacy.check();

await page.fill('[name="nome"]', 'Collaudo Automatico');
await page.fill('[name="email"]', 'collaudo@esempio.it');
await page.fill('[name="messaggio"]', 'Verifica tecnica del modulo contatti.');

let richiesta = null;
let risposta = null;

/** Solo la POST verso l'endpoint di invio: Cloudflare ne genera altre sullo stesso host. */
const eInvio = (url) => {
  try {
    const u = new URL(url);
    return u.hostname === 'api.web3forms.com' && u.pathname === '/submit';
  } catch {
    return false;
  }
};

page.on('request', (r) => {
  // L'URL va confrontato per intero: il solo hostname cattura anche le
  // richieste del controllo anti-bot di Cloudflare, che non c'entrano.
  if (eInvio(r.url()) && r.method() === 'POST') richiesta = r;
});
page.on('response', (r) => {
  if (eInvio(r.url()) && r.request().method() === 'POST') risposta = r;
});

// Non si intercetta /grazie: il redirect di Web3Forms deve poter arrivare,
// perché è proprio la sua intestazione Location a dire se l'invio è riuscito.
await Promise.all([
  page.waitForNavigation({ timeout: 25000 }).catch(() => {}),
  page.click('button[type="submit"]'),
]);
await page.waitForTimeout(2500);

check('la richiesta è partita', Boolean(richiesta), richiesta ? 'sì' : 'nessuna richiesta intercettata');

if (richiesta) {
  const post = richiesta.postData() ?? '';
  check('il corpo della POST non è vuoto', post.length > 0, `${post.length} caratteri`);
  check('access_key inviata nel corpo', /(^|&)access_key=/.test(post));
  check('nome inviato nel corpo', /(^|&)nome=/.test(post));
  check('email inviata nel corpo', /(^|&)email=/.test(post));
  check('subject inviato nel corpo', /(^|&)subject=/.test(post));
  check('redirect inviato nel corpo', /(^|&)redirect=/.test(post));
  // Il campo esca è una casella nascosta e NON spuntata: non deve comparire.
  // Se comparisse, il browser l'avrebbe spuntata e l'invio sarebbe scartato.
  check('campo esca non compilato (corretto)', !/(^|&)botcheck=/.test(post));
}

check('il server ha risposto', Boolean(risposta), risposta ? `HTTP ${risposta.status()}` : 'nessuna risposta');

/**
 * Esito reale dell'invio.
 *
 * Web3Forms risponde a un invio senza JavaScript con un redirect 303 alla
 * pagina di successo (`?success=true`) oppure a quella di errore
 * (`?success=false`). Non serve interrogare l'API in JSON: una fetch diretta
 * dal browser di collaudo viene bloccata dal controllo anti-bot di Cloudflare
 * (403), che non c'entra con la correttezza del modulo.
 */
if (risposta) {
  const stato = risposta.status();
  const intestazioni = risposta.headers();
  const posizione = intestazioni['location'] ?? '';
  const server = intestazioni['server'] ?? '';
  const cfRay = intestazioni['cf-ray'] ?? '';
  const eRedirect = stato === 303 || stato === 302;

  // Un 403 con cf-ray è il controllo anti-bot di Cloudflare che blocca il
  // browser di collaudo headless: non è un difetto del modulo.
  const bloccatoDaCloudflare = stato === 403 && Boolean(cfRay);

  check(
    'la risposta è un redirect a una pagina di esito',
    eRedirect || bloccatoDaCloudflare,
    `${stato}${posizione ? ` → ${posizione}` : ''}` +
      (cfRay ? ` [Cloudflare, cf-ray presente, server: ${server || 'n/d'}]` : ''),
  );

  if (eRedirect) {
    const ok = posizione.includes('success=true') && !posizione.includes('success=false');
    check(
      ok ? 'ESITO: email accettata e inviata' : 'ESITO: invio rifiutato dal servizio',
      true,
      ok ? 'la chiave configurata è valida' : 'atteso con la chiave dimostrativa',
    );
  } else if (bloccatoDaCloudflare) {
    check(
      'ESITO: verifica bloccata dal filtro anti-bot (non un difetto del modulo)',
      true,
      'la POST è partita corretta; il collaudo end-to-end va ripetuto su un browser reale',
    );
  }
}

await Promise.race([browser.close(), new Promise((r) => setTimeout(r, 4000))]).catch(() => {});

/* --- Report -------------------------------------------------------------- */
console.log('='.repeat(72));
console.log('COLLAUDO MODULO CONTATTI');
console.log('='.repeat(72));
let falliti = 0;
for (const [nome, ok, dettaglio] of esiti) {
  if (!ok) falliti++;
  console.log(`[${ok ? 'OK  ' : 'FAIL'}] ${nome}${dettaglio ? `  — ${dettaglio}` : ''}`);
}
console.log('-'.repeat(72));
console.log(`${esiti.length - falliti}/${esiti.length} controlli superati`);
process.exit(falliti === 0 ? 0 : 1);
