"""
Misura il contrasto reale fra il titolo e lo sfondo nelle aperture dei sentieri.

Legge le strisce di sfondo ritagliate dal browser con
`scripts/test_leggibilita_hero.mjs` e calcola il contrasto con il colore del
titolo secondo la formula WCAG.

Perché sui pixel e non a stima: sotto il titolo c'è una fotografia con un velo
scuro sopra, e il colore che ne risulta non si può dedurre dai valori scritti
nel foglio di stile. Va letto da quello che si vede.

Uso:  python scripts/misura_contrasto_hero.py [cartella]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

from PIL import Image

SOGLIA = 4.5


def canale(v: float) -> float:
    v = v / 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def luminanza(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.2126 * canale(r) + 0.7152 * canale(g) + 0.0722 * canale(b)


def contrasto(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    l1, l2 = luminanza(a), luminanza(b)
    chiaro, scuro = max(l1, l2), min(l1, l2)
    return (chiaro + 0.05) / (scuro + 0.05)


def colore_da_css(valore: str) -> tuple[int, int, int]:
    numeri = [int(n) for n in re.findall(r"\d+", valore)[:3]]
    return (numeri[0], numeri[1], numeri[2])


def media(pixel: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    n = len(pixel)
    return (
        sum(p[0] for p in pixel) // n,
        sum(p[1] for p in pixel) // n,
        sum(p[2] for p in pixel) // n,
    )


def main() -> int:
    cartella = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "hero-misure")
    if not cartella.is_dir():
        print(f"cartella non trovata: {cartella}")
        print("Esegui prima: node scripts/test_leggibilita_hero.mjs")
        return 1

    strisce = sorted(cartella.glob("*-sfondo.png"))
    if not strisce:
        print("nessuna striscia di sfondo da analizzare")
        return 1

    print("=" * 78)
    print("CONTRASTO DEL TITOLO SULLE APERTURE DEI SENTIERI")
    print("=" * 78)

    falliti = 0
    for striscia_file in strisce:
        slug = striscia_file.stem.replace("-sfondo", "")
        dati_file = cartella / f"{slug}.json"
        if not dati_file.is_file():
            continue

        colore_testo = colore_da_css(json.loads(dati_file.read_text(encoding="utf-8"))["colore"])

        with Image.open(striscia_file) as im:
            pixel = list(im.convert("RGB").getdata())

        # Caso peggiore per un testo chiaro: il pixel più chiaro dello sfondo.
        piu_chiaro = max(pixel, key=luminanza)
        medio = media(pixel)
        rapporto = contrasto(colore_testo, piu_chiaro)
        rapporto_medio = contrasto(colore_testo, medio)

        ok = rapporto >= SOGLIA
        if not ok:
            falliti += 1

        print(f"[{'OK  ' if ok else 'FAIL'}] {slug}")
        print(
            f"         caso peggiore  testo rgb{colore_testo} su rgb{piu_chiaro}"
            f"  ->  {rapporto:.2f}:1"
        )
        print(
            f"         media          testo rgb{colore_testo} su rgb{medio}"
            f"  ->  {rapporto_medio:.2f}:1"
        )

    print("-" * 78)
    if falliti:
        print(f"CONTRASTI INSUFFICIENTI: {falliti} (richiesto {SOGLIA}:1 nel caso peggiore)")
        return 1

    print(f"tutti i {len(strisce)} titoli sono leggibili anche nel caso peggiore")
    return 0


if __name__ == "__main__":
    sys.exit(main())
