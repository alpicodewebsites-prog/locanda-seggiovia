import pathlib
p = pathlib.Path("scripts/pannello_bilingue.py")
t = p.read_text(encoding="utf-8")

vecchio = '''        if riga.startswith("    description: "):
            fuori.append("    description: La stessa pagina in inglese.\\n")
            continue'''

nuovo = '''        # La descrizione può essere su più righe (`>-`): va sostituita tutta,
        # altrimenti le continuazioni restano orfane e il file non è più YAML.
        if riga.startswith("    description: "):
            fuori.append("    description: La stessa pagina in inglese.\\n")
            salta_descrizione = riga.rstrip().endswith((">-", "|", ">"))
            continue

        if salta_descrizione:
            if riga.startswith("      ") or not riga.strip():
                continue
            salta_descrizione = False'''

if vecchio not in t:
    print("  ancoraggio non trovato"); raise SystemExit(1)
t = t.replace(vecchio, nuovo, 1)
t = t.replace("    salta = False\n", "    salta = False\n    salta_descrizione = False\n", 1)
p.write_text(t, encoding="utf-8", newline="")
print("  generatore corretto: descrizioni su più righe")
