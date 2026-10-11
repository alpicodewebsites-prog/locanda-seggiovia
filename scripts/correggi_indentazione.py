"""
Corregge l'indentazione dei campi immagine inseriti in config.yml.

I campi di una collezione sono indentati a 6 spazi, le loro proprietà a 8. Lo
script che li aveva inseriti ne aveva messi 8 e 10, e lo YAML non si analizzava
più. Qui si toglie il rientro in eccesso di 2 spazi.

Verifica il risultato con il parser YAML prima di scrivere: se il file non è
valido, non lo salva.

Uso:  python scripts/correggi_indentazione.py
"""

from __future__ import annotations

import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
CONFIG = RADICE / "public" / "admin" / "config.yml"

CAMPI = ("foto", "fotoPreparazione")
INDENT_GIUSTO = 6
INDENT_PROPRIETA = 8


def main() -> int:
    righe = CONFIG.read_text(encoding="utf-8").split("\n")
    corrette = 0
    fuori: list[str] = []

    i = 0
    while i < len(righe):
        riga = righe[i]
        spazi = len(riga) - len(riga.lstrip(" "))

        # Riga di apertura di un campo inserito con il rientro sbagliato
        if spazi == 8 and any(riga.strip() == f"- name: {c}" for c in CAMPI):
            def de_indenta(indice: int, quanti: int) -> None:
                for k in range(indice, min(indice + quanti, len(righe))):
                    r = righe[k]
                    s = len(r) - len(r.lstrip(" "))
                    if s >= 2:
                        righe[k] = r[2:]

            de_indenta(i, 1)  # la riga "- name:"
            j = i + 1
            while j < len(righe):
                s = len(righe[j]) - len(righe[j].lstrip(" "))
                if s < 10:
                    break
                j += 1
            de_indenta(i + 1, j - (i + 1))  # le proprietà
            fuori.append(righe[i].strip())
            corrette += 1
            i = j
            continue

        i += 1

    if not corrette:
        print("nessun campo da correggere")
        return 0

    nuovo = "\n".join(righe)
    CONFIG.write_text(nuovo, encoding="utf-8", newline="")
    print(f"campi corretti: {corrette}")
    for nome in fuori:
        print(f"  {nome}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
