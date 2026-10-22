"""Allinea il controllo dei contrasti al nuovo colore delle etichette."""

from __future__ import annotations

import pathlib

FILE = (
    pathlib.Path(__file__).resolve().parent.parent
    / "scripts"
    / "verifica_contrasto_cieli.py"
)


def main() -> int:
    testo = FILE.read_text(encoding="utf-8")
    vecchio = 'SECONDARIO = "#3a3a35"'
    nuovo = 'SECONDARIO = "#32322d"'
    if nuovo in testo:
        print("  gia' aggiornato")
        return 0
    if vecchio not in testo:
        print("  costante non trovata")
        return 1
    FILE.write_text(testo.replace(vecchio, nuovo, 1), encoding="utf-8", newline="")
    print("  costante aggiornata a #32322d")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
