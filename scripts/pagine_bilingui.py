"""
Rende bilingui le funzioni che caricano i contenuti delle pagine.

COME
Ogni `caricaX()` accetta una lingua. I TESTI vengono cercati nella versione
tradotta (`testi.en`) e, se manca, si ripiega sull'italiano: meglio una pagina
inglese con un testo italiano dentro che una pagina che non si compila. Il
ripiego non passa inosservato, perché `scripts/verifica_traduzioni.py` elenca le
schede senza traduzione.

Le FOTOGRAFIE restano in italiano per tutte e due le lingue: un'immagine non ha
lingua, e non ha senso duplicarne il file.

Uso:  python scripts/pagine_bilingui.py
"""

from __future__ import annotations

import pathlib

FILE = pathlib.Path(__file__).resolve().parent.parent / "src" / "lib" / "pagine.ts"

COLLEZIONI = [
    ("caricaHome", "ContenutoHome", "home"),
    ("caricaLocanda", "ContenutoLocanda", "paginaLocanda"),
    ("caricaSentieri", "ContenutoSentieri", "paginaSentieri"),
    ("caricaGnocchi", "ContenutoGnocchi", "gnocchi"),
]

IMPORT = """import { getEntry } from 'astro:content';
import type { Lingua } from '../i18n';
import { idTradotto } from './contenuti';
"""


def main() -> int:
    testo = FILE.read_text(encoding="utf-8")
    fatte = 0

    # --- L'import ----------------------------------------------------------
    if "idTradotto" not in testo:
        vecchio = "import { getEntry } from 'astro:content';\n"
        if vecchio not in testo:
            print("  import di getEntry non trovato")
            return 1
        testo = testo.replace(vecchio, IMPORT, 1)
        print("  import aggiunti")
        fatte += 1

    # --- Le quattro funzioni ----------------------------------------------
    for funzione, tipo, collezione in COLLEZIONI:
        vecchio = (
            f"export async function {funzione}(): Promise<{tipo}> {{\n"
            f"  const testi = await getEntry('{collezione}', 'testi');\n"
        )
        nuovo = (
            f"export async function {funzione}(lingua: Lingua = 'it'): Promise<{tipo}> {{\n"
            f"  // Si cerca la versione tradotta; se manca, si ripiega sull'italiano.\n"
            f"  const testi =\n"
            f"    (await getEntry('{collezione}', idTradotto('testi', lingua))) ??\n"
            f"    (await getEntry('{collezione}', 'testi'));\n"
        )
        if vecchio in testo:
            testo = testo.replace(vecchio, nuovo, 1)
            print(f"  {funzione}: lingua accettata")
            fatte += 1
        else:
            print(f"  {funzione}: forma attesa non trovata")

    FILE.write_text(testo, encoding="utf-8", newline="")
    print(f"  modifiche: {fatte}")
    return 0 if fatte == 5 else 1


if __name__ == "__main__":
    raise SystemExit(main())
