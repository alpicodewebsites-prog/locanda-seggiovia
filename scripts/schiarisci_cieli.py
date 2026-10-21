"""Schiarisce i due cieli che non reggevano i testi piccoli."""

from __future__ import annotations

import pathlib

COMPONENTE = (
    pathlib.Path(__file__).resolve().parent.parent
    / "src"
    / "components"
    / "MeteoSentiero.astro"
)

SOSTITUZIONI = [
    # --- Rovesci -----------------------------------------------------------
    # Si toglie la seconda striscia, che era SCURA (nero al 12%): abbassava la
    # luminosità del fondo proprio dove il testo piccolo doveva restare
    # leggibile. Le strisce chiare bastano a leggersi come pioggia.
    (
        """  .meteo[data-cielo='rovesci'] {
    background-color: #b3b9ba;
    background-image:
      repeating-linear-gradient(100deg, rgba(255, 255, 255, 0.46) 0 1px, transparent 1px 6px),
      repeating-linear-gradient(100deg, rgba(40, 50, 52, 0.12) 0 1px, transparent 1px 13px),
      linear-gradient(160deg, #ccd1d2, #b3b8b9);
  }""",
        """  .meteo[data-cielo='rovesci'] {
    background-color: #b9bfc0;
    background-image:
      repeating-linear-gradient(100deg, rgba(255, 255, 255, 0.5) 0 1px, transparent 1px 6px),
      linear-gradient(160deg, #cfd4d5, #a6acae);
  }""",
    ),
    # --- Temporale --------------------------------------------------------
    (
        """      linear-gradient(160deg, #bfc1ba, #a9aba4);""",
        """      linear-gradient(160deg, #c4c6bf, #aaaca5);""",
    ),
]


def main() -> int:
    testo = COMPONENTE.read_text(encoding="utf-8")
    fatte = 0
    for vecchio, nuovo in SOSTITUZIONI:
        if vecchio in testo:
            testo = testo.replace(vecchio, nuovo, 1)
            fatte += 1
        else:
            print(f"  NON TROVATO: {vecchio.strip().splitlines()[0][:60]}")
    COMPONENTE.write_text(testo, encoding="utf-8", newline="")
    print(f"  sostituzioni: {fatte}/{len(SOSTITUZIONI)}")
    return 0 if fatte == len(SOSTITUZIONI) else 1


if __name__ == "__main__":
    raise SystemExit(main())
