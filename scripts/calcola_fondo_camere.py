"""Cerca un fondo per la pagina Camere che si distingua davvero da quello del sito."""

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


def verde(h: str) -> int:
    """Quanto e' verde: canale verde meno la media di rosso e blu."""
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return g - (r + b) // 2


PAGINA = "#e2ded5"

print(f"fondo del sito: {PAGINA}  luminanza {lum(PAGINA):.3f}")
print()
print("candidati per la pagina Camere:")
print(f"  {'colore':9} {'luminanza':>9} {'stacco':>7} {'verde':>6}   note 4,5:1   etich. 4,5:1")
for c in ["#dbdfd6", "#d8ddd2", "#d5dacd", "#d1d7c8", "#ccd3c3", "#c8d0be"]:
    stacco = abs(lum(PAGINA) - lum(c))
    note = cr("#605d56", c)
    etich = cr("#78542b", c)
    corpo = cr("#4f4c46", c)
    segno_n = "OK" if note >= 4.5 else "NO"
    segno_e = "OK" if etich >= 4.5 else "NO"
    print(
        f"  {c:9} {lum(c):9.3f} {stacco:7.4f} {verde(c):6d}     {note:4.2f} {segno_n}      {etich:4.2f} {segno_e}"
    )
print()
print("esito: uno stacco di luminanza sotto 0,02 non si percepisce;")
print("       sopra 0,04 il fondo si distingue a colpo d'occhio.")
