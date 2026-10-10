"""
Controlli di qualità sull'output di build (dist/).
Verifica i fatti, non le impressioni: title, meta, canonical, Open Graph,
JSON-LD, integrità dei link interni, sitemap e robots.

Dalla settimana 2 il sito ha più pagine: i controlli di SEO si applicano a
TUTTE le pagine, non solo alla home.

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
    """Raccoglie href/src interni, immagini e titoli."""

    def __init__(self) -> None:
        super().__init__()
        self.href: list[str] = []
        self.src: list[str] = []
        self.img_senza_alt: list[str] = []
        self.h1: list[str] = []
        self.h2: list[str] = []
        self._livello = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.href.append(a["href"])
        if tag in ("img", "source") and a.get("src"):
            self.src.append(a["src"])
        if tag == "img" and "alt" not in a:
            self.img_senza_alt.append(a.get("src", "(senza src)"))
        if tag == "h1":
            self._livello = 1
        elif tag == "h2":
            self._livello = 2

    def handle_endtag(self, tag):
        if tag in ("h1", "h2"):
            self._livello = 0

    def handle_data(self, data):
        testo = data.strip()
        if not testo:
            return
        if self._livello == 1:
            self.h1.append(testo)
        elif self._livello == 2:
            self.h2.append(testo)


# Pagine che devono esistere e i controlli SEO specifici.
PAGINE = {
    "index.html": {"titolo_min": 10, "richiede_h1": True},
    "camere/index.html": {"titolo_min": 10, "richiede_h1": True},
    "ristorante/index.html": {"titolo_min": 10, "richiede_h1": True},
    "contatti/index.html": {"titolo_min": 10, "richiede_h1": True},
    "grazie/index.html": {"titolo_min": 10, "richiede_h1": True},
    "404.html": {"titolo_min": 10, "richiede_h1": True},
}

# Pagine previste ma non ancora realizzate (settimana 3).
PAGINE_FUTURE = {
    "/la-locanda",
    "/gnocchi-con-la-fioreta",
    "/sentieri",
    "/privacy",
    "/cookie",
}


def seo_pagina(percorso: Path, rel: str) -> LinkParser:
    """Controlli SEO applicati a una singola pagina."""
    html = leggi(percorso)
    p = LinkParser()
    p.feed(html)

    m_title = re.search(r"<title>(.*?)</title>", html, re.S)
    title = m_title.group(1).strip() if m_title else ""
    check(f"{rel}: title presente", bool(title), title[:70] if title else "")
    check(f"{rel}: title entro 65 caratteri", 0 < len(title) <= 65, f"{len(title)} caratteri")
    check(f"{rel}: title contiene il nome della struttura", "Locanda Seggiovia" in title)

    m_desc = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
    desc = m_desc.group(1).strip() if m_desc else ""
    check(
        f"{rel}: description fra 70 e 165 caratteri",
        70 <= len(desc) <= 165,
        f"{len(desc)} caratteri",
    )

    # Le pagine di utilità non vanno indicizzate.
    e_utilità = rel in ("404.html", "grazie/index.html")
    if e_utilità:
        check(f"{rel}: pagina di utilità con noindex", 'name="robots"' in html and "noindex" in html)
    else:
        check(f"{rel}: canonical assoluto", bool(re.search(r'rel="canonical" href="https?://', html)))
        for prop in ("og:title", "og:description", "og:url", "og:image"):
            check(f"{rel}: {prop} presente", f'property="{prop}"' in html)

    check(f"{rel}: esattamente un h1", len(p.h1) == 1, f"{len(p.h1)} trovati")
    check(f"{rel}: nessuna img senza alt", not p.img_senza_alt, ", ".join(p.img_senza_alt[:2]))

    # I dati strutturati devono essere JSON valido quando ci sono.
    blocchi = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    for i, b in enumerate(blocchi):
        try:
            json.loads(b)
        except json.JSONDecodeError as e:
            check(f"{rel}: JSON-LD blocco {i + 1} valido", False, str(e))

    return p


def main() -> int:
    if not DIST.exists():
        print("ERRORE: dist/ non esiste. Esegui prima `npm run build`.")
        return 1

    # --- Le pagine esistono e rispettano i controlli SEO --------------------
    href_raccolti: set[str] = set()
    for rel, regole in PAGINE.items():
        percorso = DIST / rel
        check(f"{rel} generato", percorso.exists())
        if not percorso.exists():
            continue
        p = seo_pagina(percorso, rel)
        href_raccolti.update(h for h in p.href if h.startswith("/"))

    index = DIST / "index.html"
    if not index.exists():
        return 1
    html_home = leggi(index)

    # --- Dati strutturati della home ----------------------------------------
    blocchi_home = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html_home, re.S)
    tipi = []
    for b in blocchi_home:
        try:
            tipi.append(json.loads(b).get("@type"))
        except json.JSONDecodeError:
            pass
    tipi_appiattiti = {t for x in tipi for t in (x if isinstance(x, list) else [x])}
    check("home: schema Restaurant presente", "Restaurant" in tipi_appiattiti)
    check("home: schema LodgingBusiness presente", "LodgingBusiness" in tipi_appiattiti)
    check("home: exactly one lang dichiarato", 'lang="it"' in html_home)
    check("home: link di salto al contenuto", "Vai al contenuto" in html_home)

    # --- Dati strutturati specifici delle pagine nuove ----------------------
    camere_html = leggi(DIST / "camere/index.html") if (DIST / "camere/index.html").exists() else ""
    check("camere: schema OfferCatalog presente", "OfferCatalog" in camere_html)
    check("camere: tariffe in tabella", "<table" in camere_html and "tariffe" in camere_html)

    rist_html = leggi(DIST / "ristorante/index.html") if (DIST / "ristorante/index.html").exists() else ""
    check("ristorante: schema Menu presente", '"@type": "Menu"' in rist_html or '"@type":"Menu"' in rist_html)
    check("ristorante: categorie del menù presenti", "Antipasti" in rist_html and "Dolci" in rist_html)

    contatti_html = leggi(DIST / "contatti/index.html") if (DIST / "contatti/index.html").exists() else ""
    check("contatti: form Web3Forms presente", 'action="https://api.web3forms.com/submit"' in contatti_html)
    check("contatti: campo access_key presente", 'name="access_key"' in contatti_html)
    check("contatti: campo esca antispam presente", 'name="botcheck"' in contatti_html)
    check("contatti: redirect a /grazie configurato", 'name="redirect"' in contatti_html and "/grazie" in contatti_html)
    check("contatti: campo consenso privacy", 'name="privacy"' in contatti_html)

    # --- Il CMS non deve essere indicizzabile ma deve essere pubblicato ------
    admin = DIST / "admin" / "index.html"
    admin_cfg = DIST / "admin" / "config.yml"
    check("admin/index.html pubblicato", admin.exists())
    check("admin/config.yml pubblicato", admin_cfg.exists())
    if admin.exists():
        check("admin: noindex dichiarato", "noindex" in leggi(admin))
    if admin_cfg.exists():
        cfg = leggi(admin_cfg)
        check("admin: backend GitHub configurato", "name: github" in cfg)
        check("admin: branch main", "branch: main" in cfg)
        for collezione in ("camere", "menu", "gnocchi", "sentieri"):
            check(f"admin: collezione '{collezione}' configurata", f"name: {collezione}" in cfg)
        check("admin: percorsi in src/content", "folder: src/content/" in cfg)
        # Le cartelle del CMS devono esistere davvero nel progetto.
        radice = Path(__file__).resolve().parent.parent
        for cartella in ("camere", "menu", "gnocchi", "sentieri"):
            check(
                f"admin: cartella src/content/{cartella} esiste",
                (radice / "src" / "content" / cartella).is_dir(),
            )

    # --- Link interni: ogni href deve esistere o essere previsto ------------
    rotti = []
    for href in href_raccolti:
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
        if pulito.rstrip("/") in PAGINE_FUTURE:
            continue
        rotti.append(href)
    check("nessun link interno rotto", not rotti, ", ".join(sorted(rotti)[:6]))

    # --- File statici -------------------------------------------------------
    for f in ("robots.txt", "sitemap-index.xml", "favicon.svg", "og-default.jpg", "apple-touch-icon.png"):
        check(f"{f} presente", (DIST / f).exists())

    robots = leggi(DIST / "robots.txt") if (DIST / "robots.txt").exists() else ""
    check("robots.txt dichiara la sitemap", "Sitemap:" in robots)
    check("robots.txt blocca /admin/", "Disallow: /admin/" in robots)

    # --- La sitemap non deve includere le pagine di utilità ------------------
    fogli = sorted(DIST.glob("sitemap-*.xml"))
    if fogli:
        s = "".join(leggi(f) for f in fogli)
        check("sitemap: non include /admin/", "/admin/" not in s)
        check("sitemap: non include /grazie", "/grazie" not in s)
        check("sitemap: include /camere", "/camere" in s)

    # --- Il segnaposto non deve spacciarsi per foto reale -------------------
    check(
        "nessun alt che dichiari foto inesistenti",
        "facciata in pietra della Locanda" not in html_home,
    )

    # --- Report -------------------------------------------------------------
    print("=" * 74)
    print("VERIFICA BUILD — Locanda Seggiovia")
    print("=" * 74)
    falliti = 0
    for nome, ok, dettaglio in esiti:
        segno = "OK  " if ok else "FAIL"
        if not ok:
            falliti += 1
        riga = f"[{segno}] {nome}"
        if dettaglio:
            riga += f"  — {dettaglio}"
        print(riga)

    print("-" * 74)
    print(f"{len(esiti) - falliti}/{len(esiti)} controlli superati")
    return 1 if falliti else 0


if __name__ == "__main__":
    sys.exit(main())
