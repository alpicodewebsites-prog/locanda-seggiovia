/**
 * Content collections — schema dei contenuti gestiti dal CMS.
 *
 * In Astro 7 le collezioni si definiscono qui e i file si caricano con il loader
 * `glob()`. Ogni campo dichiarato qui corrisponde a un campo modificabile in
 * /admin.
 *
 * ----------------------------------------------------------------------------
 * PERCHÉ I CAMPI DELLE PAGINE SONO (QUASI) TUTTI OPZIONALI
 *
 * Ogni pagina ha DUE file: `testi.md` e `foto.md`. Il loader `glob()` applica
 * però UN SOLO schema a tutti i file della cartella, quindi `testi.md` viene
 * validato contro lo stesso schema di `foto.md`.
 *
 * Se `titolo` fosse obbligatorio, `foto.md` — che non lo contiene — farebbe
 * fallire la compilazione. Da qui la scelta: nella collezione di una pagina i
 * campi sono opzionali, e i valori di riserva stanno in `src/lib/pagine.ts`, che
 * li applica SOLO se il file manca davvero.
 *
 * Le collezioni a elenco (camere, menu, sentieri) hanno invece i campi
 * obbligatori: lì ogni file è una scheda completa.
 * ----------------------------------------------------------------------------
 *
 * ATTENZIONE: i campi opzionali sono davvero opzionali. Se un'informazione non
 * esiste, va lasciata vuota: non va inventata. Il CMS è configurato con
 * `omit_empty_optional_fields`, quindi un campo vuoto non viene scritto nel file
 * e il sito semplicemente non lo mostra.
 */
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

/** Campo immagine riutilizzabile: percorso dentro src/assets. */
const immagine = z.string().optional();

/* -------------------------------------------------------------------------- */
/* Pagine singole — testi e fotografie in due file separati                    */
/*                                                                             */
/* La divisione non è un capriccio: Sveltia chiama le cartelle della libreria  */
/* «Collezione › etichetta della voce». Con una voce sola, nella libreria —    */
/* dove si gestiscono SOLO fotografie — si leggeva «Testi, paragrafi e foto».  */
/* -------------------------------------------------------------------------- */

/** Home page. */
const home = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/home' }),
  schema: z.object({
    // --- Testi (in testi.md) ---------------------------------------------
    titolo: z.string().optional(),
    sottotitolo: z.string().optional(),
    /** Descrizione per i motori di ricerca: non si vede in pagina. */
    descrizione: z.string().optional(),
    accessi: z
      .array(
        z.object({
          etichetta: z.string(),
          titolo: z.string(),
          nota: z.string(),
          collegamento: z.string(),
        }),
      )
      .optional(),
    invitoSentieri: z.string().optional(),
    pulsanteGnocchi: z.string().optional(),
    locandaEtichetta: z.string().optional(),
    locandaTitolo: z.string().optional(),
    locandaParagrafi: z.array(z.string()).optional(),
    locandaCollegamento: z.string().optional(),
    territorioEtichetta: z.string().optional(),
    territorioTitolo: z.string().optional(),
    territorioTesto: z.string().optional(),
    // --- Fotografie (in foto.md) -----------------------------------------
    hero: immagine,
    panorama: immagine,
    montagne: immagine,
    facciata: immagine,
  }),
});

/** Pagina La Locanda. */
const paginaLocanda = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/la-locanda' }),
  schema: z.object({
    titolo: z.string().optional(),
    sottotitolo: z.string().optional(),
    facciata: immagine,
    cucina: immagine,
  }),
});

/** Pagina Sentieri (l'elenco). */
const paginaSentieri = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/sentieri-pagina' }),
  schema: z.object({
    titolo: z.string().optional(),
    sottotitolo: z.string().optional(),
    montagne: immagine,
    panorama: immagine,
  }),
});

/** Gnocchi con la Fioreta. */
const gnocchi = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/gnocchi' }),
  schema: z.object({
    // --- Testi (in testi.md) ---------------------------------------------
    titolo: z.string().optional(),
    sottotitolo: z.string().optional(),
    storia: z.string().optional(),
    /** Composizione del piatto secondo la ricetta De.Co. */
    ricetta: z
      .array(z.object({ ingrediente: z.string(), quantita: z.string() }))
      .optional(),
    lavorazione: z
      .array(z.object({ titolo: z.string(), testo: z.string() }))
      .optional(),
    condimento: z.string().optional(),
    riconoscimenti: z.array(z.string()).optional(),
    // --- Fotografie (in foto.md) -----------------------------------------
    foto: immagine,
    fotoPreparazione: immagine,
    /**
     * Le fotografie dei singoli ingredienti, per la fascia «tavolo» della home.
     *
     * Si accoppiano alla ricetta PER POSIZIONE: la prima foto è il primo
     * ingrediente della ricetta. Se ne mancano, quelle senza foto mostrano
     * solo il nome.
     */
    fotoIngredienti: z.array(z.string()).optional(),
  }),
});

/* -------------------------------------------------------------------------- */
/* Collezioni a elenco — una scheda per file                                   */
/* -------------------------------------------------------------------------- */

const camere = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/camere' }),
  schema: z.object({
    titolo: z.string(),
    /** Ordine di comparsa nella pagina Camere. */
    ordine: z.number().default(0),
    descrizione: z.string(),
    occupanti: z.string().optional(),
    /** Tariffe per persona, per giorno. */
    tariffe: z.object({
      bnb: z.number(),
      mezzaPensione: z.number(),
      pensioneCompleta: z.number(),
    }),
    supplementoDus: z.number().optional(),
    /** Dotazione della camera. */
    servizi: z.array(z.string()).default([]),
    /** Fotografia della camera. */
    foto: immagine,
  }),
});

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

export const collections = {
  camere,
  menu,
  sentieri,
  home,
  paginaLocanda,
  paginaSentieri,
  gnocchi,
};
