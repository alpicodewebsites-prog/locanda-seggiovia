"""
Controlli di qualità sull'output di build (dist/).
Verifica i fatti, non le impressioni: title, meta, canonical, Open Graph,
JSON-LD, integrità dei link interni, sitemap e robots.

Uso:  python scripts/verify_build.py
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "dist"

esiti: list[tuple[str, bool, str]] = []


def check(nome: str, ok: bool, dettaglio: str = "") -> None:
    esiti.append((nome, bool(ok), dettaglio))


def leggi(percorso: Path) -> str:
    return percorso.read_text(encoding="utf-8")


class LinkParser(HTMLParser):
    """Raccoglie href/src interni e i link cliccabili."""

    def __init__(self) -> None:
        super().__init__()
        self.href: list[str] = []
        self.src: list[str] = []
        self.img_senza_alt: list[str] = []
        self.h1: list[str] = []
        self._in_h1 = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.href.append(a["href"])
        if tag in ("img", "source") and a.get("src"):
            self.src.append(a["src"])
        if tag == "img" and "alt" not in a:
            self.img_senza_alt.append(a.get("src", "(senza src)"))
        if tag == "h1":
            self._in_h1 = True

    def handle_endtag(self, tag):
        if tag == "h1":
            self._in_h1 = False

    def handle_data(self, data):
        if self._in_h1 and data.strip():
            self.h1.append(data.strip())


def main() -> int:
    if not DIST.exists():
        print("ERRORE: dist/ non esiste. Esegui prima `npm run build`.")
        return 1

    index = DIST / "index.html"
    check("index.html generato", index.exists())
    if not index.exists():
        return 1

    html = leggi(index)
    p = LinkParser()
    p.feed(html)

    # --- Titolo e descrizione -------------------------------------------------
    m_title = re.search(r"<title>(.*?)</title>", html, re.S)
    title = m_title.group(1).strip() if m_title else ""
    check("title presente", bool(title), title[:90])
    check("title entro 65 caratteri", len(title) <= 65, f"{len(title)} caratteri")
    check(
        "title contiene il nome della struttura",
        "Locanda Seggiovia" in title,
    )

    m_desc = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
    desc = m_desc.group(1).strip() if m_desc else ""
    check("meta description presente", bool(desc), f"{len(desc)} caratteri")
    check("description fra 70 e 165 caratteri", 70 <= len(desc) <= 165, f"{len(desc)}")

    # --- Canonical / OG ------------------------------------------------------
    check("canonical presente", 'rel="canonical"' in html)
    m_can = re.search(r'<link rel="canonical" href="(.*?)"', html)
    check(
        "canonical è un URL assoluto",
        bool(m_can) and m_can.group(1).startswith("http"),
        m_can.group(1) if m_can else "",
    )
    for prop in ("og:title", "og:description", "og:url", "og:image", "og:type", "og:locale"):
        check(f"{prop} presente", f'property="{prop}"' in html)
    check("twitter:card presente", 'name="twitter:card"' in html)

    # --- Struttura -----------------------------------------------------------
    check("esattamente un h1", len(p.h1) == 1, f"{len(p.h1)} trovati")
    check("lingua dichiarata it", 'lang="it"' in html)
    check("viewport presente", 'name="viewport"' in html)
    check(
        "link di salto al contenuto",
        "Vai al contenuto" in html,
    )

    # --- Immagini ------------------------------------------------------------
    check("nessuna img senza alt", not p.img_senza_alt, ", ".join(p.img_senza_alt[:3]))
    check("immagini con srcset responsive", "srcset=" in html)

    # --- Dati strutturati ----------------------------------------------------
    blocchi = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S
    )
    check("JSON-LD presente", len(blocchi) >= 2, f"{len(blocchi)} blocchi")
    tipi = []
    for b in blocchi:
        try:
            dati = json.loads(b)
            tipi.append(dati.get("@type"))
        except json.JSONDecodeError as e:
            check("JSON-LD valido", False, str(e))
    check("JSON-LD valido", all(t is not None for t in tipi), str(tipi))
    tipi_appiattiti = {t for x in tipi for t in (x if isinstance(x, list) else [x])}
    check("schema Restaurant presente", "Restaurant" in tipi_appiattiti)
    check("schema LodgingBusiness presente", "LodgingBusiness" in tipi_appiattiti)

    # --- Link interni: ogni href deve esistere o essere una pagina prevista ---
    pagine_future = {
        "/la-locanda",
        "/camere",
        "/ristorante",
        "/gnocchi-con-la-fioretta",
        "/gnocchi-con-la-fioreta",
        "/sentieri",
        "/contatti",
        "/privacy",
        "/cookie",
    }
    rotti = []
    for href in {h for h in p.href if h.startswith("/") and not h.startswith("//")}:
        pulito = href.split("#")[0].split("?")[0]
        if not pulito or pulito == "/":
            continue
        candidati = [
            DIST / pulito.lstrip("/"),
            DIST / pulito.lstrip("/") / "index.html",
            DIST / (pulito.lstrip("/") + ".html"),
        ]
        if any(c.exists() for c in candidati):
            continue
        if pulito.rstrip("/") in pagine_future:
            continue  # prevista in una fase successiva (settimana 2–3)
        rotti.append(href)
    check("nessun link interno rotto", not rotti, ", ".join(sorted(rotti)[:6]))

    # --- File statici --------------------------------------------------------
    for f in ("robots.txt", "sitemap-index.xml", "favicon.svg", "og-default.jpg", "apple-touch-icon.png"):
        check(f"{f} presente", (DIST / f).exists())

    robots = leggi(DIST / "robots.txt") if (DIST / "robots.txt").exists() else ""
    check("robots.txt dichiara la sitemap", "Sitemap:" in robots)
    check("robots.txt blocca /admin/", "Disallow: /admin/" in robots)

    sitemap_idx = DIST / "sitemap-index.xml"
    if sitemap_idx.exists():
        s = leggi(sitemap_idx)
        check("sitemap contiene locandaseggiovia", "locandaseggiovia" in s)

    # --- Il segnaposto non deve spacciarsi per foto reale --------------------
    check(
        "nessun alt che dichiari foto inesistenti",
        "facciata in pietra della Locanda" not in html,
    )

    # --- Report --------------------------------------------------------------
    print("=" * 72)
    print("VERIFICA BUILD — Locanda Seggiovia")
    print("=" * 72)
    falliti = 0
    for nome, ok, dettaglio in esiti:
        segno = "OK  " if ok else "FAIL"
        if not ok:
            falliti += 1
        riga = f"[{segno}] {nome}"
        if dettaglio:
            riga += f"  — {dettaglio}"
        print(riga)

    print("-" * 72)
    print(f"{len(esiti) - falliti}/{len(esiti)} controlli superati")
    return 1 if falliti else 0


if __name__ == "__main__":
    sys.exit(main())
