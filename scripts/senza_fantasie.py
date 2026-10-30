import pathlib, re

# ------------------------------------------------------- 1. VIA LE FANTASIE
tolte = 0
for file in pathlib.Path("src/pages").rglob("*.astro"):
    t = file.read_text(encoding="utf-8")
    nuovo = re.sub(r"\bfantasia(?:-\d)?\s+", "", t)
    nuovo = re.sub(r"\s+fantasia(?:-\d)?\b", "", nuovo)
    if nuovo != t:
        file.write_text(nuovo, encoding="utf-8", newline="")
        tolte += 1
        print(f"  {file.relative_to('src/pages')}: fantasia tolta")

# Anche il CSS: i cinque motivi non servono piu'.
css = pathlib.Path("src/styles/global.css")
t = css.read_text(encoding="utf-8")
inizio = t.find("/* ==========================================================================\n   LE FANTASIE DEI TITOLI")
if inizio != -1:
    t = t[:inizio].rstrip("\n") + "\n"
    css.write_text(t, encoding="utf-8", newline="")
    print("  global.css: blocco delle fantasie rimosso")
else:
    print("  global.css: blocco non trovato")

# ------------------------------------------- 2. SENTIERI IN DUE FILE VERTICALI
t = css.read_text(encoding="utf-8")
vecchio = """/* --------------------------------------------------------------------------
   L'elenco dei sentieri: una colonna sola.

   Sette sentieri uno sotto l'altro, a tutta larghezza. Le schede hanno già il
   filetto di separazione in basso: in colonna diventa l'elenco stesso, e si
   legge come un indice invece che come una griglia di riquadri.

   Il testo però non deve correre per tutto lo schermo: sopra le 62 battute una
   riga stanca. Per questo le descrizioni hanno un limite di larghezza, mentre
   il filetto continua da bordo a bordo.
   -------------------------------------------------------------------------- */
.elenco-sentieri {
  margin: 0;
  padding: 0;
  list-style: none;
}

.elenco-sentieri .scheda-sentiero__testo {
  max-width: 62ch;
}
"""
nuovo = """/* --------------------------------------------------------------------------
   L'elenco dei sentieri: due file verticali.

   Non è una griglia che riempie riga per riga: è testo su due colonne, come un
   indice. I sette sentieri scendono lungo la prima fila e proseguono nella
   seconda — quattro sopra, tre sotto — invece di alternarsi a destra e a
   sinistra. Si legge in verticale, che è come si legge un elenco.

   `break-inside: avoid` tiene ogni scheda intera: senza, una si spezzerebbe a
   metà fra il fondo di una colonna e la cima dell'altra.
   -------------------------------------------------------------------------- */
.elenco-sentieri {
  margin: 0;
  padding: 0;
  list-style: none;
  column-count: 2;
  column-gap: 3.5rem;
}

.elenco-sentieri > li {
  break-inside: avoid;
}

.elenco-sentieri .scheda-sentiero__testo {
  max-width: 46ch;
}

@media (max-width: 47.99rem) {
  .elenco-sentieri {
    column-count: 1;
  }
}
"""
if vecchio in t:
    css.write_text(t.replace(vecchio, nuovo, 1), encoding="utf-8", newline="")
    print("  global.css: due file verticali")
else:
    print("  global.css: blocco dell'elenco non trovato")

print(f"  pagine toccate: {tolte}")
