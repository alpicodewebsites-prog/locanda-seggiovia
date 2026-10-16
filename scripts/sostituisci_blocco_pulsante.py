"""
Sostituisce il blocco di stile della fascia degli gnocchi con quello a pillola.

Uso:  python scripts/sostituisci_blocco_pulsante.py
"""

from __future__ import annotations

import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
CSS = RADICE / "src" / "styles" / "global.css"

INIZIO = "  /*\n    Fascia degli gnocchi — da bordo a bordo."
FINE = "  .btn--ghost {"

NUOVO = '''  /*
    Pulsante degli gnocchi — a pillola, largo quanto il suo testo.

    Non occupa tutta la pagina: si dimensiona sul contenuto e sta al centro.
    La forma tonda lo distingue dagli altri comandi del sito, che sono
    rettangolari — è l'unico elemento a pillola, quindi si riconosce.

    L'accento è quello del sito — `--color-accento`, la stessa ocra dei
    pulsanti — non un oro nuovo: un secondo tono quasi uguale si vedrebbe come
    una sbavatura. Il testo è scuro sopra, a 7,68:1 di contrasto.

    Transizioni: si elencano le proprietà una per una invece di `all`. `all`
    animerebbe anche cose che non devono muoversi e costa di più; l'effetto
    percepito è identico.
  */
  .pulsante-gnocchi {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    /* Larghezza dal contenuto, non dal contenitore. */
    width: fit-content;
    max-width: 100%;
    /* Forma a pillola: il raggio supera la metà dell'altezza, quindi i lati
       restano tondi a prescindere da quanto è alto il pulsante. */
    border-radius: 9999px;
    /* Orizzontale generoso: è quello che dà l'aria da pillola. */
    padding: 1.15rem 2.25rem;
    background-color: var(--color-accento);
    color: var(--color-accento-testo);
    font-size: clamp(1rem, 2vw, 1.25rem);
    font-weight: 600;
    line-height: 1.35;
    text-align: center;
    /* Va a capo se serve, ma le righe restano lunghe uguali. */
    text-wrap: balance;
    text-decoration: none;
    transition:
      background-color 300ms ease,
      color 300ms ease,
      transform 300ms ease,
      box-shadow 300ms ease;
  }

  .pulsante-gnocchi__freccia {
    flex: none;
    font-size: 1.1em;
    line-height: 1;
    /* Spostata a sinistra: all'apparire del puntatore scorre a destra. */
    transform: translateX(-0.15rem);
    transition: transform 300ms ease;
  }

  .pulsante-gnocchi:hover,
  .pulsante-gnocchi:focus-visible {
    background-color: var(--color-accento-scuro);
    transform: translateY(-2px);
    /* Ombra tenue e calda, non nera: su un fondo chiaro un'ombra grigia
       sporca, una colorata si posa. */
    box-shadow: 0 12px 26px -14px color-mix(in srgb, var(--color-accento-scuro) 75%, transparent);
  }

  .pulsante-gnocchi:hover .pulsante-gnocchi__freccia,
  .pulsante-gnocchi:focus-visible .pulsante-gnocchi__freccia {
    transform: translateX(0.35rem);
  }

  .pulsante-gnocchi:active {
    transform: translateY(0);
    box-shadow: none;
  }

  .pulsante-gnocchi:focus-visible {
    outline: 3px solid var(--color-forest-700);
    outline-offset: 3px;
  }

  @media (min-width: 768px) {
    .pulsante-gnocchi {
      padding: 1.3rem 3rem;
      gap: 0.85rem;
    }
  }

  /* Chi ha chiesto meno movimento non vede il sollevamento né lo scorrimento
     della freccia: la freccia resta visibile, semplicemente ferma. */
  @media (prefers-reduced-motion: reduce) {
    .pulsante-gnocchi,
    .pulsante-gnocchi__freccia {
      transition: none;
    }

    .pulsante-gnocchi:hover,
    .pulsante-gnocchi:focus-visible,
    .pulsante-gnocchi:active,
    .pulsante-gnocchi:hover .pulsante-gnocchi__freccia,
    .pulsante-gnocchi:focus-visible .pulsante-gnocchi__freccia {
      transform: none;
    }
  }

'''


def main() -> int:
    testo = CSS.read_text(encoding="utf-8")

    i = testo.find(INIZIO)
    if i == -1:
        print("blocco di partenza non trovato")
        return 1

    j = testo.find(FINE, i)
    if j == -1:
        print("confine finale non trovato")
        return 1

    righe = testo[i:j].count("\n")
    CSS.write_text(testo[:i] + NUOVO + testo[j:], encoding="utf-8", newline="")
    print(f"blocco sostituito ({righe} righe rimosse, {NUOVO.count(chr(10))} aggiunte)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
