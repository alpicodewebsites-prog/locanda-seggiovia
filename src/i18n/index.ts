/**
 * Le lingue del sito, e le funzioni per passare dall'una all'altra.
 *
 * ----------------------------------------------------------------------------
 * PERCHÉ PAGINE VERE E NON UNA TRADUZIONE A RUNTIME
 *
 * Si poteva fare più in fretta: un dizionario in JavaScript, un selettore che
 * cambia il testo senza ricaricare, e la tendina funziona. Ma quel sito non
 * esisterebbe per Google: la versione inglese sarebbe invisibile ai motori di
 * ricerca, e chi cerca «hiking trails Recoaro Terme» in inglese non ci
 * arriverebbe mai. Per una locanda che vive di escursionisti stranieri sarebbe
 * stata una tendina che serve a niente.
 *
 * Qui quindi ogni pagina esiste due volte, come pagina vera: `/camere/` e
 * `/en/rooms/`. Il selettore è fatto di collegamenti, non di JavaScript.
 * Conseguenze, tutte buone:
 *   - funziona anche senza JavaScript
 *   - ogni versione ha il suo indirizzo, condivisibile e indicizzabile
 *   - `<html lang>` è giusto, quindi i lettori di schermo leggono con la voce
 *     giusta e Google capisce che lingua è
 *   - si può collegare la versione inglese da un sito o da una mail
 *
 * Il costo: i testi vanno tradotti, e la cliente li deve tenere aggiornati in
 * due lingue. È il prezzo di un sito che si trova; l'alternativa era un sito
 * bilingue che nessuno trova.
 * ----------------------------------------------------------------------------
 */

/** Le lingue disponibili. L'ordine è quello del selettore. */
export const LINGUE = [
  {
    /** Codice usato negli indirizzi e nei contenuti. */
    codice: 'it',
    /** Valore di `<html lang>` e di `hreflang`. */
    html: 'it-IT',
    /** Nome nella lingua stessa: è così che si scrive in un selettore. */
    nome: 'Italiano',
    /** Sigla per il selettore compatto. */
    breve: 'IT',
  },
  {
    codice: 'en',
    html: 'en',
    nome: 'English',
    breve: 'EN',
  },
] as const;

export type Lingua = (typeof LINGUE)[number]['codice'];

/** La lingua di chi arriva senza indicazioni. */
export const LINGUA_PREDEFINITA: Lingua = 'it';

/** La lingua scritta nell'indirizzo. Tutto ciò che non è `/en/` è italiano. */
export function linguaDaPercorso(percorso: string): Lingua {
  const primo = percorso.split('/').filter(Boolean)[0];
  return primo === 'en' ? 'en' : 'it';
}

/** Quella comoda nelle pagine, che hanno `Astro.url`. */
export function linguaDaUrl(url: URL): Lingua {
  return linguaDaPercorso(url.pathname);
}

/**
 * La corrispondenza fra indirizzi italiani e inglesi.
 *
 * `/camere/` → `/en/rooms/` non si può indovinare: gli indirizzi inglesi sono
 * tradotti, non prefissati. Un indirizzo inglese fatto di parole italiane
 * («/en/camere/») si legge male e perde valore nei motori di ricerca, che
 * guardano anche le parole dell'indirizzo.
 */
export const PERCORSI: Record<string, Record<Lingua, string>> = {
  '/': { it: '/', en: '/en/' },
  '/la-locanda': { it: '/la-locanda', en: '/en/the-inn' },
  '/camere': { it: '/camere', en: '/en/rooms' },
  '/ristorante': { it: '/ristorante', en: '/en/restaurant' },
  '/gnocchi-con-la-fioreta': { it: '/gnocchi-con-la-fioreta', en: '/en/gnocchi' },
  '/sentieri': { it: '/sentieri', en: '/en/trails' },
  '/contatti': { it: '/contatti', en: '/en/contact' },
  '/privacy': { it: '/privacy', en: '/en/privacy' },
  '/cookie': { it: '/cookie', en: '/en/cookies' },
  '/grazie': { it: '/grazie', en: '/en/thank-you' },
};

/**
 * I percorsi che hanno DAVVERO una pagina inglese.
 *
 * ----------------------------------------------------------------------------
 * PERCHÉ NON BASTA PREFISSARE
 *
 * Tradurre il sito è un lavoro a tappe: per un po' di tempo alcune pagine
 * esisteranno in inglese e altre no. Se il menu inglese puntasse comunque a
 * `/en/restaurant/`, il visitatore che ha appena scelto «English» troverebbe un
 * errore al primo clic — peggio di una pagina in italiano.
 *
 * Qui l'elenco delle pagine inglesi si legge DAI FILE, non da una lista scritta
 * a mano: `import.meta.glob` guarda dentro `src/pages/en/` in fase di
 * compilazione. Così, appena una pagina tradotta viene aggiunta, i collegamenti
 * verso di lei si accendono da soli e nessuno deve ricordarsi di aggiornare
 * nient'altro.
 * ----------------------------------------------------------------------------
 */
const FILE_EN = import.meta.glob('/src/pages/en/*.astro');
const FILE_EN_SCHEDE = import.meta.glob('/src/pages/en/trails/*.astro');

/** Da `/src/pages/en/rooms.astro` a `/en/rooms/`, che è il valore in PERCORSI. */
function percorsoIngleseDaFile(percorsoFile: string): string {
  const nome = percorsoFile.replace('/src/pages/en/', '').replace(/\.astro$/, '');
  return nome === 'index' ? '/en/' : `/en/${nome}/`;
}

const DISPONIBILI_EN = new Set<string>(
  Object.keys(FILE_EN)
    .map(percorsoIngleseDaFile)
    .flatMap((percorsoEn) =>
      Object.entries(PERCORSI)
        // I valori in PERCORSI sono senza slash finale, quelli ricavati dai file
        // ce l'hanno: vanno confrontati nella stessa forma.
        .filter(([, voci]) => conSlashFinale(voci.en) === conSlashFinale(percorsoEn))
        .map(([logico]) => logico),
    ),
);

/**
 * Le schede dei sentieri hanno una pagina inglese solo quando esiste il file
 * della scheda. `index.astro` è l'ELENCO, non una scheda: contarlo qui faceva
 * puntare i collegamenti a `/en/trails/<slug>/` prima che quelle pagine
 * esistessero.
 */
const SCHEDE_EN = Object.keys(FILE_EN_SCHEDE).some(
  (percorsoFile) => !percorsoFile.endsWith('/index.astro'),
);

/** Toglie lo slash finale, tranne sulla radice. */
function normalizza(percorso: string): string {
  return percorso.length > 1 ? percorso.replace(/\/$/, '') : percorso;
}

/**
 * Rimette lo slash finale, come lo hanno gli indirizzi di questo sito.
 *
 * Serve perché `canonical` e `hreflang` devono indicare lo STESSO indirizzo:
 * se uno dice `/grazie/` e l'altro `/grazie`, Google li tratta come due
 * indirizzi diversi e i collegamenti fra lingue non funzionano come dovrebbero.
 */
function conSlashFinale(percorso: string): string {
  return percorso.endsWith('/') ? percorso : `${percorso}/`;
}

/** Il percorso logico: quello italiano, che fa da chiave in `PERCORSI`. */
export function percorsoLogico(percorso: string): string {
  const pulito = normalizza(percorso);

  for (const [logico, voci] of Object.entries(PERCORSI)) {
    /*
      Le due parti vanno confrontate nella stessa forma: `normalizza` toglie lo
      slash finale dalla richiesta, ma i valori della mappa lo hanno (`/en/`).
      Senza questa normalizzazione la home inglese non veniva riconosciuta, e le
      due home non si dichiaravano a vicenda.
    */
    if (normalizza(voci.it) === pulito || normalizza(voci.en) === pulito) return logico;
  }

  /*
    Le schede dei sentieri hanno lo stesso slug nelle due lingue: il nome di un
    sentiero non si traduce. `/en/trails/gino-solda` e `/sentieri/gino-solda`
    sono quindi lo stesso percorso logico.
  */
  const scheda = pulito.match(/^\/en\/trails\/(.+)$/);
  if (scheda) return `/sentieri/${scheda[1]}`;

  return pulito;
}

/** Il percorso di una pagina nella lingua richiesta. */
export function percorsoLocalizzato(percorso: string, lingua: Lingua): string {
  const logico = percorsoLogico(percorso);
  const voce = PERCORSI[logico];

  if (voce) {
    /*
      Se la pagina inglese non esiste ancora, si manda alla versione italiana:
      meglio una pagina comprensibile in un'altra lingua che un errore. Il
      collegamento si sistema da solo quando la traduzione arriva.
    */
    if (lingua === 'en' && !DISPONIBILI_EN.has(logico)) return conSlashFinale(voce.it);
    return conSlashFinale(voce[lingua]);
  }

  const scheda = logico.match(/^\/sentieri\/(.+)$/);
  if (scheda) {
    const inInglese = lingua === 'en' && SCHEDE_EN;
    return inInglese ? `/en/trails/${scheda[1]}/` : `/sentieri/${scheda[1]}/`;
  }

  return lingua === 'it' ? conSlashFinale(logico) : conSlashFinale(`/en${logico}`);
}

/** Quella comoda nei modelli, che hanno il percorso corrente. */
export function percorsoAlternativo(percorso: string, lingua: Lingua): string {
  return percorsoLocalizzato(percorso, lingua);
}

/**
 * Gli indirizzi alternativi di una pagina, per `hreflang`.
 *
 * Non basta dichiarare la lingua: senza questi collegamenti Google tratta le
 * due versioni come due pagine che si fanno concorrenza, e sceglie lui quale
 * mostrare. Con, capisce che sono la stessa pagina in due lingue.
 */
/**
 * Vero se la pagina esiste in entrambe le lingue.
 *
 * La 404 e la conferma di invio no: la prima è una pagina sola servita per
 * qualunque indirizzo sbagliato, la seconda ha una versione inglese ma non è una
 * pagina di contenuto da collegare. Serve a non annunciare e non collegare
 * indirizzi che non esistono.
 */
export function paginaBilingue(percorso: string): boolean {
  const logico = percorsoLogico(percorso);
  return PERCORSI[logico] !== undefined || /^\/sentieri\/[^/]+$/.test(logico);
}

export function alternativeLinguistiche(percorso: string) {
  const logico = percorsoLogico(percorso);

  /*
    Solo per le pagine che esistono davvero in entrambe le lingue.

    La 404 è una pagina sola, servita per qualunque indirizzo sbagliato: non ha
    una versione inglese e non deve dichiararne una. Senza questo controllo
    annunciava `/404/` e `/en/404/`, due indirizzi che non esistono — e il
    controllo dei collegamenti interni lo ha segnalato.
  */
  if (!paginaBilingue(percorso)) return [];

  return [
    ...LINGUE.map((l) => ({
      hreflang: l.html,
      href: percorsoLocalizzato(logico, l.codice),
    })),
    // Chi non ha una lingua preferita vede l'italiano.
    { hreflang: 'x-default', href: percorsoLocalizzato(logico, LINGUA_PREDEFINITA) },
  ];
}

/** I dati della lingua, per `<html lang>` e per il selettore. */
export function datiLingua(codice: Lingua) {
  return LINGUE.find((l) => l.codice === codice) ?? LINGUE[0];
}

/**
 * Riempie i segnaposto di un testo: `{gestori}` diventa il valore passato.
 *
 * Serve alle frasi che contengono dati della struttura. In italiano una frase
 * come «La locanda la portano {gestori}» funziona; in inglese la stessa
 * informazione va in un punto diverso della frase. Se si concatenasse a mano
 * («The inn is run by » + gestori), ogni lingua dovrebbe portarsi dietro la
 * propria impalcatura. Con i segnaposto, l'ordine lo decide la traduzione.
 *
 * Se un segnaposto non ha un valore resta visibile com'è: meglio una scritta
 * evidente in pagina che una frase muta che nessuno nota.
 */
export function riempi(modello: string, valori: Record<string, string>): string {
  return modello.replace(/\{(\w+)\}/g, (intero, chiave: string) => valori[chiave] ?? intero);
}
