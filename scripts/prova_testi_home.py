"""
Prova che i testi della home vengano DAVVERO dal pannello.

Il controllo non è «il campo esiste nella configurazione»: è «cambiando il file
di contenuto, la pagina pubblicata cambia». Sono due cose diverse, e solo la
seconda dimostra che il collegamento funziona.

Procedura: si cambia il titolo nel file di contenuto, si ricompila, si legge il
titolo nella pagina costruita, e si rimette tutto com'era. Se il titolo letto è
quello nuovo, il collegamento è provato.

Uso:  python scripts/prova_testi_home.py
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
CONTENUTO = RADICE / "src" / "content" / "home" / "pagina.md"
PAGINA = RADICE / "dist" / "index.html"

PROVA = "PROVA DI COLLEGAMENTO — questo testo arriva dal pannello"


def compila() -> bool:
    esito = subprocess.run(
        ["npm", "run", "build"],
        cwd=RADICE,
        capture_output=True,
        text=True,
        shell=True,
    )
    return esito.returncode == 0


def titolo_in_pagina() -> str | None:
    if not PAGINA.is_file():
        return None
    html = PAGINA.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if not m:
        return None
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()


def main() -> int:
    originale = CONTENUTO.read_text(encoding="utf-8")

    m = re.search(r"(?m)^titolo:\s*.+$", originale)
    if not m:
        print("campo «titolo» non trovato nel file di contenuto")
        return 1

    print("=== PRIMA ===")
    if not compila():
        print("  compilazione fallita")
        return 1
    prima = titolo_in_pagina()
    print(f"  titolo nella pagina: {prima!r}")

    try:
        # Si sostituisce il titolo, mantenendo il resto del file intatto.
        modificato = originale.replace(m.group(0), f"titolo: '{PROVA}'", 1)
        CONTENUTO.write_text(modificato, encoding="utf-8", newline="")

        print("\n=== DOPO AVER CAMBIATO IL TESTO NEL PANNELLO ===")
        if not compila():
            print("  compilazione fallita")
            return 1
        dopo = titolo_in_pagina()
        print(f"  titolo nella pagina: {dopo!r}")

        collegato = dopo == PROVA
        print(
            "\n  il testo della pagina segue il pannello: "
            + ("SI" if collegato else "NO — il collegamento non funziona")
        )
        return 0 if collegato else 1
    finally:
        # Il file torna SEMPRE com'era, anche se qualcosa va storto.
        CONTENUTO.write_text(originale, encoding="utf-8", newline="")
        compila()
        print("\n  file di contenuto ripristinato e sito ricompilato")


if __name__ == "__main__":
    sys.exit(main())
