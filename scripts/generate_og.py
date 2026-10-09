"""
Genera i file social e le icone a partire dalla stessa arte segnaposto:
  public/og-default.jpg      1200x630  — immagine Open Graph / Twitter
  public/apple-touch-icon.png 180x180  — icona iOS

Uso:  python scripts/generate_og.py
"""

from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

import generate_placeholders as gp

PUBLIC = Path(__file__).resolve().parent.parent / "public"

TESTO_RIGA_1 = "Locanda Seggiovia"
TESTO_RIGA_2 = "Recoaro Terme / Piccole Dolomiti"


def load_font(size: int):
    for nome in ("segoeui.ttf", "arial.ttf", "georgia.ttf", "DejaVuSerif.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(nome, size)
        except OSError:
            continue
    return ImageFont.load_default()


def og_image() -> None:
    """Fascia 1200x630: paesaggio + velo scuro in basso + wordmark."""
    w, h = 1200, 630
    rng = random.Random(9001)

    img = gp.sky(w, h, (96, 112, 132), (206, 190, 176), 0.68, gp.GLOW_300)
    gp.draw_ridge_stack(
        img,
        rng,
        sky_color=(96, 112, 132),
        near_color=(36, 42, 40),
        far_color=(150, 156, 160),
        count=5,
        roughness=0.22,
        sun_x=0.68,
    )
    img = gp.finish(img, rng)

    # Velo scuro dal basso: garantisce il contrasto del testo.
    velo = Image.new("L", (w, h), 0)
    vd = ImageDraw.Draw(velo)
    for y in range(h):
        t = max(0.0, (y / h - 0.34) / 0.66)
        vd.line([(0, y), (w, y)], fill=int(232 * (t**1.25)))
    img = Image.composite(Image.new("RGB", (w, h), (20, 20, 19)), img, velo)

    draw = ImageDraw.Draw(img)
    f1 = load_font(64)
    f2 = load_font(27)

    x, y2 = 64, h - 92
    draw.text((x, y2), TESTO_RIGA_2, font=f2, fill=(214, 210, 202))
    draw.text((x, y2 - 76), TESTO_RIGA_1, font=f1, fill=(248, 246, 242))

    # Filo sottile: firma grafica, coerente con le righe del sito.
    draw.line([(x, y2 - 108), (x + 96, y2 - 108)], fill=(216, 179, 163), width=3)

    out = PUBLIC / "og-default.jpg"
    img.save(out, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"  og-default.jpg   {w}x{h}  {out.stat().st_size // 1024} KB")


def apple_icon() -> None:
    """Icona iOS: stesso disegno del favicon, in PNG."""
    s = 180
    img = Image.new("RGB", (s, s), (45, 61, 49))
    draw = ImageDraw.Draw(img)

    # Due creste, la seconda più alta: stessa forma del favicon.svg.
    def cresta(punti, colore):
        draw.polygon([(int(px * s), int(py * s)) for px, py in punti], fill=colore)

    cresta(
        [(0, 0.72), (0.22, 0.47), (0.37, 0.62), (0.59, 0.34), (0.78, 0.59), (1, 0.44), (1, 1), (0, 1)],
        (242, 240, 235),
    )
    cresta([(0.59, 0.34), (0.78, 0.59), (0.69, 0.59), (0.59, 0.46)], (207, 202, 190))

    out = PUBLIC / "apple-touch-icon.png"
    img.save(out, "PNG", optimize=True)
    print(f"  apple-touch-icon.png  {s}x{s}  {out.stat().st_size // 1024} KB")


def main() -> None:
    print("Generazione file social e icone ->", PUBLIC)
    og_image()
    apple_icon()
    print("Fatto.")


if __name__ == "__main__":
    main()
