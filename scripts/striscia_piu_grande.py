import pathlib
p = pathlib.Path("src/components/Carosello.astro")
t = p.read_text(encoding="utf-8")

sostituzioni = [
    # Le fotografie passano da ~420 a ~600 px di larghezza a schermo pieno.
    (
        "    width: clamp(16rem, 29vw, 30rem);",
        "    width: clamp(18rem, 40vw, 42rem);",
    ),
    # Il passo fra una fotografia e l'altra cresce con loro.
    ("    margin-right: 1.5rem;", "    margin-right: 2rem;"),
    # Le misure richieste al costruttore di immagini seguono la nuova larghezza:
    # chiedere 640 px per mostrarne 600 va bene, chiedere 420 no.
    ('widths={[420, 640, 900]}\n                  sizes="(min-width: 64rem) 26rem, 80vw"',
     'widths={[480, 720, 1080]}\n                  sizes="(min-width: 64rem) 42rem, 90vw"'),
    ('widths={[420, 640, 900]}\n                  sizes="(min-width: 64rem) 26rem, 80vw"',
     'widths={[480, 720, 1080]}\n                  sizes="(min-width: 64rem) 42rem, 90vw"'),
    ("    font-size: 0.78rem;", "    font-size: 0.82rem;"),
]

for vecchio, nuovo in sostituzioni:
    if vecchio in t:
        t = t.replace(vecchio, nuovo, 1)
    else:
        print(f"  non trovato: {vecchio.splitlines()[0][:56]}")

p.write_text(t, encoding="utf-8", newline="")
print("  striscia: fotografie ingrandite")
