"""
Rimuove la vecchia regola `.tavolo` col fondo di legno.

Il difetto: nel foglio erano rimaste DUE regole `.tavolo`. La nuova imposta il
colore unico, la vecchia imposta anche un `background-image` con le venature
del legno. La nuova non dichiara `background-image`, quindi quella vecchia
continuava ad applicarsi: il fondo risultava del colore giusto ma con sopra le
righe del legno.

Non si vedeva leggendo il codice — si vedeva guardando la pagina.
"""

from __future__ import annotations

import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
CSS = RADICE / "src" / "styles" / "global.css"

# Inizio del commento della vecchia regola.
INIZIO = "  /*\n    ==========================================================================\n    LA FASCIA DEL TAVOLO"
# La vecchia regola finisce con la chiusura di `.tavolo { ... }`.
FINE = "    color: var(--color-wood-100);\n  }\n"


def main() -> int:
    testo = CSS.read_text(encoding="utf-8")

    i = testo.find(INIZIO)
    if i == -1:
        print("vecchia regola non trovata: forse è già stata tolta")
        return 0

    j = testo.find(FINE, i)
    if j == -1:
        print("fine della vecchia regola non trovata")
        return 1
    j += len(FINE)

    rimosse = testo[i:j].count("\n")
    CSS.write_text(testo[:i] + testo[j:], encoding="utf-8", newline="")
    print(f"vecchia regola rimossa: {rimosse} righe")

    # Controllo: quante regole `.tavolo` restano, e c'è ancora un background-image?
    dopo = CSS.read_text(encoding="utf-8")
    quante = dopo.count("\n  .tavolo {")
    print(f"  regole `.tavolo` rimaste: {quante}")
    if "repeating-linear-gradient" in dopo:
        print("  ATTENZIONE: c'è ancora un repeating-linear-gradient")
    return 0 if quante == 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
