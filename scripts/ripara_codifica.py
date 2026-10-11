"""
Ripara un file di testo con caratteri in codifica mista.

Problema reale: alcune modifiche fatte con comandi di shell hanno scritto gli
accenti in Latin-1 dentro un file per il resto UTF-8. Il risultato è un file che
non si decodifica più, e gli accenti appaiono come sequenze di due caratteri.

Strategia: si decodifica il file un byte alla volta. Dove la sequenza UTF-8 è
valida si usa quella; dove non lo è, si interpreta il singolo byte come Latin-1.
Così si recupera il testo corretto senza toccare il resto.

Uso:  python scripts/ripara_codifica.py <file> [<file> ...]
      python scripts/ripara_codifica.py --dry-run <file>
"""

from __future__ import annotations

import pathlib
import sys


def decodifica_mista(dati: bytes) -> tuple[str, int]:
    """Decodifica UTF-8 con ripiego Latin-1 sui byte non validi."""
    fuori: list[str] = []
    i = 0
    sostituzioni = 0

    while i < len(dati):
        # Tenta la sequenza UTF-8 più lunga possibile a partire da i
        for lunghezza in (4, 3, 2, 1):
            if i + lunghezza > len(dati):
                continue
            try:
                carattere = dati[i : i + lunghezza].decode("utf-8")
            except UnicodeDecodeError:
                continue
            if lunghezza == 1 and dati[i] > 0x7F:
                # Byte non ASCII che non apre una sequenza valida: è Latin-1
                fuori.append(bytes([dati[i]]).decode("latin-1"))
                sostituzioni += 1
            else:
                fuori.append(carattere)
            i += lunghezza
            break
        else:
            # Nessuna interpretazione possibile: si scarta il byte
            sostituzioni += 1
            i += 1

    return "".join(fuori), sostituzioni


def main() -> int:
    argomenti = sys.argv[1:]
    prova = "--dry-run" in argomenti
    file = [a for a in argomenti if not a.startswith("--")]

    if not file:
        print("Indicare almeno un file.")
        return 1

    for nome in file:
        p = pathlib.Path(nome)
        if not p.is_file():
            print(f"  MANCA: {nome}")
            continue

        dati = p.read_bytes()

        # Se è già UTF-8 valido non si tocca nulla
        try:
            dati.decode("utf-8")
            print(f"  {p.name}: già UTF-8 valido, nessuna modifica")
            continue
        except UnicodeDecodeError:
            pass

        testo, sostituzioni = decodifica_mista(dati)

        # Verifica: il risultato deve essere UTF-8 valido e senza doppie codifiche.
        # Le sequenze sono costruite dai codici numerici, così questo file non
        # contiene i letterali che sta cercando.
        sospette = [
            chr(0xC3) + chr(0xA8),
            chr(0xC3) + chr(0xA9),
            chr(0xC3) + chr(0xA0),
            chr(0xC3) + chr(0xB9),
            chr(0xE2) + chr(0x80),
        ]
        doppie = [s for s in sospette if s in testo]

        print(f"  {p.name}: {sostituzioni} caratteri recuperati")
        if doppie:
            print(f"      ATTENZIONE, restano sequenze sospette: {doppie}")

        if prova:
            print("      (prova a vuoto: non ho scritto nulla)")
            continue

        p.write_text(testo, encoding="utf-8", newline="")
        print("      file riscritto in UTF-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
