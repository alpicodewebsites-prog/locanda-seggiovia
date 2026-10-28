import pathlib
p = pathlib.Path("src/components/Header.astro")
t = p.read_text(encoding="utf-8")
vecchio = 'class="site-header__sotto hidden text-[0.68rem] leading-none tracking-[0.14em] uppercase sm:inline"'
nuovo = 'class="site-header__sotto hidden text-[0.68rem] leading-none tracking-[0.14em] uppercase xl:inline"'
if vecchio in t:
    t = t.replace(vecchio, nuovo, 1)
    p.write_text(t, encoding="utf-8", newline="")
    print("  la localita' in barra compare da 1280 px")
else:
    print("  NON TROVATO")
