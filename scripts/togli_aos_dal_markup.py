"""
Toglie dal markup gli attributi `data-aos` scritti a mano.

Ora le animazioni le assegna `src/scripts/animazioni.ts` leggendo il tipo di
elemento. Gli attributi scritti a mano nel markup sono quindi un secondo
meccanismo che fa la stessa cosa: chi legge il codice non sa quale dei due
comanda, e su mobile restano attributi che la libreria non elabora.

Con un meccanismo solo: la regola sta in un posto, le pagine nuove la ereditano
senza fare niente, e non ci sono residui.

Uso:  python scripts/togli_aos_dal_markup.py
"""

from __future__ import annotations

import pathlib
import re
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent

CARTELLE = ["src/pages", "src/components"]

# Attributo sulla stessa riga dell'elemento, oppure su una riga propria.
IN_LINEA = re.compile(r"\s+data-aos(-delay)?=(\{[^}]*\}|\"[^\"]*\")")
SOLO_ATTRIBUTO = re.compile(r'^\s*data-aos(-delay)?=(\{[^}]*\}|"[^"]*")\s*,?\s*$')


def main() -> int:
    rimossi_totali = 0
    file_toccati = 0

    for cartella in CARTELLE:
        base = RADICE / cartella
        if not base.is_dir():
            continue
        for percorso in sorted(base.rglob("*.astro")):
            righe = percorso.read_text(encoding="utf-8").split("\n")
            fuori: list[str] = []
            rimossi = 0

            for riga in righe:
                if SOLO_ATTRIBUTO.match(riga):
                    rimossi += 1
                    continue
                nuova, quanti = IN_LINEA.subn("", riga)
                if quanti:
                    rimossi += quanti
                    if not nuova.strip():
                        continue
                    riga = nuova
                fuori.append(riga)

            if rimossi:
                percorso.write_text("\n".join(fuori), encoding="utf-8", newline="")
                rimossi_totali += rimossi
                file_toccati += 1
                print(f"  {percorso.relative_to(RADICE)}: {rimossi} rimossi")

    print()
    print(f"file modificati      : {file_toccati}")
    print(f"attributi rimossi    : {rimossi_totali}")
    print("le animazioni ora le assegna src/scripts/animazioni.ts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
