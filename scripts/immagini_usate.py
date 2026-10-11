"""
Elenca le immagini di src/assets e dice quali sono usate e quali no.

Serve a due cose: documentare con precisione dove appare ogni fotografia, e
accorgersi se dopo un cambio di impaginazione restano file orfani che nessuno
usa più (peso inutile nel repository e confusione nella libreria del pannello).

Uso:  python scripts/immagini_usate.py
"""

from __future__ import annotations

import pathlib
import re
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
ASSETS = RADICE / "src" / "assets"

# Dove cercare i riferimenti: contenuti, impostazioni e codice delle pagine
CARTELLE_RIFERIMENTI = ["src/content", "src/pages", "src/components", "src/lib", "src/layouts"]

# File da ignorare nella ricerca: contengono nomi di immagini negli esempi e nei
# commenti, quindi farebbero risultare "usata" un'immagine che nessuna pagina
# mostra davvero.
FILE_IGNORATI = {"src/lib/immagini.ts"}


def main() -> int:
    if not ASSETS.is_dir():
        print("cartella src/assets non trovata")
        return 1

    immagini = sorted(p.name for p in ASSETS.iterdir() if p.is_file())

    # Raccoglie tutti i testi in cui possono comparire i nomi dei file
    testi: list[tuple[pathlib.Path, str]] = []
    for cartella in CARTELLE_RIFERIMENTI:
        base = RADICE / cartella
        if not base.is_dir():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".md", ".astro", ".ts", ".mjs"}:
                relativo = str(p.relative_to(RADICE)).replace("\\", "/")
                if relativo in FILE_IGNORATI:
                    continue
                testi.append((p, p.read_text(encoding="utf-8")))

    usate: dict[str, list[str]] = {}
    orfane: list[str] = []

    for nome in immagini:
        senza_estensione = re.sub(r"\.[a-z0-9]+$", "", nome, flags=re.I)
        dove: list[str] = []

        # Il confronto usa un confine a sinistra: senza di esso «gnocchi-fioreta»
        # combacerebbe dentro «piatto-gnocchi-fioreta», facendo risultare usata
        # un'immagine che nessuno mostra.
        modello = re.compile(
            rf"(?<![\w-])({re.escape(nome)}|{re.escape(senza_estensione)})(?![\w-])"
        )

        for percorso, testo in testi:
            if modello.search(testo):
                dove.append(str(percorso.relative_to(RADICE)))

        if dove:
            usate[nome] = dove
        else:
            orfane.append(nome)

    print("=" * 74)
    print(f"IMMAGINI IN src/assets: {len(immagini)}")
    print("=" * 74)
    print()
    print(f"USATE ({len(usate)}):")
    for nome, dove in usate.items():
        print(f"  {nome}")
        for d in dove:
            print(f"      {d}")
    print()
    print(f"NON USATE ({len(orfane)}):")
    for nome in orfane:
        print(f"  {nome}")
    if not orfane:
        print("  nessuna")

    return 0


if __name__ == "__main__":
    sys.exit(main())
