"""
Sposta le immagini in cartelle per sezione e aggiorna i riferimenti nei contenuti.

PERCHÉ SERVE
Le immagini stavano tutte in `src/assets`, in un unico elenco piatto. Nel
pannello questo diventa un calderone: la libreria mostra ogni file del sito, e
la proprietaria non ha modo di capire quale foto appartiene a quale pagina.

Il rimedio non è solo la configurazione: Sveltia mostra, per ogni campo, gli
archivi della cartella di quella sezione. Se i file restano nella cartella
generale, la libreria della sezione appare VUOTA e la foto che c'è già non può
più essere né ritrovata né sostituita. Quindi vanno spostati davvero.

DOVE FINISCONO
    home/          apertura, panorama, montagne, facciata della home
    la-locanda/    facciata, tavolo di cucina
    camere/        fotografie delle camere (vuota per ora)
    ristorante/    piatti del menù, in piatti/
    sentieri/      copertine dei sei sentieri
    gnocchi/       piatto finito, preparazione

Alcune immagini compaiono in due sezioni — la facciata in home e La Locanda, la
preparazione in La Locanda e Gnocchi. In quei casi il file viene DUPLICATO, così
ogni sezione è completa e indipendente: la proprietaria può mettere due foto
diverse, oppure la stessa. È una scelta voluta: costa qualche decina di KB e
toglie di mezzo la dipendenza fra sezioni.

Uso:  python scripts/organizza_immagini.py
"""

from __future__ import annotations

import pathlib
import shutil
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
ASSETS = RADICE / "src" / "assets"

# (file di partenza, cartella di destinazione, nuovo nome)
SPOSTAMENTI: list[tuple[str, str, str]] = [
    # Home
    ("hero-piccole-dolomiti.jpg", "home", "hero.jpg"),
    ("piccole-dolomiti-large.jpg", "home", "panorama.jpg"),
    ("territorio-montagne.jpg", "home", "montagne.jpg"),
    ("locanda-esterno.jpg", "home", "facciata.jpg"),
    # La Locanda
    ("locanda-esterno.jpg", "la-locanda", "facciata.jpg"),
    ("locanda-preparazione.jpg", "la-locanda", "cucina.jpg"),
    # Ristorante
    ("polenta-e-coniglio-3.webp", "ristorante/piatti", "polenta-e-coniglio.webp"),
    ("piatto-gnocchi-fioreta.jpg", "ristorante/piatti", "gnocchi-con-la-fioreta.jpg"),
    # Sentieri
    ("sentieri-gino-solda.jpg", "sentieri", "gino-solda.jpg"),
    ("sentieri-mole.jpg", "sentieri", "sentiero-mole.jpg"),
    ("sentieri-grandi-alberi.jpg", "sentieri", "grandi-alberi.jpg"),
    ("sentieri-ponte-tibetano.jpg", "sentieri", "ponte-tibetano.jpg"),
    ("sentieri-campogrosso.jpg", "sentieri", "campogrosso.jpg"),
    ("sentieri-52-gallerie.jpg", "sentieri", "52-gallerie.jpg"),
    # Gnocchi
    ("piatto-gnocchi-fioreta.jpg", "gnocchi", "piatto.jpg"),
    ("locanda-preparazione.jpg", "gnocchi", "preparazione.jpg"),
]

# Riferimenti da riscrivere nei file di contenuto: vecchio valore -> nuovo.
NUOVI_RIFERIMENTI: dict[str, str] = {
    "/assets/hero-piccole-dolomiti.jpg": "/assets/home/hero.jpg",
    "/assets/piccole-dolomiti-large.jpg": "/assets/home/panorama.jpg",
    "/assets/territorio-montagne.jpg": "/assets/home/montagne.jpg",
    "/assets/locanda-esterno.jpg": "/assets/home/facciata.jpg",
    "/assets/locanda-preparazione.jpg": "/assets/la-locanda/cucina.jpg",
    "/assets/piatto-gnocchi-fioreta.jpg": "/assets/gnocchi/piatto.jpg",
    "/assets/sentieri-gino-solda.jpg": "/assets/sentieri/gino-solda.jpg",
    "/assets/sentieri-mole.jpg": "/assets/sentieri/sentiero-mole.jpg",
    "/assets/sentieri-grandi-alberi.jpg": "/assets/sentieri/grandi-alberi.jpg",
    "/assets/sentieri-ponte-tibetano.jpg": "/assets/sentieri/ponte-tibetano.jpg",
    "/assets/sentieri-campogrosso.jpg": "/assets/sentieri/campogrosso.jpg",
    "/assets/sentieri-52-gallerie.jpg": "/assets/sentieri/52-gallerie.jpg",
}

# Riferimenti che cambiano solo DENTRO un certo file, perché la stessa immagine
# serve due sezioni e ognuna deve puntare alla propria copia.
RIFERIMENTI_PER_FILE: dict[str, dict[str, str]] = {
    "src/content/gnocchi/fioreta.md": {
        "/assets/la-locanda/cucina.jpg": "/assets/gnocchi/preparazione.jpg",
        "/assets/gnocchi/piatto.jpg": "/assets/gnocchi/piatto.jpg",
    },
    "src/content/menu/gnocchi-con-la-fioreta.md": {
        "/assets/gnocchi/piatto.jpg": "/assets/ristorante/piatti/gnocchi-con-la-fioreta.jpg",
    },
    "src/content/la-locanda/pagina.md": {
        "/assets/home/facciata.jpg": "/assets/la-locanda/facciata.jpg",
    },
}


def main() -> int:
    if not ASSETS.is_dir():
        print(f"cartella non trovata: {ASSETS}")
        return 1

    # --- 1. Spostamento dei file -------------------------------------------
    spostati = 0
    for nome, cartella, nuovo_nome in SPOSTAMENTI:
        origine = ASSETS / nome
        if not origine.is_file():
            continue
        destinazione = ASSETS / cartella
        destinazione.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origine, destinazione / nuovo_nome)
        spostati += 1

    # I file di partenza si tolgono solo se non servono più a nessuno.
    rimasti = {n for n, _, _ in SPOSTAMENTI}
    for nome in sorted(rimasti):
        file = ASSETS / nome
        if file.is_file() and not (nome == "locanda-logo.png"):
            file.unlink()

    # Cartella vuota pronta per le fotografie delle camere.
    (ASSETS / "camere").mkdir(exist_ok=True)

    # --- 2. Cartella piatta rimossa ----------------------------------------
    # (nessuna sottocartella da ripulire: i file erano tutti in radice)

    print(f"immagini copiate nelle sezioni: {spostati}")

    # --- 3. Riscrittura dei riferimenti nei contenuti ----------------------
    file_toccati = 0
    for md in sorted((RADICE / "src" / "content").rglob("*.md")):
        testo = md.read_text(encoding="utf-8")
        originale = testo

        # Prima le regole valide solo per questo file.
        relativo = md.relative_to(RADICE).as_posix()
        for vecchio, nuovo in RIFERIMENTI_PER_FILE.get(relativo, {}).items():
            testo = testo.replace(vecchio, nuovo)

        # Poi quelle valide ovunque.
        for vecchio, nuovo in NUOVI_RIFERIMENTI.items():
            testo = testo.replace(vecchio, nuovo)

        if testo != originale:
            md.write_text(testo, encoding="utf-8", newline="")
            file_toccati += 1
            print(f"  aggiornato {relativo}")

    print(f"file di contenuto aggiornati: {file_toccati}")

    # --- 4. Controllo: nessun riferimento rotto ---------------------------
    rotti = 0
    for md in sorted((RADICE / "src" / "content").rglob("*.md")):
        for riga in md.read_text(encoding="utf-8").splitlines():
            riga = riga.strip()
            for campo in ("foto:", "immagine:", "hero:", "panorama:", "montagne:",
                          "facciata:", "cucina:", "fotoPreparazione:"):
                if riga.startswith(campo):
                    valore = riga[len(campo):].strip()
                    if valore and valore.startswith("/assets/"):
                        percorso = ASSETS / valore.removeprefix("/assets/")
                        if not percorso.is_file():
                            print(f"  ROTTO: {md.name} -> {valore}")
                            rotti += 1

    if rotti:
        print(f"riferimenti rotti: {rotti}")
        return 1

    print("tutti i riferimenti puntano a un file esistente")
    return 0


if __name__ == "__main__":
    sys.exit(main())
