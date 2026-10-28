/**
 * Come le pagine leggono i contenuti nella lingua giusta.
 *
 * ----------------------------------------------------------------------------
 * COME SONO FATTI I CONTENUTI BILINGUI
 *
 * Non ci sono collezioni separate per lingua, e non è una scorciatoia: il loader
 * `glob()` di Astro legge già le sottocartelle e i file con suffisso, quindi la
 * stessa collezione contiene entrambe le versioni, e si distinguono dal nome del
 * file.
 *
 *   src/content/sentieri/gino-solda.md      → id: gino-solda      (italiano)
 *   src/content/sentieri/gino-solda.en.md   → id: gino-solda.en   (inglese)
 *
 * Perché il suffisso e non una cartella `en/`: perché è la forma che il pannello
 * di gestione (Sveltia) sa mostrare come UNA scheda con due lingue affiancate.
 * Con due cartelle separate la cliente vedrebbe due schede distinte e dovrebbe
 * ricordarsi di aggiornarle entrambe: prima o poi una resta indietro. Con il
 * suffisso apre la scheda del sentiero e trova italiano e inglese nello stesso
 * posto.
 *
 * I file che non contengono testo — le fotografie — non sono tradotti: restano
 * uno solo per tutte e due le lingue, perché un'immagine non ha lingua.
 * ----------------------------------------------------------------------------
 */
import type { Lingua } from '../i18n';

/**
 * Il suffisso dei file in inglese.
 *
 * ----------------------------------------------------------------------------
 * PERCHÉ UN TRATTINO E NON UN PUNTO
 *
 * La prima versione usava `testi.en.md`, che è la convenzione più diffusa. Astro
 * però costruisce l'identificativo di una voce a partire dal nome del file
 * togliendo i caratteri che non sono lettere, cifre o trattini: il punto
 * sparisce, e `testi.en` diventa `testien`.
 *
 * Il risultato era silenzioso e insidioso: la ricerca di `testi.en` non trovava
 * niente, la pagina ripiegava sull'italiano, e non si vedeva nessun errore —
 * solo un avviso facile da prendere per rumore. L'ho scoperto elencando gli id
 * veri delle collezioni, non leggendo il codice.
 *
 * Con il trattino l'identificativo diventa `testi-en` e resta riconoscibile.
 * ----------------------------------------------------------------------------
 */
const SUFFISSO = '-en';

/** L'id del file di traduzione a partire dall'id italiano. */
export function idTradotto(id: string, lingua: Lingua): string {
  return lingua === 'en' ? `${id}${SUFFISSO}` : id;
}

/** Toglie il suffisso, per confrontare le due versioni. */
export function idBase(id: string): string {
  return id.endsWith(SUFFISSO) ? id.slice(0, -SUFFISSO.length) : id;
}

/** Vero se il file è della lingua richiesta. */
export function inLingua(id: string, lingua: Lingua): boolean {
  return id.endsWith(SUFFISSO) === (lingua === 'en');
}

/**
 * Le schede di una collezione nella lingua richiesta.
 *
 * `getCollection()` restituisce tutte e due le versioni di ogni scheda. Qui si
 * tiene solo quella giusta, mantenendo l'ordine deciso in `ordine`.
 */
export function schedeLingua<T extends { id: string }>(voci: T[], lingua: Lingua): T[] {
  return voci.filter((v) => inLingua(v.id, lingua));
}

/**
 * Sceglie la versione tradotta, ripiegando sull'italiano se manca.
 *
 * Il ripiego serve a non far cadere la compilazione mentre una traduzione è in
 * corso. Ma un ripiego silenzioso sarebbe peggio del guasto: la pagina inglese
 * mostrerebbe contenuto italiano e nessuno se ne accorgerebbe. Per questo
 * `scripts/verifica_traduzioni.py` confronta gli elenchi dei file e segnala le
 * schede senza traduzione: il ripiego tiene in piedi il sito, il controllo dice
 * cosa manca.
 */
export function conRipiego<T extends { id: string }>(
  voci: T[],
  id: string,
  lingua: Lingua,
): T | undefined {
  const cercato = idTradotto(id, lingua);
  return voci.find((v) => v.id === cercato) ?? voci.find((v) => v.id === id);
}
