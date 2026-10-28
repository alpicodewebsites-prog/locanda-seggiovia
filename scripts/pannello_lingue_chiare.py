"""
Rende il pannello più chiaro: separatore fra le lingue, nomi che si leggono
anche troncati, e il carosello della home modificabile.

TRE COSE

1. IL CAROSELLO. Prima le quattro diapositive si potevano cambiare solo nel
   codice. Ora sono un campo del pannello, nella stessa voce dove si modificano
   già i testi della home: la cliente cambia fotografia, titolo, due righe e
   indirizzo senza chiedere niente.

2. IL SEPARATORE. Sveltia non ha cartelle per le collezioni: ha solo un
   separatore visivo (`divider`). Fra il blocco italiano e quello inglese ce n'è
   uno, così i due gruppi non si mescolano.

3. I NOMI. Le etichette erano «Home Page» e «Home Page — English», e nella barra
   laterale la seconda si troncava in «Home Page — En...»: proprio la parte che
   diceva la lingua spariva. Ora la lingua viene PRIMA — «IT · Home Page»,
   «EN · Home Page» — e resta visibile anche quando il resto è tagliato.

Uso:  python scripts/pannello_lingue_chiare.py
"""

from __future__ import annotations

import pathlib
import re

CONFIG = (
    pathlib.Path(__file__).resolve().parent.parent / "public" / "admin" / "config.yml"
)

# I campi delle collezioni a pagine fisse sono rientrati di 10 spazi.
ANCORA_CAMPI = (
    "          - { label: 'Sezione «Territorio» — introduzione', "
    "name: territorioTesto, widget: text }\n"
)

CAMPO_CAROSELLO = """          # --- Il carosello ---------------------------------------------------
          # Le diapositive che scorrono in cima alla home. Ognuna porta a una
          # pagina: la fotografia è l'invito, la pagina è dove si va.
          - label: Carosello della home
            name: carosello
            widget: list
            required: false
            label_singular: Diapositiva
            summary: '{{fields.titolo}}'
            fields:
              - { label: Titolo, name: titolo, widget: string }
              - { label: Testo (due righe), name: testo, widget: text }
              - { label: Fotografia, name: immagine, widget: image, required: false }
              - label: Collegamento
                name: collegamento
                widget: string
                hint: 'La pagina a cui porta il clic, per esempio /camere'
"""


def main() -> int:
    testo = CONFIG.read_text(encoding="utf-8")

    # --- 1. Il campo del carosello, in tutte e due le collezioni della home ---
    if "name: carosello" in testo:
        print("  carosello: campo già presente")
    else:
        quante = testo.count(ANCORA_CAMPI)
        if quante != 2:
            print(f"  carosello: attese 2 righe di ancoraggio, trovate {quante}")
            return 1
        testo = testo.replace(ANCORA_CAMPI, ANCORA_CAMPI + "\n" + CAMPO_CAROSELLO, 2)
        print("  carosello: campo aggiunto alle due collezioni della home")

    # --- 2. Separatore fra le due lingue --------------------------------------
    if "- divider: true" in testo:
        print("  separatore: già presente")
    else:
        testa = "  - name: home-en\n"
        if testa not in testo:
            print("  separatore: la prima collezione inglese non si trova")
            return 1
        testo = testo.replace(
            testa,
            "  # --- Da qui in giù, le stesse collezioni in inglese -------------------\n"
            "  - divider: true\n\n" + testa,
            1,
        )
        print("  separatore: aggiunto fra italiano e inglese")

    # --- 3. I nomi: la lingua per prima --------------------------------------
    def rinomina(match: re.Match[str]) -> str:
        rientro, etichetta = match.group(1), match.group(2)
        if etichetta.startswith(("IT · ", "EN · ")):
            return match.group(0)
        # `rientro` contiene già «label: »: va scritta una volta sola.
        if " — English" in etichetta:
            return f"{rientro}EN · {etichetta.replace(' — English', '')}"
        return f"{rientro}IT · {etichetta}"

    prima = testo
    testo = re.sub(r"(?m)^(    label: )(.+)$", rinomina, testo)
    if testo != prima:
        print("  nomi: lingua messa davanti a ogni collezione")

    CONFIG.write_text(testo, encoding="utf-8", newline="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
