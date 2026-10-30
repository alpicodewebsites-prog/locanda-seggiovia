import pathlib
p = pathlib.Path("src/styles/global.css")
t = p.read_text(encoding="utf-8")

vecchio = """/* --------------------------------------------------------------------------
   L'elenco dei sentieri: una riga da tre, una da quattro.

   Dodici colonne: le prime tre schede ne prendono quattro ciascuna (tre per
   riga), le successive tre ciascuna (quattro per riga). Su telefono ognuna
   prende tutta la larghezza.
   -------------------------------------------------------------------------- */
.elenco-sentieri {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 0 2rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.elenco-sentieri > li {
  grid-column: span 12;
}

@media (min-width: 48rem) {
  .elenco-sentieri > li:nth-child(-n + 3) {
    grid-column: span 4;
  }

  .elenco-sentieri > li:nth-child(n + 4) {
    grid-column: span 3;
  }
}
"""

nuovo = """/* --------------------------------------------------------------------------
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

if vecchio not in t:
    print("  blocco non trovato")
else:
    p.write_text(t.replace(vecchio, nuovo, 1), encoding="utf-8", newline="")
    print("  elenco dei sentieri: una colonna")
