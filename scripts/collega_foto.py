"""
Collega le pagine alle fotografie gestite dal pannello.

Sostituisce gli import statici delle immagini con la lettura delle impostazioni
(`lib/foto-sito.ts`), così la proprietaria può cambiare le foto dal pannello.

Uso:  python scripts/collega_foto.py
"""

from __future__ import annotations

import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent

# percorso del file -> elenco di (testo da cercare, testo sostitutivo)
SOSTITUZIONI: dict[str, list[tuple[str, str]]] = {
    "src/pages/camere.astro": [
        (
            "import imgCamere from '../assets/locanda-preparazione.jpg';",
            "import { caricaFotoSito } from '../lib/foto-sito';",
        ),
        (
            "import imgEsterno from '../assets/locanda-esterno.jpg';",
            "const foto = await caricaFotoSito();",
        ),
        ("src={imgCamere}", "src={foto.locandaCucina}"),
        ("src={imgEsterno}", "src={foto.locandaEsterno}"),
    ],
    "src/pages/la-locanda.astro": [
        (
            "import imgEsterno from '../assets/locanda-esterno.jpg';",
            "import { caricaFotoSito } from '../lib/foto-sito';",
        ),
        (
            "import imgPreparazione from '../assets/locanda-preparazione.jpg';",
            "const foto = await caricaFotoSito();",
        ),
        ("src={imgEsterno}", "src={foto.locandaEsterno}"),
    ],
    "src/pages/sentieri/index.astro": [
        (
            "import imgChiusura from '../../assets/piccole-dolomiti-large.jpg';",
            "import { caricaFotoSito } from '../../lib/foto-sito';",
        ),
        (
            "import imgMontagne from '../../assets/territorio-montagne.jpg';",
            "const foto = await caricaFotoSito();",
        ),
        ("src={imgChiusura}", "src={foto.panorama}"),
        ("src={imgMontagne}", "src={foto.montagne}"),
    ],
}


def main() -> int:
    problemi = 0

    for percorso, coppie in SOSTITUZIONI.items():
        p = RADICE / percorso
        if not p.exists():
            print(f"  MANCA: {percorso}")
            problemi += 1
            continue

        testo = p.read_text(encoding="utf-8")
        for vecchio, nuovo in coppie:
            if vecchio not in testo:
                print(f"  non trovato in {p.name}: {vecchio[:60]}")
                problemi += 1
                continue
            testo = testo.replace(vecchio, nuovo)

        p.write_text(testo, encoding="utf-8", newline="")
        print(f"  {p.name}: aggiornato")

    print()
    print("problemi:", problemi)
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
