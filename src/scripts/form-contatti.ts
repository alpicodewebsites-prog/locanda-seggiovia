/**
 * Invio del modulo contatti a Web3Forms.
 *
 * Il modulo funziona anche senza JavaScript: l'attributo `action` fa una POST
 * normale e Web3Forms reindirizza alla pagina /grazie tramite il campo
 * `redirect`. Questo script aggiunge il livello successivo — invio senza
 * ricaricamento ed esito leggibile — ma non è indispensabile.
 */

type Esito = { ok: boolean; messaggio: string };

const ENDPOINT = 'https://api.web3forms.com/submit';

function mostraEsito(contenitore: HTMLElement, { ok, messaggio }: Esito): void {
  contenitore.textContent = messaggio;
  contenitore.classList.remove('hidden');
  contenitore.classList.toggle('text-forest-700', ok);
  contenitore.classList.toggle('text-glow-500', !ok);
  contenitore.focus?.();
}

export function renderFormEsito(): void {
  const modulo = document.getElementById('modulo-contatti') as HTMLFormElement | null;
  if (!modulo) return;

  const esito = document.getElementById('esito-modulo');
  if (!esito) return;

  const reindirizzamento = modulo.dataset.redirect ?? '/grazie';

  modulo.addEventListener('submit', async (evento) => {
    // Senza reCAPTCHA configurato non c'è nulla da attendere: si invia subito.
    const campoRecaptcha = modulo.querySelector<HTMLInputElement>('#recaptchaResponse');

    if (!campoRecaptcha) {
      // Lascia fare al browser: POST classica con redirect a /grazie.
      return;
    }

    evento.preventDefault();

    const siteKey = document.querySelector<HTMLScriptElement>(
      'script[src*="recaptcha/api.js"]',
    )?.src;
    const chiave = siteKey ? new URL(siteKey).searchParams.get('render') : null;

    const bottone = modulo.querySelector<HTMLButtonElement>('button[type="submit"]');
    bottone?.setAttribute('disabled', 'true');
    mostraEsito(esito, { ok: true, messaggio: 'Invio in corso…' });

    try {
      if (!chiave) throw new Error('Chiave reCAPTCHA non trovata.');

      // reCAPTCHA v3 non mostra nulla all'utente: restituisce un punteggio.
      const grecaptcha = (window as unknown as { grecaptcha?: any }).grecaptcha;
      if (!grecaptcha) throw new Error('reCAPTCHA non ancora caricato. Riprova.');

      const token: string = await new Promise((resolve, reject) => {
        grecaptcha.ready(() => {
          grecaptcha
            .execute(chiave, { action: 'contatti' })
            .then(resolve)
            .catch(() => reject(new Error('Verifica di sicurezza non riuscita.')));
        });
      });

      campoRecaptcha.value = token;

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
      mostraEsito(esito, {
        ok: true,
        messaggio: 'Messaggio inviato. Ti risponderemo al più presto.',
      });
    } catch (errore) {
      mostraEsito(esito, {
        ok: false,
        messaggio:
          errore instanceof Error
            ? `${errore.message} Puoi anche scriverci a locandaseggiovia@gmail.com.`
            : 'Invio non riuscito. Puoi anche scriverci a locandaseggiovia@gmail.com.',
      });
    } finally {
      bottone?.removeAttribute('disabled');
    }
  });
}
