"""
Unisce i fotogrammi catturati in un GIF.

Uso:  python scripts/crea_gif.py <cartella-fotogrammi> <file-gif> [durata-ms]

Il GIF è il formato giusto per mostrare un movimento dentro una conversazione:
parte da solo, non richiede un lettore video, e si può guardare più volte.
"""

from __future__ import annotations

import pathlib
import sys

from PIL import Image


def main() -> int:
    if len(sys.argv) < 3:
        print("Uso: python scripts/crea_gif.py <cartella> <file.gif> [durata-ms]")
        return 1

    cartella = pathlib.Path(sys.argv[1])
    uscita = pathlib.Path(sys.argv[2])
    durata = int(sys.argv[3]) if len(sys.argv) > 3 else 140

    fotogrammi = sorted(cartella.glob("frame-*.png"))
    if not fotogrammi:
        print(f"nessun fotogramma in {cartella}")
        return 1

    immagini = [Image.open(f).convert("RGB") for f in fotogrammi]

    # Riduzione a una palette condivisa: senza, il GIF userebbe una palette per
    # fotogramma e il colore cambierebbe a scatti durante la riproduzione.
    larghezza, altezza = immagini[0].size
    immagini = [im.resize((larghezza, altezza), Image.LANCZOS) for im in immagini]

    uscita.parent.mkdir(parents=True, exist_ok=True)
    immagini[0].save(
        uscita,
        save_all=True,
        append_images=immagini[1:],
        duration=durata,
        loop=0,
        optimize=True,
    )

    peso = uscita.stat().st_size / 1024
    print(f"  {uscita.name}: {len(immagini)} fotogrammi, {peso:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
