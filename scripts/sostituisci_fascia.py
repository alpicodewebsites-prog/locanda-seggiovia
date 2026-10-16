"""Sostituisce la fascia degli ingredienti con la versione a sole immagini."""

from __future__ import annotations

import pathlib
import re

RADICE = pathlib.Path(__file__).resolve().parent.parent
PAGINA = RADICE / "src" / "pages" / "index.astro"

NUOVO = '''  <!-- ==================================================================
       La fascia degli gnocchi
       ------------------------------------------------------------------
       Prima qui c'erano solo il pulsante e una fascia grigia vuota: il
       pulsante sembrava appoggiato li' per caso.

       Ora il fondo e' il legno del tavolo e sopra ci stanno tre dettagli
       fotografici degli ingredienti. NIENTE TESTI: nessun titolo, nessun
       valore, nessun elenco. Le immagini fanno da sfondo alla fascia e il
       pulsante ci sta sopra come l'azione di quella parte della pagina.

       I tre dettagli sono ritagli di una fotografia VERA della locanda — il
       tavolo con la fioreta, la farina, il burro e il formaggio — non immagini
       d'archivio. Sono tutti dello stesso formato, cosi' la fila resta ordinata.

       Le immagini sono decorative: non aggiungono informazione che la pagina
       non dia gia', quindi vanno con `alt` vuoto. La sezione ha comunque un
       nome, per chi naviga con un lettore di schermo.
       ================================================================== -->
  <section class="tavolo" aria-label="Gli gnocchi con la Fioreta">
    <div class="shell">
      <ul class="tavolo__dettagli">
        {
          dettagliIngredienti.map((dettaglio) => (
            <li class="dettaglio">
              <Image
                src={dettaglio}
                alt=""
                widths={[144, 216, 288, 432]}
                sizes="(min-width: 768px) 15vw, 30vw"
                format="webp"
                quality={82}
                loading="lazy"
                decoding="async"
              />
            </li>
          ))
        }
      </ul>

      <div class="tavolo__invito">
        <a href="/gnocchi-con-la-fioreta" class="pulsante-gnocchi">
          {testi.pulsanteGnocchi}
          <span class="pulsante-gnocchi__freccia" aria-hidden="true">→</span>
        </a>
      </div>
    </div>
  </section>
'''


def main() -> int:
    testo = PAGINA.read_text(encoding="utf-8")

    inizio = testo.find("  <!-- ==================================================================\n       Il tavolo degli gnocchi")
    if inizio == -1:
        print("sezione non trovata")
        return 1

    fine = testo.find("  </section>", inizio)
    if fine == -1:
        print("fine sezione non trovata")
        return 1
    fine += len("  </section>\n")

    PAGINA.write_text(testo[:inizio] + NUOVO + testo[fine:], encoding="utf-8", newline="")
    print("sezione sostituita")

    # --- Le variabili degli ingredienti non servono piu' -------------------
    t = PAGINA.read_text(encoding="utf-8")
    vecchio_blocco = re.search(
        r"/\*\*\n \* Gli ingredienti degli gnocchi.*?\n\);\n\n", t, re.S
    )
    if vecchio_blocco:
        t = t.replace(vecchio_blocco.group(0), "")
        print("rimosse le variabili degli ingredienti")

    # Si aggiunge la lista dei tre dettagli, presi dalla cartella.
    import glob

    dettagli = sorted(
        p.name
        for p in (RADICE / "src" / "assets" / "gnocchi" / "dettagli").glob("*.jpg")
    )
    print(f"  dettagli trovati: {dettagli}")

    if "dettagliIngredienti" in t and "const dettagliIngredienti" not in t:
        elenco = ",\n".join(
            f"  (await import('../assets/gnocchi/dettagli/{n}')).default" for n in dettagli
        )
        ancora = "/**\n * Home — pagina di apertura."
        blocco = (
            "/**\n"
            " * I tre dettagli fotografici degli ingredienti, per la fascia della home.\n"
            " *\n"
            " * Sono ritagli di una fotografia vera della locanda. Stanno in\n"
            " * `src/assets/gnocchi/dettagli/` e si sostituiscono rigenerandoli con\n"
            " * `python scripts/ritaglia_ingredienti.py`.\n"
            " */\n"
            "const dettagliIngredienti = [\n" + elenco + ",\n];\n\n"
        )
        t = t.replace(ancora, blocco + ancora, 1)
        print("aggiunta la lista dei dettagli")

    PAGINA.write_text(t, encoding="utf-8", newline="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
