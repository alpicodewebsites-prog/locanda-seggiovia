"""
Controlla le etichette del pannello.

Nasce da un difetto vero: l'etichetta «I due accessi dell''apertura» compariva
nel pannello con DUE apostrofi. Nel file YAML era scritta così:

    - label: I due accessi dell''apertura

In YAML, dentro apici singoli (`'...'`), due apostrofi consecutivi ne
rappresentano uno solo. Ma in un valore NON quotato restano due caratteri
letterali. Il file era formalmente valido, quindi nessun controllo lo segnalava:
l'errore si vedeva solo guardando il pannello.

Questo script distingue i due casi e segnala solo quello sbagliato.

Uso:  python scripts/verifica_etichette.py
"""

from __future__ import annotations

import pathlib
import re
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
CONFIG = RADICE / "public" / "admin" / "config.yml"


def main() -> int:
    testo = CONFIG.read_text(encoding="utf-8")
    problemi = 0

    print("=" * 74)
    print("ETICHETTE DEL PANNELLO")
    print("=" * 74)

    # --- 1. Apostrofi doppi in valori non quotati --------------------------
    for numero, riga in enumerate(testo.splitlines(), start=1):
        spoglia = riga.strip()
        if spoglia.startswith("#"):
            continue

        m = re.match(r"^-?\s*(label|hint|description)\s*:\s*(.+)$", spoglia)
        if not m:
            continue

        valore = m.group(2).strip()
        campo = m.group(1)

        # Se il valore è racchiuso fra apici singoli, `''` è la forma corretta.
        quotato_singolo = valore.startswith("'") and valore.endswith("'") and len(valore) > 2
        # Idem fra apici doppi, ma lì si usa \"
        quotato_doppio = valore.startswith('"') and valore.endswith('"') and len(valore) > 2

        if "''" in valore and not quotato_singolo:
            print(f"  [FAIL] riga {numero}: apostrofo doppio in un valore non quotato")
            print(f"         {spoglia[:90]}")
            print("         Nel pannello comparirebbe con due apostrofi. Racchiudi il")
            print("         valore fra apici doppi, oppure usa un apostrofo solo.")
            problemi += 1

        if quotato_doppio and "''" in valore:
            print(f"  [FAIL] riga {numero}: apostrofo doppio dentro apici doppi")
            print(f"         {spoglia[:90]}")
            problemi += 1

    if problemi == 0:
        print("  [OK  ] nessun apostrofo doppio sbagliato")

    # --- 2. Ogni voce di pagina dice che cosa contiene ---------------------
    # Il committente ha chiesto etichette che dicano «foto e paragrafi», non
    # solo «foto»: un'etichetta generica non aiuta chi cerca.
    print()
    generiche = []
    for m in re.finditer(r"^        label:\s*(.+)$", testo, re.M):
        etichetta = m.group(1).strip().strip("'\"")
        if etichetta.lower() in {"foto", "fotografie", "testi", "immagini", "contenuti"}:
            generiche.append(etichetta)

    if generiche:
        for e in generiche:
            print(f"  [FAIL] etichetta troppo generica: «{e}»")
            problemi += len(generiche)
    else:
        print("  [OK  ] nessuna etichetta generica: ogni voce dice che cosa contiene")

    # --- 3. Le fotografie dichiarano l'orientamento -------------------------
    print()
    foto = re.findall(r"^          - label:\s*'?(Fotografia[^'\n]*)'?\s*$", testo, re.M)
    senza_verso = [f for f in foto if "verticale" not in f.lower() and "orizzontale" not in f.lower()]
    if senza_verso:
        for f in senza_verso:
            print(f"  [FAIL] fotografia senza orientamento: «{f.strip()}»")
            problemi += len(senza_verso)
    else:
        print(f"  [OK  ] tutte le {len(foto)} fotografie dichiarano l'orientamento")

    print("-" * 74)
    if problemi:
        print(f"CONTROLLI NON SUPERATI: {problemi}")
        return 1
    print("etichette a posto")
    return 0


if __name__ == "__main__":
    sys.exit(main())
