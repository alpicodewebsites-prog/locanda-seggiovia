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
 */
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

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
  }),
});

/* -------------------------------------------------------------------------- */
/* Sentieri — schema pronto; i contenuti arrivano nella settimana 3             */
/* -------------------------------------------------------------------------- */

const sentieri = defineCollection({
  // Pattern passato come stringa singola con negazione: il loader unisce gli
  // array in una sola stringa, quindi la forma ad array non funziona.
  // README.md è documentazione per chi sviluppa, non un contenuto del sito.
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
    /** Immagine di copertina, percorso relativo alla root (es. /images/...). */
    immagine: z.string().optional(),
  }),
});

export const collections = { camere, menu, gnocchi, sentieri };
