import pathlib
p = pathlib.Path("src/pages/contatti.astro")
t = p.read_text(encoding="utf-8")
vecchio = '<section class="pt-16 pb-12 md:pt-24 md:pb-16">'
if "fantasia" not in t and vecchio in t:
    p.write_text(t.replace(vecchio, '<section class="fantasia fantasia-5 pt-16 pb-12 md:pt-24 md:pb-16">', 1), encoding="utf-8", newline="")
    print("  contatti: fantasia-5")
else:
    print("  contatti: niente da fare")
