import pathlib
p = pathlib.Path("scripts/verifica_config.mjs")
t = p.read_text(encoding="utf-8")
vecchio = "const collezioni = Array.isArray(config.collections) ? config.collections : [];"
nuovo = ("/*\n"
         "  Nell'elenco può esserci un separatore (`divider: true`): non è una\n"
         "  collezione, non ha nome né percorso, e va tolto prima dei controlli.\n"
         "*/\n"
         "const collezioni = (Array.isArray(config.collections) ? config.collections : []).filter(\n"
         "  (c) => c && c.divider !== true,\n"
         ");")
if vecchio not in t:
    print("  ancoraggio non trovato"); raise SystemExit(1)
p.write_text(t.replace(vecchio, nuovo, 1), encoding="utf-8", newline="")
print("  verifica_config: separatori ignorati")
