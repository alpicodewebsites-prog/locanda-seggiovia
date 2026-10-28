"""Rende bilingui intestazione e piede di pagina."""

from __future__ import annotations
import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
HEADER = RADICE / "src" / "components" / "Header.astro"
FOOTER = RADICE / "src" / "components" / "Footer.astro"

NORM = 'const pulito = (p: string) => (p.length > 1 ? p.replace(/\\/$/, "") : p);\n'

def main() -> int:
    h = HEADER.read_text(encoding="utf-8")

    # --- import
    h = h.replace(
        "import { site, navigazione } from '../data/site';",
        "import { site, navigazione } from '../data/site';\n"
        "import { percorsoLocalizzato, linguaDaUrl } from '../i18n';\n"
        "import { etichetteNavigazione } from '../i18n/ui';",
        1,
    )

    # --- la lingua, ricavata dall'indirizzo (il guscio inglese resta corretto)
    h = h.replace(
        "const { trasparente = false } = Astro.props;",
        "const { trasparente = false } = Astro.props;\n"
        "/** La lingua si ricava dall'indirizzo: `/en/...` e' inglese. */\n"
        "const lingua = linguaDaUrl(Astro.url);\n"
        "const etichette = etichetteNavigazione(lingua);",
        1,
    )

    # --- la voce attiva va confrontata con l'indirizzo DELLA LINGUA
    h = h.replace(
        """const isAttiva = (href: string) =>
  href === '/' ? path === '/' : path === href || path.startsWith(`${href}/`);""",
        """const isAttiva = (href: string) => {
  const qui = pulito(percorsoLocalizzato(href, lingua));
  const corrente = pulito(path);
  return qui === '/' ? corrente === '/' : corrente === qui || corrente.startsWith(`${qui}/`);
};""",
        1,
    )
    if "const pulito" not in h:
        h = h.replace("const isAttiva", NORM + "\nconst isAttiva", 1)

    # --- collegamenti
    h = h.replace('href="/"', "href={percorsoLocalizzato('/', lingua)}")
    h = h.replace("href={voce.href}", "href={percorsoLocalizzato(voce.href, lingua)}")
    h = h.replace(
        'href="/contatti" class="btn btn--primary btn--barra"',
        "href={percorsoLocalizzato('/contatti', lingua)} class=\"btn btn--primary btn--barra\"",
    )

    # --- etichette
    h = h.replace("{voce.label}", "{etichette[voce.href] ?? voce.label}")

    HEADER.write_text(h, encoding="utf-8", newline="")
    print("  header: fatto")

    f = FOOTER.read_text(encoding="utf-8")
    f = f.replace(
        "import { site, indirizzoBreve, navigazione, mappaLinkUrl } from '../data/site';",
        "import { site, indirizzoBreve, navigazione, mappaLinkUrl } from '../data/site';\n"
        "import { percorsoLocalizzato, linguaDaUrl } from '../i18n';\n"
        "import { etichetteNavigazione, traduzioni } from '../i18n/ui';",
        1,
    )
    f = f.replace(
        "const anno = new Date().getFullYear();",
        "const anno = new Date().getFullYear();\n"
        "const lingua = linguaDaUrl(Astro.url);\n"
        "const etichette = etichetteNavigazione(lingua);\n"
        "const t = traduzioni(lingua);",
        1,
    )
    f = f.replace("href={voce.href}", "href={percorsoLocalizzato(voce.href, lingua)}")
    f = f.replace("{voce.label}", "{etichette[voce.href] ?? voce.label}")
    f = f.replace('href="/privacy"', "href={percorsoLocalizzato('/privacy', lingua)}")
    f = f.replace('href="/cookie"', "href={percorsoLocalizzato('/cookie', lingua)}")
    f = f.replace('href="/contatti"', "href={percorsoLocalizzato('/contatti', lingua)}")
    f = f.replace(">Privacy Policy<", ">{t.footer.privacy}<")
    f = f.replace(">Cookie Policy<", ">{t.footer.cookie}<")
    f = f.replace(">Contatti</a>", ">{t.nav.contatti}</a>")

    FOOTER.write_text(f, encoding="utf-8", newline="")
    print("  footer: fatto")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
