/**
 * Verifica la configurazione del pannello di gestione (public/admin/config.yml).
 *
 * Nasce da un errore reale: un campo inserito con il rientro sbagliato ha reso
 * il file YAML non analizzabile, e il pannello mostrava «C'è un errore nella
 * configurazione del CMS» senza dire dove. Questo controllo lo intercetta prima
 * del deploy.
 *
 * Controlla:
 *   1. che il file sia YAML valido;
 *   2. che ogni collezione abbia nome, etichetta e un percorso;
 *   3. che la cartella o il file indicati esistano davvero nel progetto;
 *   4. che i nomi dei campi non siano duplicati dentro la stessa collezione.
 *
 * Uso:  node scripts/verifica_config.mjs
 */
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const YAML = require('yaml');

const RADICE = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const CONFIG = resolve(RADICE, 'public/admin/config.yml');

const esiti = [];
const check = (nome, ok, dettaglio = '') => esiti.push([nome, Boolean(ok), dettaglio]);

/* --- 1. Il file si analizza? --------------------------------------------- */
let config = null;

if (!existsSync(CONFIG)) {
  check('config.yml esiste', false, CONFIG);
} else {
  const testo = readFileSync(CONFIG, 'utf8');
  try {
    config = YAML.parse(testo);
    check('config.yml è YAML valido', true);
  } catch (errore) {
    // Il messaggio del parser indica riga e colonna: è l'informazione che serve
    const messaggio = String(errore.message).split('\n')[0];
    const posizione = errore.linePos?.[0];
    check(
      'config.yml è YAML valido',
      false,
      posizione ? `${messaggio} (riga ${posizione.line}, colonna ${posizione.col})` : messaggio,
    );
  }
}

/* --- Controlli sulle collezioni ------------------------------------------ */
if (config) {
  check('esiste la sezione backend', Boolean(config.backend), config.backend?.name ?? '');
  check(
    'il backend è github con un repository',
    config.backend?.name === 'github' && Boolean(config.backend?.repo),
    config.backend?.repo ?? '',
  );

  const collezioni = Array.isArray(config.collections) ? config.collections : [];
  check('ci sono collezioni', collezioni.length > 0, `${collezioni.length} collezioni`);

  for (const c of collezioni) {
    const etichetta = c?.name ?? '(senza nome)';

    check(`[${etichetta}] ha un nome`, Boolean(c?.name));
    check(`[${etichetta}] ha un'etichetta`, Boolean(c?.label));

    // Collezione a cartella (più file) oppure a file singolo (impostazioni)
    const aCartella = Boolean(c?.folder);
    const aFileSingolo = Array.isArray(c?.files) && c.files.length > 0;

    check(
      `[${etichetta}] ha un percorso (folder oppure files)`,
      aCartella || aFileSingolo,
      aCartella ? c.folder : aFileSingolo ? c.files.map((f) => f.file).join(', ') : 'nessuno',
    );

    // I percorsi devono esistere nel progetto
    const percorsi = aCartella ? [c.folder] : (c.files ?? []).map((f) => f.file);
    for (const percorso of percorsi) {
      if (!percorso) continue;
      const assoluto = resolve(RADICE, percorso.replace(/^\//, ''));
      check(`[${etichetta}] il percorso esiste`, existsSync(assoluto), percorso);
    }

    // Campi: nessun duplicato, e ogni campo ha un widget
    const gruppi = aCartella ? [{ nome: etichetta, campi: c.fields ?? [] }] : (c.files ?? []).map((f) => ({ nome: `${etichetta}/${f.name ?? f.file}`, campi: f.fields ?? [] }));

    for (const gruppo of gruppi) {
      const nomi = gruppo.campi.map((f) => f?.name).filter(Boolean);
      const duplicati = nomi.filter((n, i) => nomi.indexOf(n) !== i);
      check(
        `[${gruppo.nome}] nessun campo duplicato`,
        duplicati.length === 0,
        duplicati.join(', '),
      );
      const senzaWidget = gruppo.campi.filter((f) => f?.name && !f?.widget).map((f) => f.name);
      check(
        `[${gruppo.nome}] ogni campo ha un widget`,
        senzaWidget.length === 0,
        senzaWidget.join(', '),
      );
    }
  }
}

/* --- Report --------------------------------------------------------------- */
console.log('='.repeat(74));
console.log('VERIFICA CONFIGURAZIONE PANNELLO');
console.log('='.repeat(74));

let falliti = 0;
for (const [nome, ok, dettaglio] of esiti) {
  if (!ok) falliti++;
  console.log(`[${ok ? 'OK  ' : 'FAIL'}] ${nome}${dettaglio ? `  — ${dettaglio}` : ''}`);
}

console.log('-'.repeat(74));
console.log(`${esiti.length - falliti}/${esiti.length} controlli superati`);
process.exit(falliti === 0 ? 0 : 1);
