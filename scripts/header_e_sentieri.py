import pathlib, re

# ---------------------------------------------------------------- 1. HEADER
h = pathlib.Path("src/components/Header.astro")
t = h.read_text(encoding="utf-8")
vecchio = (
    '        <span class="site-header__sotto hidden text-[0.68rem] leading-none '
    'tracking-[0.14em] uppercase xl:inline">\n'
    "          Recoaro Terme\n"
    "        </span>\n"
)
if vecchio in t:
    t = t.replace(vecchio, "", 1)
    h.write_text(t, encoding="utf-8", newline="")
    print("  header: tolta la scritta «Recoaro Terme»")
else:
    print("  header: la scritta non e' stata trovata (forse gia' tolta)")

# --------------------------------------------------------------- 2. SENTIERI
p = pathlib.Path("src/pages/sentieri/index.astro")
t = p.read_text(encoding="utf-8")

# Il cartello col numero non si usa piu': i sentieri senza numero CAI
# sembravano sbagliati accanto agli altri.
t = t.replace("import Segnavia from '../../components/Segnavia.astro';\n", "")
t = t.replace(
    """            // Il numero del segnavia senza il prefisso «CAI »: sul cartello si
            // stampa la cifra, come sui cartelli veri. Se il contenuto non lo
            // riporta, il cartello resta senza numero.
            const numero = sentiero.data.segnavia?.replace(/^CAI\\s*/i, '').trim();

""",
    "",
)
t = t.replace("                  <Segnavia numero={numero} nome={sentiero.data.nome} />\n\n", "")
t = t.replace(
    '<ul class="grid gap-x-10 md:grid-cols-2">',
    '{/*\n'
    '        Sette sentieri: una riga da tre e una da quattro.\n'
    '\n'
    '        Non è una griglia da due: le prime tre schede occupano quattro\n'
    '        colonne di dodici (tre per riga), le altre tre colonne (quattro per\n'
    '        riga). Un elenco solo, senza duplicare il codice, e le due righe\n'
    '        hanno il peso che meritano.\n'
    '      */}\n'
    '      <ul class="elenco-sentieri">',
)
p.write_text(t, encoding="utf-8", newline="")
print("  sentieri: cartello tolto, griglia 3 + 4")

# ---------------------------------------------------------------- 3. CSS
c = pathlib.Path("src/styles/global.css")
t = c.read_text(encoding="utf-8")
if ".elenco-sentieri {" not in t:
    ancora = ".scheda-sentiero {\n"
    nuovo = """/* --------------------------------------------------------------------------
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

""" + ancora
    t = t.replace(ancora, nuovo, 1)
    c.write_text(t, encoding="utf-8", newline="")
    print("  global.css: griglia dell'elenco")
else:
    print("  global.css: griglia gia' presente")
