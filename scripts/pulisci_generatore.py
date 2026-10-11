"""
Toglie dal generatore di segnaposto le voci non più utilizzate.

Il generatore serve a creare immagini provvisorie quando una fotografia reale
non c'è ancora. Dopo il passaggio delle foto alla gestione dal pannello, alcune
voci producevano file che nessuna pagina usava: restavano nel repository e
confondevano la libreria del pannello.

Questo script rimuove dal file le voci indicate, insieme al commento che le
precede quando appartiene solo a loro.

Uso:  python scripts/pulisci_generatore.py
"""

from __future__ import annotations

import pathlib
import re
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
GENERATORE = RADICE / "scripts" / "generate_placeholders.py"

# Voci non più prodotte: le immagini corrispondenti sono state eliminate perché
# nessuna pagina le referenzia.
DA_RIMUOVERE = [
    "locanda-facciata",
    "sentieri-pasubio",
    "sentieri-piccole-dolomiti",
    "territorio-malghe",
    "locanda-ambienti",
    "camere-interno",
    "ristorante-sala",
    "gnocchi-fioreta",
]


def main() -> int:
    if not GENERATORE.is_file():
        print("generatore non trovato")
        return 1

    righe = GENERATORE.read_text(encoding="utf-8").split("\n")
    fuori: list[str] = []
    i = 0
    rimosse: list[str] = []

    while i < len(righe):
        riga = righe[i]

        # Due formati possibili:
        #   ("nome", ...          → voce su una riga sola
        #   (                     → voce su più righe, nome sulla successiva
        #       "nome", ...
        m = re.match(r'^\s*\("([a-z0-9-]+)"', riga)
        nome_trovato = m.group(1) if m else None
        salto_iniziale = 1

        if not nome_trovato and riga.strip() == "(" and i + 1 < len(righe):
            m2 = re.match(r'^\s*"([a-z0-9-]+)"', righe[i + 1])
            if m2:
                nome_trovato = m2.group(1)
                salto_iniziale = 2

        if nome_trovato and nome_trovato in DA_RIMUOVERE:
            nome = nome_trovato

            # Toglie il commento immediatamente sopra, se c'è
            while fuori and fuori[-1].strip().startswith("#"):
                fuori.pop()
            while fuori and not fuori[-1].strip():
                fuori.pop()

            # Salta la voce fino alla riga che la chiude con "),"
            i += salto_iniziale
            while i < len(righe):
                if righe[i].rstrip().endswith("),"):
                    i += 1
                    break
                i += 1

            rimosse.append(nome)
            continue

        fuori.append(riga)
        i += 1

    if not rimosse:
        print("nessuna voce da rimuovere")
        return 0

    GENERATORE.write_text("\n".join(fuori), encoding="utf-8", newline="")
    print(f"voci rimosse dal generatore: {len(rimosse)}")
    for nome in rimosse:
        print(f"  {nome}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
