"""
Le due schede camera inglesi.

Tariffe, ordine e servizi restano identici: i prezzi sono dati, non testo, e non
si traducono (né si arrotondano). Cambiano solo nome, descrizione, occupanti e i
nomi dei servizi, che sono parole.

Uso:  python scripts/traduce_camere.py
"""

from __future__ import annotations

import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
CARTELLA = RADICE / "src" / "content" / "camere"

SINGOLA = """---
titolo: Single room
ordine: 1
descrizione: >-
  A single room with private bathroom, furnished in wood and stone. The answer
  for anyone coming up alone, for one trail or for a few quiet days.
occupanti: 1 person
tariffe:
  bnb: 60
  mezzaPensione: 80
  pensioneCompleta: 88
servizi:
  - TV
  - Safe
  - Toiletries
---

Rates per person, per day.
"""

DOPPIA = """---
titolo: Double room
ordine: 2
descrizione: >-
  A double room with private bathroom. Two people, the same stone roof and the
  same view of the Piccole Dolomiti.
occupanti: 2 people
tariffe:
  bnb: 55
  mezzaPensione: 78
  pensioneCompleta: 84
servizi:
  - TV
  - Safe
  - Toiletries
---

Rates per person, per day.
"""


def main() -> int:
    for nome, contenuto in [("singola-en.md", SINGOLA), ("doppia-en.md", DOPPIA)]:
        (CARTELLA / nome).write_text(contenuto, encoding="utf-8", newline="")
        print(f"  {nome}")
    print("  schede scritte: 2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
