/**
 * Caricamento dei contenuti delle pagine singole.
 *
 * Ogni pagina ha DUE file, e quindi due voci nel pannello:
 *
 *     src/content/home/testi.md          -> «Testi e paragrafi»
 *     src/content/home/foto.md           -> «Fotografie»
 *
 * La divisione serve alla libreria immagini: Sveltia chiama le cartelle
 * «Collezione › etichetta della voce», e in una libreria di sole fotografie non
 * deve comparire la parola «testi».
 *
 * Questo modulo legge le due voci e prepara:
 *   - i TESTI, pronti da stampare, con un valore di riserva se il file manca;
 *   - le FOTOGRAFIE, risolte in immagini per il componente `Image` di Astro.
 *
 * Se un campo immagine è vuoto, o il file indicato non esiste, il valore è
 * `null` e la pagina semplicemente non mostra quella fotografia: non compare un
 * riquadro rotto. È il comportamento voluto quando si svuota un campo.
 */
import { getEntry } from 'astro:content';
import type { Lingua } from '../i18n';
import { idTradotto } from './contenuti';
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
 * Valori di riserva, usati SOLO se il file dei testi manca o è incompleto.
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

export async function caricaHome(lingua: Lingua = 'it'): Promise<ContenutoHome> {
  // Si cerca la versione tradotta; se manca, si ripiega sull'italiano.
  const testi =
    (await getEntry('home', idTradotto('testi', lingua))) ??
    (await getEntry('home', 'testi'));
  const foto = await getEntry('home', 'foto');

  const d = testi?.data;

  return {
    testi: d
      ? {
          titolo: d.titolo ?? TESTI_HOME_RISERVA.titolo,
          sottotitolo: d.sottotitolo ?? TESTI_HOME_RISERVA.sottotitolo,
          descrizione: d.descrizione ?? TESTI_HOME_RISERVA.descrizione,
          accessi: d.accessi ?? [],
          invitoSentieri: d.invitoSentieri ?? TESTI_HOME_RISERVA.invitoSentieri,
          pulsanteGnocchi: d.pulsanteGnocchi ?? TESTI_HOME_RISERVA.pulsanteGnocchi,
          locandaEtichetta: d.locandaEtichetta ?? TESTI_HOME_RISERVA.locandaEtichetta,
          locandaTitolo: d.locandaTitolo ?? TESTI_HOME_RISERVA.locandaTitolo,
          locandaParagrafi: d.locandaParagrafi ?? [],
          locandaCollegamento: d.locandaCollegamento ?? TESTI_HOME_RISERVA.locandaCollegamento,
          territorioEtichetta: d.territorioEtichetta ?? TESTI_HOME_RISERVA.territorioEtichetta,
          territorioTitolo: d.territorioTitolo ?? TESTI_HOME_RISERVA.territorioTitolo,
          territorioTesto: d.territorioTesto ?? TESTI_HOME_RISERVA.territorioTesto,
        }
      : TESTI_HOME_RISERVA,
    foto: {
      hero: risolviImmagine(foto?.data.hero),
      panorama: risolviImmagine(foto?.data.panorama),
      montagne: risolviImmagine(foto?.data.montagne),
      facciata: risolviImmagine(foto?.data.facciata),
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

export async function caricaLocanda(lingua: Lingua = 'it'): Promise<ContenutoLocanda> {
  // Si cerca la versione tradotta; se manca, si ripiega sull'italiano.
  const testi =
    (await getEntry('paginaLocanda', idTradotto('testi', lingua))) ??
    (await getEntry('paginaLocanda', 'testi'));
  const foto = await getEntry('paginaLocanda', 'foto');

  return {
    testi: {
      titolo: testi?.data.titolo ?? 'La locanda e la famiglia',
      sottotitolo: testi?.data.sottotitolo ?? '',
    },
    foto: {
      facciata: risolviImmagine(foto?.data.facciata),
      cucina: risolviImmagine(foto?.data.cucina),
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

export async function caricaSentieri(lingua: Lingua = 'it'): Promise<ContenutoSentieri> {
  // Si cerca la versione tradotta; se manca, si ripiega sull'italiano.
  const testi =
    (await getEntry('paginaSentieri', idTradotto('testi', lingua))) ??
    (await getEntry('paginaSentieri', 'testi'));
  const foto = await getEntry('paginaSentieri', 'foto');

  return {
    testi: {
      titolo: testi?.data.titolo ?? 'I sentieri delle Piccole Dolomiti',
      sottotitolo: testi?.data.sottotitolo ?? '',
    },
    foto: {
      montagne: risolviImmagine(foto?.data.montagne),
      panorama: risolviImmagine(foto?.data.panorama),
    },
  };
}

/* -------------------------------------------------------------------------- */
/* Gnocchi con la Fioreta                                                      */
/* -------------------------------------------------------------------------- */

export interface ContenutoGnocchi {
  testi: {
    titolo: string;
    sottotitolo?: string;
    storia: string;
    ricetta: { ingrediente: string; quantita: string }[];
    lavorazione: { titolo: string; testo: string }[];
    condimento: string;
    riconoscimenti: string[];
  };
  foto: { piatto: ImageMetadata | null; preparazione: ImageMetadata | null };
}

export async function caricaGnocchi(lingua: Lingua = 'it'): Promise<ContenutoGnocchi> {
  // Si cerca la versione tradotta; se manca, si ripiega sull'italiano.
  const testi =
    (await getEntry('gnocchi', idTradotto('testi', lingua))) ??
    (await getEntry('gnocchi', 'testi'));
  const foto = await getEntry('gnocchi', 'foto');

  return {
    testi: {
      titolo: testi?.data.titolo ?? 'Gnocchi con la Fioreta',
      sottotitolo: testi?.data.sottotitolo,
      storia: testi?.data.storia ?? '',
      ricetta: testi?.data.ricetta ?? [],
      lavorazione: testi?.data.lavorazione ?? [],
      condimento: testi?.data.condimento ?? '',
      riconoscimenti: testi?.data.riconoscimenti ?? [],
    },
    foto: {
      piatto: risolviImmagine(foto?.data.foto),
      preparazione: risolviImmagine(foto?.data.fotoPreparazione),
    },
  };
}
