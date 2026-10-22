"""
Dettagli rossi nell'apertura della home.

DOVE E PERCHE' SOLO LI'
Il committente ha chiesto "qualche dettaglio rosso" nella home, legandolo al
logo. Non si sparge il rosso per tutto il sito: si mette dove il logo compare
per la prima volta e dove l'occhio si posa — i due accessi dell'apertura e i due
collegamenti in fondo.

  - una barretta rossa prima delle etichette DORMIRE / MANGIARE
  - i due collegamenti che si accendono di rosso al passaggio del mouse e al
    focus da tastiera

L'apertura sta su una fotografia con un velo scuro, quindi qui si usa il tono
CHIARO (`--color-rosso-locanda-chiaro`, 5,7:1). Il rosso del logo, su quel fondo,
non si vedrebbe.

Uso:  python scripts/rosso_nella_home.py
"""

from __future__ import annotations

import pathlib

HERO = pathlib.Path(__file__).resolve().parent.parent / "src" / "components" / "Hero.astro"

SOSTITUZIONI = [
    # --- La barretta rossa prima dell'etichetta ----------------------------
    (
        """  .accesso__eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--color-stone-400);""",
        """  .accesso__eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--color-stone-400);""",
    ),
]

# La barretta, aggiunta subito dopo la regola dell'etichetta.
BARRETTA = """
  /*
    La barretta rossa: prende il colore dal logo e lega le due etichette a
    quella dell'insegna. È l'unico rosso dell'apertura, e sta sopra il testo
    quindi non tocca la leggibilità.
  */
  .accesso__eyebrow::before {
    content: '';
    width: 1.15rem;
    height: 2px;
    border-radius: 1px;
    background-color: var(--color-rosso-locanda-chiaro);
  }
"""


def main() -> int:
    testo = HERO.read_text(encoding="utf-8")
    fatte = 0

    for vecchio, nuovo in SOSTITUZIONI:
        if vecchio in testo:
            testo = testo.replace(vecchio, nuovo, 1)
            fatte += 1
        else:
            print(f"  NON TROVATO: {vecchio.strip().splitlines()[0][:56]}")

    if ".accesso__eyebrow::before" not in testo:
        # Si aggancia alla fine della regola dell'etichetta: la prima `}` dopo
        # `.accesso__eyebrow {`.
        inizio = testo.find("  .accesso__eyebrow {")
        if inizio == -1:
            print("  regola dell'etichetta non trovata")
            return 1
        fine = testo.find("\n  }\n", inizio)
        if fine == -1:
            print("  chiusura della regola non trovata")
            return 1
        fine += len("\n  }\n")
        testo = testo[:fine] + BARRETTA + testo[fine:]
        print("  barretta rossa aggiunta alle etichette")

    # --- I collegamenti si accendono di rosso ------------------------------
    vecchio_hover = """  .accesso-secondario:hover,
  .accesso-secondario:focus-visible {
    color: var(--color-stone-50);
  }"""
    nuovo_hover = """  .accesso-secondario:hover,
  .accesso-secondario:focus-visible {
    color: var(--color-rosso-locanda-chiaro);
  }"""

    if vecchio_hover in testo:
        testo = testo.replace(vecchio_hover, nuovo_hover, 1)
        print("  collegamenti in rosso al passaggio del mouse")
        fatte += 1
    else:
        print("  hover dei collegamenti non trovato")

    HERO.write_text(testo, encoding="utf-8", newline="")
    print(f"  modifiche: {fatte}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
