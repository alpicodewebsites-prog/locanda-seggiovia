"""
Controlla che i file di testo del progetto siano UTF-8 validi.

Nasce da un problema reale: alcune modifiche fatte con comandi di shell possono
riscrivere un file con una codifica diversa, e allora gli accenti si rompono
senza che nulla segnali l'errore. Il file sembra normale, ma il testo è illeggibile.

Uso:  python scripts/controlla_codifica.py
"""

from __future__ import annotations

import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent

# Cartelle da controllare
CARTELLE = ["src", "public", "docs", "scripts"]
FILE_RADICE = ["README.md", ".gitignore", "package.json", "astro.config.mjs", "tailwind.config.mjs"]

# Estensioni di testo
ESTENSIONI = {".astro", ".ts", ".css", ".md", ".yml", ".yaml", ".json", ".mjs", ".py", ".html", ".txt"}

# Sequenze tipiche di una doppia codifica (UTF-8 letto come Latin-1).
# Sono costruite dai codici numerici di proposito: scritte come testo letterale
# finirebbero dentro questo stesso file, e il controllo segnalerebbe se stesso.
SOSPETTI = [
    chr(0xC3) + chr(0xA8),  # "e" accentata doppiamente codificata
    chr(0xC3) + chr(0xA9),
    chr(0xC3) + chr(0xA0),
    chr(0xC3) + chr(0xB9),
    chr(0xC3) + chr(0xAC),
    chr(0xC3) + chr(0x88),
    chr(0xE2) + chr(0x80),  # trattini e virgolette tipografiche
    chr(0xC2) + chr(0xAB),  # virgolette caporali
    chr(0xC2) + chr(0xBB),
]


def controlla(percorso: pathlib.Path) -> list[str]:
    problemi = []
    try:
        testo = percorso.read_bytes().decode("utf-8")
    except UnicodeDecodeError as e:
        return [f"non è UTF-8 valido: {e}"]

    for sospetto in SOSPETTI:
        if sospetto in testo:
            problemi.append(f"contiene «{sospetto}» (probabile doppia codifica)")
            break

    return problemi


def main() -> int:
    da_controllare: list[pathlib.Path] = []

    for cartella in CARTELLE:
        base = RADICE / cartella
        if base.is_dir():
            da_controllare.extend(
                p for p in base.rglob("*") if p.is_file() and p.suffix.lower() in ESTENSIONI
            )

    for nome in FILE_RADICE:
        p = RADICE / nome
        if p.is_file():
            da_controllare.append(p)

    # node_modules e cartelle di build sono esclusi per costruzione
    problemi_totali = 0
    for p in sorted(da_controllare):
        problemi = controlla(p)
        if problemi:
            problemi_totali += 1
            print(f"  {p.relative_to(RADICE)}")
            for problema in problemi:
                print(f"      {problema}")

    print()
    print(f"file controllati: {len(da_controllare)}")
    if problemi_totali:
        print(f"FILE CON PROBLEMI: {problemi_totali}")
        return 1

    print("tutti i file sono UTF-8 validi e senza segni di doppia codifica")
    return 0


if __name__ == "__main__":
    sys.exit(main())
