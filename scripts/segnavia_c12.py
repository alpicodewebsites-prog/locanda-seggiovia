import pathlib

# Ponte Tibetano: l'Anello del Sengio Alto e' l'itinerario n. C12 del CAI Veneto
# (documento "ITINERARIO N. C12 - ANELLO DEL SENGIO ALTO", grandeguerra.caiveneto.it).
p = pathlib.Path("src/content/sentieri/ponte-tibetano.md")
t = p.read_text(encoding="utf-8")
if "segnavia:" not in t:
    righe = t.splitlines()
    for i, r in enumerate(righe):
        if r.startswith("immagine:"):
            righe.insert(i, "segnavia: C12")
            break
    p.write_text("\n".join(righe) + "\n", encoding="utf-8", newline="")
    print("  ponte-tibetano: segnavia C12 aggiunto")
else:
    print("  ponte-tibetano: segnavia gia' presente")
