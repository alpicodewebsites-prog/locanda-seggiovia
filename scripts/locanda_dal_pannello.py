"""
Fa sì che il titolo e il sottotitolo della pagina «La Locanda» vengano davvero
dal pannello.

IL DIFETTO
Il pannello offriva due campi, `titolo` e `sottotitolo`, che la pagina non
leggeva: il titolo grande era scritto nel codice. Chi modificava quei campi non
vedeva cambiare niente, e non c'era modo di accorgersene dall'interfaccia.

Ora la pagina legge i due campi, e i file di contenuto contengono il testo che
prima stava nel codice. Così il pannello dice il vero, e la cliente può cambiare
il titolo in tutte e due le lingue.

Se un file manca, la pagina usa il testo del dizionario invece di mostrare
«undefined».
"""

from __future__ import annotations

import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
IT = RADICE / "src" / "content" / "la-locanda" / "testi.md"
EN = RADICE / "src" / "content" / "la-locanda" / "testi-en.md"
PAGINA = RADICE / "src" / "pages" / "la-locanda.astro"

TITOLO_IT = "Una casa di pietra in piazza, ai piedi delle Piccole Dolomiti"
LEDE_IT = (
    "La Locanda Seggiovia non è nata come albergo e non lo è diventata. È la casa di "
    "una famiglia che ha scelto di restare in montagna e di aprirla a chi la montagna "
    "la viene a cercare."
)
TITOLO_EN = "A house of stone on the square, at the foot of the Piccole Dolomiti"
LEDE_EN = (
    "Locanda Seggiovia was not built as a hotel and has not become one. It is the home "
    "of a family that chose to stay in the mountains and to open it to those who come "
    "looking for them."
)

NUOVO_IT = f"""---
titolo: {TITOLO_IT}
sottotitolo: >-
  {LEDE_IT}
---
"""

NUOVO_EN = f"""---
titolo: {TITOLO_EN}
sottotitolo: >-
  {LEDE_EN}
---
"""


def main() -> int:
    IT.write_text(NUOVO_IT, encoding="utf-8", newline="")
    EN.write_text(NUOVO_EN, encoding="utf-8", newline="")
    print("  contenuti: titolo e sottotitolo ora contengono il testo visibile")

    pagina = PAGINA.read_text(encoding="utf-8")
    vecchio = """      <h1 class="display-2 mt-5 max-w-[24ch] text-stone-900">
        {t.titolo}
      </h1>
      <p class="lede mt-6 max-w-[58ch]">
        {t.lede}
      </p>"""
    nuovo = """      <h1 class="display-2 mt-5 max-w-[24ch] text-stone-900">
        {pagina.testi.titolo || t.titolo}
      </h1>
      <p class="lede mt-6 max-w-[58ch]">
        {pagina.testi.sottotitolo || t.lede}
      </p>"""

    if "pagina.testi.titolo" in pagina:
        print("  pagina: leggeva già dal pannello")
    elif vecchio in pagina:
        PAGINA.write_text(pagina.replace(vecchio, nuovo, 1), encoding="utf-8", newline="")
        print("  pagina: ora legge titolo e sottotitolo dal pannello")
    else:
        print("  pagina: punto di inserimento non trovato")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
