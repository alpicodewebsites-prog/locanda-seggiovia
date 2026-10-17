"""Alleggerisce il velo sopra la fotografia degli gnocchi."""

from __future__ import annotations

import pathlib

CSS = pathlib.Path(__file__).resolve().parent.parent / "src" / "styles" / "global.css"

SOSTITUZIONI = [
    (
        "background-color: color-mix(in srgb, var(--color-wood-900) 62%, transparent);",
        "background-color: color-mix(in srgb, var(--color-wood-900) 34%, transparent);",
    ),
    (
        "      color-mix(in srgb, var(--color-wood-900) 40%, transparent),\n"
        "      color-mix(in srgb, var(--color-wood-900) 70%, transparent)",
        "      color-mix(in srgb, var(--color-wood-900) 22%, transparent),\n"
        "      color-mix(in srgb, var(--color-wood-900) 46%, transparent)",
    ),
]


def main() -> int:
    testo = CSS.read_text(encoding="utf-8")
    fatte = 0
    for vecchio, nuovo in SOSTITUZIONI:
        if vecchio in testo:
            testo = testo.replace(vecchio, nuovo)
            fatte += 1
        else:
            print(f"  NON TROVATO: {vecchio[:60]}")
    CSS.write_text(testo, encoding="utf-8", newline="")
    print(f"  sostituzioni fatte: {fatte}/{len(SOSTITUZIONI)}")
    return 0 if fatte == len(SOSTITUZIONI) else 1


if __name__ == "__main__":
    raise SystemExit(main())
