"""
Rende leggibili i testi secondari del meteo su ogni cielo.

IL PROBLEMA
I testi piccoli usavano `color-mix(... 62%, transparent)`, cioè lo stesso nero
con il 62% di opacità. Su un cielo chiaro va bene; sul cielo dei rovesci o del
temporale, che sono grigi, il colore risultante si avvicina allo sfondo e il
contrasto scende sotto 4,5:1 — la soglia sotto la quale un testo piccolo non si
legge.

LA SOLUZIONE
Due colori PIENI invece di due opacità:
  --testo-meteo    #1c1b19   per i testi principali
  --testo-meteo-2  #3a3a35   per le etichette piccole

Un colore pieno non dipende da cosa c'è dietro: il contrasto è calcolabile e
verificabile. Con l'opacità bisognerebbe rifare il conto per ogni sfondo, e
basterebbe aggiungere un cielo perché qualcosa smettesse di leggersi.

In più si schiariscono i due cieli più cupi, che erano gli unici sotto soglia.
Restano grigi e restano "brutti" quanto serve: è il tempo, non una decorazione.
"""

from __future__ import annotations

import pathlib
import re

COMPONENTE = (
    pathlib.Path(__file__).resolve().parent.parent
    / "src"
    / "components"
    / "MeteoSentiero.astro"
)

SOSTITUZIONI = [
    # --- I due colori pieni ------------------------------------------------
    (
        "    --testo-meteo: #1c1b19;\n",
        "    --testo-meteo: #1c1b19;\n"
        "    /* Testi secondari: un grigio pieno, non un nero trasparente. */\n"
        "    --testo-meteo-2: #3a3a35;\n",
    ),
    # --- Cieli schiariti dove erano troppo cupi ---------------------------
    (
        "      linear-gradient(160deg, #c3c8c9, #9ea4a6);",
        "      linear-gradient(160deg, #ccd1d2, #b3b8b9);",
    ),
    (
        "      linear-gradient(160deg, #b6b8b1, #8f918a);",
        "      linear-gradient(160deg, #bfc1ba, #a9aba4);",
    ),
]


def main() -> int:
    testo = COMPONENTE.read_text(encoding="utf-8")
    problemi = 0

    for vecchio, nuovo in SOSTITUZIONI:
        if vecchio in testo:
            testo = testo.replace(vecchio, nuovo, 1)
        else:
            print(f"  NON TROVATO: {vecchio.strip()[:64]}")
            problemi += 1

    # La condizione resta al colore principale.
    testo, n = re.subn(
        r"color:\s*color-mix\(in srgb, var\(--testo-meteo\) 88%, transparent\);",
        "color: var(--testo-meteo);",
        testo,
    )
    print(f"  testi principali convertiti: {n}")

    # Tutti gli altri passano al grigio pieno.
    testo, n = re.subn(
        r"color:\s*color-mix\(in srgb, var\(--testo-meteo\) \d+%, transparent\);",
        "color: var(--testo-meteo-2);",
        testo,
    )
    print(f"  testi secondari convertiti: {n}")

    # La riga divisoria resta semitrasparente: è un filetto, non un testo.
    restanti = len(re.findall(r"color-mix\(in srgb, var\(--testo-meteo\)", testo))
    print(f"  usi di opacità rimasti (divisori e filetti): {restanti}")

    COMPONENTE.write_text(testo, encoding="utf-8", newline="")
    return 0 if problemi == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
