import pathlib
p = pathlib.Path("src/components/MeteoSentiero.astro")
t = p.read_text(encoding="utf-8")
if ".meteo__corpo {" not in t:
    ancora = "  .meteo__attesa {"
    i = t.find(ancora)
    if i == -1:
        print("  ancora non trovata"); raise SystemExit(1)
    regola = (
        "  /* Il corpo non aveva una regola propria: senza `position` il testo\n"
        "     resterebbe sotto le forme del cielo. */\n"
        "  .meteo__corpo {\n"
        "    position: relative;\n"
        "  }\n\n"
    )
    t = t[:i] + regola + t[i:]
    p.write_text(t, encoding="utf-8", newline="")
    print("  regola .meteo__corpo aggiunta")
else:
    print("  regola gia' presente")
