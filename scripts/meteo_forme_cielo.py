"""
Aggiunge al meteo nuvole, sole e pioggia DISEGNATI, non solo una tinta.

Il committente l'ha chiesto due volte: "dietro al meteo metti uno sfondo del tipo
nuvoloso quando e' nuvoloso, soleggiato quando e' soleggiato". La prima versione
tingeva soltanto il fondo di grigio o di oro. Si capiva, ma non si VEDEVA.

Qui si aggiungono forme: un disco di sole con l'alone, banchi di nuvole fatti di
ellissi sfumate, la nebbia a bande, i fiocchi, e nel temporale un lampo.

Sono gradienti radiali, quindi non servono file: la scheda non guadagna un solo
byte di immagine. E restano tutti CHIARI, perche' il testo scuro deve restare
leggibile: il controllo del contrasto misura i pixel veri, non le intenzioni.

Uso:  python scripts/meteo_forme_cielo.py
"""

from __future__ import annotations

import pathlib

COMPONENTE = (
    pathlib.Path(__file__).resolve().parent.parent
    / "src"
    / "components"
    / "MeteoSentiero.astro"
)

ANCORA = "  /* --- I cieli ---------------------------------------------------------"

FORME = '''  /* --- Le forme del cielo ----------------------------------------------
     Il fondo dice il colore; queste forme dicono COSA sta succedendo.
     Stanno su un livello sotto il testo, che ha `position: relative`.
  */
  .meteo::before {
    content: '';
    position: absolute;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    background-repeat: no-repeat;
  }

  /* Sole: disco pieno, alone, e un accenno di raggi. */
  .meteo[data-cielo='sereno']::before {
    background-image:
      radial-gradient(circle at 84% 16%, #fffaf0 0 7%, rgba(255, 248, 225, 0.75) 7% 12%, transparent 12.5%),
      radial-gradient(circle at 84% 16%, rgba(255, 245, 205, 0.55) 0 22%, transparent 30%);
  }

  .meteo[data-cielo='poco-nuvoloso']::before {
    background-image:
      radial-gradient(circle at 82% 15%, #fffdf6 0 6%, rgba(255, 250, 232, 0.7) 6% 11%, transparent 11.5%),
      /* una nuvola bassa, sul fianco */
      radial-gradient(ellipse 46% 26% at 18% 88%, rgba(255, 255, 255, 0.7), transparent 72%),
      radial-gradient(ellipse 34% 20% at 40% 92%, rgba(255, 255, 255, 0.6), transparent 74%);
  }

  /* Nuvoloso: banchi sovrapposti, chiari sopra e più densi in basso. */
  .meteo[data-cielo='nuvoloso']::before {
    background-image:
      radial-gradient(ellipse 52% 34% at 24% 26%, rgba(255, 255, 255, 0.8), transparent 70%),
      radial-gradient(ellipse 40% 28% at 58% 16%, rgba(255, 255, 255, 0.68), transparent 72%),
      radial-gradient(ellipse 64% 40% at 86% 46%, rgba(255, 255, 255, 0.6), transparent 74%),
      radial-gradient(ellipse 70% 30% at 40% 96%, rgba(120, 122, 118, 0.18), transparent 76%);
  }

  /* Nebbia: bande orizzontali, larghe e sfumate. */
  .meteo[data-cielo='nebbia']::before {
    background-image:
      linear-gradient(180deg, rgba(255, 255, 255, 0.55) 0 12%, transparent 30%),
      radial-gradient(ellipse 90% 16% at 50% 52%, rgba(255, 255, 255, 0.6), transparent 78%),
      radial-gradient(ellipse 90% 14% at 50% 78%, rgba(255, 255, 255, 0.5), transparent 78%);
  }

  /* Pioggia e rovesci: una nube in alto e le gocce che scendono. */
  .meteo[data-cielo='pioggia']::before,
  .meteo[data-cielo='rovesci']::before {
    background-image:
      radial-gradient(ellipse 58% 30% at 30% 8%, rgba(255, 255, 255, 0.7), transparent 72%),
      radial-gradient(ellipse 46% 24% at 72% 4%, rgba(255, 255, 255, 0.6), transparent 74%);
  }

  /* Neve: due nubi e i fiocchi sparsi. */
  .meteo[data-cielo='neve']::before {
    background-image:
      radial-gradient(ellipse 54% 28% at 26% 8%, rgba(255, 255, 255, 0.85), transparent 72%),
      radial-gradient(ellipse 44% 24% at 68% 5%, rgba(255, 255, 255, 0.75), transparent 74%),
      radial-gradient(circle at 30% 62%, #ffffff 0 2px, transparent 2.5px),
      radial-gradient(circle at 68% 74%, #ffffff 0 2px, transparent 2.5px),
      radial-gradient(circle at 46% 86%, #ffffff 0 1.6px, transparent 2.2px),
      radial-gradient(circle at 84% 58%, #ffffff 0 1.6px, transparent 2.2px);
  }

  /* Temporale: nube scura in alto e il lampo. */
  .meteo[data-cielo='temporale']::before {
    background-image:
      radial-gradient(ellipse 62% 34% at 34% 6%, rgba(70, 72, 68, 0.42), transparent 70%),
      radial-gradient(ellipse 48% 26% at 74% 2%, rgba(70, 72, 68, 0.36), transparent 72%),
      linear-gradient(112deg, transparent 46%, rgba(255, 252, 232, 0.85) 49%, transparent 52%);
  }

'''

# Il corpo del riquadro deve stare sopra le forme anche quando è vuoto
# (durante il caricamento) e quando mostra l'errore.
SOSTITUZIONI = [
    (
        "  .meteo__corpo {\n",
        "  .meteo__corpo {\n    position: relative;\n",
    ),
]


def main() -> int:
    testo = COMPONENTE.read_text(encoding="utf-8")

    if "Le forme del cielo" in testo:
        print("  forme già presenti")
    else:
        if ANCORA not in testo:
            print("  punto di inserimento non trovato")
            return 1
        testo = testo.replace(ANCORA, FORME + ANCORA, 1)
        print("  forme del cielo aggiunte")

    fatte = 0
    for vecchio, nuovo in SOSTITUZIONI:
        if vecchio in testo:
            testo = testo.replace(vecchio, nuovo, 1)
            fatte += 1
    print(f"  correzioni di livello: {fatte}/{len(SOSTITUZIONI)}")

    COMPONENTE.write_text(testo, encoding="utf-8", newline="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
