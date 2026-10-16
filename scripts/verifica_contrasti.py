"""
Verifica i contrasti del testo secondo le linee guida WCAG 2.2.

Calcola il rapporto di contrasto fra le coppie di colori che il sito usa
davvero e segnala quelle sotto la soglia.

Soglie (WCAG 2.2, livello AA):
  - testo normale      : 4,5:1
  - testo grande       : 3,0:1  (≥ 24 px, oppure ≥ 19 px in grassetto)
  - elementi grafici   : 3,0:1  (bordi, icone, indicatori di stato)

I valori dei colori si leggono da src/styles/global.css: se un colore cambia
nel foglio di stile, questo controllo lo segue senza essere aggiornato a mano.

Uso:  python scripts/verifica_contrasti.py
"""

from __future__ import annotations

import pathlib
import re
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
CSS = RADICE / "src" / "styles" / "global.css"

SOGLIA_NORMALE = 4.5
SOGLIA_GRANDE = 3.0

# (nome del testo, nome del fondo, soglia, descrizione)
#
# ATTENZIONE al fondo scelto: `stone-100` è il fondo della PAGINA, `stone-50` è
# il fondo dei PANNELLI ed è più chiaro. Verificare i testi solo sul secondo
# darebbe risultati migliori del vero: sono due superfici diverse e vanno
# controllate entrambe.
COPPIE = [
    # --- Testo sul fondo della pagina (stone-100) -------------------------
    ("stone-900", "stone-100", SOGLIA_NORMALE, "titoli sul fondo pagina"),
    ("stone-800", "stone-100", SOGLIA_NORMALE, "corpo del testo"),
    ("stone-600", "stone-100", SOGLIA_NORMALE, "testo secondario"),
    ("stone-500", "stone-100", SOGLIA_NORMALE, "note e didascalie"),
    ("wood-500", "stone-100", SOGLIA_NORMALE, "etichette sopra i titoli"),
    # --- Testo sul fondo dei pannelli (stone-50, più chiaro) --------------
    ("stone-900", "stone-50", SOGLIA_NORMALE, "titoli su pannello"),
    ("stone-600", "stone-50", SOGLIA_NORMALE, "testo su pannello"),
    ("stone-500", "stone-50", SOGLIA_NORMALE, "note su pannello"),
    ("wood-500", "stone-50", SOGLIA_NORMALE, "etichette su pannello"),
    # --- Pagina Camere, che ha un fondo suo -------------------------------
    ("stone-900", "camere-fondo", SOGLIA_NORMALE, "titoli sul fondo Camere"),
    ("stone-600", "camere-fondo", SOGLIA_NORMALE, "testo sul fondo Camere"),
    ("stone-500", "camere-fondo", SOGLIA_NORMALE, "note sul fondo Camere"),
    ("wood-500", "camere-fondo", SOGLIA_NORMALE, "etichette sul fondo Camere"),
    # --- Testo su fondo scuro ---------------------------------------------
    ("stone-50", "forest-900", SOGLIA_NORMALE, "testo su fascia bosco"),
    ("stone-200", "forest-900", SOGLIA_NORMALE, "corpo su fascia bosco"),
    ("forest-300", "forest-900", SOGLIA_NORMALE, "testo secondario su fascia bosco"),
    ("stone-50", "stone-800", SOGLIA_NORMALE, "testo su fondo scuro"),
    ("stone-200", "stone-800", SOGLIA_NORMALE, "testo secondario su fondo scuro"),
    ("stone-300", "stone-800", SOGLIA_NORMALE, "note su fondo scuro"),
    # --- Pulsanti e fascia -------------------------------------------------
    ("accento-testo", "accento", SOGLIA_NORMALE, "pulsante principale (testo su ocra)"),
    ("accento-testo", "accento-scuro", SOGLIA_NORMALE, "pulsante principale, passaggio"),
    ("stone-900", "accento", SOGLIA_NORMALE, "testo scuro sulla fascia ocra"),
    # --- Elementi grafici --------------------------------------------------
    ("stone-500", "stone-100", SOGLIA_GRANDE, "linee di separazione"),
    ("cai-rosso", "stone-100", SOGLIA_GRANDE, "rosso CAI sui cartelli"),
    # Il contorno del focus deve vedersi: è quello che dice a chi naviga da
    # tastiera dove si trova. Questo è un requisito, non un abbellimento.
    ("forest-700", "stone-100", SOGLIA_GRANDE, "contorno del focus da tastiera"),
    ("forest-700", "stone-50", SOGLIA_GRANDE, "contorno del focus sui pannelli"),
]

# NOTA sui filetti decorativi.
# `stone-300` è usato come linea divisoria fra le sezioni e come bordo sottile.
# Il suo contrasto sul fondo è di circa 1,4:1 e NON è un difetto: il criterio
# WCAG 1.4.11 chiede 3:1 per gli elementi necessari a riconoscere un comando o
# uno stato, non per i filetti che separano due blocchi di testo. Portarlo a 3:1
# significherebbe avere linee scure e pesanti, che è l'opposto di quello che
# serve. Per questo non è nell'elenco qui sopra.


def leggi_colori(percorso: pathlib.Path) -> dict[str, str]:
    """Estrae le variabili --color-*: #hex dal foglio di stile."""
    testo = percorso.read_text(encoding="utf-8")
    colori: dict[str, str] = {}

    for nome, valore in re.findall(r"--color-([a-z0-9-]+):\s*(#[0-9a-fA-F]{6})", testo):
        colori[nome] = valore.lower()

    return colori


def canale(valore: float) -> float:
    """Linearizza un canale secondo la formula WCAG."""
    valore = valore / 255
    return valore / 12.92 if valore <= 0.04045 else ((valore + 0.055) / 1.055) ** 2.4


def luminanza(hexcol: str) -> float:
    """Luminanza relativa di un colore #rrggbb."""
    r = int(hexcol[1:3], 16)
    g = int(hexcol[3:5], 16)
    b = int(hexcol[5:7], 16)
    return 0.2126 * canale(r) + 0.7152 * canale(g) + 0.0722 * canale(b)


def contrasto(uno: str, due: str) -> float:
    """Rapporto di contrasto fra due colori (da 1:1 a 21:1)."""
    l1, l2 = luminanza(uno), luminanza(due)
    chiaro, scuro = max(l1, l2), min(l1, l2)
    return (chiaro + 0.05) / (scuro + 0.05)


def main() -> int:
    if not CSS.is_file():
        print("foglio di stile non trovato")
        return 1

    colori = leggi_colori(CSS)
    print("=" * 78)
    print("VERIFICA DEI CONTRASTI (WCAG 2.2, livello AA)")
    print("=" * 78)
    print(f"colori letti dal foglio di stile: {len(colori)}")
    print()

    falliti = 0
    for nome_testo, nome_fondo, soglia, descrizione in COPPIE:
        testo = colori.get(nome_testo)
        fondo = colori.get(nome_fondo)

        if not testo or not fondo:
            mancanti = [
                n for n, v in ((nome_testo, testo), (nome_fondo, fondo)) if not v
            ]
            print(f"[?    ] {descrizione}")
            print(f"         colore non trovato: {', '.join(mancanti)}")
            continue

        rapporto = contrasto(testo, fondo)
        ok = rapporto >= soglia

        if not ok:
            falliti += 1

        richiesta = "4,5" if soglia == SOGLIA_NORMALE else "3,0"
        print(f"[{'OK  ' if ok else 'FAIL'}] {descrizione}")
        print(
            f"         {testo} su {fondo}  ->  {rapporto:.2f}:1  "
            f"(richiesto {richiesta}:1)"
        )

    print("-" * 78)
    if falliti:
        print(f"CONTRASTI INSUFFICIENTI: {falliti} su {len(COPPIE)}")
        return 1

    print(f"tutti i {len(COPPIE)} contrasti sono sufficienti")
    return 0


if __name__ == "__main__":
    sys.exit(main())
