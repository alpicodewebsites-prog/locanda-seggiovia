"""Toglie la fotografia di sfondo dalla fascia degli gnocchi."""

from __future__ import annotations

import pathlib
import re

RADICE = pathlib.Path(__file__).resolve().parent.parent
PAGINA = RADICE / "src" / "pages" / "index.astro"
CSS = RADICE / "src" / "styles" / "global.css"
IMMAGINE = RADICE / "src" / "assets" / "gnocchi" / "sfondo-gnocchi.jpg"

NUOVA_SEZIONE = '''  <!-- ==================================================================
       La fascia degli gnocchi
       ------------------------------------------------------------------
       Un fondo scuro fra il nero e il grigio, e sopra il pulsante. Niente
       fotografia, niente testo, niente elenco.

       Il fondo è fatto con un gradiente invece che con un'immagine: pesa zero
       byte, non ha una risoluzione da cui dipendere, e il contrasto del
       pulsante è lo stesso su tutta la fascia — cosa che con una fotografia
       non sarebbe garantita, perché una foto ha zone chiare e zone scure.

       La sfumatura è diagonale perché un fondo piatto sembra un rettangolo
       vuoto; così invece ha una direzione di luce.
       ================================================================== -->
  <section class="tavolo" aria-label="Gli gnocchi con la Fioreta">
    <div class="shell tavolo__sopra">
      <a href="/gnocchi-con-la-fioreta" class="pulsante-gnocchi">
        {testi.pulsanteGnocchi}
        <span class="pulsante-gnocchi__freccia" aria-hidden="true">→</span>
      </a>
    </div>
  </section>
'''

NUOVO_CSS = '''  /*
    ==========================================================================
    LA FASCIA DEGLI GNOCCHI
    ==========================================================================

    Fondo scuro fra il nero e il grigio, con il pulsante sopra.

    È un gradiente, non un'immagine: costa zero byte e non dipende da una
    risoluzione. Il contrasto del pulsante è identico su tutta la fascia,
    mentre con una fotografia cambierebbe da punto a punto.

    `min-height` e non `height`: se il testo del pulsante va su due righe, la
    fascia cresce invece di tagliarlo.
  */
  .tavolo {
    position: relative;
    isolation: isolate;
    display: grid;
    place-items: center;
    min-height: clamp(10rem, 20vw, 14rem);
    padding-block: clamp(2rem, 4vw, 3rem);
    overflow: hidden;
    /* Dal nero al grigio, in diagonale: un fondo piatto sembrerebbe un
       rettangolo vuoto. */
    background-color: var(--color-stone-900);
    background-image: linear-gradient(
      118deg,
      var(--color-stone-900) 0%,
      var(--color-stone-800) 46%,
      var(--color-stone-700) 100%
    );
  }

  .tavolo__sopra {
    display: flex;
    justify-content: center;
  }

  /* Il contorno del focus deve vedersi sul fondo scuro. */
  .tavolo :global(a:focus-visible) {
    outline: 3px solid var(--color-stone-50);
    outline-offset: 3px;
  }
'''


def main() -> int:
    # --- 1. La sezione -----------------------------------------------------
    testo = PAGINA.read_text(encoding="utf-8")
    inizio = testo.find("  <!-- ==================================================================\n       La fascia degli gnocchi")
    if inizio == -1:
        print("sezione non trovata")
        return 1
    fine = testo.find("  </section>", inizio) + len("  </section>\n")
    testo = testo[:inizio] + NUOVA_SEZIONE + testo[fine:]

    # La variabile dell'immagine non serve più.
    blocco = re.search(r"/\*\*\n \* La fotografia che fa da sfondo.*?\n\n", testo, re.S)
    if blocco:
        testo = testo.replace(blocco.group(0), "")
        print("  rimosso il riferimento all'immagine")
    if "sfondoGnocchi" in testo:
        print("  ATTENZIONE: sfondoGnocchi ancora citato")
    PAGINA.write_text(testo, encoding="utf-8", newline="")
    print("sezione sostituita")

    # --- 2. Lo stile -------------------------------------------------------
    css = CSS.read_text(encoding="utf-8")
    inizio_css = css.find("  /*\n    ==========================================================================\n    LA FASCIA DEGLI GNOCCHI")
    if inizio_css == -1:
        print("blocco CSS non trovato")
        return 1
    fine_css = css.find("  .btn--ghost", inizio_css)
    if fine_css == -1:
        fine_css = len(css)
    css = css[:inizio_css] + NUOVO_CSS + "\n" + css[fine_css:]
    CSS.write_text(css, encoding="utf-8", newline="")
    print("stile sostituito")

    # --- 3. L'immagine non serve più --------------------------------------
    if IMMAGINE.is_file():
        IMMAGINE.unlink()
        print("  immagine di sfondo rimossa dal progetto")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
