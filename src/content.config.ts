/**
 * Content collections — schema dei contenuti gestiti dal CMS.
 *
 * In Astro 7 le collezioni si definiscono qui (non più in src/content/config.ts)
 * e i file si caricano con il loader `glob()`. Ogni campo dichiarato qui
 * corrisponde a un campo modificabile in /admin.
 *
 * ATTENZIONE: i campi opzionali sono davvero opzionali. Se un'informazione non
 * esiste, va lasciata vuota: non va inventata. Il CMS è configurato con
 * `omit_empty_optional_fields`, quindi un campo vuoto non viene scritto nel file
 * e il sito semplicemente non lo mostra.
 *
 * SULLE IMMAGINI: le fotografie stanno tutte in `src/assets` e i campi immagine
 * contengono il percorso che il pannello salva, del tipo
 * `/assets/nome-file.jpg`. La risoluzione avviene con `src/lib/immagini.ts`,
 * che accetta anche il vecchio formato a sigla (`sentieri-mole`).
 */
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

/** Campo immagine riutilizzabile: percorso in src/assets. */
const immagine = z.string().optional();

/* -------------------------------------------------------------------------- */
/* Camere e tariffe                                                            */
/* -------------------------------------------------------------------------- */

const camere = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/camere' }),
  schema: z.object({
    titolo: z.string(),
    /** Ordine di comparsa nella pagina Camere. */
    ordine: z.number().default(0),
    descrizione: z.string(),
    occupanti: z.string().optional(),
    /** Tariffe per persona, per giorno. `null` = servizio non previsto. */
    tariffe: z.object({
      bnb: z.number(),
      mezzaPensione: z.number(),
      pensioneCompleta: z.number(),
    }),
    /** Supplemento doppia uso singola, per giorno. */
    supplementoDus: z.number().optional(),
    /** Dotazione della camera. */
    servizi: z.array(z.string()).default([]),
    /** Fotografia della camera. */
    foto: immagine,
  }),
});

/* -------------------------------------------------------------------------- */
/* Menù del ristorante                                                         */
/* -------------------------------------------------------------------------- */

const menu = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/menu' }),
  schema: z.object({
    nome: z.string(),
    categoria: z.enum(['antipasti', 'primi', 'secondi', 'dolci']),
    ordine: z.number().default(0),
    descrizione: z.string(),
    /** Prezzo in euro. Va lasciato vuoto se non ancora definito. */
    prezzo: z.number().optional(),
    /** Piatto della casa o specialità: viene messo in evidenza. */
    specialita: z.boolean().default(false),
    /** Fotografia del piatto. Se c'è, il piatto compare anche in galleria. */
    foto: immagine,
  }),
});

/* -------------------------------------------------------------------------- */
/* Gnocchi con la Fioreta — contenuto singolo                                  */
/* -------------------------------------------------------------------------- */

const gnocchi = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/gnocchi' }),
  schema: z.object({
    titolo: z.string(),
    sottotitolo: z.string().optional(),
    storia: z.string(),
    /** Composizione del piatto secondo la ricetta De.Co. */
    ricetta: z.array(
      z.object({
        ingrediente: z.string(),
        quantita: z.string(),
      }),
    ),
    lavorazione: z.array(
      z.object({
        titolo: z.string(),
        testo: z.string(),
      }),
    ),
    condimento: z.string(),
    /** Riconoscimenti: al momento la De.Co. di Recoaro Terme. */
    riconoscimenti: z.array(z.string()).default([]),
    /** Fotografia del piatto finito. */
    foto: immagine,
    /** Fotografia degli ingredienti o della preparazione. */
    fotoPreparazione: immagine,
  }),
});

/* -------------------------------------------------------------------------- */
/* Sentieri                                                                    */
/* -------------------------------------------------------------------------- */

const sentieri = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/sentieri' }),
  schema: z.object({
    nome: z.string(),
    ordine: z.number().default(0),
    /** Breve sommario per gli elenchi. */
    sommario: z.string(),
    /** Descrizione estesa del percorso. */
    descrizione: z.string(),
    /** Difficoltà secondo la scala del CAI. */
    difficolta: z.enum(['T', 'E', 'EE']),
    /** Dati tecnici: si compilano solo quelli noti. */
    distanza: z.string().optional(),
    dislivello: z.string().optional(),
    durata: z.string().optional(),
    /** Segnaletica CAI, se presente. */
    segnavia: z.string().optional(),
    partenza: z.string().optional(),
    /** Immagine di copertina. */
    immagine,
  }),
});

/* -------------------------------------------------------------------------- */
/* Home page — contenuto singolo                                               */
/*                                                                             */
/* Testi E fotografie della prima pagina. Prima i testi erano scritti nel      */
/* codice e si potevano cambiare solo lì; ora sono qui e si cambiano dal       */
/* pannello.                                                                   */
/* -------------------------------------------------------------------------- */

const home = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/home' }),
  schema: z.object({
    // --- Testi -----------------------------------------------------------
    titolo: z.string(),
    sottotitolo: z.string(),
    /** Descrizione per i motori di ricerca: non si vede in pagina. */
    descrizione: z.string(),
    /** I due accessi dell'apertura: Dormire e Mangiare. */
    accessi: z
      .array(
        z.object({
          etichetta: z.string(),
          titolo: z.string(),
          nota: z.string(),
          collegamento: z.string(),
        }),
      )
      .default([]),
    invitoSentieri: z.string(),
    pulsanteGnocchi: z.string(),
    locandaEtichetta: z.string(),
    locandaTitolo: z.string(),
    locandaParagrafi: z.array(z.string()).default([]),
    locandaCollegamento: z.string(),
    territorioEtichetta: z.string(),
    territorioTitolo: z.string(),
    territorioTesto: z.string(),
    // --- Fotografie ------------------------------------------------------
    hero: immagine,
    panorama: immagine,
    montagne: immagine,
    facciata: immagine,
  }),
});

/* -------------------------------------------------------------------------- */
/* Pagina La Locanda — contenuto singolo                                       */
/* -------------------------------------------------------------------------- */

const paginaLocanda = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/la-locanda' }),
  schema: z.object({
    titolo: z.string(),
    sottotitolo: z.string(),
    facciata: immagine,
    cucina: immagine,
  }),
});

/* -------------------------------------------------------------------------- */
/* Pagina Sentieri — contenuto singolo                                         */
/* -------------------------------------------------------------------------- */

const paginaSentieri = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/sentieri-pagina' }),
  schema: z.object({
    titolo: z.string(),
    sottotitolo: z.string(),
    montagne: immagine,
    panorama: immagine,
  }),
});

export const collections = {
  camere,
  menu,
  gnocchi,
  sentieri,
  home,
  paginaLocanda,
  paginaSentieri,
};
