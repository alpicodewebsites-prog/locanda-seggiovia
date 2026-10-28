/**
 * I testi dell'interfaccia, uno per lingua.
 *
 * ----------------------------------------------------------------------------
 * REGOLA
 *
 * Qui dentro va SOLO ciò che è interfaccia: voci di menu, pulsanti, etichette,
 * messaggi di errore, testi alternativi. I contenuti veri — la storia della
 * locanda, i piatti, i sentieri — stanno nelle collezioni, perché li modifica la
 * cliente dal pannello e non devono passare da una modifica al codice.
 *
 * Se un testo serve a una sola pagina e non è modificabile, può stare qui; se è
 * qualcosa che la cliente vorrebbe cambiare, deve stare nel pannello.
 * ----------------------------------------------------------------------------
 *
 * USO
 *
 *   const t = traduzioni(lingua);
 *   <h1>{t.nav.camere}</h1>
 *
 * `traduzioni()` restituisce l'oggetto della lingua, quindi i nomi dei campi
 * sono verificati dal compilatore: se si scrive `t.nav.camre` la compilazione
 * fallisce, e non si scopre in produzione.
 */
import type { Lingua } from './index';

/** Le condizioni del tempo, per codice WMO. */
type CondizioniMeteo = Record<number, string>;

export interface TestiInterfaccia {
  comune: {
    saltaAlContenuto: string;
    scopri: string;
    tuttiISentieri: string;
    tornaAllaHome: string;
    apreNuovaScheda: string;
    linguaCorrente: string;
  };
  selettore: {
    etichetta: string;
    /** Nome accessibile del selettore: «Lingua: Italiano». */
    descrizione: string;
  };
  nav: {
    laLocanda: string;
    camere: string;
    ristorante: string;
    gnocchi: string;
    sentieri: string;
    contatti: string;
    navigazionePrincipale: string;
    apriMenu: string;
    chiudiMenu: string;
    mappaDelSito: string;
    percorsoDiNavigazione: string;
  };
  footer: {
    doveSiamo: string;
    ilSito: string;
    orari: string;
    ristorante: string;
    reception: string;
    orariDaConfermare: string;
    tuttiIGiorni: string;
    privacy: string;
    cookie: string;
  };
  prenotazione: {
    titolo: string;
    descrizione: string;
    arrivo: string;
    partenza: string;
    ospiti: string;
    camera: string;
    nome: string;
    note: string;
    notaLabel: string;
    placeholderNome: string;
    invia: string;
    /** Etichette delle due camere e dell'opzione «non so ancora». */
    tipiCamera: { singola: string; doppia: string; indifferente: string };
    /** «1 persona», «2 persone», … «5 o più». */
    conteggi: string[];
  };
  grazie: {
    etichetta: string;
    titolo: string;
    testo: string;
    metaTitolo: string;
    metaDescrizione: string;
    torna: string;
  };
  nonTrovata: {
    etichetta: string;
    titolo: string;
    testo: string;
    metaTitolo: string;
    metaDescrizione: string;
    torna: string;
  };
  sentieri: {
    distanza: string;
    dislivello: string;
    durata: string;
    difficolta: string;
    quotaMassima: string;
    partenza: string;
    segnavia: string;
    tutti: string;
  };
  meteo: {
    etichetta: string;
    caricamento: string;
    fonte: string;
    fonteLink: string;
    senzaJavaScript: string;
    bollettino: string;
    oggi: string;
    domani: string;
    vento: string;
    errore: string;
    riprova: string;
    condizioniVariabili: string;
    giorni: string[];
    condizioni: CondizioniMeteo;
  };
}

const IT: TestiInterfaccia = {
  comune: {
    saltaAlContenuto: 'Salta al contenuto',
    scopri: 'Scopri',
    tuttiISentieri: 'Tutti i sentieri',
    tornaAllaHome: 'Torna alla home',
    apreNuovaScheda: 'si apre in una nuova scheda',
    linguaCorrente: 'lingua corrente',
  },
  selettore: {
    etichetta: 'Lingua',
    descrizione: 'Scegli la lingua del sito',
  },
  nav: {
    laLocanda: 'La Locanda',
    camere: 'Camere',
    ristorante: 'Ristorante',
    gnocchi: 'Gnocchi con la Fioreta',
    sentieri: 'Sentieri',
    contatti: 'Contatti',
    navigazionePrincipale: 'Navigazione principale',
    apriMenu: 'Apri il menu di navigazione',
    chiudiMenu: 'Chiudi il menu di navigazione',
    mappaDelSito: 'Mappa del sito',
    percorsoDiNavigazione: 'Percorso di navigazione',
  },
  footer: {
    doveSiamo: 'Dove siamo',
    ilSito: 'Il sito',
    orari: 'Orari',
    ristorante: 'Ristorante',
    reception: 'Reception',
    orariDaConfermare: 'orari da confermare',
    tuttiIGiorni: 'Tutti i giorni (da confermare)',
    privacy: 'Privacy Policy',
    cookie: 'Cookie Policy',
  },
  sentieri: {
    distanza: 'Distanza',
    dislivello: 'Dislivello',
    durata: 'Durata',
    difficolta: 'Difficoltà',
    quotaMassima: 'Quota massima',
    partenza: 'Partenza',
    segnavia: 'Segnavia',
    tutti: 'Tutti i sentieri',
  },
  prenotazione: {
    titolo: 'Chiedi la disponibilità',
    descrizione:
      'Scrivi quando vorresti arrivare. Ti rispondiamo noi, di solito entro un giorno.',
    arrivo: 'Arrivo',
    partenza: 'Partenza',
    ospiti: 'Ospiti',
    camera: 'Camera',
    nome: 'Nome e cognome',
    note: 'Note',
    notaLabel: 'Note',
    placeholderNome: 'Come ti chiami',
    invia: 'Invia la richiesta',
    tipiCamera: {
      singola: 'Camera singola',
      doppia: 'Camera doppia',
      indifferente: 'Non so ancora',
    },
    conteggi: ['1 persona', '2 persone', '3 persone', '4 persone', '5 o più'],
  },
  grazie: {
    etichetta: 'Messaggio inviato',
    titolo: 'Grazie, ci siamo',
    testo:
      'Il messaggio è arrivato. Ti risponderemo il prima possibile, di solito entro la giornata. Se hai fretta, chiamaci.',
    metaTitolo: 'Messaggio inviato',
    metaDescrizione:
      'Conferma di invio del modulo di contatto della Locanda Seggiovia a Recoaro Terme: il messaggio è arrivato, ti risponderemo al più presto.',
    torna: 'Torna alla home',
  },
  nonTrovata: {
    etichetta: 'Errore 404',
    titolo: 'Questo sentiero non porta da nessuna parte',
    testo:
      'La pagina che cerchi è stata spostata o non è mai esistita. Da qui puoi tornare indietro oppure andare direttamente dove serve.',
    metaTitolo: 'Pagina non trovata',
    metaDescrizione:
      'La pagina cercata non esiste. Torna alla home della Locanda Seggiovia o consulta i sentieri delle Piccole Dolomiti.',
    torna: 'Home',
  },
  meteo: {
    etichetta: 'Meteo',
    caricamento: 'Caricamento del meteo…',
    fonte: 'Dati',
    fonteLink: 'Open-Meteo',
    senzaJavaScript: 'Il meteo si carica con JavaScript attivo. Senza, resta il',
    bollettino: 'bollettino di Recoaro Terme',
    oggi: 'Oggi',
    domani: 'Domani',
    vento: 'Vento',
    errore: 'Il meteo non è disponibile in questo momento. Riprova più tardi, oppure consulta il',
    riprova: 'bollettino di Recoaro Terme',
    condizioniVariabili: 'Condizioni variabili',
    giorni: ['domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato'],
    condizioni: {
      0: 'Sereno',
      1: 'Prevalentemente sereno',
      2: 'Parzialmente nuvoloso',
      3: 'Nuvoloso',
      45: 'Nebbia',
      48: 'Nebbia con brina',
      51: 'Pioviggine debole',
      53: 'Pioviggine moderata',
      55: 'Pioviggine intensa',
      56: 'Pioviggine gelata',
      57: 'Pioviggine gelata intensa',
      61: 'Pioggia debole',
      63: 'Pioggia moderata',
      65: 'Pioggia forte',
      66: 'Pioggia gelata',
      67: 'Pioggia gelata forte',
      71: 'Neve debole',
      73: 'Neve moderata',
      75: 'Neve forte',
      77: 'Granelli di neve',
      80: 'Rovesci deboli',
      81: 'Rovesci moderati',
      82: 'Rovesci forti',
      85: 'Rovesci di neve',
      86: 'Rovesci di neve forti',
      95: 'Temporale',
      96: 'Temporale con grandine',
      99: 'Temporale con grandine forte',
    },
  },
};

const EN: TestiInterfaccia = {
  comune: {
    saltaAlContenuto: 'Skip to content',
    scopri: 'Explore',
    tuttiISentieri: 'All trails',
    tornaAllaHome: 'Back to the home page',
    apreNuovaScheda: 'opens in a new tab',
    linguaCorrente: 'current language',
  },
  selettore: {
    etichetta: 'Language',
    descrizione: 'Choose the site language',
  },
  nav: {
    laLocanda: 'The Inn',
    camere: 'Rooms',
    ristorante: 'Restaurant',
    gnocchi: 'Gnocchi with Fioreta',
    sentieri: 'Trails',
    contatti: 'Contact',
    navigazionePrincipale: 'Main navigation',
    apriMenu: 'Open the navigation menu',
    chiudiMenu: 'Close the navigation menu',
    mappaDelSito: 'Site map',
    percorsoDiNavigazione: 'Breadcrumb',
  },
  footer: {
    doveSiamo: 'Where we are',
    ilSito: 'The site',
    orari: 'Opening hours',
    ristorante: 'Restaurant',
    reception: 'Reception',
    orariDaConfermare: 'hours to be confirmed',
    tuttiIGiorni: 'Every day (to be confirmed)',
    privacy: 'Privacy Policy',
    cookie: 'Cookie Policy',
  },
  sentieri: {
    distanza: 'Distance',
    dislivello: 'Ascent',
    durata: 'Time',
    difficolta: 'Grade',
    quotaMassima: 'Highest point',
    partenza: 'Starting point',
    segnavia: 'Waymark',
    tutti: 'All trails',
  },
  prenotazione: {
    titolo: 'Check availability',
    descrizione:
      'Tell us when you would like to arrive. We answer ourselves, usually within a day.',
    arrivo: 'Arrival',
    partenza: 'Departure',
    ospiti: 'Guests',
    camera: 'Room',
    nome: 'Full name',
    note: 'Notes',
    notaLabel: 'Anything we should know',
    placeholderNome: 'Your name',
    invia: 'Send the request',
    tipiCamera: {
      singola: 'Single room',
      doppia: 'Double room',
      indifferente: 'Not sure yet',
    },
    conteggi: ['1 guest', '2 guests', '3 guests', '4 guests', '5 or more'],
  },
  grazie: {
    etichetta: 'Message sent',
    titolo: 'Thank you, we have it',
    testo:
      'Your message has reached us. We will reply as soon as we can, usually the same day. If you are in a hurry, give us a ring.',
    metaTitolo: 'Message sent',
    metaDescrizione:
      'Confirmation that your message reached Locanda Seggiovia in Recoaro Terme. We will reply as soon as possible.',
    torna: 'Back to the home page',
  },
  nonTrovata: {
    etichetta: 'Error 404',
    titolo: 'This path leads nowhere',
    testo:
      'The page you are looking for has moved, or never existed. From here you can go back, or straight to where you need.',
    metaTitolo: 'Page not found',
    metaDescrizione:
      'The page was not found. Go back to the Locanda Seggiovia home page or browse the trails of the Piccole Dolomiti.',
    torna: 'Home page',
  },
  meteo: {
    etichetta: 'Weather',
    caricamento: 'Loading the weather…',
    fonte: 'Data from',
    fonteLink: 'Open-Meteo',
    senzaJavaScript: 'The weather loads with JavaScript enabled. Without it, see the',
    bollettino: 'forecast for Recoaro Terme',
    oggi: 'Today',
    domani: 'Tomorrow',
    vento: 'Wind',
    errore: 'The weather is not available right now. Try again later, or check the',
    riprova: 'forecast for Recoaro Terme',
    condizioniVariabili: 'Changeable conditions',
    giorni: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    condizioni: {
      0: 'Clear',
      1: 'Mainly clear',
      2: 'Partly cloudy',
      3: 'Overcast',
      45: 'Fog',
      48: 'Depositing rime fog',
      51: 'Light drizzle',
      53: 'Moderate drizzle',
      55: 'Dense drizzle',
      56: 'Light freezing drizzle',
      57: 'Dense freezing drizzle',
      61: 'Slight rain',
      63: 'Moderate rain',
      65: 'Heavy rain',
      66: 'Light freezing rain',
      67: 'Heavy freezing rain',
      71: 'Slight snow',
      73: 'Moderate snow',
      75: 'Heavy snow',
      77: 'Snow grains',
      80: 'Slight rain showers',
      81: 'Moderate rain showers',
      82: 'Violent rain showers',
      85: 'Slight snow showers',
      86: 'Heavy snow showers',
      95: 'Thunderstorm',
      96: 'Thunderstorm with hail',
      99: 'Thunderstorm with heavy hail',
    },
  },
};

export const UI: Record<Lingua, TestiInterfaccia> = { it: IT, en: EN };

/** I testi della lingua richiesta. */
export function traduzioni(lingua: Lingua): TestiInterfaccia {
  return UI[lingua];
}

/**
 * Le etichette delle voci di navigazione, indicizzate per indirizzo.
 *
 * `src/data/site.ts` elenca le voci con l'indirizzo italiano e l'etichetta
 * italiana. La barra e il piè di pagina devono mostrare l'etichetta nella lingua
 * della pagina: qui l'elenco diventa una tabella da indirizzo a parola, così i
 * due componenti non devono conoscere i nomi dei campi.
 *
 * Se una voce nuova venisse aggiunta a `site.ts` senza una traduzione qui, si
 * vedrebbe l'etichetta italiana invece di una voce vuota: sbagliato ma visibile,
 * e quindi correggibile.
 */
export function etichetteNavigazione(lingua: Lingua): Record<string, string> {
  const n = traduzioni(lingua).nav;
  return {
    '/la-locanda': n.laLocanda,
    '/camere': n.camere,
    '/ristorante': n.ristorante,
    '/gnocchi-con-la-fioreta': n.gnocchi,
    '/sentieri': n.sentieri,
  };
}
