/**
 * Caricamento delle fotografie generali del sito.
 *
 * Le fotografie che non appartengono a una scheda — apertura della home,
 * facciata, panorama — stanno in `src/content/impostazioni/sito.md`, così la
 * proprietaria le trova tutte in un posto solo nel pannello.
 *
 * Questo modulo le legge e le risolve in immagini pronte per il componente
 * `Image` di Astro. Se un campo è vuoto o l'immagine non esiste, il valore è
 * `null` e le pagine semplicemente non mostrano quella fotografia: non serve
 * un segnaposto.
 */
import { getCollection } from 'astro:content';
import type { ImageMetadata } from 'astro';

import { risolviImmagine } from './immagini';

export interface FotoSito {
  hero: ImageMetadata | null;
  locandaEsterno: ImageMetadata | null;
  locandaCucina: ImageMetadata | null;
  panorama: ImageMetadata | null;
  montagne: ImageMetadata | null;
}

/** Legge le fotografie generali. Restituisce `null` per quelle mancanti. */
export async function caricaFotoSito(): Promise<FotoSito> {
  const voci = await getCollection('impostazioni');
  const dati = voci[0]?.data;

  return {
    hero: risolviImmagine(dati?.hero),
    locandaEsterno: risolviImmagine(dati?.locandaEsterno),
    locandaCucina: risolviImmagine(dati?.locandaCucina),
    panorama: risolviImmagine(dati?.panorama),
    montagne: risolviImmagine(dati?.montagne),
  };
}
