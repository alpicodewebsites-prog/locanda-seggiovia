import pathlib
p = pathlib.Path("public/admin/config.yml")
t = p.read_text(encoding="utf-8")
prima = t

t = t.replace(
    "          - label: Testo del pulsante degli gnocchi\n"
    "            name: pulsanteGnocchi\n"
    "            widget: string\n"
    "            hint: La scritta dentro il pulsante giallo a pillola.",
    "          - label: Invito agli gnocchi, sotto l'apertura\n"
    "            name: pulsanteGnocchi\n"
    "            widget: string\n"
    "            hint: >-\n"
    "              Il collegamento in fondo all'apertura, accanto a quello dei\n"
    "              sentieri. Si comporta allo stesso modo: apri la pagina degli\n"
    "              gnocchi con la Fioreta.",
    1,
)
p.write_text(t, encoding="utf-8", newline="")
print("etichetta aggiornata:", prima != t)
