"""
Rimette poche animazioni di comparsa, scelte a mano, sulle pagine interne.

Dopo aver azzerato tutte le comparse progressive (erano 47 direttive), se ne
rimettono due per pagina: il contenitore del primo blocco di contenuto e quello
dell'invito finale. Non una per riga, non una per scheda: due per pagina.

Si lavora per numero di riga, dal basso verso l'alto, così l'inserimento non
sposta i numeri delle righe ancora da trattare.

Uso:  python scripts/rimetti_aos.py
"""

from __future__ import annotations

import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent

# file -> righe (1-based) che contengono il contenitore da animare
RIGHE = {
    "src/pages/camere.astro": [71, 274],
    "src/pages/ristorante.astro": [116, 253],
    "src/pages/sentieri/index.astro": [59, 196],
    "src/pages/la-locanda.astro": [71, 214],
    "src/pages/gnocchi-con-la-fioreta.astro": [95, 204],
}

ATTRIBUTO = ' data-aos="fade-up"'


def main() -> int:
    totale = 0

    for percorso, numeri in RIGHE.items():
        p = RADICE / percorso
        if not p.exists():
            print(f"  MANCA: {percorso}")
            continue

        righe = p.read_text(encoding="utf-8").split("\n")

        for numero in sorted(numeri, reverse=True):
            indice = numero - 1
            if indice >= len(righe):
                print(f"  {percorso}: riga {numero} oltre la fine del file")
                continue

            riga = righe[indice]

            if "data-aos" in riga:
                print(f"  {percorso}: riga {numero} ha già una direttiva")
                continue

            # Inserisce l'attributo prima della chiusura del tag
            posizione = riga.rfind(">")
            if posizione == -1:
                print(f"  {percorso}: riga {numero} non contiene un tag")
                continue

            righe[indice] = riga[:posizione] + ATTRIBUTO + riga[posizione:]
            totale += 1
            print(f"  {percorso}: riga {numero} animata")

        p.write_text("\n".join(righe), encoding="utf-8", newline="")

    print()
    print(f"animazioni rimesse: {totale}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
