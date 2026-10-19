import pathlib
p = pathlib.Path("src/styles/global.css")
t = p.read_text(encoding="utf-8")

INIZIO = "  /*\n    Pulsante degli gnocchi \u2014 a pillola"
FINE = "  .pulsante-gnocchi:focus-visible {\n    outline: 2px solid var(--color-accento-chiaro);\n    outline-offset: 4px;\n  }\n"

i = t.find(INIZIO)
if i == -1:
    print("  inizio non trovato")
    raise SystemExit(1)
j = t.find(FINE, i)
if j == -1:
    print("  fine non trovata")
    raise SystemExit(1)
j += len(FINE)

rimosse = t[i:j].count("\n")
t = t[:i] + t[j:]

p.write_text(t, encoding="utf-8", newline="")
print(f"  rimosse {rimosse} righe del pulsante")

for ago in ["pulsante-gnocchi", "accento-chiaro", "fascia-scura", ".tavolo"]:
    print(f"  residui «{ago}»: {t.count(ago)}")
