"""
Verifica i contrasti del pulsante trasparente su fondo grigio scuro.

Il pulsante non ha più un fondo proprio: il testo e il bordo sono gialli e
stanno direttamente sul grigio della fascia. Quindi i contrasti vanno
verificati contro il fondo della fascia, non contro il giallo.

Servono due soglie diverse:
  4,5:1 per il TESTO  (WCAG 1.4.3)
  3,0:1 per il BORDO  (WCAG 1.4.11 — è il contorno che identifica il comando)
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


def calore(h: str) -> int:
    h = h.lstrip("#")
    return int(h[0:2], 16) - int(h[4:6], 16)


GIALLO = "#c9a96b"  # --color-accento
GIALLO_CHIARO = "#e0c48f"  # per il passaggio del mouse

print("=== fondo della fascia: un solo colore, fra il nero e il grigio ===")
for fondo in ["#1c1b19", "#232220", "#2b2a26", "#333330", "#37352f", "#3f3d38"]:
    t = cr(GIALLO, fondo)
    t2 = cr(GIALLO_CHIARO, fondo)
    esito = "OK" if t >= 4.5 else "SOTTO SOGLIA"
    verso = "quasi nero" if lum(fondo) < 0.02 else "grigio scuro"
    print(
        f"  {fondo}  luminanza {lum(fondo):.3f} calore {calore(fondo):+d}  "
        f"testo {t:5.2f}:1  (passaggio {t2:5.2f}:1)  {esito}   [{verso}]"
    )

print()
print("=== il bordo: serve 3:1 ===")
for fondo in ["#2b2a26", "#333330"]:
    print(f"  bordo {GIALLO} su {fondo}  ->  {cr(GIALLO, fondo):5.2f}:1")
