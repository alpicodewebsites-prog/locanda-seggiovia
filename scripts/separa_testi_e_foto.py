"""
Separa i TESTI dalle FOTO e numera le fotografie secondo l'ordine del sito.

DUE PROBLEMI RISOLTI

1. NELLA LIBRERIA IMMAGINI COMPARIVANO I TESTI.
   Sveltia chiama le cartelle «Collezione › etichetta della voce». Con una voce
   sola per pagina, l'etichetta doveva nominare sia i testi sia le foto, e nella
   libreria — dove si gestiscono SOLO fotografie — si leggeva «Testi, paragrafi e
   foto». Fuorviante.
   Ora ogni pagina ha DUE voci: «Testi e paragrafi» e «Fotografie». La libreria
   mostra «Home Page › Fotografie», che è quello che serve.

2. LE FOTO NON ERANO IN ORDINE.
   La libreria ordina per nome, quindi `facciata.jpg` veniva prima di
   `hero.jpg`, mentre sul sito la prima cosa che si vede è l'apertura.
   I file ora hanno un numero davanti, e i numeri seguono l'ordine in cui le
   fotografie compaiono scorrendo la pagina.

Uso:  python scripts/separa_testi_e_foto.py
"""

from __future__ import annotations

import pathlib
import re
import shutil
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
ASSETS = RADICE / "src" / "assets"
CONTENUTI = RADICE / "src" / "content"

# I campi che sono fotografie: tutto il resto è testo.
CAMPI_FOTO = {
    "hero", "panorama", "montagne", "facciata", "cucina",
    "foto", "fotoPreparazione", "immagine",
}

# Rinominazioni: (percorso attuale, nuovo percorso). Il numero segue l'ordine
# in cui la fotografia compare nella pagina.
RINOMINE: list[tuple[str, str]] = [
    # --- Home: apertura, locanda, territorio, fascia finale -----------------
    ("home/hero.jpg", "home/01-apertura.jpg"),
    ("home/facciata.jpg", "home/02-locanda-esterno.jpg"),
    ("home/montagne.jpg", "home/03-montagne.jpg"),
    ("home/panorama.jpg", "home/04-panorama.jpg"),
    # --- La Locanda: il tavolo di cucina viene prima, nella pagina ----------
    ("la-locanda/cucina.jpg", "la-locanda/01-tavolo-di-cucina.jpg"),
    ("la-locanda/facciata.jpg", "la-locanda/02-locanda-esterno.jpg"),
    # --- Pagina Sentieri ----------------------------------------------------
    ("sentieri-pagina/montagne.jpg", "sentieri-pagina/01-montagne.jpg"),
    ("sentieri-pagina/panorama.jpg", "sentieri-pagina/02-panorama.jpg"),
    # --- Gnocchi: gli ingredienti vengono prima, nella pagina ---------------
    ("gnocchi/preparazione.jpg", "gnocchi/01-ingredienti.jpg"),
    ("gnocchi/piatto.jpg", "gnocchi/02-piatto-finito.jpg"),
    # --- Ristorante ---------------------------------------------------------
    ("ristorante/piatti/gnocchi-con-la-fioreta.jpg", "ristorante/piatti/01-gnocchi-con-la-fioreta.jpg"),
    ("ristorante/piatti/polenta-e-coniglio.webp", "ristorante/piatti/02-polenta-e-coniglio.webp"),
]

# Le copertine dei sentieri, numerate nell'ordine in cui i sentieri compaiono.
ORDINE_SENTIERI: list[tuple[str, str]] = [
    ("gino-solda.jpg", "01-gino-solda.jpg"),
    ("sentiero-mole.jpg", "02-sentiero-mole.jpg"),
    ("grandi-alberi.jpg", "03-grandi-alberi.jpg"),
    ("ponte-tibetano.jpg", "04-ponte-tibetano.jpg"),
    ("campogrosso.jpg", "05-campogrosso.jpg"),
    ("52-gallerie.jpg", "06-strada-52-gallerie.jpg"),
]


def rinomina_file() -> dict[str, str]:
    """Rinomina le fotografie. Restituisce la mappa vecchio -> nuovo percorso."""
    mappa: dict[str, str] = {}

    for vecchio, nuovo in RINOMINE:
        origine = ASSETS / vecchio
        destinazione = ASSETS / nuovo
        if not origine.is_file():
            continue
        destinazione.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(origine), str(destinazione))
        mappa[f"/assets/{vecchio}"] = f"/assets/{nuovo}"

    for vecchio, nuovo in ORDINE_SENTIERI:
        origine = ASSETS / "sentieri" / vecchio
        destinazione = ASSETS / "sentieri" / nuovo
        if not origine.is_file():
            continue
        shutil.move(str(origine), str(destinazione))
        mappa[f"/assets/sentieri/{vecchio}"] = f"/assets/sentieri/{nuovo}"

    return mappa


def aggiorna_riferimenti(mappa: dict[str, str]) -> int:
    """Riscrive i percorsi delle immagini in tutti i file di contenuto."""
    toccati = 0
    for md in sorted(CONTENUTI.rglob("*.md")):
        testo = md.read_text(encoding="utf-8")
        originale = testo
        for vecchio, nuovo in mappa.items():
            testo = testo.replace(vecchio, nuovo)
        if testo != originale:
            md.write_text(testo, encoding="utf-8", newline="")
            toccati += 1
    return toccati


def separa_testi_e_foto() -> int:
    """
    Divide ogni file di pagina in due: i testi e le fotografie.

    I commenti del file originale vengono conservati in testa a quello dei
    testi, così non si perde la documentazione.
    """
    separati = 0

    for cartella in ("home", "la-locanda", "sentieri-pagina", "gnocchi"):
        for file in sorted((CONTENUTI / cartella).glob("*.md")):
            # Solo i file chiamati `pagina.md` o `fioreta.md`: se la divisione è
            # già stata fatta, i file si chiamano `testi.md` e `foto.md`.
            if file.stem in {"testi", "foto"}:
                continue

            testo = file.read_text(encoding="utf-8")
            m = re.match(r"^---\n(.*?)\n---\n?$", testo, re.S)
            if not m:
                print(f"  salto {file.name}: non è un file con frontmatter")
                continue

            blocco = m.group(1)
            testi: list[str] = []
            foto: list[str] = []
            commenti: list[str] = []

            for riga in blocco.splitlines():
                spoglia = riga.strip()
                if spoglia.startswith("#") or not spoglia:
                    commenti.append(riga)
                    continue
                chiave = spoglia.split(":")[0].strip()
                if chiave in CAMPI_FOTO:
                    foto.append(riga)
                else:
                    testi.append(riga)

            intestazione = "\n".join(commenti).strip()

            (CONTENUTI / cartella / "testi.md").write_text(
                "---\n" + (intestazione + "\n\n" if intestazione else "") + "\n".join(testi) + "\n---\n",
                encoding="utf-8",
                newline="",
            )
            (CONTENUTI / cartella / "foto.md").write_text(
                "---\n"
                "# Fotografie della pagina. Si gestiscono dalla voce «Fotografie»\n"
                "# del pannello, e stanno nella cartella della loro sezione.\n\n"
                + "\n".join(foto)
                + "\n---\n",
                encoding="utf-8",
                newline="",
            )
            file.unlink()
            separati += 1
            print(f"  {cartella}/{file.name}  ->  testi.md + foto.md")

    return separati


def main() -> int:
    if not ASSETS.is_dir():
        print("cartella immagini non trovata")
        return 1

    print("=== 1. fotografie rinominate e numerate ===")
    mappa = rinomina_file()
    print(f"  file rinominati: {len(mappa)}")

    print("\n=== 2. riferimenti aggiornati ===")
    print(f"  file di contenuto aggiornati: {aggiorna_riferimenti(mappa)}")

    print("\n=== 3. testi e foto separati ===")
    print(f"  pagine divise: {separa_testi_e_foto()}")

    # --- Controllo finale ---------------------------------------------------
    print("\n=== 4. controllo: ogni riferimento esiste? ===")
    rotti = 0
    for md in sorted(CONTENUTI.rglob("*.md")):
        for riga in md.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\s*(\w+):\s*(/assets/\S+)\s*$", riga)
            if m and not (ASSETS / m.group(2).removeprefix("/assets/")).is_file():
                print(f"  ROTTO {md.relative_to(CONTENUTI)}: {m.group(2)}")
                rotti += 1
    print(f"  riferimenti rotti: {rotti}")

    return 1 if rotti else 0


if __name__ == "__main__":
    sys.exit(main())
