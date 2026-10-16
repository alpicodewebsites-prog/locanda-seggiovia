"""
Separa le fotografie della PAGINA Sentieri da quelle dei singoli sentieri.

Il problema: `sentieri/` conteneva due cose diverse — le copertine dei sei
itinerari e le due fotografie della pagina che li elenca. Aprendo un campo, la
libreria mostrava tutte e otto insieme, e non si capiva quali fossero le une e
quali le altre.

Ora:
    sentieri/         solo le copertine dei sentieri
    sentieri-pagina/  le fotografie della pagina che li elenca

Uso:  python scripts/separa_pagina_sentieri.py
"""

from __future__ import annotations

import pathlib
import shutil
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
ASSETS = RADICE / "src" / "assets"

DA_SPOSTARE = ["montagne.jpg", "panorama.jpg"]


def main() -> int:
    origine = ASSETS / "sentieri"
    destinazione = ASSETS / "sentieri-pagina"
    destinazione.mkdir(parents=True, exist_ok=True)

    spostati = 0
    for nome in DA_SPOSTARE:
        file = origine / nome
        if not file.is_file():
            print(f"  non trovato: sentieri/{nome}")
            continue
        shutil.move(str(file), str(destinazione / nome))
        spostati += 1
        print(f"  sentieri/{nome}  ->  sentieri-pagina/{nome}")

    # Aggiorna il riferimento nel file di contenuto.
    contenuto = RADICE / "src" / "content" / "sentieri-pagina" / "pagina.md"
    if contenuto.is_file():
        testo = contenuto.read_text(encoding="utf-8")
        prima = testo
        for nome in DA_SPOSTARE:
            testo = testo.replace(f"/assets/sentieri/{nome}", f"/assets/sentieri-pagina/{nome}")
        if testo != prima:
            contenuto.write_text(testo, encoding="utf-8", newline="")
            print("  aggiornato src/content/sentieri-pagina/pagina.md")

    print(f"\n  file spostati: {spostati}")

    # Controllo: nessun riferimento rotto.
    import re

    rotti = 0
    for md in sorted((RADICE / "src" / "content").rglob("*.md")):
        for riga in md.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\s*(foto|immagine|hero|panorama|montagne|facciata|cucina|fotoPreparazione):\s*(\S+)\s*$", riga)
            if m and m.group(2).startswith("/assets/"):
                if not (ASSETS / m.group(2).removeprefix("/assets/")).is_file():
                    print(f"  ROTTO {md.name}: {m.group(2)}")
                    rotti += 1

    print(f"  riferimenti rotti: {rotti}")
    return 1 if rotti else 0


if __name__ == "__main__":
    sys.exit(main())
