"""
Le schede inglesi del menù.

Ogni file riprende i campi dell'originale e traduce solo il nome e la
descrizione. `categoria`, `ordine`, `specialita` e `foto` restano identici: sono
dati, non testo, e sbagliarli cambierebbe l'ordine del menù o farebbe sparire una
fotografia. `prezzo` resta assente, perché è assente nell'originale: non si
inventa un prezzo per poter dire di aver tradotto tutto.

Uso:  python scripts/traduce_menu.py
"""

from __future__ import annotations

import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
CARTELLA = RADICE / "src" / "content" / "menu"

# nome file -> (nome inglese, descrizione inglese)
SCHEDE = {
    "tagliere-di-malga": (
        "Malga cheese board",
        "Local malga cheeses with honey and our own mostarda.",
    ),
    "trota-affumicata": (
        "Smoked trout",
        "Lightly smoked, served cold with a citronette. This is how it starts.",
    ),
    "sopressa-fatta-in-casa": (
        "House-made sopressa",
        "Cured and aged by us, served with our own pickles.",
    ),
    "bacala-alla-vicentina": (
        "Bacalà alla vicentina",
        "Stockfish, soaked and cooked slowly with milk and onion, served with "
        "polenta. The dish nobody in Vicenza argues about.",
    ),
    "bigoli-con-anatra": (
        "Bigoli with duck",
        "Fresh pasta pressed through the torchio, with a long-cooked duck ragù.",
    ),
    "gnocchi-con-la-fioreta": (
        "Gnocchi con la Fioreta",
        "The house dish, De.Co. recognised, with browned malga butter and aged "
        "cheese.",
    ),
    "formaggio-malga-miele": (
        "Malga cheese with honey",
        "Aged malga cheese served with honey from the area.",
    ),
}

# I campi che NON si traducono, letti dall'originale.
DA_COPIARE = ("categoria", "ordine", "specialita", "foto", "prezzo")


def valore_originale(testo: str, chiave: str) -> str | None:
    """Legge il valore di un campo semplice dal frontmatter originale."""
    for riga in testo.splitlines():
        if riga.startswith(f"{chiave}:"):
            return riga.split(":", 1)[1].strip()
    return None


def main() -> int:
    for nome, (nome_en, descrizione_en) in SCHEDE.items():
        originale = CARTELLA / f"{nome}.md"
        if not originale.exists():
            print(f"  MANCA: {originale.name}")
            continue

        testo = originale.read_text(encoding="utf-8")

        righe = [
            "---",
            f"nome: {nome_en}",
        ]
        for chiave in DA_COPIARE:
            valore = valore_originale(testo, chiave)
            if valore is not None:
                righe.append(f"{chiave}: {valore}")

        # La descrizione in stile ripiegato, come negli originali.
        righe.append("descrizione: >-")
        parole = descrizione_en.split()
        riga = "  "
        for parola in parole:
            if len(riga) + len(parola) + 1 > 78:
                righe.append(riga.rstrip())
                riga = "  "
            riga += parola + " "
        righe.append(riga.rstrip())
        righe.append("---")
        righe.append("")

        destinazione = CARTELLA / f"{nome}-en.md"
        destinazione.write_text("\n".join(righe), encoding="utf-8", newline="")
        print(f"  {destinazione.name}")

    print(f"  schede scritte: {len(SCHEDE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
