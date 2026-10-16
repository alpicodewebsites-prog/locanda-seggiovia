"""
Divide l'ultimo file rimasto e toglie i BOM da tutti i file di contenuto.

Un BOM (Byte Order Mark) è una sequenza invisibile di tre byte in testa al file.
Su Windows alcuni strumenti la aggiungono da soli. In un file Markdown con
frontmatter fa un danno preciso: la prima riga non è più `---` ma
`\ufeff---`, quindi il frontmatter non viene riconosciuto e il file risulta
privo di dati.

Uso:  python scripts/ripara_bom_e_ultimo_file.py
"""

from __future__ import annotations

import pathlib
import re
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
CONTENUTI = RADICE / "src" / "content"

CAMPI_FOTO = {
    "hero", "panorama", "montagne", "facciata", "cucina",
    "foto", "fotoPreparazione", "immagine",
}


def togli_bom() -> int:
    """Toglie il BOM da tutti i file di contenuto. Restituisce quanti ne ha tolti."""
    tolti = 0
    for file in sorted(CONTENUTI.rglob("*.md")):
        grezzo = file.read_bytes()
        if grezzo.startswith(b"\xef\xbb\xbf"):
            file.write_bytes(grezzo[3:])
            print(f"  BOM tolto da {file.relative_to(CONTENUTI)}")
            tolti += 1
    return tolti


def dividi(file: pathlib.Path, cartella: str) -> bool:
    testo = file.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\s*$", testo, re.S)
    if not m:
        print(f"  {file.name}: frontmatter non riconosciuto")
        return False

    testi: list[str] = []
    foto: list[str] = []
    commenti: list[str] = []

    for riga in m.group(1).splitlines():
        spoglia = riga.strip()
        if spoglia.startswith("#") or not spoglia:
            commenti.append(riga)
            continue
        if spoglia.split(":")[0].strip() in CAMPI_FOTO:
            foto.append(riga)
        else:
            testi.append(riga)

    intestazione = "\n".join(commenti).strip()

    (CONTENUTI / cartella / "testi.md").write_text(
        "---\n" + (intestazione + "\n\n" if intestazione else "") + "\n".join(testi) + "\n---\n",
        encoding="utf-8",
        newline="",
    )
    (CONTENUTI / cartella / "foto.md").write_text(
        "---\n"
        "# Fotografie della pagina. Si gestiscono dalla voce «Fotografie» del\n"
        "# pannello, e stanno nella cartella della loro sezione.\n\n"
        + "\n".join(foto)
        + "\n---\n",
        encoding="utf-8",
        newline="",
    )
    file.unlink()
    print(f"  {cartella}/{file.name}  ->  testi.md + foto.md")
    return True


def main() -> int:
    print("=== 1. BOM tolti ===")
    print(f"  file corretti: {togli_bom()}")

    print("\n=== 2. ultimo file diviso ===")
    residuo = CONTENUTI / "sentieri-pagina" / "pagina.md"
    if residuo.is_file():
        dividi(residuo, "sentieri-pagina")
    else:
        print("  niente da dividere")

    print("\n=== 3. stato di src/content ===")
    for cartella in sorted(p for p in CONTENUTI.iterdir() if p.is_dir()):
        nomi = sorted(f.name for f in cartella.glob("*.md"))
        print(f"  {cartella.name:18} {', '.join(nomi) if nomi else '(vuota)'}")

    # Controllo: nessun BOM rimasto da nessuna parte nel progetto.
    print("\n=== 4. controllo BOM in tutto src/ ===")
    restanti = 0
    for file in sorted((RADICE / "src").rglob("*")):
        if file.is_file() and file.suffix in {".md", ".ts", ".astro", ".css", ".yml", ".yaml"}:
            if file.read_bytes().startswith(b"\xef\xbb\xbf"):
                print(f"  BOM ANCORA PRESENTE: {file.relative_to(RADICE)}")
                restanti += 1
    print(f"  file con BOM: {restanti}")

    return 1 if restanti else 0


if __name__ == "__main__":
    sys.exit(main())
