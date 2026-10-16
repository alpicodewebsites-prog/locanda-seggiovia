"""
Genera le tessere degli ingredienti per la fascia «tavolo» della home.

SEI TESSERE UGUALI, NON SEI FOTO SCARICATE
Le immagini sono disegnate una per una con lo stesso formato (quadrate), lo
stesso sfondo, la stessa luce e lo stesso spessore di tratto. È questo che le
rende uniformi: prendere cinque fotografie diverse — anche belle — darebbe
cinque inquadrature, cinque luci e cinque sfondi diversi, ed è esattamente
quello che il committente ha chiesto di evitare.

Sono DICHIARATAMENTE disegni, non scatti: quando arrivano le fotografie vere
degli ingredienti si sostituiscono dal pannello, una per una, e queste spariscono.
[verificato: il formato quadrato 800x800 è lo stesso per tutte]

Uso:  python scripts/genera_ingredienti.py
"""

from __future__ import annotations

import math
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFilter

RADICE = pathlib.Path(__file__).resolve().parent.parent
USCITA = RADICE / "src" / "assets" / "gnocchi" / "ingredienti"

# Formato unico per tutte le tessere. Non cambiarlo per una sola: la griglia
# della pagina è costruita su questo rapporto.
LATO = 800

# --- Palette, la stessa della pagina ----------------------------------------
FONDO = (236, 223, 204)  # legno-100: il piano di lavoro
FONDO_SCURO = (223, 206, 182)  # ombra sotto gli oggetti
LEGNO = (197, 162, 118)  # legno-300
SCURO = (63, 47, 33)  # legno-700
MEDIO = (130, 92, 49)  # legno-500
BIANCO = (250, 248, 244)
CREMA = (245, 238, 226)
GRIGIO = (214, 210, 202)
GIALLO = (233, 205, 138)


def tela() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """Un piano di lavoro caldo, con una lieve grana."""
    im = Image.new("RGB", (LATO, LATO), FONDO)
    d = ImageDraw.Draw(im)

    # Grana: puntini appena visibili, per non avere un fondo piatto.
    for y in range(0, LATO, 4):
        for x in range(0, LATO, 4):
            if (x * 7 + y * 13) % 97 == 0:
                d.point((x, y), fill=FONDO_SCURO)

    # Ombra morbida sul bordo inferiore: dà l'idea del piano che si allontana.
    ombra = Image.new("L", (LATO, LATO), 0)
    ImageDraw.Draw(ombra).rectangle([0, LATO - 150, LATO, LATO], fill=70)
    ombra = ombra.filter(ImageFilter.GaussianBlur(60))
    im = Image.composite(Image.new("RGB", (LATO, LATO), FONDO_SCURO), im, ombra)

    return im, ImageDraw.Draw(im)


def ombra_sotto(im: Image.Image, riquadro: tuple[int, int, int, int], forza: int = 90) -> None:
    """Ombra sfumata sotto un oggetto: senza, l'oggetto sembra incollato."""
    x0, y0, x1, y1 = riquadro
    maschera = Image.new("L", (LATO, LATO), 0)
    ImageDraw.Draw(maschera).ellipse(
        [x0 - 20, y1 - 30, x1 + 20, y1 + 34],
        fill=forza,
    )
    maschera = maschera.filter(ImageFilter.GaussianBlur(26))
    im.paste(Image.new("RGB", (LATO, LATO), (150, 128, 100)), (0, 0), maschera)


# --------------------------------------------------------------------------
# I cinque ingredienti, nell'ordine della ricetta De.Co.
# --------------------------------------------------------------------------


def fioreta() -> Image.Image:
    """La fioreta: una scodella di latte cagliato, con la superficie increspata."""
    im, d = tela()
    ombra_sotto(im, (230, 470, 570, 620))

    # Scodella
    d.ellipse([230, 380, 570, 560], fill=CREMA, outline=SCURO, width=7)
    d.ellipse([255, 405, 545, 535], fill=BIANCO)

    # Superficie del latte, appena mossa
    for i in range(4):
        y = 440 + i * 22
        d.arc([290, y - 14, 510, y + 14], 200, 340, fill=GRIGIO, width=4)

    # Una goccia che cola dal cucchiaio
    d.polygon([(400, 250), (378, 330), (422, 330)], fill=BIANCO, outline=SCURO)
    d.line([(400, 250), (400, 200)], fill=MEDIO, width=8)
    return im


def farina() -> Image.Image:
    """La farina: un mucchio setacciato, con la paletta di legno."""
    im, d = tela()
    ombra_sotto(im, (180, 480, 620, 620))

    # Mucchio
    d.polygon(
        [(180, 600), (400, 300), (620, 600)],
        fill=BIANCO,
        outline=(228, 222, 210),
    )
    # Sfumatura del mucchio: qualche linea di caduta
    for i in range(5):
        x = 260 + i * 70
        d.line([(x, 560 - i * 8), (400, 330)], fill=(240, 236, 228), width=3)

    # Paletta di legno infilata nel mucchio
    d.rounded_rectangle([470, 350, 540, 560], radius=16, fill=LEGNO, outline=SCURO, width=6)
    d.rounded_rectangle([440, 300, 570, 370], radius=22, fill=LEGNO, outline=SCURO, width=6)
    return im


def burro() -> Image.Image:
    """Il burro di malga: un panetto con l'incisione della zangola."""
    im, d = tela()
    ombra_sotto(im, (200, 470, 600, 620))

    # Panetto in prospettiva: faccia frontale e cima
    d.polygon([(210, 600), (210, 430), (400, 350), (590, 430), (590, 600)],
              fill=GIALLO, outline=SCURO)
    d.polygon([(210, 430), (400, 350), (590, 430), (400, 510)],
              fill=(243, 222, 168), outline=SCURO)

    # Due tagli sulla cima, come si fa col filo
    d.line([(300, 430), (400, 386)], fill=SCURO, width=5)
    d.line([(500, 430), (400, 386)], fill=SCURO, width=5)
    return im


def formaggio() -> Image.Image:
    """Il formaggio stagionato: una forma con la crosta scura."""
    im, d = tela()
    ombra_sotto(im, (190, 470, 610, 620))

    # Fetta vista di tre quarti
    d.polygon([(200, 590), (200, 470), (400, 380), (600, 470), (600, 590)],
              fill=(238, 216, 160), outline=SCURO)
    d.polygon([(200, 470), (400, 380), (600, 470), (400, 560)],
              fill=(247, 232, 190), outline=SCURO)

    # Crosta
    d.line([(200, 590), (200, 470)], fill=(160, 120, 70), width=12)
    d.line([(200, 470), (400, 380)], fill=(160, 120, 70), width=12)

    # I fori della stagionatura
    for cx, cy, r in [(320, 520, 13), (420, 545, 9), (500, 505, 11), (390, 480, 7)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 186, 130))
    return im


def sale() -> Image.Image:
    """Il sale: un mucchietto di granelli con la paletta di ceramica."""
    im, d = tela()
    ombra_sotto(im, (200, 500, 600, 620))

    # Mucchietto
    d.polygon([(230, 600), (400, 450), (570, 600)], fill=BIANCO, outline=(226, 222, 214))

    # Granelli sparsi sul piano
    for cx, cy in [(180, 640), (250, 665), (600, 650), (660, 630), (520, 670)]:
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=BIANCO, outline=(228, 224, 216))

    # Paletta di ceramica
    d.rounded_rectangle([330, 250, 470, 420], radius=14, fill=CREMA, outline=SCURO, width=6)
    d.ellipse([345, 265, 455, 320], fill=BIANCO, outline=GRIGIO, width=4)
    return im


INGREDIENTI = [
    ("1-fioreta", fioreta),
    ("2-farina", farina),
    ("3-burro", burro),
    ("4-formaggio", formaggio),
    ("5-sale", sale),
]


def main() -> int:
    USCITA.mkdir(parents=True, exist_ok=True)

    for nome, disegna in INGREDIENTI:
        immagine = disegna()
        percorso = USCITA / f"{nome}.jpg"
        immagine.save(percorso, "JPEG", quality=88, optimize=True)
        print(f"  {percorso.relative_to(RADICE)}   {immagine.size[0]}x{immagine.size[1]}")

    print(f"\n  {len(INGREDIENTI)} tessere, tutte {LATO}x{LATO}: formato unico.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
