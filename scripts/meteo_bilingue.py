"""
Rende bilingue il riquadro del meteo.

IL PROBLEMA
Le etichette erano scritte dentro il componente e dentro il suo script: «Meteo»,
«Oggi», «Domani», «Vento», le ventisette condizioni, i nomi dei giorni. Sulla
scheda inglese di un sentiero il meteo sarebbe rimasto in italiano.

COME
I testi ora vengono dal dizionario (`src/i18n/ui.ts`, dove le ventisette
condizioni erano già state tradotte). Resta nel componente solo ciò che NON è
lingua: la mappa dal codice WMO al cielo da disegnare (`CIELI`), che è CSS.

Uso:  python scripts/meteo_bilingue.py
"""

from __future__ import annotations

import pathlib
import re

COMPONENTE = (
    pathlib.Path(__file__).resolve().parent.parent
    / "src" / "components" / "MeteoSentiero.astro"
)

# --- Testo semplice: una sostituzione per volta -----------------------------
SEMPLICI = [
    # Import e proprietà.
    (
        "export interface Props {",
        "import { linguaDaUrl, type Lingua } from '../i18n';\n"
        "import { traduzioni } from '../i18n/ui';\n\n"
        "export interface Props {",
    ),
    (
        "  /** Quota del punto, in metri. Facoltativa. */\n  quota?: number;\n}",
        "  /** Quota del punto, in metri. Facoltativa. */\n  quota?: number;\n"
        "  /** La lingua della pagina. */\n  lingua?: Lingua;\n}",
    ),
    (
        "const { latitudine, longitudine, localita, quota } = Astro.props;",
        "const { latitudine, longitudine, localita, quota, lingua = linguaDaUrl(Astro.url) } =\n"
        "  Astro.props;\nconst t = traduzioni(lingua).meteo;",
    ),
    # Il dato che serve allo script per scegliere la lingua.
    (
        "  data-luogo={localita}\n>",
        "  data-luogo={localita}\n  data-lingua={lingua}\n>",
    ),
    # Etichette statiche.
    ('<p class="meteo__etichetta">Meteo</p>', '<p class="meteo__etichetta">{t.etichetta}</p>'),
    (
        '<p class="meteo__attesa">Caricamento del meteo…</p>',
        '<p class="meteo__attesa">{t.caricamento}</p>',
    ),
    (
        """    Dati <a href="https://open-meteo.com/" rel="noopener" target="_blank">Open-Meteo</a>,
    aggiornati a ogni apertura della pagina.""",
        """    {t.fonte} <a href="https://open-meteo.com/" rel="noopener" target="_blank">{t.fonteLink}</a>.""",
    ),
    (
        """      Il meteo si carica con JavaScript attivo. Senza, resta il
      <a href="https://www.ilmeteo.it/meteo/Recoaro+Terme">bollettino di Recoaro Terme</a>.""",
        """      {t.senzaJavaScript}
      <a href="https://www.ilmeteo.it/meteo/Recoaro+Terme">{t.bollettino}</a>.""",
    ),
]


def main() -> int:
    testo = COMPONENTE.read_text(encoding="utf-8")

    for vecchio, nuovo in SEMPLICI:
        if vecchio in testo:
            testo = testo.replace(vecchio, nuovo, 1)
        else:
            print(f"  non trovato: {vecchio.strip().splitlines()[0][:60]}")

    # --- La mappa dei cieli: da codice WMO a classe CSS --------------------
    testo = testo.replace(
        "  const CONDIZIONI: Record<number, { testo: string; cielo: string }> = {",
        "  const CIELI: Record<number, string> = {",
        1,
    )
    # `0: { testo: 'Sereno', cielo: 'sereno' },` → `0: 'sereno',`
    testo = re.sub(
        r"(\d+): \{ testo: '[^']*', cielo: '([^']*)' \},",
        r"\1: '\2',",
        testo,
    )

    # --- I due cercatori --------------------------------------------------
    vecchio_condizione = """  /** Un codice sconosciuto non deve diventare «undefined» in pagina. */
  function condizione(codice: number) {
    return CONDIZIONI[codice] ?? { testo: 'Condizioni variabili', cielo: 'nuvoloso' };
  }"""
    nuovo_condizione = """  /*
    I testi vengono dal dizionario della lingua: qui resta solo il cielo da
    disegnare, che è una classe CSS e non ha lingua.
  */
  let m: ReturnType<typeof traduzioni>['meteo'];

  /** Il cielo da disegnare per un codice. */
  function cielo(codice: number): string {
    return CIELI[codice] ?? 'nuvoloso';
  }

  /** La condizione a parole. Un codice sconosciuto non diventa «undefined». */
  function testo(codice: number): string {
    return m.condizioni[codice] ?? m.condizioniVariabili;
  }"""
    if vecchio_condizione in testo:
        testo = testo.replace(vecchio_condizione, nuovo_condizione, 1)
    else:
        print("  funzione condizione non trovata")

    # --- I nomi dei giorni ------------------------------------------------
    testo = re.sub(
        r"  const GIORNI = \['domenica'.*?\];\n",
        "",
        testo,
        count=1,
        flags=re.S,
    )
    testo = testo.replace("return GIORNI[d.getDay()] ?? data;", "return m.giorni[d.getDay()] ?? data;")
    testo = testo.replace("if (indice === 0) return 'Oggi';", "if (indice === 0) return m.oggi;")
    testo = testo.replace("if (indice === 1) return 'Domani';", "if (indice === 1) return m.domani;")

    # --- I testi rimasti --------------------------------------------------
    testo = testo.replace('el.dataset.cielo = condizione(codice).cielo;', 'el.dataset.cielo = cielo(codice);')
    testo = testo.replace('dipingiCielo(el, d.current.weather_code);', 'dipingiCielo(el, d.current.weather_code);')
    testo = testo.replace(
        '<span class="meteo__condizione">${condizione(d.current.weather_code).testo}</span>',
        '<span class="meteo__condizione">${testo(d.current.weather_code)}</span>',
    )
    testo = testo.replace(
        "${condizione(oggi.weather_code[i]).testo}",
        "${testo(oggi.weather_code[i])}",
    )
    testo = testo.replace('<dt>Vento</dt>', '<dt>${m.vento}</dt>')
    testo = testo.replace('<dt>Oggi</dt>', '<dt>${m.oggi}</dt>')

    # Il messaggio di errore.
    vecchio_errore = re.compile(
        r"  function mostraErrore\(el: HTMLElement, corpo: HTMLElement\) \{.*?\n  \}",
        re.S,
    )
    nuovo_errore = """  function mostraErrore(el: HTMLElement, corpo: HTMLElement) {
    el.dataset.cielo = 'nuvoloso';
    corpo.setAttribute('aria-busy', 'false');
    corpo.innerHTML =
      `<p class="meteo__attesa">${m.errore} ` +
      '<a href="https://www.ilmeteo.it/meteo/Recoaro+Terme" rel="noopener" target="_blank">' +
      `${m.riprova}</a>.</p>`;
  }"""
    testo = vecchio_errore.sub(nuovo_errore, testo, count=1)

    # --- La lingua, letta dal riquadro ------------------------------------
    testo = testo.replace(
        "  function avvia() {\n    document.querySelectorAll<HTMLElement>('[data-meteo]').forEach((el) => {\n      void carica(el);\n    });\n  }",
        "  function avvia() {\n    document.querySelectorAll<HTMLElement>('[data-meteo]').forEach((el) => {\n"
        "      const codice = el.dataset.lingua === 'en' ? 'en' : 'it';\n"
        "      m = traduzioni(codice).meteo;\n"
        "      void carica(el);\n    });\n  }",
        1,
    )

    COMPONENTE.write_text(testo, encoding="utf-8", newline="")
    print("  meteo: scritto")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
