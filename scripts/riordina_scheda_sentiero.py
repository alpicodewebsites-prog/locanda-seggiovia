"""
Riordina la scheda di un sentiero.

COM'ERA (e perché non funzionava)
Una griglia 7/5: a sinistra il titolo e tre righe di descrizione, a destra una
colonna con sette righe di dati tecnici, la nota, la webcam e il meteo. La
sinistra finiva quasi subito e restava vuota per centinaia di pixel, mentre la
destra diventava una lista lunga e stretta. Le due colonne non si
corrispondevano, e la pagina sembrava messa insieme senza un criterio.

COM'È ADESSO
1. I dati che servono per decidere — difficoltà, distanza, dislivello, durata,
   quota, partenza, segnavia — stanno in una fascia a tutta larghezza subito
   sotto l'apertura. Sono la cosa che si cerca per prima, e ora occupano lo
   spazio che meritano invece di essere compressi in una colonna.

2. Sotto, due colonne che si corrispondono: il racconto a sinistra, e a destra
   il meteo e la webcam. La colonna destra non è più una lista di dati ma due
   riquadri, quindi le due colonne hanno un'altezza simile.

3. Fra le due colonne resta una colonna di griglia vuota. È spazio, non un
   buco: tiene il racconto a una lunghezza leggibile e stacca la colonna delle
   condizioni.

Uso:  python scripts/riordina_scheda_sentiero.py
"""

from __future__ import annotations

import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
PAGINA = RADICE / "src" / "pages" / "sentieri" / "[id].astro"
CSS = RADICE / "src" / "styles" / "global.css"

NUOVO = '''  <!-- ==================================================================
       I dati, in una fascia a tutta larghezza
       ------------------------------------------------------------------
       Difficoltà, distanza, dislivello, durata, quota, partenza e segnavia:
       sono le cose che si cercano per prime, prima ancora di leggere di cosa
       si tratta. Prima stavano in una colonna stretta a destra, con accanto
       tre righe di testo e tanto vuoto.

       Il numero è grande e in carattere con grazie, l'etichetta piccola sopra:
       si scorre la fila e si è già deciso se il percorso è alla propria portata.
       ================================================================== -->
  <section class="dati-sentiero" aria-labelledby="titolo-dati">
    <div class="shell">
      <h2 id="titolo-dati" class="sr-only">Dati tecnici del percorso</h2>

      <dl class="dati-sentiero__fila">
        {
          datiTecnici.map((riga) => (
            <div class="dato">
              <dt class="dato__voce">{riga.voce}</dt>
              <dd class="dato__valore">{riga.valore}</dd>
            </div>
          ))
        }
      </dl>

      <p class="dati-sentiero__nota">
        Difficoltà secondo la scala del CAI. I dati sono indicativi: prima di partire
        verifica le condizioni del sentiero.
      </p>
    </div>
  </section>

  <!-- ==================================================================
       Il racconto e le condizioni
       ------------------------------------------------------------------
       Due colonne che si corrispondono: il racconto a sinistra, meteo e
       webcam a destra. Fra le due resta una colonna di griglia vuota — è
       spazio, non un buco: tiene il racconto a una lunghezza leggibile e
       stacca la colonna delle condizioni.
       ================================================================== -->
  <section class="section-y" aria-labelledby="titolo-percorso">
    <div class="shell grid gap-10 md:grid-cols-12">
      <div class="md:col-span-7">
        <h2 id="titolo-percorso" class="display-2 text-stone-900">Il percorso</h2>
        <p class="mt-6 max-w-[62ch] text-[1.0625rem] leading-relaxed text-stone-600">
          {d.descrizione}
        </p>

        <p class="mt-8">
          <a href="/sentieri" class="link-arrow">
            Tutti i sentieri
            <svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true">
              <path
                d="M1 5h11m0 0L8.5 1.5M12 5l-3.5 3.5"
                stroke="currentColor"
                stroke-width="1.4"
                stroke-linecap="round"
                stroke-linejoin="round"></path>
            </svg>
          </a>
        </p>
      </div>

      <aside class="flex flex-col gap-5 md:col-span-4 md:col-start-9" aria-labelledby="titolo-condizioni">
        <h2 id="titolo-condizioni" class="sr-only">Condizioni</h2>

        {
          meteo && (
            <MeteoSentiero
              latitudine={meteo.latitudine}
              longitudine={meteo.longitudine}
              localita={meteo.localita}
              quota={meteo.quota}
            />
          )
        }

        {
          d.webcam && (
            <a
              href={d.webcam}
              rel="noopener external"
              target="_blank"
              class="webcam"
            >
              <span class="webcam__voce">Webcam</span>
              <span class="webcam__nome">{d.webcamEtichetta ?? 'Guarda la webcam'}</span>
              <span class="webcam__nota">
                Immagine aggiornata dalla fonte, in una nuova scheda ↗
              </span>
            </a>
          )
        }
      </aside>
    </div>
  </section>
'''

NUOVO_CSS = '''  /*
    ==========================================================================
    LA FASCIA DEI DATI DI UN SENTIERO
    ==========================================================================

    Sette numeri su una fila, larghi quanto la pagina. Prima erano in una
    colonna stretta a destra: chi voleva sapere quanto era lungo il percorso
    doveva leggerlo in verticale, mentre metà della pagina restava vuota.

    La fila si adatta da sola: `auto-fit` con una larghezza minima fa il conto.
    Se un sentiero ha meno dati — per esempio senza segnavia — le celle si
    allargano invece di lasciare un buco.
  */
  .dati-sentiero {
    padding-block: clamp(1.5rem, 3.5vw, 2.25rem);
    background-color: var(--color-stone-50);
    border-bottom: 1px solid color-mix(in oklab, var(--color-stone-500) 18%, transparent);
  }

  .dati-sentiero__fila {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(6.5rem, 1fr));
    gap: clamp(1rem, 2.5vw, 2rem) clamp(1rem, 2vw, 1.75rem);
    margin: 0;
  }

  .dato {
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
    padding-left: 0.85rem;
    /* Una barretta sottile a sinistra: separa le celle senza disegnare una
       tabella. È informazione — dice dove finisce un dato e comincia il
       successivo — non decorazione. */
    border-left: 1px solid color-mix(in oklab, var(--color-stone-500) 22%, transparent);
  }

  .dato__voce {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--color-stone-500);
  }

  .dato__valore {
    margin: 0;
    font-family: var(--font-display);
    font-size: clamp(1.1rem, 1.9vw, 1.4rem);
    line-height: 1.2;
    color: var(--color-stone-900);
    font-variant-numeric: tabular-nums;
  }

  .dati-sentiero__nota {
    margin-top: 1.15rem;
    max-width: 62ch;
    font-size: 0.78rem;
    line-height: 1.5;
    color: var(--color-stone-500);
  }

  /* --- La scheda della webcam ------------------------------------------
     Sta accanto al meteo, nella colonna delle condizioni. È un collegamento,
     non un'immagine: la webcam la mostra la fonte, che la tiene aggiornata.
  */
  .webcam {
    display: block;
    padding: 1.15rem 1.25rem 1.2rem;
    border: 1px solid color-mix(in oklab, var(--color-stone-500) 24%, transparent);
    border-radius: var(--raggio-media);
    background-color: var(--color-stone-50);
    transition:
      background-color 220ms ease-out,
      border-color 220ms ease-out;
  }

  .webcam:hover {
    background-color: var(--color-stone-100);
    border-color: color-mix(in oklab, var(--color-stone-500) 40%, transparent);
  }

  .webcam:focus-visible {
    outline: 2px solid var(--color-stone-700);
    outline-offset: 2px;
  }

  .webcam__voce {
    display: block;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--color-stone-500);
  }

  .webcam__nome {
    display: block;
    margin-top: 0.2rem;
    font-family: var(--font-display);
    font-size: 1.1rem;
    line-height: 1.25;
    color: var(--color-stone-900);
  }

  .webcam__nota {
    display: block;
    margin-top: 0.3rem;
    font-size: 0.78rem;
    line-height: 1.4;
    color: var(--color-stone-600);
  }
'''


def main() -> int:
    testo = PAGINA.read_text(encoding="utf-8")

    inizio = testo.find("  <!-- ==================================================================\n       Descrizione e dati tecnici")
    if inizio == -1:
        print("  blocco non trovato")
        return 1

    # Il blocco finisce con la chiusura di `</aside>`, `</div>`, `</section>`.
    ancora = "      </aside>\n    </div>\n  </section>\n"
    fine = testo.find(ancora, inizio)
    if fine == -1:
        print("  fine del blocco non trovata")
        return 1
    fine += len(ancora)

    vecchie = testo[inizio:fine].count("\n")
    testo = testo[:inizio] + NUOVO + testo[fine:]
    PAGINA.write_text(testo, encoding="utf-8", newline="")
    print(f"  pagina: {vecchie} righe sostituite da {NUOVO.count(chr(10))}")

    # --- Lo stile ---------------------------------------------------------
    css = CSS.read_text(encoding="utf-8")
    if ".dati-sentiero" in css:
        print("  CSS: stili gia' presenti")
    else:
        ancora_css = "  /* --- Tabella tariffe"
        i = css.find(ancora_css)
        if i == -1:
            print("  CSS: punto di inserimento non trovato")
            return 1
        css = css[:i] + NUOVO_CSS + "\n" + css[i:]
        CSS.write_text(css, encoding="utf-8", newline="")
        print("  CSS: fascia dei dati e scheda webcam aggiunte")

    # --- `.spec` non serve piu' a nessuno? --------------------------------
    rimasti = []
    for percorso in sorted(RADICE.glob("src/**/*.astro")):
        if 'class="spec' in percorso.read_text(encoding="utf-8") or "spec__" in percorso.read_text(encoding="utf-8"):
            rimasti.append(percorso.name)
    print(f"  uso residuo di .spec: {rimasti if rimasti else 'nessuno'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
