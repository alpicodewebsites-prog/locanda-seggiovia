"""Conseguenze del fondo #C4C4C4 sui contrasti e sugli altri elementi."""

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


ATTUALE = "#e2ded5"
CANDIDATI = ["#c4c4c4", "#b0b0b0"]

print("=== i fondi richiesti ===")
for c in [ATTUALE] + CANDIDATI:
    nome = "attuale " if c == ATTUALE else "richiesto"
    print(f"  {nome} {c}   luminanza {lum(c):.3f}   calore {calore(c):+d}")
print()

TESTI = {
    "#1c1b19": "titoli      stone-900",
    "#232220": "corpo       stone-800",
    "#4f4c46": "testo       stone-600",
    "#605d56": "note        stone-500",
    "#78542b": "etichette   wood-500",
}

for fondo in CANDIDATI:
    print(f"=== testo su {fondo} ===")
    for t, n in TESTI.items():
        r = cr(t, fondo)
        esito = "OK" if r >= 4.5 else "SOTTO SOGLIA"
        print(f"  {n}   {r:5.2f}:1   {esito}")
    print()

print("=== quali toni servirebbero per stare sopra 4,5:1 su #c4c4c4 ===")
F = "#c4c4c4"
for t in ["#605d56", "#5a5750", "#54514b", "#4e4b45"]:
    print(f"  note      {t}  {cr(t, F):.2f}:1")
for t in ["#78542b", "#714e27", "#6a4823", "#63421f"]:
    print(f"  etichette {t}  {cr(t, F):.2f}:1")
print()

print("=== altri elementi sul fondo #c4c4c4 ===")
for nome, colore in [
    ("pannelli stone-50", "#f5f3ef"),
    ("fondo Camere", "#d5dacd"),
    ("fascia ocra", "#c9a96b"),
    ("bordi stone-200", "#d3cfc6"),
]:
    print(f"  {nome:20} {colore}  contro il fondo: {cr(colore, F):.2f}:1   (calore {calore(colore):+d})")
print()
print("  ^ un contrasto vicino a 1:1 significa che l'elemento si confonde col fondo.")
