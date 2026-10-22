import pathlib

p = pathlib.Path("scripts/verifica_contrasti.py")
t = p.read_text(encoding="utf-8")

if "rosso-locanda" in t:
    print("  coppie del rosso gia' presenti")
else:
    ancora = '    ("wood-500", "wood-100", SOGLIA_NORMALE, "quantita\' sulla tessera chiara"),'
    if ancora not in t:
        # Si prova un ancora piu' generico.
        ancora = "    # Il contorno del focus deve vedersi"
        nuovo = (
            '    # --- Rosso della locanda --------------------------------------------\n'
            '    ("rosso-locanda-scuro", "stone-100", SOGLIA_NORMALE, "testo rosso sul fondo pagina"),\n'
            '    ("rosso-locanda-chiaro", "stone-900", SOGLIA_NORMALE, "rosso chiaro sull\'apertura scura"),\n'
            '    ("rosso-locanda", "stone-100", SOGLIA_UI, "filetto rosso sul fondo pagina"),\n\n'
        )
    else:
        nuovo = ancora + "\n" + (
            '    # --- Rosso della locanda --------------------------------------------\n'
            '    ("rosso-locanda-scuro", "stone-100", SOGLIA_NORMALE, "testo rosso sul fondo pagina"),\n'
            '    ("rosso-locanda-chiaro", "stone-900", SOGLIA_NORMALE, "rosso chiaro sull\'apertura scura"),\n'
            '    ("rosso-locanda", "stone-100", SOGLIA_UI, "filetto rosso sul fondo pagina"),\n'
        )
    if ancora not in t:
        print("  ancora non trovata")
        raise SystemExit(1)
    t = t.replace(ancora, nuovo, 1)
    p.write_text(t, encoding="utf-8", newline="")
    print("  coppie del rosso aggiunte")
