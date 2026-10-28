import pathlib
p = pathlib.Path("scripts/verifica_bilingue_completo.py")
t = p.read_text(encoding="utf-8")
vecchio = '''# Le pagine che NON devono dichiarare una lingua alternativa.
SENZA_ALTERNATIVE = ["/404.html", "/grazie/", "/en/thank-you/"]'''
nuovo = '''# Le pagine che NON devono dichiarare una lingua alternativa.
#
# Solo la 404: è una pagina sola, servita per qualunque indirizzo sbagliato, e
# non ha una versione inglese. La conferma di invio invece ce l'ha, e le due si
# dichiarano a vicenda — anche se sono noindex, la dichiarazione è corretta.
SENZA_ALTERNATIVE = ["/404.html"]'''
if vecchio not in t:
    print("  ancoraggio non trovato"); raise SystemExit(1)
t = t.replace(vecchio, nuovo, 1)
p.write_text(t, encoding="utf-8", newline="")
print("  controllo corretto")
