"""
Aggiorna i dati dei sentieri con le informazioni verificate.

FONTE
Le schede di outdooractive.com gestite dal **Comune di Recoaro Terme** e da
**UM.PASUBIO**, entrambi marcati «Partner verificato», più quella di UM.PASUBIO
per la Strada delle 52 Gallerie. Le pagine sono state lette una per una; da lì
vengono distanze, dislivelli, durate, quote e coordinate.

COSA NON SI FA
Non si copia il testo delle schede: è protetto. Si prendono i NUMERI, che sono
fatti e non sono di nessuno, e si tengono le descrizioni già scritte per il sito.
Non si inventa nulla: dove un dato non è verificabile il campo resta com'era.

IL NOME DEL SENTIERO
Resta «Italo Soldà». La scheda ufficiale del Comune lo chiama «6 SENTIERO ITALO
SOLDA'», e lo stesso fa il CAI Chioggia. «Gino Soldà» è l'alpinista recoarese:
persona diversa. Il controllo automatico che pretendeva «Gino» era sbagliato.

IL METEO
Ogni sentiero dichiara DOVE si misura il meteo, non «il meteo del sentiero»: un
percorso è lungo chilometri e la temperatura cambia con la quota. Le coordinate
sono quelle del punto di partenza verificato.

Uso:  python scripts/aggiorna_dati_sentieri.py
"""

from __future__ import annotations

import pathlib
import re
import sys

# Una chiave di primo livello comincia in colonna zero: `nome:`, `quota:`, ...
# Il `:` può essere seguito da qualsiasi cosa, compreso niente.
CHIAVE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*:")

RADICE = pathlib.Path(__file__).resolve().parent.parent
CARTELLA = RADICE / "src" / "content" / "sentieri"


# ---------------------------------------------------------------------------
# I dati, per file. Ogni voce è un campo che si sostituisce o si aggiunge.
# ---------------------------------------------------------------------------
AGGIORNAMENTI: dict[str, dict[str, str]] = {
    # 6 SENTIERO ITALO SOLDA' — 11,4 km di anello dal paese, non 4,25 km.
    "gino-solda": {
        "distanza": "11,4 km",
        "dislivello": "676 m",
        "durata": "4 ore e 21 minuti",
        "quota": "1114",
        "meteoLatitudine": "45.704908",
        "meteoLongitudine": "11.224817",
        "meteoLocalita": "Recoaro Terme",
    },
    # Sentiero dei Grandi Alberi — mancavano durata e numero CAI.
    "grandi-alberi": {
        "distanza": "11,4 km",
        "dislivello": "463 m",
        "durata": "3 ore e 50 minuti",
        "segnavia": "CAI 120",
        "meteoLatitudine": "45.68339",
        "meteoLongitudine": "11.22444",
        "meteoLocalita": "Recoaro Mille",
    },
    # Strada delle 52 Gallerie — mancava il numero CAI, e c'era un dislivello piu'
    # alto del rilevato.
    "strada-52-gallerie": {
        "dislivello": "948 m",
        "durata": "3 ore e 50 minuti",
        "segnavia": "CAI 366",
        "quota": "2006",
        "meteoLatitudine": "45.778657",
        "meteoLongitudine": "11.227940",
        "meteoLocalita": "Bocchetta Campiglia",
    },
    # Ponte Tibetano — mancavano distanza, dislivello e durata.
    "ponte-tibetano": {
        "distanza": "13,2 km",
        "dislivello": "552 m",
        "durata": "4 ore e 20 minuti",
        "quota": "1545",
        "partenza": "Pian delle Fugazze / Alpe di Campogrosso",
        "meteoLatitudine": "45.759609",
        "meteoLongitudine": "11.173866",
        "meteoLocalita": "Pian delle Fugazze",
    },
    # Anello Storico di Campogrosso — coordinate del passo di partenza, e la
    # webcam del rifugio dove l'anello arriva.
    "campogrosso": {
        "meteoLatitudine": "45.7601",
        "meteoLongitudine": "11.17331",
        "meteoLocalita": "Passo Pian delle Fugazze",
        "webcam": "https://www.rifugiocampogrosso.com/webcam/",
        "webcamEtichetta": "Rifugio Campogrosso",
    },
    # Sentiero delle Mole — verso l'Alpe di Campogrosso. Le coordinate sono quelle
    # del passo, l'unico punto verificato della zona; la località lo dice.
    "sentiero-mole": {
        "meteoLatitudine": "45.759609",
        "meteoLongitudine": "11.173866",
        "meteoLocalita": "Passo Pian delle Fugazze",
    },
}


def trova_blocco(righe: list[str], chiave: str) -> tuple[int, int] | None:
    """
    Trova il campo `chiave` di primo livello e ne restituisce inizio e fine.

    Il campo finisce alla riga successiva che COMINCIA una nuova chiave di primo
    livello, oppure alla fine del frontmatter.

    ATTENZIONE — la prima versione di questa funzione cercava le righe che
    *terminavano* con `:`. Sbagliato: `dislivello: 630 m` termina con `630 m`,
    quindi la funzione non riconosceva mai la fine del campo e cancellava tutto
    quello che veniva dopo. Se n'è accorto leggendo un file: `immagine:` era
    sparita. Ora si riconosce l'inizio di una chiave, non la fine di un valore.
    """
    inizio = None
    for i, riga in enumerate(righe):
        if inizio is None:
            if riga.startswith(f"{chiave}:"):
                inizio = i
        elif CHIAVE.match(riga):
            return inizio, i
    if inizio is not None:
        return inizio, len(righe)
    return None


def imposta(righe: list[str], chiave: str, valore: str) -> list[str]:
    """Sostituisce un campo, o lo aggiunge prima di `immagine` / in fondo."""
    blocco = trova_blocco(righe, chiave)
    nuova = f"{chiave}: {valore}"

    if blocco:
        inizio, fine = blocco
        return righe[:inizio] + [nuova] + righe[fine:]

    # Non c'è: si aggiunge prima di `immagine`, che resta l'ultimo campo.
    for i, riga in enumerate(righe):
        if riga.startswith("immagine:"):
            return righe[:i] + [nuova] + righe[i:]

    # Nessun ancoraggio: si mette in fondo al frontmatter.
    for i in range(len(righe) - 1, -1, -1):
        if righe[i].startswith("---"):
            return righe[:i] + [nuova] + righe[i:]
    return righe + [nuova]


def main() -> int:
    toccati = 0

    for nome_file, campi in AGGIORNAMENTI.items():
        percorso = CARTELLA / f"{nome_file}.md"
        if not percorso.is_file():
            print(f"  MANCA: {percorso.name}")
            continue

        testo = percorso.read_text(encoding="utf-8")
        if not testo.startswith("---"):
            print(f"  SALTATO (senza frontmatter): {percorso.name}")
            continue

        # Si separa il frontmatter dal resto del file.
        righe = testo.splitlines()
        chiusura = next(i for i in range(1, len(righe)) if righe[i].startswith("---"))
        frontmatter = righe[1:chiusura]
        resto = righe[chiusura:]

        for chiave, valore in campi.items():
            frontmatter = imposta(frontmatter, chiave, valore)

        percorso.write_text(
            "\n".join(["---"] + frontmatter + resto) + "\n",
            encoding="utf-8",
            newline="",
        )
        print(f"  {percorso.name}: {len(campi)} campi")
        toccati += 1

    print(f"\n  file aggiornati: {toccati}")
    return 0 if toccati == len(AGGIORNAMENTI) else 1


if __name__ == "__main__":
    sys.exit(main())
