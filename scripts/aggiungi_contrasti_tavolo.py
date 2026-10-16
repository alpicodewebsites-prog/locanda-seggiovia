"""Aggiunge al controllo dei contrasti le coppie della fascia «tavolo»."""

from __future__ import annotations

import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
FILE = RADICE / "scripts" / "verifica_contrasti.py"

ANCORA = "    # Il contorno del focus deve vedersi"

NUOVE = """    # --- Fascia del tavolo (fondo legno scuro) ----------------------------
    ("wood-100", "wood-700", SOGLIA_NORMALE, "testo chiaro sul legno scuro"),
    ("wood-300", "wood-700", SOGLIA_NORMALE, "etichetta piccola sul legno scuro"),
    ("stone-50", "wood-700", SOGLIA_NORMALE, "titolo sul legno scuro"),
    ("wood-900", "wood-100", SOGLIA_NORMALE, "testo scuro sulla tessera chiara"),
    ("wood-500", "wood-100", SOGLIA_NORMALE, "quantita' sulla tessera chiara"),

"""


def main() -> int:
    testo = FILE.read_text(encoding="utf-8")

    if "wood-700" in testo:
        print("coppie già presenti")
        return 0

    if ANCORA not in testo:
        print("punto di inserimento non trovato")
        return 1

    FILE.write_text(testo.replace(ANCORA, NUOVE + ANCORA, 1), encoding="utf-8", newline="")
    print("coppie della fascia tavolo aggiunte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
