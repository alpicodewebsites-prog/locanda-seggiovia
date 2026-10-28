import pathlib
p = pathlib.Path("src/components/Carosello.astro")
t = p.read_text(encoding="utf-8")

sostituzioni = [
    (
        "  .carosello {\n    max-width: 42rem;",
        "  .carosello {\n    max-width: 48rem;",
    ),
    (
        "                widths={[420, 672, 900]}\n                sizes=\"(min-width: 42rem) 42rem, 92vw\"",
        "                widths={[420, 768, 1024]}\n                sizes=\"(min-width: 48rem) 48rem, 92vw\"",
    ),
    (
        "    border-radius: var(--raggio);\n    background-color: var(--color-stone-200);",
        "    border-radius: var(--raggio);\n    background-color: var(--color-stone-200);\n"
        "    /*\n      Un'ombra morbida stacca la fotografia dal fondo grigio della pagina,\n"
        "      che altrimenti la inghiotte: senza, il riquadro sembra incollato.\n"
        "    */\n    box-shadow: 0 18px 40px -22px rgba(28, 27, 25, 0.45);",
    ),
]

for vecchio, nuovo in sostituzioni:
    if vecchio in t:
        t = t.replace(vecchio, nuovo, 1)
    else:
        print(f"  non trovato: {vecchio.splitlines()[0][:60]}")

p.write_text(t, encoding="utf-8", newline="")
print("  carosello: piu' largo, con ombra")
