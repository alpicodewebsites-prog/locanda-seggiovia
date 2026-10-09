# Locanda Seggiovia — sito web

Sito statico della Locanda Seggiovia, Recoaro Terme (VI).
Costruito con **Astro 7** e **Tailwind CSS 4**. Nessun database, nessun server
applicativo, hosting gratuito.

- **Stato attuale: settimana 1 della roadmap** — MVP approvabile: infrastruttura,
  sistema di design, homepage completa, dati strutturati, immagini segnaposto,
  configurazione di deploy. Le altre pagine arrivano nelle settimane 2–3.
- Deploy: Netlify (o Cloudflare Pages), direttamente da GitHub.

---

## 1. Avvio rapido

Serve **Node.js 22.12 o superiore** (`node --version`).

```bash
npm install       # installa le dipendenze
npm run dev       # server di sviluppo su http://localhost:4321
npm run build     # genera il sito statico in dist/
npm run preview   # anteprima locale della build di produzione
```

> Su Windows, se `npm run dev -- --port XXXX` dà errore di argomenti non
> riconosciuti, usare direttamente `npx astro dev --port XXXX`.

### Verifica dell'output

Dopo `npm run build` si possono eseguire i controlli automatici:

```bash
python scripts/verify_build.py        # 35 controlli: SEO, dati strutturati, link, asset
node scripts/check_visibility.mjs     # il contenuto resta visibile anche senza JS
node scripts/shot.mjs                 # screenshot desktop + mobile per la revisione
```

`check_visibility.mjs` merita una nota: verifica che nessun elemento con
`data-aos` resti invisibile in quattro situazioni — JavaScript attivo su desktop,
su mobile, con `prefers-reduced-motion`, e **con JavaScript disattivato del
tutto**. È il controllo che impedisce il difetto classico dei siti con
animazioni al scroll: pagina bianca se lo script non parte.

---

## 2. Struttura del progetto

```
locanda-seggiovia/
├── src/
│   ├── pages/
│   │   ├── index.astro            # Homepage (settimana 1)
│   │   └── 404.astro
│   ├── components/
│   │   ├── Header.astro           # navigazione (menu mobile senza JS)
│   │   ├── Footer.astro           # recapiti, dati societari, link legali
│   │   └── Hero.astro             # apertura della home
│   ├── layouts/
│   │   └── BaseLayout.astro       # <head>, SEO, JSON-LD, AOS
│   ├── data/
│   │   └── site.ts                # ★ dati della struttura (unica fonte di verità)
│   ├── styles/
│   │   └── global.css             # ★ design system: palette, tipografia, componenti
│   └── assets/                    # ★ TUTTE le fotografie del sito (ottimizzate da Astro)
├── public/
│   ├── favicon.svg, apple-touch-icon.png, og-default.jpg
│   └── robots.txt
├── scripts/
│   ├── generate_placeholders.py    # genera le immagini segnaposto
│   ├── generate_og.py              # genera immagine social e icona iOS
│   ├── verify_build.py             # controlli automatici sull'output
│   ├── check_visibility.mjs        # nessun contenuto nascosto, anche senza JS
│   ├── diag.mjs                    # diagnostica dei valori CSS calcolati
│   └── shot.mjs                    # screenshot per la revisione visiva
├── astro.config.mjs
├── tailwind.config.mjs
├── netlify.toml
└── .env.example
```

---

## 3. Sistema di design

I token vivono in **`src/styles/global.css`**, nel blocco `@theme` di Tailwind 4.
Da lì Tailwind genera sia le classi (`bg-stone-100`) sia le variabili CSS
(`var(--color-stone-100)`) usate nei componenti.

> **Nota su Tailwind 4.** Astro 7 non usa più l'integrazione `@astrojs/tailwind`:
> la configurazione è *CSS-first*. Il file `tailwind.config.mjs` è incluso come
> documentazione dei token, ma **non è caricato**. Se serve caricarlo davvero,
> aggiungere in cima a `global.css`: `@config "../../tailwind.config.mjs";`

### Palette

| Ruolo | Token | Valore | Uso |
|---|---|---|---|
| Pietra alpina | `stone-100` | `#F2F0EB` | sfondo del sito |
| | `stone-800` | `#232220` | testo principale |
| | `stone-900` | `#1C1B19` | footer, fondali |
| Legno | `wood-700` | `#3F2F21` | superfici calde |
| Verde bosco | `forest-700` | `#2D3D31` | accenti, link, CTA |
| | `forest-900` | `#1E2A21` | fascia gastronomia |
| Alpenglow | `glow-300` | `#D8B3A3` | micro-accento, firma grafica |

### Tipografia

- **Titoli**: `Fraunces` (serif variabile con *optical size*). Usato **solo** per
  titoli e wordmark. Le grazie si assottigliano man mano che il testo cresce,
  come nella stampa tipografica.
- **Corpo**: stack di sistema (`system-ui`, `Segoe UI`, …). **Zero richieste di
  rete** per il testo: se il font dei titoli non carica, il contenuto resta
  leggibile con il serif di sistema.

### Movimento

AOS (Animate On Scroll) è integrato come richiesto, con due limitazioni deliberate:

- **Disattivato su schermi sotto i 768 px e con `prefers-reduced-motion`.**
  Un'animazione in meno è una pagina che si apre prima, e l'escursionista in
  montagna ha spesso rete debole.
- **Gli elementi non vengono mai nascosti in modo definitivo**: la classe
  `aos-ready` viene aggiunta solo dopo l'inizializzazione di AOS, quindi un
  errore JavaScript non può far sparire il contenuto.

Le animazioni usano `data-aos="fade-up"` / `fade-in` con `data-aos-delay`
progressivi, come da specifica.

---

## 4. ⚠️ Dati da confermare prima della pubblicazione

`src/data/site.ts` contiene alcuni **valori segnaposto**. Sono elencati come
`TODO` nel file e **devono** essere verificati prima del go-live:

| Campo | Stato | Perché conta |
|---|---|---|
| `telefono` / `telefonoLink` | `+39 000 000 0000` — segnaposto | è la CTA di contatto principale |
| `annoFondazione` | `null` | finché è `null` il titolo omette l'anno invece di inventarlo |
| `fiscale.partitaIva`, `fiscale.codiceFiscale` | zeri | obbligatori per legge nel footer |
| `orari` | da confermare | informazione operativa |
| `instagram` | `null` | il link compare solo se valorizzato |
| `geo.lat/lng` | centro di Recoaro | da raffinare sul civico esatto |
| `url` (in `astro.config.mjs`) | dominio ipotizzato | canonical, OG e sitemap |

**Nessun dato inventato è stato inserito al posto dei valori reali.** Dove
l'informazione mancava, il sito la omette invece di riempirla.

### Immagini

Le immagini attuali sono **segnaposto generati proceduralmente**
(`scripts/generate_placeholders.py`), non fotografie e non foto stock — il brief
le esclude. Sono di due tipi:

- **Paesaggi disegnati** (`hero-piccole-dolomiti`, `sentieri-*`,
  `territorio-malghe`, `locanda-facciata`): composizioni astratte che servono a
  valutare il taglio fotografico e i contrasti.
- **Riquadri vuoti etichettati** (`camere-interno`, `ristorante-sala`,
  `gnocchi-fioreta`): per camere, sala e piatto un disegno astratto sarebbe
  fuorviante, quindi il segnaposto dichiara esplicitamente «FOTO IN ARRIVO».

I testi `alt` **dicono che si tratta di segnaposto**. Quando arrivano gli scatti
reali: sostituire il file mantenendo il nome e aggiornare l'`alt` con la
descrizione vera del soggetto.

**Tutte le fotografie stanno in `src/assets/`**, in un unico posto: da lì Astro
le converte in WebP e genera le varianti responsive. Le pagine le richiamano con
`import immagine from '../assets/nome.jpg'`. In `public/` restano solo i file che
devono avere un URL fisso (favicon, icona iOS, immagine social, robots.txt).

---

## 5. Deploy su Netlify

1. Creare un repository su GitHub e caricare il progetto (vedi §7).
2. Su [netlify.com](https://netlify.com) → **Add new site** → **Import an existing project**.
3. Collegare il repository. Netlify legge `netlify.toml`: comando `npm run build`,
   cartella `dist`. Non serve configurare altro.
4. **Site configuration → Environment variables**: aggiungere le variabili
   elencate in `.env.example` (in particolare `PUBLIC_WEB3FORMS_KEY` e `SITE_URL`).
5. **Domain management**: puntare `locandaseggiovia.com` e attivare HTTPS
   (certificato automatico, gratuito).

Da quel momento ogni `git push` sul branch principale ripubblica il sito.

**Cloudflare Pages** funziona allo stesso modo: build command `npm run build`,
output directory `dist`, variabili d'ambiente nella sezione Settings.

---

## 6. Cosa arriva nelle prossime settimane

| Settimana | Contenuto |
|---|---|
| 2 | Pagine Camere e Ristorante · Sveltia CMS (`/admin`) · form Web3Forms |
| 3 | Pagina Gnocchi con la Fioreta · 6 pagine sentiero · pagina Contatti · Privacy e Cookie Policy |
| 4 | Audit Lighthouse · test mobile · formazione alla cliente · DNS e go-live |

### Nota su Sveltia CMS

Sveltia CMS è *Git-based*: funziona solo se il sito è pubblicato su un repository
GitHub e l'utente autorizza l'accesso. Il pannello `/admin` va quindi configurato
**dopo** la creazione del repository, altrimenti non ha nulla a cui collegarsi.
Per questo è previsto nella settimana 2 e non nella settimana 1.

---

## 7. Inizializzare il repository Git

```bash
git init
git add .
git commit -m "Settimana 1: setup Astro, design system e homepage"
git branch -M main
git remote add origin https://github.com/<utente>/locanda-seggiovia.git
git push -u origin main
```

Il file `.gitignore` esclude già `node_modules/`, `dist/`, `.astro/` e i file
`.env`.

---

## 8. Scelte tecniche e compromessi

| Scelta | Motivo |
|---|---|
| Astro, output statico | zero JavaScript non necessario, tempi di caricamento minimi su rete debole |
| Tailwind 4 CSS-first | coerente con Astro 7; un solo posto per i token |
| Un solo webfont, con *optical size* | meno richieste di rete, gerarchia tipografica reale |
| Font di sistema per il corpo | nessuna richiesta di rete, leggibilità immediata |
| Menu mobile in `<details>` | funziona anche senza JavaScript |
| AOS disattivato su mobile | come da specifica, ma senza penalizzare chi ha rete debole |
| Nessun analytics di default | nessun cookie di terze parti, nessun banner necessario |
| JSON-LD `Restaurant` + `LodgingBusiness` | una struttura con cucina e camere è entrambe le cose |

### Limiti noti di questa consegna

- Il sito ha **una sola pagina** oltre alla 404: i link alle altre sezioni
  puntano a URL previsti ma non ancora realizzati. `verify_build.py` li elenca
  come "previsti" e non come rotti.
- Il **form contatti non è ancora attivo**: arriva con la settimana 2, insieme
  alla chiave Web3Forms.
- **Nessuna verifica con un lettore di schermo reale** è stata eseguita. Sono
  applicati contrasto, focus visibile, ordine dei titoli, skip-link, `alt`
  veritieri e rispetto di `prefers-reduced-motion`, ma un test manuale con
  VoiceOver/NVDA resta da fare prima del go-live.
- Il punteggio **Lighthouse non è stato misurato**: va eseguito sulla build di
  produzione (settimana 4) e non su un server di sviluppo locale.
