"""
Sposta i contenuti inglesi in una sottocartella `en/`.

DA DOVE VIENE QUESTA SCELTA

Perché il pannello possa mostrare le due lingue, ogni versione deve stare in un
posto che si possa indicare con una regola sola. Due strade:

  a) la funzione multilingua del pannello, che però nomina i file `testi.it.md` e
     `testi.en.md`. Astro toglie il punto dall'identificativo, quindi gli id
     diventano `testiit` e `testien`: ambigui, e per giunta un sentiero il cui
     nome finisse per «en» verrebbe scambiato per una traduzione.
  b) una sottocartella `en/`: l'identificativo diventa `en/testi`, che si legge,
     non si confonde con niente, e si può indicare al pannello come cartella.

Ho scelto (b). Il prezzo è che il pannello avrà due voci per ogni collezione —
«Sentieri (elenco)» e «Sentieri — English» — invece di una sola con il selettore
di lingua. Per una persona che non programma è anzi più chiaro: sa di stare
modificando la versione inglese.

Uso:  python scripts/contenuti_in_cartelle_lingua.py
"""

from __future__ import annotations

import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
CONTENUTI = RADICE / "src" / "content"

COLLEZIONI = [
    "home",
    "la-locanda",
    "sentieri-pagina",
    "gnocchi",
    "camere",
    "menu",
    "sentieri",
]


def main() -> int:
    spostati = 0

    for collezione in COLLEZIONI:
        cartella = CONTENUTI / collezione
        if not cartella.is_dir():
            continue

        inglesi = sorted(cartella.glob("*-en.md"))
        if not inglesi:
            continue

        destinazione = cartella / "en"
        destinazione.mkdir(exist_ok=True)

        for file in inglesi:
            # `gino-solda-en.md` → `en/gino-solda.md`
            nuovo_nome = file.name[: -len("-en.md")] + ".md"
            nuova = destinazione / nuovo_nome
            if nuova.exists():
                print(f"  ATTENZIONE: {nuova} esiste già, salto {file.name}")
                continue
            file.rename(nuova)
            spostati += 1
            print(f"  {collezione}/{file.name} -> {collezione}/en/{nuovo_nome}")

    print(f"  file spostati: {spostati}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
