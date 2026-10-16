"""
Controlla le etichette e la struttura del pannello.

Nasce da tre difetti veri, tutti invisibili nel codice e visibili solo aprendo
il pannello:

1. L'etichetta «I due accessi dell''apertura» compariva con DUE apostrofi.
   In YAML, `''` rappresenta un apostrofo solo dentro apici singoli; in un valore
   non quotato restano due caratteri. Il file era formalmente valido.

2. Un valore non quotato conteneva due punti seguiti da spazio
   (`hint: Distinta da quella della home: puoi metterne una diversa.`).
   YAML lo legge come una mappa annidata e rifiuta tutto il file.

3. La libreria immagini chiama le cartelle «Collezione › etichetta della voce».
   Con una voce sola per pagina, nella libreria — dove si gestiscono SOLO
   fotografie — si leggeva «Testi, paragrafi e foto». Da qui la divisione in due
   voci, e da qui il controllo che ogni pagina ne abbia esattamente due.

Uso:  python scripts/verifica_etichette.py
"""

from __future__ import annotations

import pathlib
import re
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
CONFIG = RADICE / "public" / "admin" / "config.yml"

# Le pagine che devono avere due voci: i testi da una parte, le foto dall'altra.
PAGINE = {"home", "pagina-locanda", "pagina-sentieri", "gnocchi"}


def controlla_valori(righe: list[str]) -> int:
    """Apostrofi doppi sbagliati e due punti che rompono lo YAML."""
    problemi = 0

    for numero, riga in enumerate(righe, start=1):
        spoglia = riga.strip()
        if spoglia.startswith("#"):
            continue

        m = re.match(r"^-?\s*(label|hint|description|name|file)\s*:\s*(.+)$", spoglia)
        if not m:
            continue
        valore = m.group(2).strip()
        if not valore:
            continue

        quotato = (valore.startswith("'") and valore.endswith("'")) or (
            valore.startswith('"') and valore.endswith('"')
        )

        if "''" in valore and not quotato:
            print(f"  [FAIL] riga {numero}: apostrofo doppio in un valore non quotato")
            print(f"         {spoglia[:86]}")
            problemi += 1

        # Toglie il commento in coda prima di cercare i due punti.
        senza_commento = re.sub(r"\s+#.*$", "", valore)
        if not quotato and re.search(r":\s", senza_commento):
            print(f"  [FAIL] riga {numero}: due punti dentro un valore non quotato")
            print(f"         {spoglia[:86]}")
            print("         YAML lo legge come mappa annidata e rifiuta il file.")
            problemi += 1

    if problemi == 0:
        print("  [OK  ] nessun apostrofo doppio e nessun due punti non quotato")

    return problemi


def controlla_struttura(testo: str) -> int:
    """Ogni pagina deve avere una voce per i testi e una per le fotografie."""
    problemi = 0

    blocchi = testo.split("\n  - name: ")[1:]
    for blocco in blocchi:
        nome = blocco.split("\n")[0].strip()
        etichette = [v.strip().strip("'\"") for v in re.findall(r"\n        label:\s*(.+)", blocco)]

        if nome not in PAGINE:
            continue

        if len(etichette) < 2:
            print(f"  [FAIL] [{nome}] ha {len(etichette)} voce/i invece di due")
            problemi += 1
            continue

        testi_ok = any("test" in e.lower() for e in etichette)
        foto_ok = any("fotograf" in e.lower() for e in etichette)

        if not testi_ok:
            print(f"  [FAIL] [{nome}] manca la voce dei testi")
            problemi += 1
        if not foto_ok:
            print(f"  [FAIL] [{nome}] manca la voce delle fotografie")
            problemi += 1

        # La voce delle fotografie non deve nominare i testi: è quella che
        # compare nella libreria immagini.
        for e in etichette:
            if "fotograf" in e.lower() and re.search(r"test|paragraf", e, re.I):
                print(f"  [FAIL] [{nome}] la voce delle foto nomina i testi: «{e}»")
                problemi += 1

    if problemi == 0:
        print(f"  [OK  ] le {len(PAGINE)} pagine hanno una voce per i testi e una per le foto")

    return problemi


def controlla_foto(testo: str) -> int:
    """
    Le voci delle fotografie dichiarano l'orientamento e sono numerate.

    Si guarda SOLO dentro i blocchi chiamati `foto`: le etichette dei campi di
    testo stanno alla stessa indentazione, e senza questa distinzione il
    controllo le scambiava per fotografie e segnalava «Titolo principale» come
    «fotografia senza numero d'ordine».
    """
    problemi = 0
    foto: list[str] = []

    # Ogni voce di file comincia con `      - name: <nome>` a sei spazi.
    for blocco in re.split(r"\n(?=      - name: )", testo):
        if not re.match(r"^      - name:\s*foto\s*$", blocco, re.M):
            continue
        foto += [
            m.group(1).strip()
            for m in re.finditer(r"^          - label:\s*'?([^'\n]+?)'?\s*$", blocco, re.M)
        ]

    non_numerate = [f for f in foto if not re.match(r"^\d", f)]
    senza_verso = [f for f in foto if not re.search(r"verticale|orizzontale|quadrat", f, re.I)]

    for f in non_numerate:
        print(f"  [FAIL] fotografia senza numero d'ordine: «{f}»")
        problemi += 1
    for f in senza_verso:
        print(f"  [FAIL] fotografia senza orientamento: «{f}»")
        problemi += 1

    if not foto:
        print("  [FAIL] non è stata trovata nessuna voce «Fotografie»")
        problemi += 1
    elif problemi == 0:
        print(f"  [OK  ] le {len(foto)} fotografie sono numerate e dichiarano l'orientamento")

    return problemi


def main() -> int:
    righe = CONFIG.read_text(encoding="utf-8").splitlines()
    testo = "\n".join(righe)

    print("=" * 74)
    print("STRUTTURA ED ETICHETTE DEL PANNELLO")
    print("=" * 74)

    problemi = controlla_valori(righe)
    problemi += controlla_struttura(testo)
    problemi += controlla_foto(testo)

    print("-" * 74)
    if problemi:
        print(f"CONTROLLI NON SUPERATI: {problemi}")
        return 1
    print("pannello a posto")
    return 0


if __name__ == "__main__":
    sys.exit(main())
