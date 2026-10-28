"""
Aggiunge al pannello le collezioni inglesi, una per ogni collezione italiana.

PERCHÉ DUE COLLEZIONI E NON IL SELETTORE DI LINGUA DEL PANNELLO
La funzione multilingua del pannello (Decap/Sveltia) nomina i file `testi.it.md`
e `testi.en.md`. Astro toglie il punto dall'identificativo, quindi gli id
diventano `testiit` e `testien`: illeggibili, e ambigui — un sentiero il cui nome
finisse per «en» verrebbe scambiato per una traduzione.

Con le due collezioni, ogni versione ha una cartella sua (`src/content/x/` e
`src/content/x/en/`), gli id restano leggibili, e la cliente trova nel pannello
«Sentieri (elenco)» e «Sentieri — English»: per una persona che non programma è
più chiaro di una scheda sola con il selettore di lingua.

Le etichette dei campi restano in italiano: la cliente è italiana, e i campi sono
la parte del pannello che legge lei. È il CONTENUTO a essere in inglese.

Uso:  python scripts/pannello_bilingue.py
"""

from __future__ import annotations

import pathlib
import re

CONFIG = (
    pathlib.Path(__file__).resolve().parent.parent / "public" / "admin" / "config.yml"
)

INIZIO = "collections:\n"
MARCATORE = "# ==========================================================================\n# LE VERSIONI INGLESI\n"


def dividi_in_blocchi(testo: str) -> tuple[str, list[str]]:
    """Restituisce l'intestazione e i blocchi di collezione."""
    inizio = testo.index(INIZIO) + len(INIZIO)
    intestazione = testo[:inizio]
    corpo = testo[inizio:]

    # Ogni collezione comincia con `  - name: ` a due spazi di rientro.
    posizioni = [m.start() for m in re.finditer(r"^  - name: ", corpo, re.M)]
    blocchi = []
    for i, posizione in enumerate(posizioni):
        fine = posizioni[i + 1] if i + 1 < len(posizioni) else len(corpo)
        blocchi.append(corpo[posizione:fine])

    return intestazione, blocchi


def versione_inglese(blocco: str) -> str | None:
    """La stessa collezione, puntata ai file inglesi."""
    if "    folder: " not in blocco and "        file: " not in blocco:
        return None

    righe = blocco.splitlines(keepends=True)
    fuori: list[str] = []
    nome = None
    salta = False
    salta_descrizione = False

    for riga in righe:
        # Le schede delle FOTOGRAFIE non si traducono: la stessa immagine vale
        # per le due lingue, quindi la collezione inglese non ne ha una copia.
        # Si salta l'intera voce (nome, etichetta, file e campi).
        if re.match(r"^      - name: foto\b", riga):
            salta = True
            continue
        if salta:
            if re.match(r"^      - name: ", riga) or re.match(r"^  - name: ", riga):
                salta = False
            else:
                continue

        if nome is None and riga.startswith("  - name: "):
            nome = riga[len("  - name: ") :].strip()
            fuori.append("  - name: " + nome + "-en\n")
            continue

        if nome is not None and riga.startswith(f"    label: "):
            etichetta = riga[len("    label: ") :].rstrip("\n")
            fuori.append(f"    label: {etichetta} — English\n")
            continue

        # La descrizione può essere su più righe (`>-`): va sostituita tutta,
        # altrimenti le continuazioni restano orfane e il file non è più YAML.
        if riga.startswith("    description: "):
            fuori.append("    description: La stessa pagina in inglese.\n")
            salta_descrizione = riga.rstrip().endswith((">-", "|", ">"))
            continue

        if salta_descrizione:
            if riga.startswith("      ") or not riga.strip():
                continue
            salta_descrizione = False

        # Cartella di una collezione a elenco.
        if riga.startswith("    folder: ") and "/en" not in riga:
            percorso = riga[len("    folder: ") :].rstrip("\n")
            fuori.append(f"    folder: {percorso}/en\n")
            continue

        # File di una collezione a pagine fisse.
        if riga.startswith("        file: ") and "/en/" not in riga:
            percorso = riga[len("        file: ") :].rstrip("\n")
            cartella, _, nome_file = percorso.rpartition("/")
            fuori.append(f"        file: {cartella}/en/{nome_file}\n")
            continue

        fuori.append(riga)

    return "".join(fuori)


def main() -> int:
    testo = CONFIG.read_text(encoding="utf-8")

    if "LE VERSIONI INGLESI" in testo:
        print("  le collezioni inglesi ci sono già: niente da fare")
        return 0

    intestazione, blocchi = dividi_in_blocchi(testo)
    print(f"  collezioni italiane: {len(blocchi)}")

    inglesi = []
    for blocco in blocchi:
        nuovo = versione_inglese(blocco)
        if nuovo:
            inglesi.append("  # " + "-" * 72 + "\n")
            inglesi.append(nuovo)
            inglesi.append("\n")

    if not inglesi:
        print("  nessuna collezione da duplicare")
        return 1

    corpo = "".join(blocchi)
    nuovo_testo = (
        intestazione
        + corpo
        + "\n"
        + MARCATORE
        + "# --------------------------------------------------------------------------\n"
        + "# Ogni collezione qui sotto è la stessa di sopra, ma legge e scrive i file\n"
        + "# della cartella `en/`. Le etichette dei campi restano in italiano: è la\n"
        + "# lingua in cui lavora chi gestisce il sito. Il contenuto è in inglese.\n"
        + "# --------------------------------------------------------------------------\n\n"
        + "".join(inglesi).rstrip("\n")
        + "\n"
    )

    CONFIG.write_text(nuovo_testo, encoding="utf-8", newline="")
    print(f"  collezioni inglesi aggiunte: {len(inglesi) // 3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
