/**
 * Come le pagine leggono i contenuti nella lingua giusta.
 *
 * ----------------------------------------------------------------------------
 * COME SONO FATTI I CONTENUTI BILINGUI
 *
 * Non ci sono collezioni separate per lingua: la stessa collezione contiene
 * entrambe le versioni, e si distinguono dalla cartella. La versione inglese sta
 * in una sottocartella `en/`.
 *
 *   src/content/sentieri/gino-solda.md      → id: gino-solda       (italiano)
 *   src/content/sentieri/en/gino-solda.md   → id: en/gino-solda    (inglese)
 *
 * PERCHÉ UNA CARTELLA E NON UN SUFFISSO NEL NOME
 *
 * La prima versione usava il suffisso `-en` nel nome del file. Funzionava, ma il
 * pannello di gestione non sa indicare «i file che finiscono per -en»: sa indicare
 * una cartella. Con la cartella, ogni collezione inglese del pannello ha una
 * regola sola e non c'è niente da indovinare.
 *
 * Un secondo motivo, più sottile: un identificativo `en/testi` si legge, mentre
 * `testien` (che è quello che Astro produce con un punto nel nome, `testi.en.md`,
 * perché il punto sparisce) è illeggibile e ambiguo — un sentiero il cui nome
 * finisse per «en» verrebbe scambiato per una traduzione.
 *
 * I file che non contengono testo — le fotografie — non sono tradotti: restano
 * uno solo per tutte e due le lingue, perché un'immagine non ha lingua.
 * ----------------------------------------------------------------------------
 */
import type { Lingua } from '../i18n';

/** La cartella delle versioni inglesi, dentro ogni collezione. */
const CARTELLA_EN = 'en';

/** L'id del file di traduzione a partire dall'id italiano. */
export function idTradotto(id: string, lingua: Lingua): string {
  return lingua === 'en' ? `${CARTELLA_EN}/${id}` : id;
}

/** Toglie la cartella della lingua, per confrontare le due versioni. */
export function idBase(id: string): string {
  const prefisso = `${CARTELLA_EN}/`;
  return id.startsWith(prefisso) ? id.slice(prefisso.length) : id;
}

/** Vero se il file è della lingua richiesta. */
export function inLingua(id: string, lingua: Lingua): boolean {
  return id.startsWith(`${CARTELLA_EN}/`) === (lingua === 'en');
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
