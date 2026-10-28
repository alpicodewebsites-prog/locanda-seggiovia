"""
Le tre schede sentiero inglesi che mancavano.

Nome, numeri di segnavia, quote e coordinate restano identici: sono dati, e un
nome di sentiero è quello scritto sui cartelli. Cambiano solo le parti in lingua:
sommario, descrizione, partenza, durata, e i numeri con la virgola decimale, che
in inglese si scrivono col punto.

Uso:  python scripts/traduce_tre_sentieri.py
"""

from __future__ import annotations

import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
CARTELLA = RADICE / "src" / "content" / "sentieri"

PONTE = """---
nome: Ponte Tibetano AVIS
ordine: 3
sommario: >-
  A 105-metre suspension footbridge 30 metres above the ground, on steel
  cables, bypassing a landslide on the Strada del Re.
descrizione: >-
  The bridge hangs 30 metres up and is 105 metres long, on steel cables, and
  serves to bypass a landslide on the Strada del Re. It is dedicated to the
  memory of the 1956 tragedy. It lies on the Anello del Sengio Alto, about 40
  minutes from the Pasubio Ossuary. It cannot be crossed in snow or strong
  wind.
difficolta: E
partenza: Pian delle Fugazze / Alpe di Campogrosso
distanza: 13.2 km
dislivello: 552 m
durata: 4 h 20 min
quota: 1545
meteoLatitudine: 45.759609
meteoLongitudine: 11.173866
meteoLocalita: Pian delle Fugazze
segnavia: C12
immagine: /assets/sentieri/04-ponte-tibetano.jpg
---
"""

MOLE = """---
nome: Sentiero delle Mole (CAI 151/144)
ordine: 5
sommario: >-
  A link to the Alpe di Campogrosso from Rifugio La Guardia, passing an old
  quarry where millstones were cut.
descrizione: >-
  The path connects Rifugio La Guardia to the Alpe di Campogrosso, passing an
  old quarry where stone millstones were cut. In spring it is known for its
  wildflowers. The ground is easy and the route short: the right itinerary for
  half a day without effort.
difficolta: T
distanza: about 3.5 km
dislivello: 400 m
durata: 3 h 30 min
partenza: Rifugio La Guardia
segnavia: CAI 151/144
meteoLatitudine: 45.759609
meteoLongitudine: 11.173866
meteoLocalita: Passo Pian delle Fugazze
immagine: /assets/sentieri/02-sentiero-mole.jpg
---
"""

GALLERIE = """---
nome: Strada delle 52 Gallerie
ordine: 4
sommario: >-
  A mule track cut into the limestone to reach Rifugio Papa: 2.2 of the 6.6
  kilometres run through tunnels.
descrizione: >-
  A masterpiece of military engineering: a mule track cut into the limestone to
  reach Rifugio Papa. Of the 6.6 kilometres in all, 2.2 run through tunnels, in
  the dark. A torch is not a recommended accessory: it is necessary.
difficolta: EE
distanza: 6.6 km
dislivello: 948 m
partenza: Bocchetta Campiglia
durata: 3 h 50 min
segnavia: CAI 366
quota: 2006
meteoLatitudine: 45.778657
meteoLongitudine: 11.227940
meteoLocalita: Bocchetta Campiglia
immagine: /assets/sentieri/06-strada-52-gallerie.jpg
---
"""

SCHEDE = {
    "ponte-tibetano-en.md": PONTE,
    "sentiero-mole-en.md": MOLE,
    "strada-52-gallerie-en.md": GALLERIE,
}


def main() -> int:
    for nome, contenuto in SCHEDE.items():
        (CARTELLA / nome).write_text(contenuto, encoding="utf-8", newline="")
        print(f"  {nome}")
    print(f"  schede scritte: {len(SCHEDE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
