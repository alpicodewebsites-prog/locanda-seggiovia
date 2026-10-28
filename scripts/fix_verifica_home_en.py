import pathlib
p = pathlib.Path("scripts/verify_build.py")
t = p.read_text(encoding="utf-8")

vecchio = """    check(
        "home en: i testi sono in inglese",
        "Explore the trails" in html_en_home and "Check availability" in html_en_home,
    )"""
nuovo = """    # Dalla home è stato tolto il modulo di prenotazione: il testo che si
    # controllava prima non c'è più. Le stringhe scelte sono quelle che restano —
    # l'invito dei sentieri e il titolo del carosello.
    check(
        "home en: i testi sono in inglese",
        "Explore the trails" in html_en_home
        and "What you will find here" in html_en_home,
    )"""
if vecchio not in t:
    print("  ancoraggio 1 non trovato")
else:
    t = t.replace(vecchio, nuovo, 1)
    print("  controllo dei testi inglesi aggiornato")

vecchio2 = """                "Scopri i sentieri",
                "Chiedi la disponibilità",
                "Invia la richiesta",
                "Tutti i sentieri",
                "Come si leggono le difficoltà","""
nuovo2 = """                "Scopri i sentieri",
                "Cosa trovi qui",
                "La cucina delle valli",
                "Verifica le date",
                "Come si leggono le difficoltà","""
if vecchio2 in t:
    t = t.replace(vecchio2, nuovo2, 1)
    print("  elenco dei residui aggiornato")

p.write_text(t, encoding="utf-8", newline="")
