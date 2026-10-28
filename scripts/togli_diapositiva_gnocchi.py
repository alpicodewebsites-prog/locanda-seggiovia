import pathlib

# La diapositiva degli gnocchi sparisce: la fotografia piu' grande del piatto e'
# 432 px, e nel riquadro viene mostrata a oltre 900. Sfocata. Torna appena la
# cliente carica lo scatto vero.
blocchi = {
    "src/content/home/testi.md": """  - titolo: Gli gnocchi con la fioreta
    testo: Prodotto De.Co., due ingredienti e nessuna scorciatoia. La ricetta depositata, passo per passo.
    immagine: /assets/gnocchi/dettagli/1-gnocchi.jpg
    collegamento: /gnocchi-con-la-fioreta
""",
    "src/content/home/en/testi.md": """  - titolo: Gnocchi with fioreta
    testo: A De.Co. product, two ingredients and no shortcuts. The registered recipe, step by step.
    immagine: /assets/gnocchi/dettagli/1-gnocchi.jpg
    collegamento: /gnocchi-con-la-fioreta
""",
}

for percorso, blocco in blocchi.items():
    p = pathlib.Path(percorso)
    t = p.read_text(encoding="utf-8")
    if blocco in t:
        t = t.replace(blocco, "", 1)
        p.write_text(t, encoding="utf-8", newline="")
        print(f"  {percorso}: diapositiva degli gnocchi tolta")
    else:
        print(f"  {percorso}: blocco non trovato")
