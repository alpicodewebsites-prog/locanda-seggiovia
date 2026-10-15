"""
Genera le immagini segnaposto della Locanda Seggiovia.

Le immagini sono DISEGNATE proceduralmente: non sono foto stock e non
violano alcuna licenza. Servono come "segnaposto neutri" in attesa degli
scatti reali del territorio (Piccole Dolomiti, Pasubio, malghe).

Le immagini vengono scritte in `src/assets/`: da lì passano
dall'ottimizzazione di Astro (WebP + srcset responsive). Non esistono copie
in `public/`, così ogni fotografia ha un solo posto dove vive.

Uso:  python scripts/generate_placeholders.py
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

# --- Palette di brand (allineata a src/styles/global.css) --------------------
STONE_50 = (250, 249, 246)
STONE_100 = (242, 240, 235)
STONE_200 = (229, 225, 216)
STONE_300 = (207, 202, 190)
STONE_400 = (148, 143, 132)
STONE_600 = (79, 76, 70)
STONE_800 = (35, 34, 32)
WOOD_700 = (63, 47, 33)
WOOD_900 = (46, 34, 24)
FOREST_500 = (90, 122, 94)
FOREST_700 = (45, 61, 49)
FOREST_900 = (30, 42, 33)
GLOW_300 = (216, 179, 163)
GLOW_500 = (181, 115, 92)

OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "assets"
SEED = 20240601


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def mix(c1, c2, t: float):
    t = max(0.0, min(1.0, t))
    return tuple(int(round(lerp(c1[i], c2[i], t))) for i in range(3))


# --- Profilo di cresta -------------------------------------------------------

_GRID = 4.0


def _value_noise_1d(rng: random.Random, points: int, grid: int) -> list[float]:
    """Rumore di valore 1D con interpolazione coseno, campionato su `points`."""
    knots = [rng.random() for _ in range(grid + 1)]
    knots[-1] = knots[0]  # periodico: nessuna cucitura ai bordi

    out = []
    for i in range(points):
        x = i / (points - 1) * grid
        i0 = int(x) % grid
        f = x - int(x)
        f = (1 - math.cos(f * math.pi)) / 2  # smoothstep
        out.append(lerp(knots[i0], knots[i0 + 1], f))
    return out


def ridge_profile(rng: random.Random, points: int, roughness: float) -> list[float]:
    """
    Profilo di cresta in stile fBm: somma di ottave di rumore di valore.
    `roughness` basso -> creste frastagliate (roccia); alto -> dolci (pascolo).
    """
    # persistenza bassa + frequenza iniziale bassa = creste aguzze e credibili
    persistence = lerp(0.30, 0.62, roughness)
    total = [0.0] * points
    amp = 1.0
    freq = 2
    norm = 0.0

    for _ in range(6):
        octave = _value_noise_1d(rng, points, max(2, int(freq)))
        for i in range(points):
            total[i] += octave[i] * amp
        norm += amp
        amp *= persistence
        freq *= lerp(2.3, 1.8, roughness)

    return [v / norm for v in total]


def draw_ridge_stack(
    img: Image.Image,
    rng: random.Random,
    sky_color,
    near_color,
    far_color,
    count: int,
    roughness: float,
    sun_x: float,
) -> None:
    """
    Disegna le creste da lontano a vicino. Ogni cresta è una maschera dura;
    la foschia è una velatura verticale applicata SUBITO SOPRA il profilo,
    così l'aria resta dove deve stare (in alto) e la roccia resta scura.
    """
    width, height = img.size
    band = 0.52  # ampiezza verticale della catena montuosa

    for i in range(count):
        t = i / max(1, count - 1)

        profile = ridge_profile(rng, width, roughness=lerp(0.15, 0.85, t))

        # Le creste lontane stanno più in alto; l'ampiezza cresce avvicinandosi.
        base = lerp(0.60, 0.92, t) * height
        amp = lerp(0.13, 0.26, t) * height

        # Versante illuminato dal sole basso: il profilo destro è più alto.
        ys = [base - (v - 0.5) * amp for v in profile]

        # Colore: lontano => quasi cielo, vicino => roccia/bosco scuro.
        color = mix(far_color, near_color, t)

        mask = Image.new("L", (width, height), 0)
        mdraw = ImageDraw.Draw(mask)

        # Riempimento della sagoma sotto il profilo.
        mdraw.polygon(
            [(x, y) for x, y in enumerate(ys)]
            + [(width - 1, height), (0, height)],
            fill=255,
        )

        # Luce sul versante: pixel più chiari appena sotto la cresta.
        lit = Image.new("RGB", (width, height), color)
        ldraw = ImageDraw.Draw(lit)
        for x in range(0, width, 2):
            y = ys[x]
            ldraw.line([(x, y), (x, y + amp * 0.5)], fill=mix(color, sky_color, 0.34))

        # Sfocatura minima: solo le creste lontane perdono dettaglio.
        f = lerp(2.6, 0.0, t)
        if f > 0:
            mask = mask.filter(ImageFilter.GaussianBlur(f))
            lit = lit.filter(ImageFilter.GaussianBlur(f * 0.35))

        img.paste(lit, (0, 0), mask)

        # Le due creste più vicine portano il bosco: piantato subito dopo la
        # cresta, così la foschia lo avvolge invece di coprirlo.
        if i >= count - 2:
            forest_t = float(i - (count - 2))
            plant_conifers(
                img, rng, ys,
                color=mix(near_color, FOREST_900, 0.40 * forest_t),
                density=lerp(0.055, 0.085, t),
                tree_h=lerp(0.015, 0.028, t) * height,
            )

        # Velatura di foschia: gradiente continuo che parte dalla cresta e
        # sfuma verso l'alto. Costruito su una striscia di 1px e stirato:
        # evita le striature verticali del disegno riga-per-riga.
        hh = int(height * 0.20)
        strip = Image.new("L", (1, hh), 0)
        spx = strip.load()
        for k in range(hh):
            spx[0, k] = int(255 * (0.62 * (1 - k / hh) ** 1.7))
        strip = strip.resize((width, hh), Image.Resampling.BILINEAR)

        # Posizionata all'altezza minima della cresta: la foschia si appoggia
        # al profilo invece di tagliarlo.
        y_min = int(min(ys))
        haze = Image.new("L", (width, height), 0)
        haze.paste(strip, (0, max(0, y_min - hh)))
        haze = haze.filter(ImageFilter.GaussianBlur(7))

        veil = Image.new("RGB", (width, height), mix(sky_color, STONE_100, 0.35))
        img.paste(veil, (0, 0), haze)

        # Aloni morbidi di foschia sopra ogni valle (profondità).
        if t < 0.85:
            puff = Image.new("L", (width, height), 0)
            pdraw = ImageDraw.Draw(puff)
            for _ in range(3):
                cx = rng.uniform(0.1, 0.9) * width
                cy = base - lerp(0.05, 0.16, t) * height
                r = rng.uniform(0.10, 0.24) * width
                pdraw.ellipse([cx - r, cy - r * 0.28, cx + r, cy + r * 0.28], fill=52)
            puff = puff.filter(ImageFilter.GaussianBlur(width * 0.045))
            img.paste(veil, (0, 0), puff)


def plant_conifers(
    img: Image.Image,
    rng: random.Random,
    ys: list[float],
    color,
    density: float,
    tree_h: float,
) -> None:
    """
    Silhouette di conifere sulla cresta più vicina. Bastano pochi pixel di
    profilo frastagliato per far leggere subito la scena come alpina.
    """
    width, height = img.size
    layer = Image.new("RGB", (width, height), color)
    mask = Image.new("L", (width, height), 0)
    mdraw = ImageDraw.Draw(mask, "L")

    x = 0
    while x < width:
        step = max(3, int(rng.expovariate(density)))
        x += step
        if x >= width:
            break

        h = tree_h * rng.uniform(0.55, 1.35)
        # Le conifere sono più alte sui versanti che sulle cime battute dal vento.
        y = ys[x]
        half = h * 0.26

        # Abete stilizzato: triangolo con punta, non un cono perfetto.
        mdraw.polygon(
            [(x, y - h), (x + half, y), (x - half, y)],
            fill=255,
        )
        mdraw.polygon(
            [(x, y - h * 0.55), (x + half * 1.35, y + h * 0.55), (x - half * 1.35, y + h * 0.55)],
            fill=255,
        )

    mask = mask.filter(ImageFilter.GaussianBlur(0.7))
    img.paste(layer, (0, 0), mask)


def sky(width: int, height: int, top, bottom, sun_x: float, sun_color) -> Image.Image:
    """Sfumatura verticale + alone caldo di sole basso (alpenglow)."""
    col = Image.new("RGB", (1, height))
    px = col.load()
    for y in range(height):
        px[0, y] = mix(top, bottom, (y / max(1, height - 1)) ** 0.92)
    img = col.resize((width, height), Image.Resampling.BILINEAR)

    # Alone caldo: ellisse gaussiana costruita in maschera, non un gradiente piatto.
    glow = Image.new("L", (width, height), 0)
    gdraw = ImageDraw.Draw(glow)
    cx = sun_x * width
    cy = height * 0.30
    rx = width * 0.46
    ry = height * 0.42
    gdraw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=150)
    glow = glow.filter(ImageFilter.GaussianBlur(width * 0.10))
    img.paste(Image.new("RGB", (width, height), sun_color), (0, 0), glow)
    return img


def finish(img: Image.Image, rng: random.Random) -> Image.Image:
    """Grana sottile + vignettatura appena percettibile."""
    width, height = img.size

    noise = Image.new("L", (width, height))
    noise.putdata([128 + rng.randint(-7, 7) for _ in range(width * height)])
    noise = noise.filter(ImageFilter.GaussianBlur(0.45))
    img = Image.blend(img, Image.merge("RGB", (noise, noise, noise)), 0.05)

    # Vignettatura: due soli passaggi, angoli in basso, intensità bassa.
    vig = Image.new("L", (width, height), 0)
    vdraw = ImageDraw.Draw(vig)
    vdraw.ellipse(
        [-width * 0.22, -height * 0.30, width * 1.22, height * 1.30], fill=255
    )
    vig = vig.filter(ImageFilter.GaussianBlur(width * 0.07))
    img = Image.composite(img, Image.new("RGB", (width, height), (26, 25, 23)), vig)
    return img


# --- Scene -------------------------------------------------------------------
# (nome, w, h, seed, [cielo alto, cielo basso], [cresta lontana, cresta vicina],
#  n. creste, roughness, sun_x, sun_color)
SCENES = [
    (
        "hero-piccole-dolomiti", 2560, 1440, 4101,
        [(96, 112, 132), (206, 190, 176)],
        [(150, 156, 160), (36, 42, 40)], 6, 0.20, 0.68, GLOW_300,
    ),
    (
        # Panorama ampio usato a tutta larghezza nella chiusura della home.
        # Le fotografie fornite sono piccole: a 400px si sgranano su schermo
        # intero, quindi qui serve un disegno che regga qualsiasi larghezza.
        "piccole-dolomiti-large", 2560, 1440, 4301,
        [(112, 126, 142), (206, 186, 168)],
        [(148, 152, 156), (34, 42, 38)], 7, 0.20, 0.64, GLOW_300,
    ),
    (
        "sentieri-grandi-alberi", 1920, 1280, 4201,
        [(122, 146, 138), (206, 214, 200)],
        [(150, 162, 152), (32, 52, 40)], 7, 0.70, 0.34, STONE_100,
    ),
    (
        "sentieri-campogrosso", 1920, 1280, 4202,
        [(118, 128, 140), (204, 196, 186)],
        [(152, 152, 154), (44, 50, 48)], 6, 0.30, 0.55, STONE_200,
    ),
    (
        "sentieri-ponte-tibetano", 1920, 1280, 4203,
        [(106, 122, 134), (196, 190, 184)],
        [(142, 148, 152), (38, 44, 44)], 7, 0.24, 0.44, STONE_200,
    ),
    (
        "sentieri-52-gallerie", 1920, 1280, 4204,
        [(98, 104, 112), (172, 164, 152)],
        [(132, 130, 126), (30, 30, 30)], 6, 0.18, 0.62, GLOW_300,
    ),
    (
        "sentieri-mole", 1920, 1280, 4205,
        [(148, 160, 168), (222, 218, 206)],
        [(168, 168, 158), (72, 92, 68)], 5, 0.76, 0.40, STONE_100,
    ),
    (
        "sentieri-gino-solda", 1920, 1280, 4206,
        [(126, 138, 150), (208, 200, 192)],
        [(154, 156, 154), (46, 56, 50)], 6, 0.34, 0.66, GLOW_300,
    ),
]

# Interni e soggetti non paesaggistici: riquadro vuoto etichettato.
# Un disegno astratto NON può sostituire la foto di una camera o di un piatto,
# e far finta che sia un panorama sarebbe fuorviante.
EMPTY_SLOTS = [
]


def load_font(size: int):
    """Font scalabile di sistema; se manca, si ripiega su quello bitmap di PIL."""
    from PIL import ImageFont

    for nome in ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf", "calibri.ttf"):
        try:
            return ImageFont.truetype(nome, size)
        except OSError:
            continue
    return ImageFont.load_default()


def empty_slot(path: Path, width: int, height: int, label: str) -> None:
    """
    Segnaposto neutro per gli interni (camere, ristorante): nessuna pretesa
    di somigliare a una fotografia. Un riquadro vuoto con l'etichetta di cosa
    andrà lì. Serve a non far credere che esista una foto che non esiste.
    """
    img = Image.new("RGB", (width, height), (226, 222, 214))
    draw = ImageDraw.Draw(img)

    # Cornice interna: convenzione grafica del "riquadro da riempire".
    m = int(min(width, height) * 0.045)
    draw.rectangle([m, m, width - m, height - m], outline=(202, 196, 186), width=3)
    draw.line([(m, m), (width - m, height - m)], fill=(212, 207, 198), width=2)
    draw.line([(width - m, m), (m, height - m)], fill=(212, 207, 198), width=2)

    # Etichetta centrata su fascia piena. Solo caratteri ASCII: il font
    # predefinito di PIL non sa disegnare le lettere accentate o i trattini lunghi.
    font = load_font(max(18, int(min(width, height) * 0.030)))
    text = f"FOTO IN ARRIVO / {label}"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = int(th * 1.1), int(th * 0.65)
    cx, cy = width // 2, height // 2

    draw.rectangle(
        [
            cx - tw // 2 - pad_x,
            cy - th // 2 - pad_y,
            cx + tw // 2 + pad_x,
            cy + th // 2 + pad_y,
        ],
        fill=(242, 240, 235),
        outline=(202, 196, 186),
        width=2,
    )
    draw.text((cx - tw // 2 - bbox[0], cy - th // 2 - bbox[1]), text, fill=(110, 106, 97), font=font)

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"  {path.name}  {width}x{height}  {path.stat().st_size // 1024} KB  [riquadro vuoto]")


def stamp_label(img: Image.Image, testo: str) -> None:
    """
    Scrive l'etichetta di segnaposto DENTRO il paesaggio disegnato.

    Perché dentro l'immagine e non nella pagina: così sparisce da sola. Quando
    la fotografa carica la fotografia vera con lo stesso nome, il file viene
    sostituito e l'etichetta non c'è più. Un avviso scritto nel codice della
    pagina, invece, resterebbe lì a dire il falso finché qualcuno non se ne
    ricorda.

    Posizione in basso a sinistra con margine ampio: nei riquadri delle schede
    il ritaglio avviene in orizzontale, quindi il basso resta sempre visibile.
    """
    larghezza, altezza = img.size
    draw = ImageDraw.Draw(img, "RGBA")

    font = load_font(max(15, int(min(larghezza, altezza) * 0.022)))
    bbox = draw.textbbox((0, 0), testo, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    margine = int(min(larghezza, altezza) * 0.055)
    pad_x, pad_y = int(th * 0.9), int(th * 0.55)

    x0 = margine
    y1 = altezza - margine
    y0 = y1 - th - pad_y * 2

    # Piastra semitrasparente: il testo deve restare leggibile su qualunque
    # paesaggio, chiaro o scuro.
    draw.rectangle(
        [x0, y0, x0 + tw + pad_x * 2, y1],
        fill=(20, 20, 18, 165),
    )
    draw.text(
        (x0 + pad_x - bbox[0], y0 + pad_y - bbox[1]),
        testo,
        fill=(245, 243, 238, 235),
        font=font,
    )


def main() -> None:
    print(f"Generazione immagini segnaposto -> {OUT_DIR}")
    for name, w, h, seed, sky_cols, ridges, count, rough, sun_x, sun_col in SCENES:
        rng = random.Random(seed)
        top, bottom = sky_cols
        img = sky(w, h, top, bottom, sun_x, sun_col)

        far_c, near_c = ridges
        draw_ridge_stack(
            img, rng,
            sky_color=top,
            near_color=near_c,
            far_color=far_c,
            count=count,
            roughness=rough,
            sun_x=sun_x,
        )

        img = finish(img, rng)

        # Etichetta dichiarativa: dice che questa non è una fotografia e che
        # va sostituita. Solo caratteri ASCII, il font predefinito di PIL non
        # sa disegnare gli accenti.
        stamp_label(img, "FOTO IN ARRIVO - segnaposto, non una foto reale")

        path = OUT_DIR / f"{name}.jpg"
        path.parent.mkdir(parents=True, exist_ok=True)
        img.save(path, "JPEG", quality=86, optimize=True, progressive=True)
        print(f"  {name}.jpg  {w}x{h}  {path.stat().st_size // 1024} KB")

    # Interni: riquadri vuoti, non finti paesaggi.
    for name, w, h, label in EMPTY_SLOTS:
        empty_slot(OUT_DIR / f"{name}.jpg", w, h, label)

    print("Fatto. Sostituire con le fotografie reali mantenendo i nomi dei file.")


if __name__ == "__main__":
    main()
