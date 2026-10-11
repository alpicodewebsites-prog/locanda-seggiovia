/**
 * Risoluzione delle immagini referenziate nei contenuti.
 *
 * Le fotografie stanno tutte in `src/assets`, così Astro le ottimizza (WebP e
 * versioni ridimensionate). Il pannello di gestione scrive in quella stessa
 * cartella e salva nei file di contenuto un valore del tipo
 * `/assets/nome-file.jpg`.
 *
 * Questo modulo fa da ponte: prende quel valore — o una semplice sigla come
 * `sentieri-mole`, che è il formato usato prima — e restituisce l'immagine
 * pronta per il componente `Image` di Astro.
 *
 * Accettare entrambi i formati è voluto: i contenuti già scritti continuano a
 * funzionare anche se il pannello salva in modo diverso.
 */
import type { ImageMetadata } from 'astro';

/** Tutte le immagini di src/assets, indicizzate per nome file. */
const immagini = import.meta.glob<ImageMetadata>('../assets/*.{jpg,jpeg,png,webp,avif}', {
  eager: true,
  import: 'default',
});

const perNome = new Map<string, ImageMetadata>();
for (const [percorso, immagine] of Object.entries(immagini)) {
  const nome = percorso.split('/').pop();
  if (nome) perNome.set(nome, immagine);
}

/** Estensioni provate quando il valore non ne indica una. */
const ESTENSIONI = ['jpg', 'jpeg', 'png', 'webp', 'avif'];

/**
 * Restituisce l'immagine corrispondente al valore, oppure `null` se non esiste.
 *
 * @param valore Sigla (`sentieri-mole`) o percorso salvato dal pannello
 *   (`/assets/sentieri-mole.jpg`). Può essere vuoto.
 */
export function risolviImmagine(valore?: string | null): ImageMetadata | null {
  if (!valore) return null;

  const nome = valore.split('/').pop()?.trim();
  if (!nome) return null;

  // Caso normale: il valore contiene già il nome del file con estensione.
  const diretto = perNome.get(nome);
  if (diretto) return diretto;

  // Fallback: valore senza estensione, si prova con quelle note.
  const base = nome.replace(/\.[a-z0-9]+$/i, '');
  for (const estensione of ESTENSIONI) {
    const trovata = perNome.get(`${base}.${estensione}`);
    if (trovata) return trovata;
  }

  return null;
}

/** Elenco dei nomi file disponibili: utile per diagnostica e controlli. */
export function nomiImmaginiDisponibili(): string[] {
  return [...perNome.keys()].sort();
}
