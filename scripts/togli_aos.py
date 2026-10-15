"""
Toglie tutte le direttive di animazione al scroll (`data-aos`, `data-aos-delay`).

Il brief di progettazione vieta le comparse progressive diffuse: erano 30 su 8
pagine, con ritardi progressivi riga per riga. Qui si azzera tutto; le poche che
servono davvero vengono rimesse a mano, una per volta, dopo.

Gestisce le due forme possibili:
  - attributo sulla stessa riga dell'elemento:  <div class="..." data-aos="fade-up">
  - attributo su una riga propria:             \n        data-aos="fade-up"

Uso:  python scripts/togli_aos.py
"""

from __future__ import annotations

import pathlib
import re
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent

FILE = [
    "src/pages/index.astro",
    "src/pages/camere.astro",
    "src/pages/ristorante.astro",
    "src/pages/la-locanda.astro",
    "src/pages/gnocchi-con-la-fioreta.astro",
    "src/pages/privacy.astro",
    "src/pages/sentieri/index.astro",
    "src/components/Hero.astro",
]

# Riga che contiene soltanto una direttiva AOS (ed eventuale virgola finale)
SOLO_DIRETTIVA = re.compile(r'^\s*data-aos(-delay)?=(\{[^}]*\}|"[^"]*"),?\s*$')

# Direttiva inserita sulla stessa riga dell'elemento
IN_LINEA = re.compile(r'\s+data-aos(-delay)?=(\{[^}]*\}|"[^"]*")')


def main() -> int:
    totale = 0

    for percorso in FILE:
        p = RADICE / percorso
        if not p.exists():
            print(f"  MANCA: {percorso}")
            continue

        righe = p.read_text(encoding="utf-8").split("\n")
        fuori: list[str] = []
        rimossi = 0

        for riga in righe:
            if SOLO_DIRETTIVA.match(riga):
                rimossi += 1
                continue

            nuova, n = IN_LINEA.subn("", riga)
            if n:
                rimossi += n
                # Se la riga resta con solo spazi, si scarta
                if not nuova.strip():
                    continue
                riga = nuova

            fuori.append(riga)

        if rimossi:
            p.write_text("\n".join(fuori), encoding="utf-8", newline="")
            totale += rimossi
            print(f"  {percorso:44} {rimossi} rimosse")

    print()
    print(f"direttive rimosse in totale: {totale}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
