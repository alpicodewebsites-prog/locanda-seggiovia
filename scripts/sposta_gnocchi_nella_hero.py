"""
Sposta l'invito agli gnocchi dentro l'apertura, come secondo collegamento
leggero, e toglie la fascia col pulsante.

COSA CAMBIA

1. La fascia `.tavolo` della home sparisce: era un rettangolo scuro con dentro
   un pulsante, e sotto l'apertura non aggiungeva niente che l'apertura non
   dicesse già.

2. «Scopri la nostra produzione di gnocchi con la Fioreta» diventa un
   collegamento testuale identico a «Scopri i sentieri»: stessa classe, stesso
   aspetto, stessa risposta al puntatore e al focus. I due stanno su una griglia
   a due colonne con lo STESSO scarto della griglia dei due accessi, così
   ciascuno cade sotto la sua colonna: i sentieri sotto «Le camere», gli gnocchi
   sotto «Il ristorante».

   Usare la stessa classe non è pigrizia: è la garanzia che i due si comportino
   allo stesso modo oggi e domani. Se un giorno si cambia il colore del link,
   cambiano tutti e due.

3. Si toglie anche lo stile rimasto orfano: `.pulsante-gnocchi*`, `.tavolo*` e
   i due token che servivano solo a quelli.
"""

from __future__ import annotations

import pathlib
import re

RADICE = pathlib.Path(__file__).resolve().parent.parent
PAGINA = RADICE / "src" / "pages" / "index.astro"
HERO = RADICE / "src" / "components" / "Hero.astro"
CSS = RADICE / "src" / "styles" / "global.css"


# ---------------------------------------------------------------------------
# 1. La Hero: nuovo prop + i due collegamenti affiancati
# ---------------------------------------------------------------------------

NUOVO_BLOCCO_HERO = '''      <!--
        Due percorsi di peso minore, allineati sotto le rispettive colonne: chi
        cerca i sentieri o gli gnocchi li trova senza che l'apertura diventi una
        scelta fra tre cose uguali. Sono link testuali, non riquadri: la
        gerarchia resta leggibile.

        La griglia usa lo stesso `gap-x-14` di quella dei due accessi qui sopra,
        così ciascun collegamento cade esattamente sotto la sua colonna invece
        di galleggiare a sinistra.

        Stessa classe per tutti e due: si comportano allo stesso modo per
        costruzione, non per coincidenza.
      -->
      <ul class="mt-7 grid gap-x-14 gap-y-3 sm:grid-cols-2">
        <li>
          <a href="/sentieri" class="link-arrow accesso-secondario">
            {invitoSentieri}
            <svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true">
              <path
                d="M1 5h11m0 0L8.5 1.5M12 5l-3.5 3.5"
                stroke="currentColor"
                stroke-width="1.4"
                stroke-linecap="round"
                stroke-linejoin="round"></path>
            </svg>
          </a>
        </li>
        <li>
          <a href="/gnocchi-con-la-fioreta" class="link-arrow accesso-secondario">
            {invitoGnocchi}
            <svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true">
              <path
                d="M1 5h11m0 0L8.5 1.5M12 5l-3.5 3.5"
                stroke="currentColor"
                stroke-width="1.4"
                stroke-linecap="round"
                stroke-linejoin="round"></path>
            </svg>
          </a>
        </li>
      </ul>'''


def sistema_hero() -> int:
    testo = HERO.read_text(encoding="utf-8")

    # --- prop -------------------------------------------------------------
    if "invitoGnocchi" not in testo:
        testo = testo.replace(
            "  /** L'invito secondario ai sentieri. */\n  invitoSentieri?: string;",
            "  /** L'invito secondario ai sentieri. */\n  invitoSentieri?: string;\n"
            "  /** L'invito secondario agli gnocchi, accanto a quello dei sentieri. */\n"
            "  invitoGnocchi?: string;",
            1,
        )
        testo = testo.replace(
            "  invitoSentieri = 'Scopri i sentieri',",
            "  invitoSentieri = 'Scopri i sentieri',\n"
            "  invitoGnocchi = 'Scopri la nostra produzione di gnocchi con la Fioreta',",
            1,
        )
        print("  Hero: aggiunto il prop invitoGnocchi")

    # --- il blocco dei collegamenti ---------------------------------------
    inizio = testo.find('      <!--\n        Terzo percorso')
    if inizio == -1:
        print("  Hero: blocco dei collegamenti non trovato")
        return 1
    fine = testo.find("      </p>", inizio)
    if fine == -1:
        print("  Hero: fine del blocco non trovata")
        return 1
    fine += len("      </p>")

    testo = testo[:inizio] + NUOVO_BLOCCO_HERO + testo[fine:]
    print("  Hero: sostituito il collegamento singolo con i due affiancati")

    # --- la classe cambia nome (ora ne copre due) -------------------------
    testo = testo.replace(".accesso-sentieri", ".accesso-secondario")
    print("  Hero: classe rinominata in accesso-secondario")

    HERO.write_text(testo, encoding="utf-8", newline="")
    return 0


# ---------------------------------------------------------------------------
# 2. La pagina: via la fascia, dentro il prop
# ---------------------------------------------------------------------------


def sistema_pagina() -> int:
    testo = PAGINA.read_text(encoding="utf-8")

    # --- il prop alla Hero ------------------------------------------------
    if "invitoGnocchi" not in testo:
        testo = testo.replace(
            "    invitoSentieri={testi.invitoSentieri}\n  />",
            "    invitoSentieri={testi.invitoSentieri}\n"
            "    invitoGnocchi={testi.pulsanteGnocchi}\n  />",
            1,
        )
        print("  pagina: passato invitoGnocchi alla Hero")

    # --- la fascia --------------------------------------------------------
    inizio = testo.find("  <!-- ==================================================================\n       Invito alla pagina degli gnocchi")
    if inizio == -1:
        print("  pagina: commento della fascia non trovato")
        return 1
    fine = testo.find("  </section>", inizio)
    if fine == -1:
        print("  pagina: fine della fascia non trovata")
        return 1
    fine += len("  </section>\n")

    rimosse = testo[inizio:fine].count("\n")
    testo = testo[:inizio] + testo[fine:]
    print(f"  pagina: fascia rimossa ({rimosse} righe)")

    PAGINA.write_text(testo, encoding="utf-8", newline="")
    return 0


# ---------------------------------------------------------------------------
# 3. Lo stile rimasto orfano
# ---------------------------------------------------------------------------


def sistema_css() -> int:
    css = CSS.read_text(encoding="utf-8")

    # --- `.tavolo` e figli -------------------------------------------------
    i = css.find("  /*\n    ==========================================================================\n    LA FASCIA DEGLI GNOCCHI")
    if i != -1:
        j = css.find("  .btn--ghost", i)
        if j == -1:
            j = len(css)
        rimosse = css[i:j].count("\n")
        css = css[:i] + css[j:]
        print(f"  CSS: blocco .tavolo rimosso ({rimosse} righe)")

    # --- `.pulsante-gnocchi` e figli --------------------------------------
    i = css.find("  /*\n    ==========================================================================\n    IL PULSANTE DEGLI GNOCCHI")
    if i == -1:
        i = css.find("  .pulsante-gnocchi {")
    if i != -1:
        # Il blocco finisce dove comincia la regola successiva di pari livello.
        j = css.find("\n  .", css.find("\n  }", i))
        if j == -1:
            j = len(css)
        rimosse = css[i:j].count("\n")
        css = css[:i] + css[j:]
        print(f"  CSS: blocco .pulsante-gnocchi rimosso ({rimosse} righe)")

    # --- i due token che servivano solo a quelli --------------------------
    for token in ["--color-fascia-scura", "--color-accento-chiaro"]:
        righe = [
            r
            for r in css.splitlines()
            if r.strip().startswith(f"{token}:") or r.strip().startswith(f"{token} ")
        ]
        for r in righe:
            css = css.replace(r + "\n", "")
        if righe:
            print(f"  CSS: token {token} rimosso")

    CSS.write_text(css, encoding="utf-8", newline="")
    return 0


def main() -> int:
    if sistema_hero():
        return 1
    if sistema_pagina():
        return 1
    sistema_css()

    # Controllo: non deve restare niente di orfano.
    print()
    avanzi = []
    for percorso in [PAGINA, HERO, CSS]:
        t = percorso.read_text(encoding="utf-8")
        for ago in ["tavolo", "pulsante-gnocchi", "fascia-scura", "accento-chiaro", "accesso-sentieri"]:
            if ago in t:
                avanzi.append(f"{percorso.name}: {ago}")
    print("  residui:", avanzi if avanzi else "nessuno")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
