"""Fascia gnocchi: sfondo fotografico a copertura totale, più bassa."""

from __future__ import annotations

import pathlib
import re

RADICE = pathlib.Path(__file__).resolve().parent.parent
PAGINA = RADICE / "src" / "pages" / "index.astro"
CSS = RADICE / "src" / "styles" / "global.css"

NUOVA_SEZIONE = '''  <!-- ==================================================================
       La fascia degli gnocchi
       ------------------------------------------------------------------
       Una fotografia degli gnocchi copre tutto il rettangolo, e sopra ci sta
       il pulsante. Niente testo, niente elenco: la fascia è materia e basta.

       LA FOTOGRAFIA È QUELLA DELLA LOCANDA
       È un ritaglio del piatto vero (`gnocchi/02-piatto-finito.jpg`), non
       un'immagine presa da internet: il piatto è un prodotto De.Co., e
       mostrarne un altro al suo posto sarebbe dire una cosa falsa. In più una
       foto trovata in rete non ha una licenza libera per un sito commerciale.

       IL VELO
       Sta fra la fotografia e il pulsante. Serve perché la fotografia ha zone
       chiare (il piatto) e zone scure: senza velo il contrasto del pulsante
       cambierebbe da punto a punto e non sarebbe verificabile.

       L'immagine è decorativa (`alt` vuoto): la sezione ha un nome, e il
       pulsante dice già dove porta.
       ================================================================== -->
  <section class="tavolo" aria-label="Gli gnocchi con la Fioreta">
    <Image
      src={sfondoGnocchi}
      alt=""
      widths={[640, 960, 1280, 1800]}
      sizes="100vw"
      format="webp"
      quality={76}
      loading="lazy"
      decoding="async"
      class="tavolo__sfondo"
    />
    <div class="tavolo__velo" aria-hidden="true"></div>

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

    Una fotografia a copertura totale, bassa, con il pulsante sopra.

    L'altezza è volutamente contenuta: è una fascia di passaggio fra l'apertura
    e il resto della pagina, non una sezione da leggere. Prima era alta 448 px
    e sembrava una sala d'attesa.

    `min-height` e non `height`: se un giorno il testo del pulsante va su due
    righe, la fascia cresce invece di tagliarlo.
  */
  .tavolo {
    position: relative;
    isolation: isolate;
    display: grid;
    place-items: center;
    min-height: clamp(11rem, 22vw, 16rem);
    padding-block: clamp(2rem, 4vw, 3rem);
    overflow: hidden;
    background-color: var(--color-wood-900);
  }

  .tavolo__sfondo {
    position: absolute;
    inset: 0;
    z-index: -2;
    width: 100%;
    height: 100%;
    object-fit: cover;
    /* La fotografia è ritagliata sugli gnocchi: il centro è il punto giusto. */
    object-position: center;
  }

  /*
    Il velo. Non è nero pieno: lascia vedere gli gnocchi e abbassa insieme la
    luminosità, così il pulsante ocra resta leggibile su tutta la fascia.
  */
  .tavolo__velo {
    position: absolute;
    inset: 0;
    z-index: -1;
    background-color: color-mix(in srgb, var(--color-wood-900) 62%, transparent);
    background-image: linear-gradient(
      to bottom,
      color-mix(in srgb, var(--color-wood-900) 40%, transparent),
      color-mix(in srgb, var(--color-wood-900) 70%, transparent)
    );
  }

  .tavolo__sopra {
    display: flex;
    justify-content: center;
  }

  /* Il contorno del focus deve vedersi anche sopra la fotografia. */
  .tavolo :global(a:focus-visible) {
    outline: 3px solid var(--color-wood-100);
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

    # La lista dei tre dettagli non serve più: al suo posto lo sfondo.
    blocco = re.search(r"/\*\*\n \* I tre dettagli fotografici.*?\n\];\n\n", testo, re.S)
    if blocco:
        testo = testo.replace(blocco.group(0), "")

    if "const sfondoGnocchi" not in testo:
        ancora = "/**\n * Home — pagina di apertura."
        nuovo = (
            "/**\n"
            " * La fotografia che fa da sfondo alla fascia degli gnocchi.\n"
            " *\n"
            " * È un ritaglio del piatto vero, preparato da\n"
            " * `python scripts/prepara_sfondo_gnocchi.py`.\n"
            " */\n"
            "const sfondoGnocchi = (await import('../assets/gnocchi/sfondo-gnocchi.jpg')).default;\n\n"
        )
        testo = testo.replace(ancora, nuovo + ancora, 1)

    PAGINA.write_text(testo, encoding="utf-8", newline="")
    print("sezione sostituita")

    # --- 2. Lo stile -------------------------------------------------------
    css = CSS.read_text(encoding="utf-8")
    inizio_css = css.find("  /*\n    I tre dettagli fotografici")
    if inizio_css == -1:
        print("blocco CSS non trovato")
        return 1
    fine_css = css.find("  .btn--ghost", inizio_css)
    if fine_css == -1:
        fine_css = len(css)

    css = css[:inizio_css] + NUOVO_CSS + "\n" + css[fine_css:]
    CSS.write_text(css, encoding="utf-8", newline="")
    print("stile sostituito")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
