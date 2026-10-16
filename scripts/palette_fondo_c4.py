"""
Palette completa per il fondo #C4C4C4 richiesto dal committente.

Il fondo scuro non è una riga sola: cambia il contrasto di ogni testo e il
rapporto fra il fondo e tutto quello che ci sta sopra (pannelli, bordi, la
fascia ocra, il fondo della pagina Camere). Qui si calcola tutto insieme, così
si applica una palette coerente invece di rattoppare un tono alla volta.
"""

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


# --- Palette candidata sul fondo richiesto ---------------------------------
FONDO = "#c4c4c4"  # come richiesto, esatto
PANNELLO = "#e9e7e2"  # pannelli: uno scalino chiaro, non bianco abbagliante
BORDO = "#aeaba3"  # deve essere PIU' SCURO del fondo
DIVISORIO = "#9f9c94"
NOTE = "#4e4b45"
ETICHETTE = "#63421f"
CAMERE = "#b6bbae"  # fondo proprio della pagina Camere, piu' scuro e verdino
OCRA = "#c9a96b"
OCRA_SCURO = "#b08f4d"

print("=" * 74)
print(f"PALETTE SUL FONDO {FONDO} (luminanza {lum(FONDO):.3f})")
print("=" * 74)
print()

print("--- testo sul fondo della pagina ---")
for t, n in [
    ("#1c1b19", "titoli      stone-900"),
    ("#232220", "corpo       stone-800"),
    ("#4f4c46", "testo       stone-600"),
    (NOTE, "note        stone-500"),
    (ETICHETTE, "etichette   wood-500"),
]:
    r = cr(t, FONDO)
    print(f"  {n}  {t}   {r:5.2f}:1  {'OK' if r >= 4.5 else 'SOTTO SOGLIA'}")
print()

print("--- testo sui pannelli ---")
for t, n in [
    ("#1c1b19", "titoli"),
    ("#4f4c46", "testo"),
    (NOTE, "note"),
    (ETICHETTE, "etichette"),
]:
    r = cr(t, PANNELLO)
    print(f"  {n:12} {t}   {r:5.2f}:1  {'OK' if r >= 4.5 else 'SOTTO SOGLIA'}")
print()

print("--- testo sul fondo della pagina Camere ---")
for t, n in [
    ("#1c1b19", "titoli"),
    ("#4f4c46", "testo"),
    (NOTE, "note"),
    (ETICHETTE, "etichette"),
]:
    r = cr(t, CAMERE)
    print(f"  {n:12} {t}   {r:5.2f}:1  {'OK' if r >= 4.5 else 'SOTTO SOGLIA'}")
print()

print("--- gli elementi si distinguono dal fondo? ---")
for n, c, minimo in [
    ("pannelli", PANNELLO, 1.1),
    ("fondo Camere", CAMERE, 1.1),
    ("bordi", BORDO, 1.1),
    ("divisori", DIVISORIO, 1.2),
    ("fascia ocra", OCRA, 1.2),
]:
    r = cr(c, FONDO)
    verso = "piu' chiaro" if lum(c) > lum(FONDO) else "piu' scuro"
    print(f"  {n:14} {c}  {r:4.2f}:1  ({verso})  {'OK' if r >= minimo else 'TROPPO VICINO'}")
print()

print("--- la fascia ocra ---")
print(f"  testo scuro #1c1b19 su ocra      {cr('#1c1b19', OCRA):5.2f}:1")
print(f"  testo scuro su ocra al passaggio {cr('#1c1b19', OCRA_SCURO):5.2f}:1")
print()

print("--- testo chiaro sui fondi scuri (invariato) ---")
for t, n in [("#f5f3ef", "stone-50"), ("#e5e1d8", "stone-200"), ("#c4beb3", "stone-300")]:
    print(f"  {n:12} su bosco #1e2a21  {cr(t, '#1e2a21'):5.2f}:1")
print()

print("--- il focus da tastiera ---")
print(f"  #232220 sul fondo {FONDO}   {cr('#232220', FONDO):5.2f}:1")
print(f"  ocra sul fondo               {cr(OCRA, FONDO):5.2f}:1")
