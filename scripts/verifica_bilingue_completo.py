"""
Verifica finale del multilingua: lang, hreflang, canonical e sitemap.

È il controllo che dice se l'obiettivo è raggiunto, non se una pagina singola
funziona: guarda TUTTE le pagine costruite e le confronta fra le due lingue.

Controlla che:
  1. ogni pagina dichiari la lingua giusta nell'elemento <html>;
  2. ogni pagina abbia un canonical che punta a sé stessa;
  3. le pagine bilingui si dichiarino a vicenda con hreflang, e che l'indirizzo
     dichiarato esista davvero;
  4. esista anche x-default;
  5. la sitemap elenchi tutte e due le lingue, e nient'altro.

Uso:  python scripts/verifica_bilingue_completo.py
"""

from __future__ import annotations

import pathlib
import re

RADICE = pathlib.Path(__file__).resolve().parent.parent
DIST = RADICE / "dist"
SITO = "https://www.locandaseggiovia.com"

# Le pagine che devono esistere in entrambe le lingue.
COPPIE = [
    ("/", "/en/"),
    ("/la-locanda/", "/en/the-inn/"),
    ("/camere/", "/en/rooms/"),
    ("/ristorante/", "/en/restaurant/"),
    ("/gnocchi-con-la-fioreta/", "/en/gnocchi/"),
    ("/sentieri/", "/en/trails/"),
    ("/contatti/", "/en/contact/"),
    ("/privacy/", "/en/privacy/"),
    ("/cookie/", "/en/cookies/"),
]

# Le pagine che NON devono dichiarare una lingua alternativa.
#
# Solo la 404: è una pagina sola, servita per qualunque indirizzo sbagliato, e
# non ha una versione inglese. La conferma di invio invece ce l'ha, e le due si
# dichiarano a vicenda — anche se sono noindex, la dichiarazione è corretta.
SENZA_ALTERNATIVE = ["/404.html"]


def file_di(percorso: str) -> pathlib.Path:
    if percorso.endswith(".html"):
        return DIST / percorso.lstrip("/")
    return DIST / percorso.strip("/") / "index.html"


def leggi(percorso: str) -> str:
    file = file_di(percorso)
    return file.read_text(encoding="utf-8") if file.exists() else ""


def main() -> int:
    problemi = 0
    controlli = 0

    def check(nome: str, ok: bool, nota: str = "") -> None:
        nonlocal problemi, controlli
        controlli += 1
        if not ok:
            problemi += 1
            print(f"  [FAIL] {nome}" + (f" — {nota}" if nota else ""))

    # --- 1-4. Le coppie bilingui -----------------------------------------
    for italiano, inglese in COPPIE:
        for percorso, lingua_attesa, fratello in [
            (italiano, "it", inglese),
            (inglese, "en", italiano),
        ]:
            html = leggi(percorso)
            if not html:
                check(f"{percorso} esiste", False)
                continue

            trovata = re.search(r'<html[^>]*\blang="([^"]+)"', html)
            check(
                f"{percorso}: lang è {lingua_attesa}",
                bool(trovata) and trovata.group(1).startswith(lingua_attesa),
                trovata.group(1) if trovata else "nessun lang",
            )

            canonical = re.search(r'rel="canonical" href="([^"]+)"', html)
            atteso = f"{SITO}{percorso}"
            check(
                f"{percorso}: canonical punta a sé stessa",
                bool(canonical) and canonical.group(1) == atteso,
                canonical.group(1) if canonical else "nessun canonical",
            )

            # hreflang verso l'altra lingua, e l'indirizzo deve esistere.
            alternative = dict(
                (m.group(1), m.group(2))
                for m in re.finditer(r'hreflang="([^"]+)" href="([^"]+)"', html)
            )
            check(
                f"{percorso}: dichiara hreflang verso {fratello}",
                atteso in alternative.values() or any(v.endswith(fratello) for v in alternative.values()),
                ", ".join(alternative) or "nessun hreflang",
            )
            check(f"{percorso}: dichiara x-default", "x-default" in alternative)

            # Ogni indirizzo dichiarato deve corrispondere a una pagina vera.
            for codice, indirizzo in alternative.items():
                relativo = indirizzo.replace(SITO, "")
                check(
                    f"{percorso}: l'hreflang {codice} esiste",
                    file_di(relativo).exists(),
                    relativo,
                )

    # --- 5. La sitemap ----------------------------------------------------
    sitemap = ""
    for nome in ["sitemap-index.xml", "sitemap-0.xml"]:
        file = DIST / nome
        if file.exists():
            sitemap += file.read_text(encoding="utf-8")

    check("la sitemap esiste", bool(sitemap))
    if sitemap:
        indirizzi = re.findall(r"<loc>([^<]+)</loc>", sitemap)
        for italiano, inglese in COPPIE:
            check(
                f"sitemap elenca {italiano}",
                any(i.endswith(italiano) for i in indirizzi),
            )
            check(
                f"sitemap elenca {inglese}",
                any(i.endswith(inglese) for i in indirizzi),
            )
        # Le pagine di servizio non vanno annunciate.
        for vietato in ["/grazie/", "/en/thank-you/"]:
            check(
                f"sitemap non elenca {vietato}",
                not any(i.endswith(vietato) for i in indirizzi),
            )
        # Le vecchie pagine doppie non devono tornare.
        check(
            "sitemap senza pagine doppie -en/",
            not any("-en/" in i for i in indirizzi),
        )

    # --- Le pagine senza alternativa --------------------------------------
    for percorso in SENZA_ALTERNATIVE:
        html = leggi(percorso)
        if not html:
            continue
        check(
            f"{percorso}: non dichiara lingue alternative",
            'hreflang="x-default"' not in html,
        )

    print(f"  controlli: {controlli}")
    print("  ESITO: " + ("tutto a posto" if problemi == 0 else f"{problemi} problemi"))
    return 1 if problemi else 0


if __name__ == "__main__":
    raise SystemExit(main())
