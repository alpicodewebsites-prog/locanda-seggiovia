import pathlib
p = pathlib.Path("scripts/pannello_bilingue.py")
t = p.read_text(encoding="utf-8")

vecchio = '''    righe = blocco.splitlines(keepends=True)
    fuori: list[str] = []
    nome = None

    for riga in righe:'''

nuovo = '''    righe = blocco.splitlines(keepends=True)
    fuori: list[str] = []
    nome = None
    salta = False

    for riga in righe:
        # Le schede delle FOTOGRAFIE non si traducono: la stessa immagine vale
        # per le due lingue, quindi la collezione inglese non ne ha una copia.
        # Si salta l'intera voce (nome, etichetta, file e campi).
        if re.match(r"^      - name: foto\\b", riga):
            salta = True
            continue
        if salta:
            if re.match(r"^      - name: ", riga) or re.match(r"^  - name: ", riga):
                salta = False
            else:
                continue
'''

if vecchio not in t:
    print("  ancoraggio non trovato"); raise SystemExit(1)
t = t.replace(vecchio, nuovo, 1)
p.write_text(t, encoding="utf-8", newline="")
print("  generatore corretto: le foto non vengono duplicate")
