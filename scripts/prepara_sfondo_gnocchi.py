"""Prepara lo sfondo della fascia degli gnocchi da una foto ad alta risoluzione.

LA FOTOGRAFIA
`scaricata-37616037.jpg` - gnocchi in salsa cremosa, di Anh Nguyen, da Pexels.
Licenza Pexels: uso commerciale consentito, attribuzione non obbligatoria
(la mettiamo lo stesso, in docs/CREDITI-FOTO.md).

    https://www.pexels.com/photo/37616037/

LAVORAZIONE
Si ritaglia la parte bassa dell'inquadratura, dove gli gnocchi riempiono il
fotogramma, e si porta a una fascia larga.

Uso:  python scripts/prepara_sfondo_gnocchi.py
"""

from __future__ import annotations

import pathlib
import sys

from PIL import Image, ImageEnhance

RADICE = pathlib.Path(__file__).resolve().parent.parent
SORGENTE = RADICE / "scaricata-37616037.jpg"
USCITA = RADICE / "src" / "assets" / "gnocchi" / "sfondo-gnocchi.jpg"

# Ritaglio in frazioni del lato: non dipende dalla risoluzione del file.
RITAGLIO = (0.16, 0.615, 0.96, 0.885)

LARGHEZZA = 2000


def main() -> int:
    if not SORGENTE.is_file():
        print(f"fotografia non trovata: {SORGENTE}")
        return 1

    with Image.open(SORGENTE) as originale:
        im = originale.convert("RGB")
        l, a = im.size
        riquadro = (
            round(RITAGLIO[0] * l),
            round(RITAGLIO[1] * a),
            round(RITAGLIO[2] * l),
            round(RITAGLIO[3] * a),
        )
        im = im.crop(riquadro)
        larghezza, altezza = im.size
        im = im.resize((LARGHEZZA, round(altezza * LARGHEZZA / larghezza)), Image.LANCZOS)
        im = ImageEnhance.Contrast(im).enhance(1.06)
        im.save(USCITA, "JPEG", quality=82, optimize=True, progressive=True)

    peso = USCITA.stat().st_size / 1024
    print(f"  {USCITA.relative_to(RADICE)}")
    print(f"  {im.size[0]}x{im.size[1]} px, {peso:.0f} KB")
    print(f"  da {SORGENTE.name} ({l}x{a}), ritaglio {riquadro}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
