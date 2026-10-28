import pathlib

p = pathlib.Path("src/i18n/pagine.ts")
t = p.read_text(encoding="utf-8")

coppie = [
    (
        "  home: {\n    altFacciata: string;",
        "  home: {\n    /** Titolo per i lettori di schermo del carosello. */\n"
        "    titoloCarosello: string;\n    /** Il verbo del collegamento sotto ogni diapositiva. */\n"
        "    invitoCarosello: string;\n    precedente: string;\n    successiva: string;\n"
        "    altFacciata: string;",
    ),
    (
        "  home: {\n    altFacciata:\n      'La Locanda Seggiovia in piazza a Recoaro Terme,",
        "  home: {\n    titoloCarosello: 'Cosa trovi qui',\n    invitoCarosello: 'Scopri di più',\n"
        "    precedente: 'Diapositiva precedente',\n    successiva: 'Diapositiva successiva',\n"
        "    altFacciata:\n      'La Locanda Seggiovia in piazza a Recoaro Terme,",
    ),
    (
        "  home: {\n    altFacciata:\n      'Locanda Seggiovia on the square in Recoaro Terme,",
        "  home: {\n    titoloCarosello: 'What you will find here',\n    invitoCarosello: 'Find out more',\n"
        "    precedente: 'Previous slide',\n    successiva: 'Next slide',\n"
        "    altFacciata:\n      'Locanda Seggiovia on the square in Recoaro Terme,",
    ),
]

for vecchio, nuovo in coppie:
    if vecchio in t:
        t = t.replace(vecchio, nuovo, 1)
    else:
        print(f"  non trovato: {vecchio[:50]}")

p.write_text(t, encoding="utf-8", newline="")
print("  dizionario: stringhe del carosello aggiunte")
