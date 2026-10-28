/**
 * Controlla il file di configurazione del pannello.
 *
 * Il pannello non parte se il file non è YAML valido, e se ne accorge la
 * cliente — non io. Meglio accorgersene qui.
 *
 * Uso:  node scripts/verifica_pannello.mjs
 */
import { existsSync, readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';

const require = createRequire(import.meta.url);

let parseYaml = null;
for (const nome of ['yaml', 'js-yaml']) {
  try {
    const modulo = require(nome);
    parseYaml = nome === 'yaml' ? (t) => modulo.parse(t) : (t) => modulo.load(t);
    break;
  } catch {
    /* si prova il prossimo */
  }
}

if (!parseYaml) {
  console.log('  [FAIL] nessun lettore YAML disponibile (yaml o js-yaml)');
  process.exit(1);
}

const CONFIG = 'public/admin/config.yml';
const testo = readFileSync(CONFIG, 'utf8');

let problemi = 0;
const controlla = (nome, ok, nota = '') => {
  console.log(`  [${ok ? 'OK  ' : 'FAIL'}] ${nome}${nota ? ` — ${nota}` : ''}`);
  if (!ok) problemi++;
};

let dati;
try {
  dati = parseYaml(testo);
  controlla('il file è YAML valido', true);
} catch (errore) {
  controlla('il file è YAML valido', false, String(errore).split('\n')[0]);
  process.exit(1);
}

/*
  Nell'elenco può esserci anche un separatore (`divider: true`), che non è una
  collezione e non ha nome. Va tolto prima di controllare il resto, altrimenti
  il primo `name.endsWith` esplode.
*/
const voci = dati.collections ?? [];
const separatori = voci.filter((v) => v.divider === true);
const collezioni = voci.filter((v) => v.name);
controlla('ci sono collezioni', collezioni.length > 0, `${collezioni.length}`);
controlla(
  'c\'è un separatore fra italiano e inglese',
  separatori.length === 1,
  `${separatori.length} separatori`,
);

// Nomi unici: due collezioni con lo stesso nome rompono il pannello.
const nomi = collezioni.map((c) => c.name);
controlla('i nomi delle collezioni sono unici', new Set(nomi).size === nomi.length);

// Ogni collezione deve avere etichetta, e un posto da cui leggere.
const senzaLettura = collezioni.filter((c) => !c.folder && !c.files);
controlla('ogni collezione ha una cartella o un elenco di file', senzaLettura.length === 0,
  senzaLettura.map((c) => c.name).join(', '));

// Le collezioni inglesi devono leggere le cartelle `en/`.
const inglesi = collezioni.filter((c) => c.name.endsWith('-en'));
const italiane = collezioni.filter((c) => !c.name.endsWith('-en'));
controlla('tante collezioni inglesi quante italiane', inglesi.length === italiane.length,
  `${italiane.length} / ${inglesi.length}`);

const nonInEn = inglesi.filter((c) => {
  const percorsi = c.folder ? [c.folder] : (c.files ?? []).map((f) => path.dirname(f.file));
  return !percorsi.every((p) => p.includes('/en'));
});
controlla('le collezioni inglesi leggono da cartelle en/', nonInEn.length === 0,
  nonInEn.map((c) => c.name).join(', '));

// Le collezioni inglesi non devono duplicare le fotografie: sono condivise.
const conFoto = inglesi.filter((c) => (c.files ?? []).some((f) => f.name === 'foto'));
controlla('le collezioni inglesi non duplicano le fotografie', conFoto.length === 0,
  conFoto.map((c) => c.name).join(', '));

// Ogni file dichiarato deve esistere.
const mancanti = [];
for (const collezione of collezioni) {
  for (const voce of collezione.files ?? []) {
    if (!existsSync(voce.file)) mancanti.push(voce.file);
  }
  if (collezione.folder && !existsSync(collezione.folder)) mancanti.push(collezione.folder);
}
controlla('tutti i percorsi dichiarati esistono', mancanti.length === 0, mancanti.join(', '));

// L'etichetta deve dire che è inglese, altrimenti nel pannello sono due voci
// identiche e si sceglie a caso.
const senzaEnglish = inglesi.filter(
  (c) => !c.label.includes('English') && !c.label.startsWith('EN · '),
);
controlla('le collezioni inglesi si riconoscono dall\'etichetta', senzaEnglish.length === 0,
  senzaEnglish.map((c) => c.label).join(', '));

console.log('');
console.log(problemi ? `PROBLEMI: ${problemi}` : 'il pannello è a posto');
process.exit(problemi ? 1 : 0);
