/**
 * Caricamento differito della mappa di Google.
 *
 * L'iframe di Google Maps imposta cookie di terze parti appena viene caricato.
 * Qui non parte da solo: si attiva quando l'utente preme il pulsante, così la
 * scelta è sua. È il motivo per cui il sito non ha un banner cookie.
 *
 * Senza JavaScript non succede nulla di rotto: resta visibile l'indirizzo e il
 * collegamento che apre la mappa in una nuova scheda.
 */

const PLACEHOLDER_ID = 'segnaposto-mappa';
const BOTTONE_ID = 'carica-mappa';
const CONTENITORE_ID = 'contenitore-mappa';

export function caricaMappaAlClic(): void {
  const contenitore = document.getElementById(CONTENITORE_ID);
  const segnaposto = document.getElementById(PLACEHOLDER_ID);
  const bottone = document.getElementById(BOTTONE_ID);

  if (!contenitore || !segnaposto || !bottone) return;

  const src = contenitore.dataset.src;
  if (!src) return;

  bottone.addEventListener('click', () => {
    const iframe = document.createElement('iframe');
    iframe.src = src;
    iframe.title = `Mappa di Google: ${contenitore.dataset.titolo ?? 'posizione della struttura'}`;
    iframe.loading = 'lazy';
    iframe.className = 'block h-[320px] w-full border-0 md:h-[420px]';
    iframe.setAttribute('referrerpolicy', 'no-referrer-when-downgrade');
    iframe.setAttribute(
      'sandbox',
      'allow-scripts allow-same-origin allow-popups allow-forms',
    );

    segnaposto.replaceWith(iframe);
  });
}
