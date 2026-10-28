import pathlib

# --- 1. Immagini delle diapositive: solo fotografie vere -------------------
p = pathlib.Path("src/content/home/testi.md")
t = p.read_text(encoding="utf-8")
t = t.replace(
    "immagine: /assets/sentieri/03-grandi-alberi.jpg",
    "immagine: /assets/sentieri/06-strada-52-gallerie.jpg",
)
t = t.replace(
    "immagine: /assets/gnocchi/02-piatto-finito.jpg",
    "immagine: /assets/gnocchi/dettagli/1-gnocchi.jpg",
)
p.write_text(t, encoding="utf-8", newline="")
print("  testi.md: immagini sostituite con fotografie vere")

# --- 2. Il componente: etichette dei comandi nella lingua della pagina -----
c = pathlib.Path("src/components/Carosello.astro")
s2 = c.read_text(encoding="utf-8")
s2 = s2.replace(
    "  /** «Vai a» — il verbo davanti al nome della pagina. */\n  invito: string;\n}",
    "  /** «Vai a» — il verbo davanti al nome della pagina. */\n  invito: string;\n"
    "  /** Etichette dei comandi, per chi usa un lettore di schermo. */\n"
    "  precedente: string;\n  successiva: string;\n}",
)
s2 = s2.replace(
    "const { diapositive, lingua, etichetta, invito } = Astro.props;",
    "const { diapositive, lingua, etichetta, invito, precedente, successiva } = Astro.props;",
)
s2 = s2.replace(
    'class="carosello__freccia" data-indietro aria-label="…"',
    'class="carosello__freccia" data-indietro aria-label={precedente}',
)
s2 = s2.replace(
    'class="carosello__freccia" data-avanti aria-label="…"',
    'class="carosello__freccia" data-avanti aria-label={successiva}',
)
c.write_text(s2, encoding="utf-8", newline="")
print("  Carosello: etichette dei comandi")
