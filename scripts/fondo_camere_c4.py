"""Trova il fondo della pagina Camere che si distingue dal grigio #C4C4C4 e regge il testo."""

from __future__ import annotations


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


def cr(a: str, b: str) -> float:
    l1, l2 = lum(a), lum(b)
    chiaro, scuro = max(l1, l2), min(l1, l2)
    return (chiaro + 0.05) / (scuro + 0.05)


FONDO = "#c4c4c4"
TESTO = "#4f4c46"
NOTE = "#4e4b45"
ETICHETTE = "#63421f"

print(f"fondo del sito {FONDO}  luminanza {lum(FONDO):.3f}")
print()
print(f"{'colore':9} {'lum':>6} {'vs fondo':>9} {'testo':>7} {'note':>6} {'etich.':>7}   esito")
for c in [
    "#b6bbae",
    "#bcc1b4",
    "#c2c7ba",
    "#c8cdc0",
    "#ced3c6",
    "#d4d9cc",
    "#dadfd2",
]:
    rt, rn, re_ = cr(TESTO, c), cr(NOTE, c), cr(ETICHETTE, c)
    ok = rt >= 4.5 and rn >= 4.5 and re_ >= 4.5
    stacco = cr(c, FONDO)
    print(
        f"{c:9} {lum(c):6.3f} {stacco:9.3f} {rt:7.2f} {rn:6.2f} {re_:7.2f}   "
        + ("tutto OK" if ok else "testo sotto soglia")
    )
print()
print("serve: testo >= 4,50 e stacco dal fondo >= 1,10 perche' si veda")
