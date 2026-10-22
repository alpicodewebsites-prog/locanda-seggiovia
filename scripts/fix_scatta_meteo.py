import pathlib
p = pathlib.Path("scripts/scatta_meteo.mjs")
t = p.read_text(encoding="utf-8")
t = t.replace(
    "const colonna = page.locator('aside[aria-labelledby=\"titolo-dati\"]');",
    "const colonna = page.locator('[data-meteo]');",
)
p.write_text(t, encoding="utf-8", newline="")
print("  selettore corretto")
