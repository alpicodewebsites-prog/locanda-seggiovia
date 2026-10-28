import pathlib
p = pathlib.Path("scripts/pannello_lingue_chiare.py")
t = p.read_text(encoding="utf-8")
vecchio = '''        if " — English" in etichetta:
            return f"{rientro}label: EN · {etichetta.replace(' — English', '')}"
        return f"{rientro}label: IT · {etichetta}"'''
nuovo = '''        # `rientro` contiene già «label: »: va scritta una volta sola.
        if " — English" in etichetta:
            return f"{rientro}EN · {etichetta.replace(' — English', '')}"
        return f"{rientro}IT · {etichetta}"'''
if vecchio not in t:
    print("  ancoraggio non trovato"); raise SystemExit(1)
p.write_text(t.replace(vecchio, nuovo, 1), encoding="utf-8", newline="")
print("  corretto")
