"""
Ricava tre dettagli uniformi dalla fotografia vera degli ingredienti.

PERCHÉ RITAGLI
La fotografia del tavolo è una sola, ed è piccola (300x367). Per la fascia
della home servono più immagini, tutte dello stesso formato, che mostrino gli
ingredienti da vicino: il dettaglio si legge meglio del piano largo, e il
ritaglio quadrato le rende uniformi come chiesto.

Sono RITAGLI DI UNA FOTOGRAFIA VERA, non immagini d'archivio: il tavolo, le
scodelle e gli ingredienti sono quelli della locanda.

Uso:  python scripts/ritaglia_ingredienti.py
"""

from __future__ import annotations

import pathlib
import sys

from PIL import Image

RADICE = pathlib.Path(__file__).resolve().parent.parent
SORGENTE = RADICE / "src" / "assets" / "gnocchi" / "01-ingredienti.jpg"
USCITA = RADICE / "src" / "assets" / "gnocchi" / "dettagli"

# Lato del ritaglio in pixel di partenza. La fotografia è 300x367: ritagli da
# 108 px lasciano un margine di ingrandimento contenuto quando si mostrano a
# 130-150 px nella pagina, e a quella misura restano nitidi.
LATO = 108

# (nome, sinistra, alto) — l'angolo in alto a sinistra di ogni riquadro.
# Le posizioni sono state scelte guardando la fotografia: ognuna inquadra un
# ingrediente diverso.
DETTAGLI: list[tuple[str, int, int]] = [
    # La scodella con gli gnocchi già formati, in alto
    ("1-gnocchi", 62, 126),
    # La fioreta nella ciotola con la grattugia e il formaggio
    ("2-fioreta", 68, 238),
    # Le ciotoline con la farina, il formaggio grattugiato e il burro
    ("3-farina-burro-formaggio", 150, 200),
]


def main() -> int:
    if not SORGENTE.is_file():
        print(f"fotografia non trovata: {SORGENTE}")
        return 1

    USCITA.mkdir(parents=True, exist_ok=True)

    with Image.open(SORGENTE) as originale:
        larghezza, altezza = originale.size
        im = originale.convert("RGB")

        for nome, x, y in DETTAGLI:
            # Il ritaglio non deve uscire dalla fotografia.
            x = max(0, min(x, larghezza - LATO))
            y = max(0, min(y, altezza - LATO))

            dettaglio = im.crop((x, y, x + LATO, y + LATO))
            # Si porta a 432 px con un ingrandimento morbido: nella pagina si
            # mostra a 144 px, quindi il file resta piccolo ma definito anche
            # sugli schermi ad alta densità.
            dettaglio = dettaglio.resize((432, 432), Image.LANCZOS)

            percorso = USCITA / f"{nome}.jpg"
            dettaglio.save(percorso, "JPEG", quality=86, optimize=True)
            print(f"  {percorso.relative_to(RADICE)}   {dettaglio.size[0]}x{dettaglio.size[1]}   da ({x},{y})")

    print(f"\n  {len(DETTAGLI)} dettagli, tutti {432}x{432}: formato unico.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
