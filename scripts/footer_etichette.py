"""Traduce le intestazioni e le righe di orario del pie' di pagina."""

from __future__ import annotations
import pathlib

F = pathlib.Path(__file__).resolve().parent.parent / "src" / "components" / "Footer.astro"

SOSTITUZIONI = [
    (">Dove siamo<", ">{t.footer.doveSiamo}<"),
    (">Il sito<", ">{t.footer.ilSito}<"),
    (">Orari<", ">{t.footer.orari}<"),
    (">Ristorante<", ">{t.footer.ristorante}<"),
    (">Reception<", ">{t.footer.reception}<"),
    (">A pranzo e a cena — orari da confermare<", ">{t.footer.orariDaConfermare}<"),
    (">Tutti i giorni (da confermare)<", ">{t.footer.tuttiIGiorni}<"),
]

def main() -> int:
    t = F.read_text(encoding="utf-8")
    for vecchio, nuovo in SOSTITUZIONI:
        if vecchio in t:
            t = t.replace(vecchio, nuovo)
        else:
            print(f"  non trovato: {vecchio}")
    F.write_text(t, encoding="utf-8", newline="")
    print("  footer: intestazioni e orari tradotti")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
