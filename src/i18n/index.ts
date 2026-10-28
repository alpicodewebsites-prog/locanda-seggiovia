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
    if (voci.it === pulito || voci.en === pulito) return logico;
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

  if (voce) return conSlashFinale(voce[lingua]);

  const scheda = logico.match(/^\/sentieri\/(.+)$/);
  if (scheda) {
    return lingua === 'en' ? `/en/trails/${scheda[1]}/` : `/sentieri/${scheda[1]}/`;
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
export function alternativeLinguistiche(percorso: string) {
  const logico = percorsoLogico(percorso);
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
