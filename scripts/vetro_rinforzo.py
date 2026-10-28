import pathlib
p = pathlib.Path("src/components/Carosello.astro")
t = p.read_text(encoding="utf-8")

sostituzioni = [
    # Aloni piu' presenti: il vetro deve avere qualcosa da sfuocare.
    ("    filter: blur(70px);\n    opacity: 0.5;", "    filter: blur(80px);\n    opacity: 0.72;"),
    (
        "    width: 46rem;\n    height: 26rem;\n    top: 4%;\n    left: 8%;",
        "    width: 56rem;\n    height: 32rem;\n    top: -6%;\n    left: -2%;",
    ),
    (
        "    width: 40rem;\n    height: 24rem;\n    right: 6%;\n    bottom: 2%;",
        "    width: 48rem;\n    height: 30rem;\n    right: -4%;\n    bottom: -8%;",
    ),
    # Cornice piu' generosa e vetro un filo piu' bianco.
    (
        "    padding: 0.9rem;\n    border: 1px solid rgba(255, 255, 255, 0.55);",
        "    padding: 1.15rem;\n    border: 1px solid rgba(255, 255, 255, 0.6);",
    ),
    (
        "    background-color: rgba(255, 255, 255, 0.16);",
        "    background-color: rgba(255, 255, 255, 0.2);",
    ),
]

for vecchio, nuovo in sostituzioni:
    if vecchio in t:
        t = t.replace(vecchio, nuovo, 1)
    else:
        print(f"  non trovato: {vecchio.splitlines()[0][:50]}")

p.write_text(t, encoding="utf-8", newline="")
print("  vetro rinforzato")
