import pathlib
p = pathlib.Path("src/components/Footer.astro")
t = p.read_text(encoding="utf-8")
if "orariNellaLingua" not in t:
    vecchio = "const t = traduzioni(lingua);"
    nuovo = (
        "const t = traduzioni(lingua);\n"
        "/** Gli orari nella lingua della pagina. */\n"
        "const orariNellaLingua = lingua === 'en' ? site.orariEn : site.orari;"
    )
    if vecchio not in t:
        print("  ancoraggio non trovato"); raise SystemExit(1)
    t = t.replace(vecchio, nuovo, 1)
t = t.replace("site.orari.map(", "orariNellaLingua.map(")
p.write_text(t, encoding="utf-8", newline="")
print("  footer: orari nella lingua giusta")
