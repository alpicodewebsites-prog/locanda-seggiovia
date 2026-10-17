"""
Prepara lo sfondo della fascia degli gnocchi.

La fotografia di partenza è quella scattata in locanda (`02-piatto-finito.jpg`,
300x187). Si ritaglia togliendo il bordo del piatto, così restano SOLO gli
gnocchi, e si porta alla larghezza che serve per una fascia a tutta pagina.

Sull'ingrandimento: la sorgente è piccola, quindi il file viene ingrandito di
circa cinque volte. Non è un problema perché questa immagine sta DIETRO a un
velo scuro e a un pulsante: quello che si vede è la trama degli gnocchi, non il
dettaglio. Un'immagine nitidissima non aggiungerebbe nulla e peserebbe molto di
più.

Uso:  python scripts/prepara_sfondo_gnocchi.py
"""

from __future__ import annotations

import pathlib
import sys

from PIL import Image, ImageEnhance, ImageFilter

RADICE = pathlib.Path(__file__).resolve().parent.parent
SORGENTE = RADICE / "src" / "assets" / "gnocchi" / "02-piatto-finito.jpg"
USCITA = RADICE / "src" / "assets" / "gnocchi" / "sfondo-gnocchi.jpg"

# Ritaglio: si toglie il bordo del piatto sopra e sotto, per lasciare in
# inquadratura solo gli gnocchi. Valori misurati guardando la fotografia.
RITAGLIO = (8, 62, 298, 180)  # sinistra, alto, destra, basso

# Larghezza finale: sufficiente per uno schermo grande, senza esagerare.
LARGHEZZA = 1800


def main() -> int:
    if not SORGENTE.is_file():
        print(f"fotografia non trovata: {SORGENTE}")
        return 1

    with Image.open(SORGENTE) as originale:
        im = originale.convert("RGB").crop(RITAGLIO)
        larghezza, altezza = im.size

        nuova_altezza = round(altezza * LARGHEZZA / larghezza)
        im = im.resize((LARGHEZZA, nuova_altezza), Image.LANCZOS)

        # Un filo di contrasto e di saturazione: la fotografia è un po' piatta,
        # e sotto il velo scuro tenderebbe al grigio.
        im = ImageEnhance.Contrast(im).enhance(1.08)
        im = ImageEnhance.Color(im).enhance(1.05)
        # Micro-sfocatura: nasconde il rumore dell'ingrandimento senza far
        # perdere la forma degli gnocchi.
        im = im.filter(ImageFilter.GaussianBlur(0.6))

        im.save(USCITA, "JPEG", quality=78, optimize=True, progressive=True)

    peso = USCITA.stat().st_size / 1024
    print(f"  {USCITA.relative_to(RADICE)}")
    print(f"  {im.size[0]}x{im.size[1]} px, {peso:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
