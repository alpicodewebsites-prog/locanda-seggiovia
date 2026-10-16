"""Sostituisce lo stile della fascia: da tessere con testo a sole immagini."""

from __future__ import annotations

import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
CSS = RADICE / "src" / "styles" / "global.css"

INIZIO = "  /*\n    ATTENZIONE alla specificità"

NUOVO = '''  /*
    I tre dettagli fotografici, posati sul legno.

    Sono decorativi e non invasivi: piccoli, distanziati, senza cornice e senza
    testo sotto. Fanno da materia alla fascia, non da contenuto da leggere.

    Il formato è quadrato e uguale per tutti e tre — `aspect-ratio` più
    `object-fit: cover` — così la fila resta ordinata qualunque cosa contengano
    le fotografie.
  */
  .tavolo__dettagli {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: clamp(0.75rem, 2.5vw, 1.75rem);
    margin: 0;
    padding: 0;
    list-style: none;
  }

  .dettaglio {
    aspect-ratio: 1 / 1;
    width: clamp(5.5rem, 14vw, 9rem);
    overflow: hidden;
    /* Angoli appena arrotondati: le fotografie sembrano appoggiate, non
       incorniciate. */
    border-radius: 0.4rem;
    /* Un'ombra bassa: le immagini prendono posto sul tavolo invece di
       galleggiarci sopra. */
    box-shadow: 0 12px 26px -16px color-mix(in srgb, var(--color-wood-900) 85%, transparent);
  }

  .dettaglio :global(img) {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .tavolo__invito {
    display: flex;
    justify-content: center;
    margin-top: clamp(2rem, 5vw, 3rem);
  }

  /* Il contorno del focus deve vedersi anche sul legno scuro. */
  .tavolo :global(a:focus-visible) {
    outline: 3px solid var(--color-wood-100);
    outline-offset: 3px;
  }
'''


def main() -> int:
    testo = CSS.read_text(encoding="utf-8")

    inizio = testo.find(INIZIO)
    if inizio == -1:
        print("blocco non trovato")
        return 1

    # Il blocco finisce prima della regola del pulsante o della successiva.
    fine = testo.find("  .btn--ghost", inizio)
    if fine == -1:
        fine = len(testo)

    rimosse = testo[inizio:fine].count("\n")
    CSS.write_text(testo[:inizio] + NUOVO + "\n" + testo[fine:], encoding="utf-8", newline="")
    print(f"blocco sostituito: {rimosse} righe rimosse, {NUOVO.count(chr(10))} aggiunte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
