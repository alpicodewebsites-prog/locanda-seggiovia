import pathlib
p = pathlib.Path("scripts/verifica_pannello.mjs")
t = p.read_text(encoding="utf-8")

vecchio = """const collezioni = dati.collections ?? [];
controlla('ci sono collezioni', collezioni.length > 0, `${collezioni.length}`);"""

nuovo = """/*
  Nell'elenco può esserci anche un separatore (`divider: true`), che non è una
  collezione e non ha nome. Va tolto prima di controllare il resto, altrimenti
  il primo `name.endsWith` esplode.
*/
const voci = dati.collections ?? [];
const separatori = voci.filter((v) => v.divider === true);
const collezioni = voci.filter((v) => v.name);
controlla('ci sono collezioni', collezioni.length > 0, `${collezioni.length}`);
controlla(
  'c\\'è un separatore fra italiano e inglese',
  separatori.length === 1,
  `${separatori.length} separatori`,
);"""

if vecchio not in t:
    print("  ancoraggio non trovato"); raise SystemExit(1)
t = t.replace(vecchio, nuovo, 1)
p.write_text(t, encoding="utf-8", newline="")
print("  verifica_pannello aggiornato")
