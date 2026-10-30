import json, urllib.parse, urllib.request

QUERIES = ["Piccole Dolomiti", "Recoaro Terme", "Pasubio", "Carega"]

def cerca(testo, limite=12):
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {testo}",
        "gsrnamespace": "6",
        "gsrlimit": str(limite),
        "prop": "imageinfo",
        "iiprop": "url|size|extmetadata",
        "iiurlwidth": "1600",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    richiesta = urllib.request.Request(url, headers={"User-Agent": "LocandaSeggiovia/1.0 (sito web)"})
    with urllib.request.urlopen(richiesta, timeout=40) as risposta:
        dati = json.load(risposta)
    return dati.get("query", {}).get("pages", {})

for testo in QUERIES:
    print(f"=== {testo} ===")
    try:
        pagine = cerca(testo)
    except Exception as errore:
        print(f"  errore: {errore}")
        continue
    righe = []
    for pagina in pagine.values():
        info = (pagina.get("imageinfo") or [{}])[0]
        larghezza = info.get("width", 0)
        altezza = info.get("height", 0)
        if larghezza < 1600:
            continue
        meta = info.get("extmetadata", {})
        licenza = meta.get("LicenseShortName", {}).get("value", "?")
        autore = meta.get("Artist", {}).get("value", "?")
        autore = __import__("re").sub(r"<[^>]+>", "", autore)[:40]
        righe.append((larghezza * altezza, pagina.get("title", ""), f"{larghezza}x{altezza}", licenza, autore, info.get("thumburl") or info.get("url")))
    righe.sort(reverse=True)
    for _, titolo, dimensioni, licenza, autore, _url in righe[:6]:
        print(f"  {dimensioni:>10}  {licenza:<22} {titolo[5:60]}")
    if not righe:
        print("  nessuna immagine abbastanza grande")
