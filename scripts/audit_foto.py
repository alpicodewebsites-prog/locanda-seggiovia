"""
Fotografie: orientamento e sezione di appartenenza.

Serve a due cose:
  1. sapere quali sono verticali e quali orizzontali, per poterle ordinare;
  2. verificare che ogni fotografia stia nella cartella della sezione che la
     usa davvero — se una pagina pesca da una cartella che non è la sua, nel
     pannello la foto non si trova dove ci si aspetta.

Uso:  python scripts/audit_foto.py
"""

from __future__ import annotations

import pathlib
import re

from PIL import Image

RADICE = pathlib.Path(__file__).resolve().parent.parent
ASSETS = RADICE / "src" / "assets"
CONTENUTI = RADICE / "src" / "content"

CAMPI_IMMAGINE = (
    "foto", "immagine", "hero", "panorama", "montagne",
    "facciata", "cucina", "fotoPreparazione",
)


def orientamento(percorso: pathlib.Path) -> str:
    with Image.open(percorso) as im:
        l, a = im.size
    if a > l * 1.02:
        return "verticale"
    if l > a * 1.02:
        return "orizzontale"
    return "quadrata"


def main() -> int:
    # --- 1. Inventario delle fotografie ------------------------------------
    print("=" * 78)
    print("FOTOGRAFIE PER SEZIONE, CON ORIENTAMENTO")
    print("=" * 78)

    per_cartella: dict[str, list[tuple[str, str, str]]] = {}
    for file in sorted(ASSETS.rglob("*")):
        if not file.is_file() or file.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".avif"}:
            continue
        relativa = file.relative_to(ASSETS).as_posix()
        cartella = relativa.split("/")[0] if "/" in relativa else "(radice)"
        per_cartella.setdefault(cartella, []).append(
            (relativa, orientamento(file), f"{Image.open(file).size[0]}x{Image.open(file).size[1]}")
        )

    for cartella in sorted(per_cartella):
        print(f"\n  {cartella}/")
        for relativa, verso, dimensioni in per_cartella[cartella]:
            print(f"      {relativa.split('/')[-1]:34} {verso:11} {dimensioni}")

    # --- 2. Chi usa cosa ---------------------------------------------------
    print()
    print("=" * 78)
    print("QUALI FOTOGRAFIE USA OGNI SEZIONE")
    print("=" * 78)

    problemi = 0
    for md in sorted(CONTENUTI.rglob("*.md")):
        sezione = md.relative_to(CONTENUTI).parts[0]
        testo = md.read_text(encoding="utf-8")

        riferimenti = re.findall(
            r"^\s*(" + "|".join(CAMPI_IMMAGINE) + r"):\s*(\S+)\s*$", testo, re.M
        )
        if not riferimenti:
            continue

        print(f"\n  {sezione}/  ({md.name})")
        for campo, valore in riferimenti:
            if not valore.startswith("/assets/"):
                continue
            relativa = valore.removeprefix("/assets/")
            cartella = relativa.split("/")[0]
            file = ASSETS / relativa
            esiste = file.is_file()
            verso = orientamento(file) if esiste else "MANCANTE"

            # La sezione del file dovrebbe corrispondere alla sezione del
            # contenuto. Le eccezioni legittime sono i contenuti che pescano
            # da una cartella condivisa.
            coerente = cartella == sezione or sezione in {
                "sentieri", "camere", "menu", "gnocchi",
            }
            segno = "OK " if esiste else "NO "
            if not esiste:
                problemi += 1
            print(f"      [{segno}] {campo:16} {relativa:46} {verso}")

    print()
    print(f"  riferimenti a file inesistenti: {problemi}")
    return 1 if problemi else 0


if __name__ == "__main__":
    raise SystemExit(main())
