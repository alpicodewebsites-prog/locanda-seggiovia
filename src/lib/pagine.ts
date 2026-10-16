/**
 * Caricamento dei contenuti delle pagine singole.
 *
 * Ogni pagina che ha testi o fotografie proprie ha la sua collezione, e quindi
 * la sua voce nel pannello:
 *
 *     src/content/home/pagina.md          -> «Home Page»
 *     src/content/la-locanda/pagina.md    -> «Pagina La Locanda»
 *
 * Questo modulo le legge e prepara due cose distinte:
 *   - i TESTI, pronti da stampare;
 *   - le FOTOGRAFIE, risolte in immagini per il componente `Image` di Astro.
 *
 * Se un campo immagine è vuoto, o il file indicato non esiste, il valore è
 * `null` e la pagina semplicemente non mostra quella fotografia: non compare un
 * riquadro rotto. È il comportamento voluto quando la proprietaria svuota un
 * campo dal pannello.
 */
import { getCollection } from 'astro:content';
import type { ImageMetadata } from 'astro';

import { risolviImmagine } from './immagini';

/* -------------------------------------------------------------------------- */
/* Home                                                                        */
/* -------------------------------------------------------------------------- */

export interface TestiHome {
  titolo: string;
  sottotitolo: string;
  descrizione: string;
  accessi: { etichetta: string; titolo: string; nota: string; collegamento: string }[];
  invitoSentieri: string;
  pulsanteGnocchi: string;
  locandaEtichetta: string;
  locandaTitolo: string;
  locandaParagrafi: string[];
  locandaCollegamento: string;
  territorioEtichetta: string;
  territorioTitolo: string;
  territorioTesto: string;
}

export interface FotoHome {
  hero: ImageMetadata | null;
  panorama: ImageMetadata | null;
  montagne: ImageMetadata | null;
  facciata: ImageMetadata | null;
}

/**
 * Valori di riserva, usati SOLO se il file di contenuto manca del tutto.
 *
 * Servono a una cosa sola: che una svista nel pannello non lasci la home senza
 * titolo. Se il file c'è, questi valori non si vedono mai.
 */
const TESTI_HOME_RISERVA: TestiHome = {
  titolo: 'Rifugio alpino ai piedi delle Piccole Dolomiti',
  sottotitolo:
    'Camere, cucina tradizionale alto-vicentina e i sentieri che partono dal centro di Recoaro Terme.',
  descrizione:
    'Camere e ristorante nel centro di Recoaro Terme, ai piedi delle Piccole Dolomiti e del Pasubio.',
  accessi: [],
  invitoSentieri: 'Scopri i sentieri',
  pulsanteGnocchi: 'Scopri la nostra produzione di gnocchi con la Fioreta',
  locandaEtichetta: 'La locanda',
  locandaTitolo: 'Un rifugio, non un albergo',
  locandaParagrafi: [],
  locandaCollegamento: 'La locanda e la famiglia',
  territorioEtichetta: 'Territorio',
  territorioTitolo: 'I sentieri cominciano dal centro del paese',
  territorioTesto: '',
};

export interface ContenutoHome {
  testi: TestiHome;
  foto: FotoHome;
}

export async function caricaHome(): Promise<ContenutoHome> {
  const voci = await getCollection('home');
  const dati = voci[0]?.data;

  const testi: TestiHome = dati
    ? {
        titolo: dati.titolo,
        sottotitolo: dati.sottotitolo,
        descrizione: dati.descrizione,
        accessi: dati.accessi ?? [],
        invitoSentieri: dati.invitoSentieri,
        pulsanteGnocchi: dati.pulsanteGnocchi,
        locandaEtichetta: dati.locandaEtichetta,
        locandaTitolo: dati.locandaTitolo,
        locandaParagrafi: dati.locandaParagrafi ?? [],
        locandaCollegamento: dati.locandaCollegamento,
        territorioEtichetta: dati.territorioEtichetta,
        territorioTitolo: dati.territorioTitolo,
        territorioTesto: dati.territorioTesto,
      }
    : TESTI_HOME_RISERVA;

  return {
    testi,
    foto: {
      hero: risolviImmagine(dati?.hero),
      panorama: risolviImmagine(dati?.panorama),
      montagne: risolviImmagine(dati?.montagne),
      facciata: risolviImmagine(dati?.facciata),
    },
  };
}

/* -------------------------------------------------------------------------- */
/* La Locanda                                                                  */
/* -------------------------------------------------------------------------- */

export interface ContenutoLocanda {
  testi: { titolo: string; sottotitolo: string };
  foto: { facciata: ImageMetadata | null; cucina: ImageMetadata | null };
}

export async function caricaLocanda(): Promise<ContenutoLocanda> {
  const voci = await getCollection('paginaLocanda');
  const dati = voci[0]?.data;

  return {
    testi: {
      titolo: dati?.titolo ?? 'La locanda e la famiglia',
      sottotitolo: dati?.sottotitolo ?? '',
    },
    foto: {
      facciata: risolviImmagine(dati?.facciata),
      cucina: risolviImmagine(dati?.cucina),
    },
  };
}

/* -------------------------------------------------------------------------- */
/* Pagina Sentieri                                                             */
/* -------------------------------------------------------------------------- */

export interface ContenutoSentieri {
  testi: { titolo: string; sottotitolo: string };
  foto: { montagne: ImageMetadata | null; panorama: ImageMetadata | null };
}

export async function caricaSentieri(): Promise<ContenutoSentieri> {
  const voci = await getCollection('paginaSentieri');
  const dati = voci[0]?.data;

  return {
    testi: {
      titolo: dati?.titolo ?? 'I sentieri delle Piccole Dolomiti',
      sottotitolo: dati?.sottotitolo ?? '',
    },
    foto: {
      montagne: risolviImmagine(dati?.montagne),
      panorama: risolviImmagine(dati?.panorama),
    },
  };
}
