"""
Misura il contrasto dei testi del meteo su ogni cielo.

Legge le fotografie prodotte da `fotografa_cieli.mjs` (sfondo senza testo) e
calcola il contrasto con i due colori di testo:

    #1c1b19  testi principali
    #3a3a35  testi secondari

Si prende il PICCOLO PEGGIORE: il punto più scuro del fondo, perché è lì che il
testo scuro si legge peggio. Se passa lì, passa ovunque.

Uso:  python scripts/verifica_contrasto_cieli.py
"""

from __future__ import annotations

import pathlib
import sys

from PIL import Image

RADICE = pathlib.Path(__file__).resolve().parent.parent
CARTELLA = RADICE / "cieli"

PRINCIPALE = "#1c1b19"
SECONDARIO = "#32322d"
SOGLIA = 4.5


def canale(v: float) -> float:
    v = v / 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def lum(h: str) -> float:
    h = h.lstrip("#")
    return (
        0.2126 * canale(int(h[0:2], 16))
        + 0.7152 * canale(int(h[2:4], 16))
        + 0.0722 * canale(int(h[4:6], 16))
    )


def contrasto(a: float, b: float) -> float:
    chiaro, scuro = max(a, b), min(a, b)
    return (chiaro + 0.05) / (scuro + 0.05)


def main() -> int:
    if not CARTELLA.is_dir():
        print(f"  cartella non trovata: {CARTELLA}")
        print("  esegui prima: node scripts/fotografa_cieli.mjs <indirizzo>")
        return 1

    immagini = sorted(CARTELLA.glob("*.png"))
    if not immagini:
        print("  nessuna immagine: esegui prima fotografa_cieli.mjs")
        return 1

    l_principale = lum(PRINCIPALE)
    l_secondario = lum(SECONDARIO)
    problemi = 0

    print(f"  {'cielo':<16} {'fondo piu scuro':<18} {'principale':>11} {'secondario':>11}")
    print("  " + "-" * 60)

    for percorso in immagini:
        with Image.open(percorso) as im:
            rgb = im.convert("RGB")
            # Il pixel peggiore: quello con la luminanza più bassa.
            peggiore = min(
                (
                    0.2126 * canale(r) + 0.7152 * canale(g) + 0.0722 * canale(b),
                    (r, g, b),
                )
                for r, g, b in rgb.getdata()
            )
        l_fondo, colore = peggiore

        cp = contrasto(l_principale, l_fondo)
        cs = contrasto(l_secondario, l_fondo)
        esito = ""
        if cp < SOGLIA or cs < SOGLIA:
            esito = "  <-- SOTTO SOGLIA"
            problemi += 1

        print(
            f"  {percorso.stem:<16} #{colore[0]:02x}{colore[1]:02x}{colore[2]:02x}"
            f"{'':<8} {cp:>9.2f}:1 {cs:>9.2f}:1{esito}"
        )

    print()
    if problemi:
        print(f"  CIELI SOTTO SOGLIA: {problemi} (serve {SOGLIA}:1)")
        return 1

    print(f"  tutti i cieli sopra {SOGLIA}:1, sia per i testi principali sia per i secondari")
    return 0


if __name__ == "__main__":
    sys.exit(main())
