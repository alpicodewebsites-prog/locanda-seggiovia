import pathlib

# 1. Un predicato esplicito, usato da due punti.
indice = pathlib.Path("src/i18n/index.ts")
t = indice.read_text(encoding="utf-8")
if "export function paginaBilingue" not in t:
    vecchio = "export function alternativeLinguistiche(percorso: string) {"
    nuovo = '''/**
 * Vero se la pagina esiste in entrambe le lingue.
 *
 * La 404 e la conferma di invio no: la prima è una pagina sola servita per
 * qualunque indirizzo sbagliato, la seconda ha una versione inglese ma non è una
 * pagina di contenuto da collegare. Serve a non annunciare e non collegare
 * indirizzi che non esistono.
 */
export function paginaBilingue(percorso: string): boolean {
  const logico = percorsoLogico(percorso);
  return PERCORSI[logico] !== undefined || /^\\/sentieri\\/[^/]+$/.test(logico);
}

export function alternativeLinguistiche(percorso: string) {'''
    t = t.replace(vecchio, nuovo, 1)

# La funzione ora usa il predicato.
t = t.replace("  const paginaNota = PERCORSI[logico] !== undefined || /^\\/sentieri\\/[^/]+$/.test(logico);\n  if (!paginaNota) return [];",
              "  if (!paginaBilingue(percorso)) return [];")
indice.write_text(t, encoding="utf-8", newline="")
print("  i18n: predicato paginaBilingue aggiunto")

# 2. Il selettore manda alla home quando la pagina non esiste nell'altra lingua.
sel = pathlib.Path("src/components/SelettoreLingua.astro")
s2 = sel.read_text(encoding="utf-8")
s2 = s2.replace(
    "import { LINGUE, linguaDaUrl, percorsoLocalizzato } from '../i18n';",
    "import { LINGUE, linguaDaUrl, paginaBilingue, percorsoLocalizzato } from '../i18n';",
)
s2 = s2.replace(
    "const voci = LINGUE.map((l) => ({\n  ...l,\n  href: percorsoLocalizzato(percorso, l.codice),",
    "/*\n  Se la pagina corrente non esiste nell'altra lingua — la 404, per esempio —\n  il selettore porta alla home di quella lingua invece che a un indirizzo\n  inesistente. Un collegamento che funziona è meglio di uno corretto.\n*/\nconst nota = paginaBilingue(percorso);\n\nconst voci = LINGUE.map((l) => ({\n  ...l,\n  href: percorsoLocalizzato(nota ? percorso : '/', l.codice),",
)
sel.write_text(s2, encoding="utf-8", newline="")
print("  selettore: ripiego sulla home")
