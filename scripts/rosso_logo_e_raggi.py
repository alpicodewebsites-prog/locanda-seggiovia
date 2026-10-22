"""
Rosso del logo, logo nell'header, pulsanti piu' stondati.

IL ROSSO NON E' INVENTATO
E' campionato dal logo della locanda (`scripts/campiona_rosso_logo.py`):
il colore dominante e' #b51c06, la media #ab2617. Il tono scelto sta in mezzo.

TRE TONI, PERCHE' SERVONO A COSE DIVERSE
  --color-rosso-locanda        #b51c06  filetti e frecce su fondo CHIARO
  --color-rosso-locanda-scuro  #8e1a0a  testo su fondo chiaro (il #b51c06 come
                                         testo darebbe 3,9:1, sotto i 4,5:1)
  --color-rosso-locanda-chiaro #e88a74  qualunque cosa stia su fondo SCURO,
                                         come l'apertura: 5,7:1 sul velo scuro

Un solo rosso non poteva bastare: lo stesso colore che si vede bene su un fondo
chiaro sparisce su uno scuro. Chi ha chiesto il rosso ha chiesto un colore, non
un contrasto sbagliato.

I PULSANTI
`--raggio` era 2px: per questo i pulsanti sembravano squadrati. Passa a 0.75rem.
Toccava anche i campi dei moduli, ed e' giusto: un pulsante stondato accanto a un
campo squadrato sembra un errore.

IL LOGO
Nell'header non c'era: solo la scritta. Ora c'e', prima del nome, alto 36 px.
L'`alt` e' vuoto di proposito: il nome e' scritto subito accanto, e un lettore di
schermo lo leggerebbe due volte.

Uso:  python scripts/rosso_logo_e_raggi.py
"""

from __future__ import annotations

import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
CSS = RADICE / "src" / "styles" / "global.css"
HEADER = RADICE / "src" / "components" / "Header.astro"
HERO = RADICE / "src" / "components" / "Hero.astro"

TOKEN = """  /* --- Rosso della locanda ---------------------------------------------
     Campionato dal logo, non scelto a occhio. Tre toni perché lo stesso rosso
     non può stare su un fondo chiaro e su uno scuro: vedi i commenti qui sotto.
  */
  /* Filetti e frecce su fondo chiaro. */
  --color-rosso-locanda: #b51c06;
  /* Testo su fondo chiaro: il tono sopra darebbe 3,9:1. */
  --color-rosso-locanda-scuro: #8e1a0a;
  /* Tutto ciò che sta su fondo scuro, come l'apertura: 5,7:1 sul velo. */
  --color-rosso-locanda-chiaro: #e88a74;
"""


def main() -> int:
    # --- 1. Il foglio di stile --------------------------------------------
    css = CSS.read_text(encoding="utf-8")
    fatte = 0

    if "--raggio: 2px;" in css:
        css = css.replace("--raggio: 2px;", "--raggio: 0.75rem;", 1)
        print("  raggio dei pulsanti: 2px -> 0.75rem")
        fatte += 1

    if "--color-rosso-locanda" not in css:
        ancora = "  --color-cai-rosso: #c1272d;\n"
        if ancora not in css:
            print("  ancora dei colori non trovata")
            return 1
        css = css.replace(ancora, ancora + TOKEN, 1)
        print("  tre toni di rosso aggiunti")
        fatte += 1

    CSS.write_text(css, encoding="utf-8", newline="")
    print(f"  modifiche al foglio: {fatte}")

    # --- 2. Il logo nell'header -------------------------------------------
    header = HEADER.read_text(encoding="utf-8")

    if "imgLogo" not in header:
        # L'import va dopo l'ultimo import esistente.
        righe = header.splitlines()
        ultimo = max(i for i, r in enumerate(righe) if r.startswith("import "))
        righe.insert(ultimo + 1, "import imgLogo from '../assets/locanda-logo.png';")
        header = "\n".join(righe) + "\n"
        print("  header: import del logo aggiunto")

    if "site-header__logo" not in header:
        ancora = """    <a
      href="/"
      class="site-header__wordmark group flex shrink-0 items-baseline gap-2.5 leading-none"
      aria-label={`${site.nome} — home`}
    >"""
        if ancora not in header:
            print("  header: wordmark non trovato")
            return 1
        nuovo = """    <a
      href="/"
      class="site-header__wordmark group flex shrink-0 items-center gap-2.5 leading-none"
      aria-label={`${site.nome} — home`}
    >
      {/*
        Il logo, prima del nome. `alt` vuoto: il nome è scritto subito accanto,
        e con un alt lo si sentirebbe due volte. Sotto i 380 px resta nascosto,
        dove lo spazio è già conteso fra nome e pulsante «Contatti».
      */}
      <img
        src={imgLogo.src}
        alt=""
        width="47"
        height="36"
        decoding="async"
        class="site-header__logo hidden h-9 w-auto shrink-0 object-contain min-[380px]:block"
      />"""
        header = header.replace(ancora, nuovo, 1)
        print("  header: logo inserito prima del nome")

    HEADER.write_text(header, encoding="utf-8", newline="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
