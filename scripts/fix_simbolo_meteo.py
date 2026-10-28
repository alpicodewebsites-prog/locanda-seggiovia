import pathlib
p = pathlib.Path("src/components/MeteoSentiero.astro")
t = p.read_text(encoding="utf-8")
vecchio = "${simbolo(condizione(d.current.weather_code).cielo)}"
nuovo = "${simbolo(cielo(d.current.weather_code))}"
if vecchio in t:
    t = t.replace(vecchio, nuovo, 1)
    p.write_text(t, encoding="utf-8", newline="")
    print("  corretto: simbolo(cielo(...))")
else:
    print("  stringa non trovata")
