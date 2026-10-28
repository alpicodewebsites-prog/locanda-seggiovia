import pathlib

p = pathlib.Path("src/lib/pagine.ts")
t = p.read_text(encoding="utf-8")

# --- 1. Il tipo: il carosello deve essere dichiarato ----------------------
vecchio_tipo = "export interface ContenutoHome {"
nuovo_tipo = """export interface Diapositiva {
  titolo: string;
  testo: string;
  /** Percorso dell'immagine, ancora da risolvere. */
  immagine?: string;
  collegamento: string;
}

export interface ContenutoHome {"""
if vecchio_tipo in t:
    t = t.replace(vecchio_tipo, nuovo_tipo, 1)
else:
    print("  tipo ContenutoHome non trovato")

# --- 2. Il campo, nel tipo dei testi -------------------------------------
t = t.replace(
    "    territorioTesto: string;\n  };",
    "    territorioTesto: string;\n    carosello: Diapositiva[];\n  };",
    1,
)

# --- 3. E nel valore restituito ------------------------------------------
t = t.replace(
    "          territorioTesto: d.territorioTesto ?? TESTI_HOME_RISERVA.territorioTesto,\n        }",
    "          territorioTesto: d.territorioTesto ?? TESTI_HOME_RISERVA.territorioTesto,\n"
    "          // Le diapositive del carosello: se mancano, la sezione sparisce.\n"
    "          carosello: d.carosello ?? [],\n        }",
    1,
)

p.write_text(t, encoding="utf-8", newline="")
print("  pagine.ts: il carosello arriva alla home")

# --- 4. La riserva, per quando il contenuto manca del tutto ---------------
print("  controllo della riserva:")
print("    " + ("TESTI_HOME_RISERVA contiene carosello" if "carosello" in t else "la riserva non lo ha: il tipo lo chiede"))
