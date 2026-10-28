import pathlib
p = pathlib.Path("scripts/verifica_pannello.mjs")
t = p.read_text(encoding="utf-8")
vecchio = "const senzaEnglish = inglesi.filter((c) => !c.label.includes('English'));"
nuovo = ("const senzaEnglish = inglesi.filter(\n"
         "  (c) => !c.label.includes('English') && !c.label.startsWith('EN · '),\n"
         ");")
if vecchio not in t:
    print("  ancoraggio non trovato"); raise SystemExit(1)
p.write_text(t.replace(vecchio, nuovo, 1), encoding="utf-8", newline="")
print("  controllo aggiornato")
