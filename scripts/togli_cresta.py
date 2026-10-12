"""
Rimuove dalle pagine l'elemento decorativo «Cresta» (il profilo di montagna).

Ogni uso è racchiuso in un blocco con un commento e un contenitore che gli dà
spazio verticale. Si toglie il blocco intero, non solo il disegno: altrimenti
resterebbe una fascia vuota dove prima c'era la linea.

Uso:  python scripts/togli_cresta.py
"""

from __future__ import annotations

import pathlib
import re
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent

PAGINE = [
    "src/pages/index.astro",
    "src/pages/camere.astro",
    "src/pages/la-locanda.astro",
    "src/pages/ristorante.astro",
]

# Blocco completo: commento facoltativo, contenitore, componente, chiusura.
BLOCCO = re.compile(
    r"\n[ \t]*<!--[^\n]*[Pp]ausa[^\n]*-->\n"  # il commento che lo introduce
    r"[ \t]*<div class=\"shell[^\"]*\">\n"  # il contenitore con lo spazio verticale
    r"[ \t]*<Cresta[^>]*/>\n"  # il disegno
    r"[ \t]*</div>\n",
)

# Variante senza commento, nel caso il blocco sia scritto diversamente.
BLOCCO_SENZA_COMMENTO = re.compile(
    r"\n[ \t]*<div class=\"shell[^\"]*\">\n[ \t]*<Cresta[^>]*/>\n[ \t]*</div>\n",
)

IMPORT = re.compile(r"^[ \t]*import Cresta from '[^']*';\n", re.MULTILINE)


def main() -> int:
    totale_blocchi = 0
    totale_import = 0
    problemi = 0

    for percorso in PAGINE:
        p = RADICE / percorso
        if not p.exists():
            print(f"  MANCA: {percorso}")
            problemi += 1
            continue

        testo = p.read_text(encoding="utf-8")
        prima = testo

        testo, n1 = BLOCCO.subn("\n", testo)
        testo, n2 = BLOCCO_SENZA_COMMENTO.subn("\n", testo)
        testo, n3 = IMPORT.subn("", testo)

        blocchi = n1 + n2
        totale_blocchi += blocchi
        totale_import += n3

        if testo == prima:
            print(f"  {p.name}: nessuna modifica")
            continue

        p.write_text(testo, encoding="utf-8", newline="")
        print(f"  {p.name}: {blocchi} blocchi rimossi, {n3} import rimosso")

        # Controllo: non deve restare nessun riferimento
        residuo = re.findall(r"Cresta", testo)
        if residuo:
            print(f"      ATTENZIONE: restano {len(residuo)} riferimenti a Cresta")
            problemi += 1

    print()
    print(f"blocchi rimossi: {totale_blocchi}")
    print(f"import rimossi: {totale_import}")
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
