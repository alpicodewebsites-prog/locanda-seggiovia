/**
 * Dati della struttura — unica fonte di verità.
 *
 * ⚠️  CAMPI DA CONFERMARE CON LA CLIENTE (contrassegnati con `TODO`):
 *     telefono, anno di fondazione, P.IVA/C.F., orari, link Instagram.
 *     Sono valori segnaposto: il sito NON va pubblicato prima di averli verificati.
 */

/**
 * Dominio pubblico del sito — unica fonte di verità.
 *
 * Serve a canonical, Open Graph, sitemap e al redirect del modulo contatti.
 * Si può sovrascrivere senza toccare il codice con la variabile SITE_URL.
 *
 * Nota: questo valore NON va importato da astro.config.mjs dentro una pagina.
 * Farlo crea una dipendenza circolare con il chunk di configurazione di Astro e
 * rompe la compilazione. astro.config.mjs importa da qui, non viceversa.
 */
export const SITE_URL = (process.env.SITE_URL ?? 'https://www.locandaseggiovia.com').replace(
  /\/+$/,
  '',
);

export const site = {
  nome: 'Locanda Seggiovia',
  nomeLegale: 'Locanda Seggiovia',
  tagline: 'Rifugio alpino a Recoaro Terme',

  // TODO: sostituire con il dominio definitivo (usato da canonical, OG, sitemap).
  url: SITE_URL,

  // TODO: confermare l'anno di fondazione. Nel frattempo l'anno è omesso
  // dalla frase di apertura invece di inventarlo.
  annoFondazione: null as number | null,

  gestione: 'Famiglia Asnicar Bertoldi',
  gestori: 'Loris Asnicar e famiglia',

  indirizzo: {
    via: 'Piazza A. Savoia Duca Aosta 7',
    cap: '36076',
    citta: 'Recoaro Terme',
    provincia: 'VI',
    regione: 'Veneto',
    paese: 'IT',
  },

  // Recapiti reali. Il numero è quello storico dell'attività, pubblicato sul
  // sito precedente: 0445 76162 (fisso, unico per tavoli e informazioni).
  telefono: '0445 76162',
  telefonoLink: 'tel:+39044576162',

  email: 'locandaseggiovia@gmail.com',

  /** Apertura continuativa: dal sito precedente, «Siamo aperti tutto l'anno». */
  apertoTuttoLAnno: true,

  // TODO: confermare che l'account esista e inserire l'URL definitivo.
  instagram: null as string | null,

  geo: {
    // Coordinate del centro di Recoaro Terme: da raffinare sul civico esatto.
    lat: 45.6899,
    lng: 11.2356,
  },

  // TODO: confermare gli orari reali di ristorante e reception.
  orari: [
    { giorno: 'Ristorante', valore: 'A pranzo e a cena — orari da confermare' },
    { giorno: 'Reception', valore: 'Tutti i giorni (da confermare)' },
  ],

  // Dal listino del sito precedente:
  //   «In B&B è compresa la prima colazione»
  //   «A disposizione con richiesta: linea wi-fi negli spazi comuni dell'hotel»
  // Il Wi-Fi era quindi negli spazi comuni, non in camera: la pagina Camere
  // non deve prometterlo in camera.
  colazioneInclusaBnb: true,
  wifiSpaziComuni: true,

  // --- Politiche di soggiorno (fornite dalla cliente) ----------------------
  // Stanno qui, e non nei file del CMS, perché valgono per tutte le camere:
  // duplicarle camera per camera vorrebbe dire poterle far divergere.
  soggiornoMinimo: 3,
  /** Supplemento doppia uso singola, in euro al giorno. */
  supplementoDus: 10,
  animali: {
    /** Supplemento giornaliero, in euro. */
    supplementoGiorno: 20,
    /** Pulizie finali, una tantum, in euro. */
    pulizieFinali: 50,
  },

  // TODO: dati fiscali obbligatori per la pubblicazione.
  // La ragione sociale è quella pubblicata sul sito precedente; partita IVA e
  // codice fiscale restano da confermare (erano pubblicati solo nell'elenco dei
  // contributi regionali, non come dati societari).
  fiscale: {
    ragioneSociale: 'Ristorante Asnicar Bertoldi SNC',
    partitaIva: '00000000000',
    codiceFiscale: '0000000000000000',
    rea: null as string | null,
  },
} as const;

/** Indirizzo su una riga, per il footer e i dati strutturati. */
export const indirizzoBreve = `${site.indirizzo.via}, ${site.indirizzo.cap} ${site.indirizzo.citta} (${site.indirizzo.provincia})`;

/** Indirizzo per l'embed di Google Maps (nessuna API key, nessun cookie di terze parti prima del consenso). */
export const mappaEmbedUrl = `https://www.google.com/maps?q=${encodeURIComponent(
  `${site.nome}, ${indirizzoBreve}`
)}&output=embed`;

export const mappaLinkUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
  `${site.nome}, ${indirizzoBreve}`
)}`;

export const navigazione = [
  { label: 'La Locanda', href: '/la-locanda' },
  { label: 'Camere', href: '/camere' },
  { label: 'Ristorante', href: '/ristorante' },
  { label: 'Gnocchi con la Fioreta', href: '/gnocchi-con-la-fioreta' },
  { label: 'Sentieri', href: '/sentieri' },
  { label: 'Contatti', href: '/contatti' },
] as const;
