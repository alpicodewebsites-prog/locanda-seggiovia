import pathlib
p = pathlib.Path("src/components/Carosello.astro")
t = p.read_text(encoding="utf-8")
prima = t.count("widths={[420, 640, 900]}")
t = t.replace("widths={[420, 640, 900]}", "widths={[480, 720, 1080]}")
p.write_text(t, encoding="utf-8", newline="")
print(f"  misure richieste aggiornate: {prima} occorrenze")
