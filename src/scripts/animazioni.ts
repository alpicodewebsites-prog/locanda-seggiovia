/**
 * Assegna le animazioni di scorrimento agli elementi strutturali.
 *
 * PERCHÉ COSÌ, E NON CON `data-aos` SCRITTO A MANO
 *
 * Scrivere `data-aos` su ogni titolo, paragrafo e immagine di diciassette pagine
 * significherebbe centinaia di attributi sparsi nel markup: difficili da
 * correggere tutti insieme, facili da dimenticare su una pagina nuova, e
 * invisibili a chi legge il codice di una singola pagina senza sapere che
 * esiste una convenzione.
 *
 * Qui la regola sta in un posto solo: il tipo di elemento decide l'animazione.
 * Una pagina nuova eredita le animazioni senza fare niente.
 *
 * COME FUNZIONA
 *
 * Si gira il contenuto (`<main>`) e si assegnano gli attributi PRIMA che AOS
 * venga inizializzato, così la libreria li trova già in pagina.
 *
 * Ogni elemento viene assegnato una volta sola. Tre regole evitano le
 * animazioni sovrapposte, che sono il difetto tipico di chi anima «tutto»:
 *
 *   1. un elemento dentro un contenitore già animato viene saltato
 *      (il titolo dentro una scheda non si anima: si anima la scheda);
 *   2. un contenitore che racchiude elementi già animati viene saltato
 *      (la lista non si anima se si animano le schede che contiene);
 *   3. chi ha già `data-aos` scritto nel markup resta com'è.
 *
 * L'apertura della home è esclusa: è già a schermo quando la pagina si apre, e
 * animarla significherebbe farla comparire dopo, che è l'opposto di quello che
 * serve.
 */

/**
 * Tipo di animazione e ritardo, per tipo di elemento.
 *
 * I ritardi sono tarati sulla durata dell'animazione, che è 400 ms: il massimo
 * è 200 ms, cioè metà. Con ritardi più lunghi l'ultimo elemento di una griglia
 * arriverebbe quando i primi sono già fermi da un pezzo, e il movimento non si
 * leggerebbe più come una cosa sola.
 */
const TIPI = {
  titolo: { anim: 'fade-up', delay: 60 },
  paragrafo: { anim: 'fade-up', delay: 100 },
  immagine: { anim: 'zoom-in', delay: 140 },
  elenco: { anim: 'fade-in', delay: 60 },
  tabella: { anim: 'fade-in', delay: 60 },
  scheda: { anim: 'fade-up', delay: 60 },
} as const;

/** Passo del ritardo fra schede consecutive. */
const PASSO_SCHEDE = 70;

/** Ritardo massimo. Oltre, l'utente aspetta invece di vedere. */
const RITARDO_MASSIMO = 200;

export function preparaAnimazioni(): void {
  const contenuto = document.querySelector('main');
  if (!contenuto) return;

  const assegnati = new Set<Element>();

  /** L'elemento sta dentro qualcosa che abbiamo già animato? */
  const dentroAnimato = (el: Element): boolean => {
    for (const assegnato of assegnati) {
      if (assegnato !== el && assegnato.contains(el)) return true;
    }
    return false;
  };

  const assegnabile = (el: Element): boolean => {
    if (el.hasAttribute('data-aos')) return false; // già scritto nel markup
    if (assegnati.has(el)) return false;
    if (dentroAnimato(el)) return false;
    // Contiene già elementi animati: animare anche il contenitore
    // significherebbe due movimenti sovrapposti.
    if (el.querySelector('[data-aos]')) return false;
    return true;
  };

  const assegna = (el: Element, anim: string, delay: number): void => {
    if (!assegnabile(el)) return;
    el.setAttribute('data-aos', anim);
    if (delay > 0) {
      el.setAttribute('data-aos-delay', String(Math.min(delay, RITARDO_MASSIMO)));
    }
    assegnati.add(el);
  };

  // L'apertura resta ferma: è la prima cosa che si vede, non deve comparire.
  contenuto.querySelectorAll('.hero-apertura, .hero-apertura *').forEach((el) => {
    assegnati.add(el);
  });

  /*
    1. Schede e riquadri: si animano come un blocco unico.
       Il ritardo cresce fra elementi consecutivi, così una griglia entra in
       sequenza invece che tutta insieme.

       `figure` NON è qui di proposito: quasi sempre racchiude soltanto
       un'immagine, e la regola vuole che sia l'immagine a ingrandirsi. Se il
       contenitore la rivendicasse, l'immagine resterebbe ferma. Stesso motivo
       per `table`, che ha una sua regola più sotto.
  */
  contenuto
    .querySelectorAll('.card-accento, .scheda-piatto, .scheda-sentiero')
    .forEach((el) => {
      const fratelli = el.parentElement ? Array.from(el.parentElement.children) : [];
      const posizione = fratelli.indexOf(el);
      const ritardo = TIPI.scheda.delay + (posizione > 0 ? (posizione % 3) * PASSO_SCHEDE : 0);
      assegna(el, TIPI.scheda.anim, ritardo);
    });

  // 2. Titoli
  contenuto.querySelectorAll('h2, h3, h4').forEach((el) => {
    assegna(el, TIPI.titolo.anim, TIPI.titolo.delay);
  });

  // 3. Paragrafi
  contenuto.querySelectorAll('p').forEach((el) => {
    assegna(el, TIPI.paragrafo.anim, TIPI.paragrafo.delay);
  });

  // 4. Immagini: si ingrandiscono appena, dal 95% al 100%.
  contenuto.querySelectorAll('img').forEach((el) => {
    assegna(el, TIPI.immagine.anim, TIPI.immagine.delay);
  });

  // 5. Tabelle: dissolvenza, senza spostamento. Una tabella è lunga, e
  //    farla salire dal basso sarebbe pesante da guardare.
  contenuto.querySelectorAll('table').forEach((el) => {
    assegna(el, TIPI.tabella.anim, TIPI.tabella.delay);
  });

  // 6. Elenchi
  contenuto.querySelectorAll('ul, ol, dl').forEach((el) => {
    assegna(el, TIPI.elenco.anim, TIPI.elenco.delay);
  });
}
