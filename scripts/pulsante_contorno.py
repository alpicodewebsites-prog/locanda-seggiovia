"""Fascia a colore unico e pulsante trasparente con bordo e testo gialli."""

from __future__ import annotations

import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
CSS = RADICE / "src" / "styles" / "global.css"

SOSTITUZIONI = [
    # --- 1. Il fondo della fascia: un colore solo -------------------------
    (
        """    /* Dal nero al grigio, in diagonale: un fondo piatto sembrerebbe un
       rettangolo vuoto. */
    background-color: var(--color-stone-900);
    background-image: linear-gradient(
      118deg,
      var(--color-stone-900) 0%,
      var(--color-stone-600) 52%,
      var(--color-stone-400) 100%
    );""",
        """    /* Un colore SOLO, fra il nero e il grigio. Non una sfumatura: la
       richiesta era un unico tono. È più scuro del grigio della pagina, così
       la fascia si stacca, e più chiaro del nero, così non sembra un buco. */
    background-color: var(--color-fascia-scura);""",
    ),
    # --- 2. Il pulsante: via il fondo, restano bordo e testo gialli --------
    (
        """    background-color: var(--color-accento);
    color: var(--color-accento-testo);
    font-size: clamp(1rem, 2vw, 1.25rem);""",
        """    /*
       Trasparente, con il bordo e il testo nel giallo della casa.
       Non ha più un fondo proprio: quello che lo identifica come comando è il
       contorno, che sul grigio scuro sta a 6,4:1 — ben oltre i 3:1 che il
       criterio sui contrasti chiede per il bordo di un comando.
    */
    background-color: transparent;
    border: 2px solid var(--color-accento);
    color: var(--color-accento);
    font-size: clamp(1rem, 2vw, 1.25rem);""",
    ),
    # --- 3. Il passaggio del mouse: velo giallo, non riempimento ---------
    (
        """  .pulsante-gnocchi:hover,
  .pulsante-gnocchi:focus-visible {
    background-color: var(--color-accento-scuro);
    transform: translateY(-2px);""",
        """  .pulsante-gnocchi:hover,
  .pulsante-gnocchi:focus-visible {
    /* Un velo appena percettibile, non un riempimento: il pulsante resta
       trasparente e lascia vedere il fondo della fascia. */
    background-color: color-mix(in srgb, var(--color-accento) 14%, transparent);
    border-color: var(--color-accento-chiaro);
    color: var(--color-accento-chiaro);
    transform: translateY(-2px);""",
    ),
    # --- 4. Il contorno del focus: giallo, non grigio --------------------
    (
        """  .pulsante-gnocchi:focus-visible {
    outline: 3px solid var(--color-forest-700);
    outline-offset: 3px;
  }""",
        """  .pulsante-gnocchi:focus-visible {
    outline: 2px solid var(--color-accento-chiaro);
    outline-offset: 4px;
  }""",
    ),
]

TOKEN = """  /* Fondo della fascia degli gnocchi: un grigio scuro, fra il nero e il grigio.
     Non è `stone-800` (quasi nero) né `stone-700` (più caldo e più chiaro):
     questo è il tono che regge il giallo del pulsante a 6,4:1. */
  --color-fascia-scura: #2b2a26;
  /* Giallo più chiaro, per il passaggio del mouse e il contorno del focus. */
  --color-accento-chiaro: #e0c48f;
"""


def main() -> int:
    css = CSS.read_text(encoding="utf-8")
    fatte = 0

    for vecchio, nuovo in SOSTITUZIONI:
        if vecchio in css:
            css = css.replace(vecchio, nuovo, 1)
            fatte += 1
        else:
            print(f"  NON TROVATO: {vecchio.strip().splitlines()[0][:64]}")

    # I due token nuovi, accanto agli altri.
    if "--color-fascia-scura" not in css:
        ancora = "  --color-accento-testo:"
        i = css.find(ancora)
        if i == -1:
            print("  punto di inserimento dei token non trovato")
            return 1
        css = css[:i] + TOKEN + "\n" + css[i:]
        print("  token aggiunti")

    CSS.write_text(css, encoding="utf-8", newline="")
    print(f"  sostituzioni: {fatte}/{len(SOSTITUZIONI)}")
    return 0 if fatte == len(SOSTITUZIONI) else 1


if __name__ == "__main__":
    raise SystemExit(main())
