"""
Rende riconoscibile il tempo: nuvole piu' visibili e un simbolo accanto ai gradi.

IL PROBLEMA
Le nuvole erano disegnate in bianco su un cielo gia' chiaro. Sulla carta il
contrasto doveva vedersi; guardando il fotogramma, non si vedeva niente: erano
bianco su crema. La tinta del fondo cambiava, le nuvole no.

DUE CORREZIONI

1. Nuvole in un grigio, non in bianco. Diventano masse leggibili.
   Ma non si puo' scurire a piacere: il fondo deve restare abbastanza chiaro
   perché il testo piccolo ci stia sopra a 4,5:1. Quindi la densita' cambia per
   cielo: forte dove il fondo e' chiaro (nuvoloso, neve), leggera sul temporale,
   che e' gia' scuro di suo.

2. Un simbolo del tempo accanto alla temperatura. Il fondo dice l'atmosfera; il
   simbolo dice la condizione senza ambiguita', e non dipende da quanto e' scuro
   il cielo. E' l'unica parte di questo riquadro che si legge anche a colpo
   d'occhio su uno schermo piccolo.

Uso:  python scripts/meteo_simboli.py
"""

from __future__ import annotations

import pathlib
import re

COMPONENTE = (
    pathlib.Path(__file__).resolve().parent.parent
    / "src"
    / "components"
    / "MeteoSentiero.astro"
)

# --- Le nuvole, riscritte in grigio -----------------------------------------
NUOVE_FORME = '''  /* --- Le forme del cielo ----------------------------------------------
     Il fondo dice il colore; queste forme dicono COSA sta succedendo.

     Sono grigie, non bianche: su un cielo chiaro una nuvola bianca non si vede,
     e la prima versione di questo riquadro aveva esattamente quel difetto.

     La densità cambia con il cielo: più marcata dove il fondo è chiaro, più
     leggera sul temporale, che è già scuro e non tollera altro grigio sopra il
     testo.
  */
  .meteo::before {
    content: '';
    position: absolute;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    background-repeat: no-repeat;
  }

  .meteo[data-cielo='sereno']::before {
    background-image:
      radial-gradient(circle at 84% 16%, #fffaf0 0 7%, rgba(255, 248, 225, 0.75) 7% 12%, transparent 12.5%),
      radial-gradient(circle at 84% 16%, rgba(255, 245, 205, 0.55) 0 22%, transparent 30%);
  }

  .meteo[data-cielo='poco-nuvoloso']::before {
    background-image:
      radial-gradient(circle at 84% 14%, #fffdf6 0 6%, rgba(255, 250, 232, 0.7) 6% 11%, transparent 11.5%),
      radial-gradient(ellipse 44% 22% at 20% 88%, rgba(120, 123, 118, 0.30), transparent 70%),
      radial-gradient(ellipse 32% 17% at 42% 93%, rgba(120, 123, 118, 0.24), transparent 72%);
  }

  .meteo[data-cielo='nuvoloso']::before {
    background-image:
      radial-gradient(ellipse 50% 30% at 24% 24%, rgba(118, 121, 116, 0.34), transparent 70%),
      radial-gradient(ellipse 38% 24% at 58% 14%, rgba(118, 121, 116, 0.30), transparent 72%),
      radial-gradient(ellipse 60% 32% at 86% 42%, rgba(118, 121, 116, 0.26), transparent 74%),
      radial-gradient(ellipse 66% 22% at 40% 96%, rgba(118, 121, 116, 0.20), transparent 76%);
  }

  .meteo[data-cielo='nebbia']::before {
    background-image:
      linear-gradient(180deg, rgba(255, 255, 255, 0.45) 0 12%, transparent 30%),
      radial-gradient(ellipse 90% 14% at 50% 52%, rgba(255, 255, 255, 0.70), transparent 78%),
      radial-gradient(ellipse 90% 12% at 50% 78%, rgba(255, 255, 255, 0.60), transparent 78%);
  }

  .meteo[data-cielo='pioggia']::before,
  .meteo[data-cielo='rovesci']::before {
    background-image:
      radial-gradient(ellipse 54% 26% at 30% 6%, rgba(112, 116, 116, 0.34), transparent 72%),
      radial-gradient(ellipse 44% 21% at 72% 3%, rgba(112, 116, 116, 0.28), transparent 74%);
  }

  .meteo[data-cielo='neve']::before {
    background-image:
      radial-gradient(ellipse 50% 24% at 26% 6%, rgba(130, 136, 137, 0.28), transparent 72%),
      radial-gradient(ellipse 42% 20% at 68% 4%, rgba(130, 136, 137, 0.24), transparent 74%),
      radial-gradient(circle at 30% 62%, #ffffff 0 2px, transparent 2.5px),
      radial-gradient(circle at 68% 74%, #ffffff 0 2px, transparent 2.5px),
      radial-gradient(circle at 46% 86%, #ffffff 0 1.6px, transparent 2.2px),
      radial-gradient(circle at 84% 58%, #ffffff 0 1.6px, transparent 2.2px);
  }

  /* Il temporale è già scuro: le nuvole restano leggere, e il lampo fa il
     resto. Scurirle ancora porterebbe il testo sotto la soglia. */
  .meteo[data-cielo='temporale']::before {
    background-image:
      radial-gradient(ellipse 58% 28% at 34% 5%, rgba(84, 86, 82, 0.20), transparent 70%),
      radial-gradient(ellipse 44% 22% at 74% 2%, rgba(84, 86, 82, 0.16), transparent 72%),
      linear-gradient(112deg, transparent 46%, rgba(255, 252, 232, 0.85) 49%, transparent 52%);
  }

'''

# --- Il simbolo del tempo ---------------------------------------------------
GLIFI = '''  /*
    Il simbolo del tempo. Il fondo dice l'atmosfera; questo dice la condizione.

    Sta accanto alla temperatura e non nel fondo perché il fondo è subordinato
    al contrasto del testo: non può diventare scuro quanto servirebbe per far
    vedere una nuvola. Il simbolo no: è un contorno, si legge sempre.
  */
  const GLIFI: Record<string, string> = {
    sereno:
      '<circle cx="12" cy="12" r="4.2"/><path d="M12 2.6v2.4M12 19v2.4M2.6 12h2.4M19 12h2.4M5.4 5.4l1.7 1.7M16.9 16.9l1.7 1.7M18.6 5.4l-1.7 1.7M7.1 16.9l-1.7 1.7"/>',
    'poco-nuvoloso':
      '<circle cx="9" cy="9" r="3.4"/><path d="M9 3.2v1.6M3.2 9h1.6M4.9 4.9l1.1 1.1"/><path d="M9 18.5h8a3 3 0 0 0 .3-6 4.6 4.6 0 0 0-8.6-1"/>',
    nuvoloso:
      '<path d="M6.5 18h10.5a3.3 3.3 0 0 0 .3-6.6 5 5 0 0 0-9.4-1.2A3.3 3.3 0 0 0 6.5 18z"/>',
    nebbia:
      '<path d="M5 9.5h14M4 13h16M6 16.5h12M7.5 20h9"/>',
    pioggia:
      '<path d="M6.5 14h10.5a3.3 3.3 0 0 0 .3-6.6 5 5 0 0 0-9.4-1.2A3.3 3.3 0 0 0 6.5 14z"/><path d="M8.5 17l-1 3M12.5 17l-1 3M16.5 17l-1 3"/>',
    rovesci:
      '<path d="M6.5 13h10.5a3.3 3.3 0 0 0 .3-6.6 5 5 0 0 0-9.4-1.2A3.3 3.3 0 0 0 6.5 13z"/><path d="M8 16l-1.4 4M12 16l-1.4 4M16 16l-1.4 4"/>',
    neve:
      '<path d="M6.5 14h10.5a3.3 3.3 0 0 0 .3-6.6 5 5 0 0 0-9.4-1.2A3.3 3.3 0 0 0 6.5 14z"/><circle cx="9" cy="18" r="1.1"/><circle cx="13" cy="19.4" r="1.1"/><circle cx="17" cy="17.6" r="1.1"/>',
    temporale:
      '<path d="M6.5 13h10.5a3.3 3.3 0 0 0 .3-6.6 5 5 0 0 0-9.4-1.2A3.3 3.3 0 0 0 6.5 13z"/><path d="M13.4 15l-3 4.2h2.4l-.9 3.4 3.2-4.6h-2.3z"/>',
  };

'''

SOSTITUZIONI = [
    # Il blocco delle forme.
    (
        re.compile(r"  /\* --- Le forme del cielo.*?(?=  /\* --- I cieli ---)", re.S),
        NUOVE_FORME,
    ),
    # Il simbolo, prima della funzione che lo usa.
    (
        re.compile(r"  const GIORNI = \['domenica'"),
        GLIFI + "  const GIORNI = ['domenica'",
    ),
    # Uso del simbolo accanto alla temperatura.
    (
        "  function gradi(valore: number): string {",
        """  /** Il simbolo in linea, dimensionato come il testo che accompagna. */
  function simbolo(cielo: string): string {
    const forme = GLIFI[cielo] ?? GLIFI.nuvoloso;
    return (
      '<svg class="meteo__simbolo" viewBox="0 0 24 24" width="26" height="26" ' +
      'fill="none" stroke="currentColor" stroke-width="1.5" ' +
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      forme +
      '</svg>'
    );
  }

  function gradi(valore: number): string {""",
    ),
    # Il simbolo entra nel disegno, accanto alla condizione.
    (
        """      <div class="meteo__adesso">
        <span class="meteo__gradi">${gradi(d.current.temperature_2m)}</span>
        <span class="meteo__condizione">${condizione(d.current.weather_code).testo}</span>
      </div>""",
        """      <div class="meteo__adesso">
        <span class="meteo__gradi">${gradi(d.current.temperature_2m)}</span>
        ${simbolo(condizione(d.current.weather_code).cielo)}
        <span class="meteo__condizione">${condizione(d.current.weather_code).testo}</span>
      </div>""",
    ),
]

STILE_SIMBOLO = """  .meteo__simbolo {
    flex: none;
    align-self: center;
    width: 1.75rem;
    height: 1.75rem;
    color: var(--testo-meteo);
    opacity: 0.85;
  }

"""


def main() -> int:
    testo = COMPONENTE.read_text(encoding="utf-8")

    for vecchio, nuovo in SOSTITUZIONI:
        if isinstance(vecchio, re.Pattern):
            if not vecchio.search(testo):
                print(f"  NON TROVATO: {vecchio.pattern[:50]}")
                continue
            testo = vecchio.sub(nuovo, testo, count=1)
        else:
            if vecchio not in testo:
                print(f"  NON TROVATO: {vecchio[:56]}")
                continue
            testo = testo.replace(vecchio, nuovo, 1)
    print("  forme e simboli applicati")

    if ".meteo__simbolo {" not in testo:
        ancora = "  .meteo__condizione {"
        i = testo.find(ancora)
        if i == -1:
            print("  ancora dello stile non trovata")
            return 1
        testo = testo[:i] + STILE_SIMBOLO + testo[i:]
        print("  stile del simbolo aggiunto")

    COMPONENTE.write_text(testo, encoding="utf-8", newline="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
