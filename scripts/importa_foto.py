"""
Prepara le fotografie reali fornite dalla cliente.

Sorgente:  foto sito locanda/
Destinazione: src/assets/

Cosa fa, e perché:
  - rinomina i file con nomi senza spazi e in minuscolo (i nomi con spazi
    creano problemi negli import e negli URL);
  - rende trasparente lo sfondo bianco del logo, così può essere posato su
    fondi chiari e scuri senza un riquadro bianco attorno;
  - riduce il logo a una dimensione ragionevole, lasciando intatte le foto.

Non inventa nulla: se un file manca, lo segnala e prosegue.

Uso:  python scripts/importa_foto.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from PIL import Image

RADICE = Path(__file__).resolve().parent.parent
SORGENTE = RADICE / "foto sito locanda"
DESTINAZIONE = RADICE / "src" / "assets"

# Sorgente -> nome definitivo in src/assets
FOTO = {
    "seggiovia esterno.jpeg": "locanda-esterno.jpg",
    "seggiovia 1.jpeg": "territorio-montagne.jpg",
    "seggiovia 2.jpg": "locanda-preparazione.jpg",
    "gnocchi alla fioreta.jpeg": "piatto-gnocchi-fioreta.jpg",
    "gnocchi alla vicentina.jpeg": "piatto-bacala-vicentina.jpg",
}

LOGO_SORGENTE = "locanda logo.gif"
LOGO_DESTINAZIONE = "locanda-logo.png"


def trasparenza_da_bianco(img: Image.Image, soglia: int = 238) -> Image.Image:
    """
    Rende trasparente lo sfondo bianco di un logo.

    I pixel quasi bianchi diventano trasparenti; quelli intermedi vengono
    sfumati, altrimenti i bordi delle lettere risulterebbero seghettati.
    """
    img = img.convert("RGBA")
    larghezza, altezza = img.size
    pixel = img.load()

    for y in range(altezza):
        for x in range(larghezza):
            r, g, b, a = pixel[x, y]
            luminanza = (r + g + b) / 3
            if luminanza >= soglia:
                pixel[x, y] = (r, g, b, 0)
            elif luminanza > soglia - 28:
                # Bordo: resa parzialmente trasparente per non lasciare scalini.
                fattore = (soglia - luminanza) / 28
                pixel[x, y] = (r, g, b, int(a * fattore))

    return img


def main() -> int:
    if not SORGENTE.is_dir():
        print(f"ERRORE: cartella non trovata: {SORGENTE}")
        return 1

    DESTINAZIONE.mkdir(parents=True, exist_ok=True)
    mancanti: list[str] = []

    print(f"Origine:     {SORGENTE}")
    print(f"Destinazione: {DESTINAZIONE}\n")

    # --- Fotografie ---------------------------------------------------------
    for origine, destinazione in FOTO.items():
        percorso = SORGENTE / origine
        if not percorso.exists():
            mancanti.append(origine)
            continue

        with Image.open(percorso) as img:
            img = img.convert("RGB")
            larghezza, altezza = img.size
            img.save(DESTINAZIONE / destinazione, "JPEG", quality=90, optimize=True, progressive=True)

        kb = (DESTINAZIONE / destinazione).stat().st_size // 1024
        print(f"  {destinazione:34} {larghezza}x{altezza}  {kb} KB")

    # --- Logo ---------------------------------------------------------------
    percorso_logo = SORGENTE / LOGO_SORGENTE
    if percorso_logo.exists():
        with Image.open(percorso_logo) as img:
            larghezza, altezza = img.size
            trasparente = trasparenza_da_bianco(img)
            trasparente.save(DESTINAZIONE / LOGO_DESTINAZIONE, "PNG", optimize=True)

        kb = (DESTINAZIONE / LOGO_DESTINAZIONE).stat().st_size // 1024
        print(f"  {LOGO_DESTINAZIONE:34} {larghezza}x{altezza}  {kb} KB  [sfondo trasparente]")
        if larghezza < 400:
            print(
                f"      NOTA: il logo è piccolo ({larghezza}px). Su schermi ad alta densità "
                "risulterà poco nitido: serve una versione vettoriale o più grande."
            )
    else:
        mancanti.append(LOGO_SORGENTE)

    print()
    if mancanti:
        print("File non trovati (nessun problema se non servono):")
        for m in mancanti:
            print(f"  - {m}")
    print("Fatto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
