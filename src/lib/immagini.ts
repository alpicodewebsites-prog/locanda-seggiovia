/**
 * Risoluzione delle immagini referenziate nei contenuti.
 *
 * Le fotografie stanno in `src/assets`, divise per sezione del sito:
 *
 *     src/assets/home/            apertura, panorama, montagne, facciata
 *     src/assets/la-locanda/      facciata, tavolo di cucina
 *     src/assets/camere/          fotografie delle camere
 *     src/assets/ristorante/      piatti, in piatti/
 *     src/assets/sentieri/        copertine dei sentieri
 *     src/assets/gnocchi/         piatto finito, preparazione
 *
 * Astro ottimizza le immagini da lì (WebP e versioni ridimensionate), quindi il
 * sito resta leggero. Il pannello di gestione scrive in quelle cartelle e salva
 * nei file di contenuto un valore del tipo `/assets/sentieri/gino-solda.jpg`.
 *
 * IL GLOB DEVE ESSERE RICORSIVO (`**`): con `*` le immagini nelle sottocartelle
 * non verrebbero nemmeno viste, e ogni pagina resterebbe senza fotografia.
 *
 * La ricerca accetta due forme, e questo è voluto:
 *   - il percorso completo (`/assets/sentieri/gino-solda.jpg`), che è quello
 *     che scrive il pannello;
 *   - il solo nome del file (`gino-solda.jpg`), che è quello che scrivevano i
 *     contenuti preparati prima della riorganizzazione.
 * Accettarle entrambe significa che i contenuti già scritti continuano a
 * funzionare comunque.
 */
import type { ImageMetadata } from 'astro';

/** Tutte le immagini di src/assets, sottocartelle comprese. */
const immagini = import.meta.glob<ImageMetadata>('../assets/**/*.{jpg,jpeg,png,webp,avif}', {
  eager: true,
  import: 'default',
});

/** Indice doppio: per percorso e per nome file. */
const perPercorso = new Map<string, ImageMetadata>();
const perNome = new Map<string, ImageMetadata>();

for (const [chiave, immagine] of Object.entries(immagini)) {
  // La chiave è del tipo `../assets/sentieri/gino-solda.jpg`.
  const percorso = chiave.replace(/^\.\.\/assets\//, '').replace(/^\.\//, '');
  perPercorso.set(percorso, immagine);

  const nome = percorso.split('/').pop();
  // In caso di omonimia vince il primo trovato: il percorso resta comunque la
  // via precisa per distinguerli.
  if (nome && !perNome.has(nome)) perNome.set(nome, immagine);
}

/** Estensioni provate quando il valore non ne indica una. */
const ESTENSIONI = ['jpg', 'jpeg', 'png', 'webp', 'avif'];

/**
 * Restituisce l'immagine corrispondente al valore, oppure `null` se non esiste.
 *
 * @param valore Percorso (`/assets/sentieri/gino-solda.jpg`) o solo nome file
 *   (`gino-solda.jpg`). Può essere vuoto: in quel caso restituisce `null` e la
 *   pagina semplicemente non mostra quella fotografia.
 */
export function risolviImmagine(valore?: string | null): ImageMetadata | null {
  if (!valore) return null;

  // Un campo svuotato nel pannello può arrivare come stringa vuota o con soli
  // spazi: non è un'immagine, e non deve far comparire un riquadro rotto.
  const pulito = String(valore).trim();
  if (!pulito) return null;

  const relativo = pulito.replace(/^\/?assets\//, '').replace(/^\//, '');

  // 1. Percorso esatto.
  const perPercorsoEsatto = perPercorso.get(relativo);
  if (perPercorsoEsatto) return perPercorsoEsatto;

  // 2. Solo nome file.
  const nome = relativo.split('/').pop();
  if (nome) {
    const perNomeEsatto = perNome.get(nome);
    if (perNomeEsatto) return perNomeEsatto;
  }

  // 3. Valore senza estensione: si prova con quelle note, prima nel percorso
  //    indicato e poi fra i nomi.
  const base = relativo.replace(/\.[a-z0-9]+$/i, '');
  const cartella = base.includes('/') ? base.slice(0, base.lastIndexOf('/') + 1) : '';
  const soloBase = base.split('/').pop() ?? base;

  for (const estensione of ESTENSIONI) {
    const tentativo = perPercorso.get(`${cartella}${soloBase}.${estensione}`);
    if (tentativo) return tentativo;
  }
  for (const estensione of ESTENSIONI) {
    const tentativo = perNome.get(`${soloBase}.${estensione}`);
    if (tentativo) return tentativo;
  }

  return null;
}

/** Elenco dei percorsi disponibili: utile per diagnostica e controlli. */
export function nomiImmaginiDisponibili(): string[] {
  return [...perPercorso.keys()].sort();
}

/** Elenco raggruppato per sezione: serve ai controlli automatici. */
export function immaginiPerSezione(): Record<string, string[]> {
  const sezioni: Record<string, string[]> = {};
  for (const percorso of perPercorso.keys()) {
    const parti = percorso.split('/');
    const sezione = parti.length > 1 ? parti[0] : '(radice)';
    (sezioni[sezione] ??= []).push(percorso);
  }
  for (const elenco of Object.values(sezioni)) elenco.sort();
  return sezioni;
}
