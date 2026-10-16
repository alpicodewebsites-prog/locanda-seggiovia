"""Verifica la palette candidata prima di applicarla."""

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


def calore(h: str) -> int:
    h = h.lstrip("#")
    return int(h[0:2], 16) - int(h[4:6], 16)


# Palette candidata
FONDO = "#e2ded5"
PANNELLO = "#f5f3ef"
CAMERE = "#dbdfd6"

print("=== quanto cambia il fondo ===")
for nome, c in [("attuale", "#ebe9e4"), ("proposto", FONDO), ("#e5e5e5 (tuo)", "#e5e5e5"), ("#eaeaea (tuo)", "#eaeaea")]:
    print(f"  {nome:16} {c}  luminanza {lum(c):.3f}  calore {calore(c):+d}")
print()

print("=== testo sul fondo della pagina ===")
TESTI = {
    "#1c1b19": "titoli (stone-900)",
    "#232220": "corpo (stone-800)",
    "#4f4c46": "testo (stone-600)",
    "#605d56": "note (stone-500 nuovo)",
    "#78542b": "etichette (wood-500 nuovo)",
}
for t, n in TESTI.items():
    r = cr(t, FONDO)
    print(f"  {n:28} {r:5.2f}:1  {'OK' if r >= 4.5 else 'SOTTO SOGLIA'}")
print()

print("=== testo sul fondo dei pannelli ===")
for t, n in TESTI.items():
    r = cr(t, PANNELLO)
    print(f"  {n:28} {r:5.2f}:1  {'OK' if r >= 4.5 else 'SOTTO SOGLIA'}")
print()

print("=== pagina Camere: fondo verde desaturato ===")
for t, n in TESTI.items():
    r = cr(t, CAMERE)
    print(f"  {n:28} {r:5.2f}:1  {'OK' if r >= 4.5 else 'SOTTO SOGLIA'}")
print()

print("=== il fondo Camere si distingue dalla pagina? ===")
print(f"  pagina {FONDO} lum {lum(FONDO):.3f}   camere {CAMERE} lum {lum(CAMERE):.3f}")
print(f"  differenza di luminanza: {abs(lum(FONDO) - lum(CAMERE)):.4f}")
print()

print("=== bordi: devono restare visibili sul nuovo fondo ===")
for b in ["#d3cfc6", "#c4beb3", "#dfdcd5"]:
    print(f"  {b}  luminanza {lum(b):.3f}  contrasto col fondo {cr(b, FONDO):.2f}:1")
print()

print("=== testo chiaro sui fondi scuri: invariato? ===")
for t, n in [("#f5f3ef", "stone-50"), ("#dfdcd5", "stone-200"), ("#c4beb3", "stone-300")]:
    print(f"  {n:12} su #1e2a21 (bosco) {cr(t, '#1e2a21'):5.2f}:1   su #232220 (scuro) {cr(t, '#232220'):5.2f}:1")
print()

print("=== la fascia ocra sul nuovo fondo ===")
print(f"  testo scuro su ocra #c9a96b      {cr('#1c1b19', '#c9a96b'):5.2f}:1")
print(f"  ocra contro il fondo pagina      {cr('#c9a96b', FONDO):5.2f}:1")
