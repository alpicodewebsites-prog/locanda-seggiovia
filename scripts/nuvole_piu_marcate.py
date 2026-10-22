"""Rende piu' marcate le nuvole, restando dentro le soglie di contrasto."""

from __future__ import annotations

import pathlib

COMPONENTE = (
    pathlib.Path(__file__).resolve().parent.parent
    / "src"
    / "components"
    / "MeteoSentiero.astro"
)

# (vecchio, nuovo) sull'alfa delle nuvole. Il grigio resta lo stesso: cambia
# quanto e' denso. Il temporale non si tocca, e' gia' scuro.
SOSTITUZIONI = [
    ("rgba(120, 123, 118, 0.30)", "rgba(120, 123, 118, 0.44)"),
    ("rgba(120, 123, 118, 0.24)", "rgba(120, 123, 118, 0.34)"),
    ("rgba(118, 121, 116, 0.34)", "rgba(118, 121, 116, 0.54)"),
    ("rgba(118, 121, 116, 0.30)", "rgba(118, 121, 116, 0.48)"),
    ("rgba(118, 121, 116, 0.26)", "rgba(118, 121, 116, 0.42)"),
    ("rgba(118, 121, 116, 0.20)", "rgba(118, 121, 116, 0.34)"),
    ("rgba(112, 116, 116, 0.34)", "rgba(112, 116, 116, 0.50)"),
    ("rgba(112, 116, 116, 0.28)", "rgba(112, 116, 116, 0.42)"),
    ("rgba(130, 136, 137, 0.28)", "rgba(130, 136, 137, 0.44)"),
    ("rgba(130, 136, 137, 0.24)", "rgba(130, 136, 137, 0.36)"),
]


def main() -> int:
    testo = COMPONENTE.read_text(encoding="utf-8")
    fatte = 0
    for vecchio, nuovo in SOSTITUZIONI:
        if vecchio in testo:
            testo = testo.replace(vecchio, nuovo)
            fatte += 1
        else:
            print(f"  non trovato: {vecchio}")
    COMPONENTE.write_text(testo, encoding="utf-8", newline="")
    print(f"  alfa delle nuvole alzate: {fatte}/{len(SOSTITUZIONI)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
