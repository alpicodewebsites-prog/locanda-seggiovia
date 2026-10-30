import pathlib

# ---------------------------------------------------------------- 1. STRISCIA
c = pathlib.Path("src/components/Carosello.astro")
t = c.read_text(encoding="utf-8")
t = t.replace(
    "  .striscia-sezione {\n    padding-block: var(--spacing-section);\n    overflow: hidden;\n  }",
    "  .striscia-sezione {\n    /* Meno aria sopra e sotto: è una fascia, non una sezione di testo. */\n"
    "    padding-block: clamp(2.5rem, 6vw, 4.5rem);\n    overflow: hidden;\n  }",
    1,
)
t = t.replace("    width: clamp(15rem, 26vw, 26rem);", "    width: clamp(16rem, 29vw, 30rem);", 1)
c.write_text(t, encoding="utf-8", newline="")
print("  striscia: immagini un po' piu' grandi, meno vuoto attorno")

# ------------------------------------------------------- 2. LE FANTASIE
CSS = pathlib.Path("src/styles/global.css")
t = CSS.read_text(encoding="utf-8")

if ".fantasia-1" not in t:
    FANTASIE = """
/* ==========================================================================
   LE FANTASIE DEI TITOLI
   --------------------------------------------------------------------------
   Un motivo dietro al titolo di ogni sezione, diverso per sezione. Sono
   `background-image` con un SVG dentro il dato: nessun file da caricare, nessun
   elemento in più nell'impaginazione, e il motivo non può finire sopra il
   testo.

   I colori vengono dal logo: il rosso della locanda, l'ocra, il verde bosco.
   Sono tenuti molto trasparenti apposta: devono fare atmosfera, non competere
   con la lettura.
   ========================================================================== */

.fantasia {
  background-repeat: repeat;
  background-position: top left;
}

.fantasia-1 {
  /* Archi concentrici, come le arcate del portico. */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='72' height='72'%3E%3Cpath d='M0 72a36 36 0 0 1 72 0' fill='none' stroke='%23b51c06' stroke-opacity='.13' stroke-width='2'/%3E%3Cpath d='M0 72a18 18 0 0 1 36 0' fill='none' stroke='%23c9a96b' stroke-opacity='.2' stroke-width='2'/%3E%3C/svg%3E");
  background-size: 72px 72px;
}

.fantasia-2 {
  /* Onde, come l'acqua delle terme. */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='88' height='44'%3E%3Cpath d='M0 22q22-16 44 0t44 0' fill='none' stroke='%23b51c06' stroke-opacity='.12' stroke-width='2'/%3E%3Cpath d='M0 38q22-16 44 0t44 0' fill='none' stroke='%232d3d31' stroke-opacity='.12' stroke-width='2'/%3E%3C/svg%3E");
  background-size: 88px 44px;
}

.fantasia-3 {
  /* Cime: due montagne e una stella. */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='84' height='56'%3E%3Cpath d='M0 56 28 10 56 56' fill='none' stroke='%23b51c06' stroke-opacity='.12' stroke-width='2'/%3E%3Cpath d='M44 56 62 28 80 56' fill='none' stroke='%23c9a96b' stroke-opacity='.22' stroke-width='2'/%3E%3Ccircle cx='16' cy='14' r='2' fill='%23b51c06' fill-opacity='.22'/%3E%3C/svg%3E");
  background-size: 84px 56px;
}

.fantasia-4 {
  /* Rombi, come le piastrelle del tavolo di cucina. */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='56'%3E%3Crect x='16' y='16' width='24' height='24' transform='rotate(45 28 28)' fill='none' stroke='%23b51c06' stroke-opacity='.11' stroke-width='2'/%3E%3Ccircle cx='28' cy='28' r='2.5' fill='%23c9a96b' fill-opacity='.28'/%3E%3C/svg%3E");
  background-size: 56px 56px;
}

.fantasia-5 {
  /* Coriandoli: cerchi di tre colori. */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='64'%3E%3Ccircle cx='12' cy='14' r='3' fill='%23b51c06' fill-opacity='.16'/%3E%3Ccircle cx='44' cy='28' r='2.2' fill='%23c9a96b' fill-opacity='.3'/%3E%3Ccircle cx='26' cy='48' r='2.6' fill='%232d3d31' fill-opacity='.14'/%3E%3C/svg%3E");
  background-size: 64px 64px;
}

"""
    CSS.write_text(t + FANTASIE, encoding="utf-8", newline="")
    print("  global.css: cinque fantasie")
else:
    print("  global.css: fantasie gia' presenti")

# --------------------------------------------- 3. APPLICARLE ALLE INTESTAZIONI
TESTATA = 'class="border-b border-stone-200 pt-16 pb-12 md:pt-24 md:pb-16"'
PAGINE = {
    "src/pages/camere.astro": 1,
    "src/pages/ristorante.astro": 4,
    "src/pages/sentieri/index.astro": 3,
    "src/pages/contatti.astro": 5,
    "src/pages/gnocchi-con-la-fioreta.astro": 2,
    "src/pages/la-locanda.astro": 1,
    "src/pages/privacy.astro": 4,
    "src/pages/cookie.astro": 4,
}

for percorso, numero in PAGINE.items():
    p = pathlib.Path(percorso)
    if not p.exists():
        print(f"  {percorso}: non esiste")
        continue
    t = p.read_text(encoding="utf-8")
    if f"fantasia-{numero}" in t:
        print(f"  {percorso}: gia' fatta")
        continue
    if TESTATA in t:
        t = t.replace(TESTATA, f'class="fantasia fantasia-{numero} border-b border-stone-200 pt-16 pb-12 md:pt-24 md:pb-16"', 1)
        p.write_text(t, encoding="utf-8", newline="")
        print(f"  {percorso}: fantasia-{numero}")
    else:
        print(f"  {percorso}: intestazione non trovata")

# La sezione «La locanda» della home.
h = pathlib.Path("src/pages/index.astro")
t = h.read_text(encoding="utf-8")
if "fantasia" not in t:
    t = t.replace(
        '<section class="section-y bg-stone-50" aria-labelledby="titolo-locanda">',
        '<section class="section-y fantasia fantasia-2 bg-stone-50" aria-labelledby="titolo-locanda">',
        1,
    )
    h.write_text(t, encoding="utf-8", newline="")
    print("  home: fantasia-2 sulla sezione della locanda")
