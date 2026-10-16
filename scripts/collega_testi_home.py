"""
Collega i testi e le fotografie della home al pannello.

Prima erano scritti dentro `index.astro` e `Hero.astro`: cambiarli richiedeva
di mettere mano al codice. Ora arrivano dal file di contenuto, e questo script
fa le sostituzioni in un posto solo invece che a mano in dieci punti.

Uso:  python scripts/collega_testi_home.py
"""

from __future__ import annotations

import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent

# (file, da sostituire, con cosa)
SOSTITUZIONI: list[tuple[str, str, str]] = [
    # --- index.astro: caricamento -----------------------------------------
    (
        "src/pages/index.astro",
        "import { caricaFotoSito } from '../lib/foto-sito';\n\n/** Fotografie generali, modificabili dal pannello. */\nconst foto = await caricaFotoSito();\n\nconst imgLocanda = foto.locandaEsterno;",
        "import { caricaHome } from '../lib/pagine';\n\n/**\n * Testi e fotografie della home, modificabili dal pannello.\n *\n * Arrivano da `src/content/home/pagina.md`: cambiarli lì cambia questa pagina.\n * La voce si chiama «Home Page» nel pannello.\n */\nconst home = await caricaHome();\nconst foto = home.foto;\nconst testi = home.testi;\n\nconst imgLocanda = foto.facciata;",
    ),
    # --- index.astro: descrizione per i motori ----------------------------
    (
        "src/pages/index.astro",
        "const description =\n  'Camere e ristorante nel centro di Recoaro Terme, ai piedi delle Piccole Dolomiti e del Pasubio. Cucina alto-vicentina e Gnocchi con la Fioreta De.Co.';",
        "/** Descrizione per i motori di ricerca: si modifica dal pannello. */\nconst description = testi.descrizione;",
    ),
    # --- index.astro: apertura --------------------------------------------
    (
        "src/pages/index.astro",
        "<Hero immagine={foto.hero} />",
        "<Hero\n    immagine={foto.hero}\n    titolo={testi.titolo}\n    sottotitolo={testi.sottotitolo}\n    accessi={testi.accessi}\n    invitoSentieri={testi.invitoSentieri}\n  />",
    ),
    # --- index.astro: pulsante gnocchi ------------------------------------
    (
        "src/pages/index.astro",
        "        Scopri la nostra produzione di gnocchi con la Fioreta\n        <span class=\"pulsante-gnocchi__freccia\" aria-hidden=\"true\">→</span>",
        "        {testi.pulsanteGnocchi}\n        <span class=\"pulsante-gnocchi__freccia\" aria-hidden=\"true\">→</span>",
    ),
    # --- index.astro: sezione La locanda ----------------------------------
    (
        "src/pages/index.astro",
        '<p class="eyebrow text-forest-500">La locanda</p>',
        '<p class="eyebrow text-forest-500">{testi.locandaEtichetta}</p>',
    ),
    (
        "src/pages/index.astro",
        "Un rifugio, non un albergo\n        </h2>",
        "{testi.locandaTitolo}\n        </h2>",
    ),
    # --- index.astro: sezione Territorio ----------------------------------
    (
        "src/pages/index.astro",
        '<p class="eyebrow text-wood-500">Territorio</p>',
        '<p class="eyebrow text-wood-500">{testi.territorioEtichetta}</p>',
    ),
    (
        "src/pages/index.astro",
        "I sentieri cominciano dal centro del paese\n          </h2>",
        "{testi.territorioTitolo}\n          </h2>",
    ),
    (
        "src/pages/index.astro",
        "<p class=\"lede text-[1rem]\">\n            Sei itinerari fra Piccole Dolomiti, Gruppo del Carega e Pasubio. Difficoltà dal\n            turistico all’escursionistico esposto, tutti documentati con dati tecnici reali.\n          </p>",
        '<p class="lede text-[1rem]">{testi.territorioTesto}</p>',
    ),
]


def main() -> int:
    problemi = 0
    for file, vecchio, nuovo in SOSTITUZIONI:
        percorso = RADICE / file
        testo = percorso.read_text(encoding="utf-8")
        if vecchio not in testo:
            print(f"  NON TROVATO in {file}: {vecchio[:62]!r}")
            problemi += 1
            continue
        percorso.write_text(testo.replace(vecchio, nuovo, 1), encoding="utf-8", newline="")
        print(f"  ok  {file}: {vecchio[:52].splitlines()[0]!r}")

    if problemi:
        print(f"\nsostituzioni non riuscite: {problemi}")
        return 1
    print("\ntutte le sostituzioni applicate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
