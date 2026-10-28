import pathlib
p = pathlib.Path("scripts/verifica_traduzioni.py")
t = p.read_text(encoding="utf-8")

vecchio = '''        italiani = sorted(
            p for p in cartella.glob("*.md") if not p.stem.endswith("-en") and p.name not in SENZA_TESTO
        )
        inglesi = {p.stem for p in cartella.glob("*-en.md")}

        for italiano in italiani:
            coppie += 1
            atteso = f"{italiano.stem}-en"
            if atteso not in inglesi:
                mancanti.append(f"{collezione}/{italiano.name}")
                continue

            # Il file esiste: si guarda se dentro è rimasto italiano.
            testo_inglese = (cartella / f"{atteso}.md").read_text(encoding="utf-8").lower()'''

nuovo = '''        # Le versioni inglesi stanno nella sottocartella `en/`, con lo stesso
        # nome dell'originale: `camere/doppia.md` <-> `camere/en/doppia.md`.
        italiani = sorted(p for p in cartella.glob("*.md") if p.name not in SENZA_TESTO)
        inglesi = {p.name for p in (cartella / "en").glob("*.md")}

        for italiano in italiani:
            coppie += 1
            if italiano.name not in inglesi:
                mancanti.append(f"{collezione}/{italiano.name}")
                continue

            # Il file esiste: si guarda se dentro è rimasto italiano.
            testo_inglese = (cartella / "en" / italiano.name).read_text(encoding="utf-8").lower()'''

if vecchio not in t:
    print("  ancoraggio non trovato"); raise SystemExit(1)
t = t.replace(vecchio, nuovo, 1)
t = t.replace('sospetti.append((f"{collezione}/{atteso}.md", trovate))',
              'sospetti.append((f"{collezione}/en/{italiano.name}", trovate))')
p.write_text(t, encoding="utf-8", newline="")
print("  controllo aggiornato alla nuova struttura")
