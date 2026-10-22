"""Porta il logo dell'header a 48 px, per dargli piu' presenza."""

from __future__ import annotations

import pathlib

HEADER = (
    pathlib.Path(__file__).resolve().parent.parent / "src" / "components" / "Header.astro"
)

SOSTITUZIONI = [
    ('width="47"', 'width="62"'),
    ('height="36"', 'height="48"'),
    ('class="site-header__logo hidden h-9 w-auto', 'class="site-header__logo hidden h-12 w-auto'),
]


def main() -> int:
    testo = HEADER.read_text(encoding="utf-8")
    fatte = 0
    for vecchio, nuovo in SOSTITUZIONI:
        if vecchio in testo:
            testo = testo.replace(vecchio, nuovo, 1)
            fatte += 1
        else:
            print(f"  NON TROVATO: {vecchio}")
    HEADER.write_text(testo, encoding="utf-8", newline="")
    print(f"  sostituzioni: {fatte}/{len(SOSTITUZIONI)}")
    return 0 if fatte == len(SOSTITUZIONI) else 1


if __name__ == "__main__":
    raise SystemExit(main())
