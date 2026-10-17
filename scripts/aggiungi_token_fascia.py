import pathlib
p = pathlib.Path("src/styles/global.css")
t = p.read_text(encoding="utf-8")

if "--color-fascia-scura:" in t:
    print("token gia' definiti")
else:
    ancora = "--color-accento:"
    i = t.find(ancora)
    if i == -1:
        print("ancora non trovata")
        raise SystemExit(1)
    token = (
        "/* Fondo della fascia degli gnocchi: un grigio scuro, fra il nero e il\n"
        "     grigio. Non stone-800 (quasi nero) ne' stone-700 (piu' chiaro):\n"
        "     e' il tono che regge il giallo del pulsante a 6,4:1. */\n"
        "  --color-fascia-scura: #2b2a26;\n"
        "  /* Giallo piu' chiaro: passaggio del mouse e contorno del focus. */\n"
        "  --color-accento-chiaro: #e0c48f;\n"
    )
    t = t[:i] + token + "  " + t[i:]
    p.write_text(t, encoding="utf-8", newline="")
    print("token inseriti")
