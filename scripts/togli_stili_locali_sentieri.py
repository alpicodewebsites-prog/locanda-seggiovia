"""
Toglie dalla home gli stili delle schede dei sentieri, ora in global.css.

Erano stati scritti come stili locali della pagina. Spostandoli nel foglio
condiviso — perché servono anche alla pagina Sentieri — la copia locale diventa
un doppione: due definizioni della stessa cosa che, prima o poi, divergono.

Uso:  python scripts/togli_stili_locali_sentieri.py
"""

from __future__ import annotations

import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
PAGINA = RADICE / "src" / "pages" / "index.astro"

INIZIO = "  /*\n    Schede dei sentieri."
FINE = "  /*\n    Schede dei piatti"


def main() -> int:
    testo = PAGINA.read_text(encoding="utf-8")

    i = testo.find(INIZIO)
    if i == -1:
        print("blocco non trovato: niente da fare")
        return 0

    j = testo.find(FINE, i)
    if j == -1:
        print("confine finale non trovato: interrotto per sicurezza")
        return 1

    rimosse = testo[i:j].count("\n")
    PAGINA.write_text(testo[:i] + testo[j:], encoding="utf-8", newline="")
    print(f"rimosse {rimosse} righe di stili locali duplicati")
    print("gli stili restano in src/styles/global.css")
    return 0


if __name__ == "__main__":
    sys.exit(main())
