"""
Controlla che ogni contenuto abbia la sua versione inglese.

PERCHÉ SERVE
Il codice ripiega sull'italiano quando la traduzione manca: è giusto, perché una
pagina inglese con un testo italiano dentro è meglio di una pagina che non si
compila. Ma il ripiego è SILENZIOSO, e un sito mezzo tradotto che nessuno nota è
esattamente il modo in cui questi lavori restano a metà.

Questo controllo elenca le schede senza traduzione, e segnala i file inglesi che
contengono ancora parole italiane.

Uso:  python scripts/verifica_traduzioni.py
"""

from __future__ import annotations

import pathlib
import re
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
CONTENUTI = RADICE / "src" / "content"

# Le stesse collezioni dichiarate in src/content.config.ts.
COLLEZIONI = [
    "home",
    "la-locanda",
    "sentieri-pagina",
    "gnocchi",
    "camere",
    "menu",
    "sentieri",
]

# File che non contengono testo: non hanno bisogno di traduzione.
SENZA_TESTO = {"foto.md"}

# Parole che in un file inglese non dovrebbero comparire, escluse quelle che sono
# nomi propri o nomi di piatti (che restano in italiano di proposito).
PAROLE_ITALIANE = [
    "della",
    "degli",
    "nella",
    "negli",
    "sono",
    "questo",
    "questa",
    "anche",
    "solo",
    "sempre",
    "perché",
    "essere",
    "viene",
    "hanno",
    "dopo",
    "senza",
]

# Nomi e parole che restano in italiano di proposito.
CONSENTITE = {
    "sentiero",
    "sentieri",
    "rifugio",
    "malga",
    "malghe",
    "fioreta",
    "recoaro",
    "piccole",
    "dolomiti",
    "pasubio",
    "carega",
    "campogrosso",
    "gnocchi",
    "sopressa",
    "bigoli",
    "bacalà",
    "vicentina",
    "asnicar",
    "bertoldi",
    "seggiovia",
    "locanda",
    "cai",
    "avis",
    "bocchetta",
    "campiglia",
    "fugazze",
    "soldà",
    "spitz",
    "gallerie",
    "anello",
    "storico",
    "orso",
    "gallo",
    "mole",
    "alberi",
    "grandi",
    "requaro",
    "festa",
    "nonna",
    "maria",
    "deco",
    "de.co",
    "vicenza",
    "veneto",
    "agno",
    "sengio",
    "alto",
    "pasubio",
}


def main() -> int:
    mancanti: list[str] = []
    sospetti: list[tuple[str, list[str]]] = []
    coppie = 0

    for collezione in COLLEZIONI:
        cartella = CONTENUTI / collezione
        if not cartella.is_dir():
            continue

        italiani = sorted(
            p for p in cartella.glob("*.md") if not p.stem.endswith("-en") and p.name not in SENZA_TESTO
        )
        inglesi = {p.stem for p in cartella.glob("*-en.md")}

        for italiano in italiani:
            coppie += 1
            atteso = f"{italiano.stem}-en"
            if atteso not in inglesi:
                mancanti.append(f"{collezione}/{italiano.name}")
                continue

            # Il file esiste: si guarda se dentro è rimasto italiano.
            testo_inglese = (cartella / f"{atteso}.md").read_text(encoding="utf-8").lower()
            trovate = [
                parola
                for parola in PAROLE_ITALIANE
                if parola not in CONSENTITE and re.search(rf"\b{parola}\b", testo_inglese)
            ]
            if trovate:
                sospetti.append((f"{collezione}/{atteso}.md", trovate))

    print(f"  schede di contenuto: {coppie}")
    print(f"  tradotte: {coppie - len(mancanti)}")
    print()

    if mancanti:
        print(f"  SENZA TRADUZIONE ({len(mancanti)}):")
        for voce in mancanti:
            print(f"    {voce}")
        print()

    if sospetti:
        print("  DA RILEGGERE (contengono parole italiane):")
        for nome, parole in sospetti:
            print(f"    {nome}: {', '.join(parole)}")
        print()

    if mancanti:
        print(f"  ESITO: mancano {len(mancanti)} traduzioni")
        return 1

    print("  ESITO: tutte le schede hanno la versione inglese")
    if sospetti:
        print(f"  ({len(sospetti)} file da rileggere a occhio, ma nessuna traduzione manca)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
