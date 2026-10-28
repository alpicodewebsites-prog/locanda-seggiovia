import pathlib
p = pathlib.Path("src/components/Header.astro")
t = p.read_text(encoding="utf-8")

sostituzioni = [
    (
        "import { etichetteNavigazione } from '../i18n/ui';",
        "import { etichetteNavigazione, traduzioni } from '../i18n/ui';\n"
        "import SelettoreLingua from './SelettoreLingua.astro';",
    ),
    (
        "const etichette = etichetteNavigazione(lingua);",
        "const etichette = etichetteNavigazione(lingua);\nconst u = traduzioni(lingua);",
    ),
    ("{etichette['/contatti'] ?? 'Contatti'}", "{u.nav.contatti}"),
]

for vecchio, nuovo in sostituzioni:
    if vecchio in t:
        t = t.replace(vecchio, nuovo, 1)
    else:
        print(f"  non trovato: {vecchio[:60]}")

p.write_text(t, encoding="utf-8", newline="")
print("  header: import e selettore sistemati")
