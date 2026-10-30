import json, pathlib, re, urllib.parse, urllib.request

CARTELLA = pathlib.Path("materiale-commons")
CARTELLA.mkdir(exist_ok=True)

QUERIES = ["Recoaro Terme", "Pasubio"]
SCELTI = {
    "Recoaro Terme - Scorcio 01.jpg",
    "Recoaro Terme - Scorcio 02.jpg",
    "Recoaro Terme - Scorcio 04.jpg",
    "Recoaro Terme - Scorcio 05.jpg",
    "Recoaro Terme - Scorcio 06.jpg",
    "Pasubio, Vicenza - panoramio.jpg",
    "Monte Pasubio.jpg",
}

def cerca(testo):
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": f"filetype:bitmap {testo}", "gsrnamespace": "6", "gsrlimit": "14",
        "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": "1800",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    richiesta = urllib.request.Request(url, headers={"User-Agent": "LocandaSeggiovia/1.0"})
    with urllib.request.urlopen(richiesta, timeout=40) as risposta:
        return json.load(risposta).get("query", {}).get("pages", {})

scaricate = 0
for testo in QUERIES:
    for pagina in cerca(testo).values():
        titolo = pagina.get("title", "").replace("File:", "")
        if titolo not in SCELTI:
            continue
        info = (pagina.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        licenza = meta.get("LicenseShortName", {}).get("value", "?")
        autore = re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", "?"))[:60].strip()
        pagina_meta = meta.get("DescriptionUrl", {}).get("value", "")
        sorgente = info.get("thumburl") or info.get("url")
        destinazione = CARTELLA / re.sub(r"[^A-Za-z0-9._-]+", "-", titolo).lower()
        if destinazione.exists():
            continue
        try:
            richiesta = urllib.request.Request(sorgente, headers={"User-Agent": "LocandaSeggiovia/1.0"})
            with urllib.request.urlopen(richiesta, timeout=90) as risposta:
                destinazione.write_bytes(risposta.read())
            scaricate += 1
            print(f"  {destinazione.name}")
            print(f"     {info.get('thumbwidth')}x{info.get('thumbheight')} · {licenza} · {autore}")
        except Exception as errore:
            print(f"  errore su {titolo}: {errore}")

print(f"  scaricate: {scaricate}")
