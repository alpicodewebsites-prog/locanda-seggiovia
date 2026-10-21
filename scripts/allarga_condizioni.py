"""Allarga la colonna delle condizioni e stringe quella del racconto."""

from __future__ import annotations

import pathlib

PAGINA = (
    pathlib.Path(__file__).resolve().parent.parent
    / "src"
    / "pages"
    / "sentieri"
    / "[id].astro"
)

SOSTITUZIONI = [
    # Il racconto resta su 6 colonne: la misura di lettura non cambia, perché
    # il testo ha già `max-w-[62ch]`.
    ('<div class="md:col-span-7">', '<div class="md:col-span-6">'),
    # Le condizioni passano da 4 a 5 colonne, e cominciano all'ottava: resta
    # la settima libera come spazio fra le due.
    (
        'class="flex flex-col gap-5 md:col-span-4 md:col-start-9"',
        'class="flex flex-col gap-5 md:col-span-5 md:col-start-8"',
    ),
]


def main() -> int:
    testo = PAGINA.read_text(encoding="utf-8")
    fatte = 0
    for vecchio, nuovo in SOSTITUZIONI:
        if vecchio in testo:
            testo = testo.replace(vecchio, nuovo, 1)
            fatte += 1
        else:
            print(f"  NON TROVATO: {vecchio[:60]}")
    PAGINA.write_text(testo, encoding="utf-8", newline="")
    print(f"  sostituzioni: {fatte}/{len(SOSTITUZIONI)}")
    return 0 if fatte == len(SOSTITUZIONI) else 1


if __name__ == "__main__":
    raise SystemExit(main())
