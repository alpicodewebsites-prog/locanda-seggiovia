/**
 * Invio della richiesta di disponibilità.
 *
 * Differenza rispetto al modulo contatti: qui l'esito compare SEMPRE nella
 * pagina, senza ricaricarla, perché il messaggio di conferma fa parte della
 * richiesta — «ti risponderemo entro 24 ore» è la rassicurazione che chiude il
 * percorso.
 *
 * Senza JavaScript il modulo resta utilizzabile: l'attributo `action` fa una
 * POST normale verso Web3Forms, che reindirizza a /grazie.
 */

const ENDPOINT = 'https://api.web3forms.com/submit';

/** Il messaggio mostrato quando l'invio riesce. */
const CONFERMA = 'Richiesta inviata. Ti risponderemo entro 24 ore.';

/**
 * Trova, per ogni modulo di prenotazione presente nella pagina, il paragrafo
 * dove scrivere l'esito.
 */
function preparaModulo(modulo: HTMLFormElement): void {
  const idEsito = `${modulo.id}-esito`;
  const esito = document.getElementById(idEsito);
  if (!esito) return;

  const bottone = modulo.querySelector<HTMLButtonElement>('button[type="submit"]');

  const scrivi = (messaggio: string, ok: boolean): void => {
    esito.textContent = messaggio;
    esito.classList.remove('hidden');
    esito.classList.toggle('text-forest-700', ok);
    esito.classList.toggle('text-glow-500', !ok);
  };

  modulo.addEventListener('submit', (evento) => {
    // Se il browser segnala campi non validi, si lascia fare a lui: mostra i
    // suoi messaggi, che sono localizzati e accessibili.
    if (!modulo.checkValidity()) return;

    evento.preventDefault();

    // Controllo di buon senso: la partenza non può precedere l'arrivo.
    const arrivo = modulo.querySelector<HTMLInputElement>('input[name="arrivo"]')?.value;
    const partenza = modulo.querySelector<HTMLInputElement>('input[name="partenza"]')?.value;

    if (arrivo && partenza && partenza < arrivo) {
      scrivi('La data di partenza è precedente a quella di arrivo. Controlla le date.', false);
      esito.focus();
      return;
    }

    void invia(modulo, bottone, scrivi, esito);
  });
}

async function invia(
  modulo: HTMLFormElement,
  bottone: HTMLButtonElement | null,
  scrivi: (messaggio: string, ok: boolean) => void,
  esito: HTMLElement,
): Promise<void> {
  bottone?.setAttribute('disabled', 'true');
  scrivi('Invio in corso…', true);

  try {
    const risposta = await fetch(ENDPOINT, {
      method: 'POST',
      body: new FormData(modulo),
      headers: { Accept: 'application/json' },
    });

    const dati = (await risposta.json()) as { success?: boolean; message?: string };

    if (!risposta.ok || !dati.success) {
      throw new Error(dati.message ?? 'Invio non riuscito.');
    }

    modulo.reset();
    scrivi(CONFERMA, true);
  } catch (errore) {
    scrivi(
      errore instanceof Error
        ? `${errore.message} Puoi anche chiamarci: il numero è qui accanto.`
        : 'Invio non riuscito. Puoi anche chiamarci: il numero è qui accanto.',
      false,
    );
  } finally {
    bottone?.removeAttribute('disabled');
    esito.focus();
  }
}

export function attivaRichiestePrenotazione(): void {
  const moduli = document.querySelectorAll<HTMLFormElement>('form.prenotazione');
  moduli.forEach(preparaModulo);
}
