import pathlib
p = pathlib.Path("src/pages/ristorante.astro")
t = p.read_text(encoding="utf-8")
prima = t

# La colonna di introduzione si stringe, quella dei piatti si allarga.
t = t.replace('<div class="md:col-span-4">\n        <h2 id="titolo-menu"',
              '<div class="md:col-span-3">\n        <h2 id="titolo-menu"', 1)
t = t.replace('<div class="md:col-span-8">\n        {',
              '<div class="md:col-span-9">\n        {', 1)

p.write_text(t, encoding="utf-8", newline="")
print("griglia 4/8 -> 3/9:", prima != t)
