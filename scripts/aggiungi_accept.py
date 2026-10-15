"""
Aggiunge il filtro sui formati a ogni campo immagine di config.yml.

`accept` è un'opzione reale e documentata del campo Image/File: limita i tipi di
file che si possono caricare, e il pannello filtra anche la finestra di scelta
del file. Senza, si potrebbe caricare per errore un PSD o un TIFF.

(Sveltia esclude già BMP, TIFF, PSD e simili dai campi immagine; `accept` rende
la restrizione esplicita e leggibile nella configurazione, e impedisce anche i
formati che Sveltia accetterebbe ma Astro non sa ottimizzare bene.)

Uso:  python scripts/aggiungi_accept.py
"""

from __future__ import annotations

import pathlib
import re
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
CONFIG = RADICE / "public" / "admin" / "config.yml"

# Formati che Astro sa ottimizzare e che i browser mostrano ovunque.
FORMATI = "image/jpeg,image/png,image/webp,image/avif"

WIDGET = re.compile(r"^(\s*)widget: image\s*$")


def main() -> int:
    righe = CONFIG.read_text(encoding="utf-8").split("\n")
    fuori: list[str] = []
    aggiunti = 0
    gia_presenti = 0

    for i, riga in enumerate(righe):
        fuori.append(riga)

        m = WIDGET.match(riga)
        if not m:
            continue

        indent = m.group(1)

        # Se il campo successivo ha già `accept`, non si tocca
        if i + 1 < len(righe) and re.match(r"^\s*accept:", righe[i + 1]):
            gia_presenti += 1
            continue

        fuori.append(f"{indent}accept: {FORMATI}")
        aggiunti += 1

    if aggiunti:
        CONFIG.write_text("\n".join(fuori), encoding="utf-8", newline="")

    print(f"campi immagine trovati : {aggiunti + gia_presenti}")
    print(f"accept aggiunto        : {aggiunti}")
    print(f"gia presenti           : {gia_presenti}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
