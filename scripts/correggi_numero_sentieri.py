import pathlib, re

# I sentieri sono diventati sette quando ho aggiunto l'Orso e Gallo, ma due
# testi dicevano ancora "sei". Il numero va corretto nell'italiano E
# nell'inglese: lasciarlo sbagliato in una sola lingua sarebbe peggio.
correzioni = [
    ("src/content/home/testi.md", "Sei itinerari", "Sette itinerari"),
    ("src/content/home/testi.en.md", "Six itineraries", "Seven itineraries"),
    ("src/content/sentieri-pagina/testi.md", "Sei itinerari", "Sette itinerari"),
    ("src/content/sentieri-pagina/testi.en.md", "Seven itineraries", "Seven itineraries"),
]

for percorso, vecchio, nuovo in correzioni:
    p = pathlib.Path(percorso)
    t = p.read_text(encoding="utf-8")
    if vecchio in t:
        p.write_text(t.replace(vecchio, nuovo, 1), encoding="utf-8", newline="")
        print(f"  {percorso}: '{vecchio}' -> '{nuovo}'")
    else:
        print(f"  {percorso}: '{vecchio}' non trovato (forse gia' corretto)")
