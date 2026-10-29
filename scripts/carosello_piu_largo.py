import pathlib
p = pathlib.Path("src/components/Carosello.astro")
t = p.read_text(encoding="utf-8")

sostituzioni = [
    # 1. Riquadro piu' largo: 60rem -> 74rem (960 -> 1184 px).
    ("    --largo: 60rem;", "    --largo: 74rem;"),
    (
        '                  sizes="(min-width: 64rem) 60rem, 94vw"',
        '                  sizes="(min-width: 74rem) 74rem, 94vw"',
    ),
    # 2. La fotografia un filo piu' scura: su uno scatto luminoso il testo
    #    chiaro non si legge, e scurire il vetro non basta.
    (
        "    aspect-ratio: 16 / 9;\n    object-fit: cover;\n"
        "    transition: transform 900ms cubic-bezier(0.22, 0.61, 0.36, 1);",
        "    aspect-ratio: 16 / 9;\n    object-fit: cover;\n"
        "    /*\n"
        "      Un filo piu' scura. Su una fotografia luminosa — cielo azzurro,\n"
        "      roccia al sole — il titolo chiaro si perde anche col velo. Il\n"
        "      `brightness` abbassa tutta l'immagine, non solo il fondo: cosi' il\n"
        "      testo resta leggibile in qualunque punto cada.\n"
        "    */\n"
        "    filter: brightness(0.82) saturate(1.04);\n"
        "    transition: transform 900ms cubic-bezier(0.22, 0.61, 0.36, 1);",
    ),
    # 3. Velo piu' deciso in basso, e una sfumatura laterale dove sta il testo.
    (
        """    background: linear-gradient(
      to top,
      rgba(20, 20, 18, 0.58) 0%,
      rgba(20, 20, 18, 0.2) 36%,
      rgba(20, 20, 18, 0) 64%
    );""",
        """    background:
      linear-gradient(
        to top,
        rgba(16, 16, 14, 0.78) 0%,
        rgba(16, 16, 14, 0.42) 30%,
        rgba(16, 16, 14, 0) 62%
      ),
      /* Da sinistra, dove appoggia il testo: senza, una roccia chiara sul
         bordo sinistro cancella il titolo. */
      linear-gradient(
        to right,
        rgba(16, 16, 14, 0.55) 0%,
        rgba(16, 16, 14, 0.22) 42%,
        rgba(16, 16, 14, 0) 70%
      );""",
    ),
    # 4. Ombra del testo piu' ferma.
    (
        "    text-shadow: 0 2px 18px rgba(15, 15, 12, 0.55);",
        "    text-shadow:\n      0 1px 3px rgba(10, 10, 8, 0.85),\n      0 4px 26px rgba(10, 10, 8, 0.7);",
    ),
    (
        "    text-shadow: 0 1px 12px rgba(15, 15, 12, 0.6);",
        "    text-shadow:\n      0 1px 3px rgba(10, 10, 8, 0.8),\n      0 3px 18px rgba(10, 10, 8, 0.6);",
    ),
]

for vecchio, nuovo in sostituzioni:
    if vecchio in t:
        t = t.replace(vecchio, nuovo, 1)
    else:
        print(f"  NON TROVATO: {vecchio.strip().splitlines()[0][:64]}")

p.write_text(t, encoding="utf-8", newline="")
print("  carosello: piu' largo, foto piu' scura, testo piu' leggibile")
