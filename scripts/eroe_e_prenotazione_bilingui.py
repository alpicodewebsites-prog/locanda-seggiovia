"""
Rende bilingui l'apertura (Hero) e il modulo di prenotazione.

I due componenti erano scritti in italiano dentro il codice: i loro collegamenti
puntavano a `/sentieri`, `/camere`, `/grazie`, e le etichette dei campi erano
scritte a mano. Sulla home inglese sarebbero rimasti in italiano.

Qui i collegamenti passano da `percorsoLocalizzato` e le etichette dal
dizionario. I valori di riserva (quando il pannello non ha ancora compilato un
campo) restano: servono solo in quel caso.

Uso:  python scripts/eroe_e_prenotazione_bilingui.py
"""

from __future__ import annotations

import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
HERO = RADICE / "src" / "components" / "Hero.astro"
PREN = RADICE / "src" / "components" / "RichiestaPrenotazione.astro"

IMPORT = "import { percorsoLocalizzato, linguaDaUrl, type Lingua } from '../i18n';\n"

# --- Hero -------------------------------------------------------------------
HERO_SOSTITUZIONI = [
    (
        "export interface Props {",
        IMPORT + "\nexport interface Props {",
    ),
    (
        "  invitoGnocchi?: string;\n}",
        "  invitoGnocchi?: string;\n  /** La lingua della pagina: decide dove portano i collegamenti. */\n  lingua?: Lingua;\n}",
    ),
    (
        "  invitoGnocchi = 'Scopri la nostra produzione di gnocchi con la Fioreta',\n} = Astro.props;",
        "  invitoGnocchi = 'Scopri la nostra produzione di gnocchi con la Fioreta',\n  lingua = linguaDaUrl(Astro.url),\n} = Astro.props;",
    ),
    (
        '<a href={accesso.collegamento} class="accesso">',
        '<a href={percorsoLocalizzato(accesso.collegamento, lingua)} class="accesso">',
    ),
    (
        '<a href="/sentieri" class="link-arrow accesso-secondario">',
        '<a href={percorsoLocalizzato(\'/sentieri\', lingua)} class="link-arrow accesso-secondario">',
    ),
    (
        '<a href="/gnocchi-con-la-fioreta" class="link-arrow accesso-secondario">',
        '<a href={percorsoLocalizzato(\'/gnocchi-con-la-fioreta\', lingua)} class="link-arrow accesso-secondario">',
    ),
]

# --- RichiestaPrenotazione --------------------------------------------------
PREN_SOSTITUZIONI = [
    (
        "export interface Props {",
        IMPORT + "import { traduzioni } from '../i18n/ui';\n\nexport interface Props {",
    ),
    (
        "  id?: string;\n}",
        "  id?: string;\n  /** La lingua della pagina. */\n  lingua?: Lingua;\n}",
    ),
    (
        """const {
  titolo = 'Chiedi la disponibilità',
  descrizione = 'Scrivi quando vorresti arrivare. Ti rispondiamo noi, di solito entro un giorno.',
  id = 'modulo-prenotazione',
} = Astro.props;""",
        """const {
  id = 'modulo-prenotazione',
  lingua = linguaDaUrl(Astro.url),
} = Astro.props;

const t = traduzioni(lingua).prenotazione;
const titolo = Astro.props.titolo ?? t.titolo;
const descrizione = Astro.props.descrizione ?? t.descrizione;""",
    ),
    # Il ritorno del modulo va nella lingua giusta.
    (
        "const redirectUrl = new URL('/grazie', SITE_URL).href;",
        "const redirectUrl = new URL(percorsoLocalizzato('/grazie', lingua), SITE_URL).href;",
    ),
    (
        """const tipiCamera = [
  { value: 'singola', label: 'Camera singola' },
  { value: 'doppia', label: 'Camera doppia' },
  { value: 'indifferente', label: 'Non so ancora' },
];""",
        """const tipiCamera = [
  { value: 'singola', label: t.tipiCamera.singola },
  { value: 'doppia', label: t.tipiCamera.doppia },
  { value: 'indifferente', label: t.tipiCamera.indifferente },
];""",
    ),
    ('<span class="campo__etichetta">Arrivo</span>', '<span class="campo__etichetta">{t.arrivo}</span>'),
    (
        '<span class="campo__etichetta">Partenza</span>',
        '<span class="campo__etichetta">{t.partenza}</span>',
    ),
    ('<span class="campo__etichetta">Ospiti</span>', '<span class="campo__etichetta">{t.ospiti}</span>'),
    ('<span class="campo__etichetta">Camera</span>', '<span class="campo__etichetta">{t.camera}</span>'),
    (
        'Nomedicodice',
        'Nomedicodice',
    ),
    (
        """                Nome e cognome <span class="campo__obbligatorio" aria-hidden="true">*</span>""",
        """                {t.nome} <span class="campo__obbligatorio" aria-hidden="true">*</span>""",
    ),
    ('placeholder="Come ti chiami"', 'placeholder={t.placeholderNome}'),
    (
        '<span class="campo__etichetta">Note</span>',
        '<span class="campo__etichetta">{t.note}</span>',
    ),
    (
        '<button type="submit" class="btn btn--primary">Invia la richiesta</button>',
        '<button type="submit" class="btn btn--primary">{t.invia}</button>',
    ),
]


def applica(percorso: pathlib.Path, sostituzioni: list[tuple[str, str]]) -> None:
    testo = percorso.read_text(encoding="utf-8")
    for vecchio, nuovo in sostituzioni:
        if vecchio in testo:
            testo = testo.replace(vecchio, nuovo, 1)
        else:
            print(f"  {percorso.name}: NON TROVATO -> {vecchio.strip().splitlines()[0][:60]}")
    percorso.write_text(testo, encoding="utf-8", newline="")
    print(f"  {percorso.name}: fatto")


def main() -> int:
    applica(HERO, HERO_SOSTITUZIONI)
    applica(PREN, PREN_SOSTITUZIONI)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
