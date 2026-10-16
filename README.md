# Locanda Seggiovia — sito web

Sito statico della Locanda Seggiovia, Recoaro Terme (VI).
Costruito con **Astro 7** e **Tailwind CSS 4**. Nessun database, nessun server
applicativo, hosting gratuito.

- **Stato attuale: settimana 3 completata** — tutte le pagine della roadmap sono
  realizzate: home, La Locanda, Camere, Ristorante, Gnocchi con la Fioreta,
  panoramica Sentieri con 6 schede di dettaglio, Contatti (form, orari, mappa),
  Privacy e Cookie Policy. Pannello di gestione contenuti attivo.
- Deploy: Vercel (anteprima attiva) e Netlify (hosting previsto al go-live).

---

## ⚠️ Servono tre fotografie — è la cosa che manca davvero

Il sito è completo e funzionante, ma **9 delle 14 immagini sono segnaposto
grafici generati**, non fotografie. È il motivo principale per cui il sito
appare anonimo: nessuna scelta di colore sostituisce una fotografia che non
esiste.

Oggi ogni segnaposto dichiara di esserlo (l'etichetta è scritta dentro
l'immagine, quindi sparisce da sola quando il file viene sostituito).

**Le tre prioritarie, in ordine di impatto:**

| # | Fotografia | Dove va | Requisito | Perché |
|---|---|---|---|---|
| 1 | Piccole Dolomiti o un sentiero | apertura della home | ≥ **2500 px** di larghezza | è la prima cosa che si vede aprendo il sito |
| 2 | Le camere | pagina Camere | ≥ 1600 px, orizzontale | oggi la pagina non ha nessuna foto di una camera |
| 3 | La sala del ristorante | pagina Ristorante | ≥ 1600 px, orizzontale | la cucina è il secondo motivo per cui si viene |

Vanno caricate dal pannello `/admin`, ognuna nella sezione della sua pagina
(*Home Page*, *Pagina La Locanda*, *Camere (elenco)*…). Caricando un file con lo
stesso nome, l'etichetta di segnaposto sparisce da sola. Dettagli nella
[guida alla cliente](docs/GUIDA-CLIENTE.md).

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
python scripts/verify_build.py        # 300 controlli: SEO di tutte le pagine, contenuti, CMS, link
node scripts/check_visibility.mjs     # il contenuto resta visibile anche senza JS
node scripts/test_header.mjs          # barra trasparente/solida, anche senza JS
node scripts/test_overlap.mjs         # la barra non copre mai il testo (28 misure di schermo)
node scripts/test_scroll.mjs          # ogni pagina scorre davvero
node scripts/test_form.mjs            # collaudo del modulo contatti (richiede `npm run preview`)
node scripts/test_mappa.mjs           # la mappa non parte prima del clic
node scripts/shot.mjs                 # screenshot desktop + mobile per la revisione
```

Tre di questi meritano una nota, perché nascono da difetti veri trovati durante
lo sviluppo:

- `test_overlap.mjs` misura **28 combinazioni** di larghezza e altezza. La
  sovrapposizione fra barra e titolo si manifestava solo su schermi bassi (560–700
  px): provando a 900 px non si vedeva.
- `test_header.mjs` verifica anche **senza JavaScript**: la prima versione della
  barra trasparente diventava invisibile sopra la fotografia se lo script non
  partiva.
- `test_scroll.mjs` nasce da un falso allarme del proprio autore: misurava la
  posizione di scroll subito dopo averla impostata, ma con `scroll-behavior:
  smooth` lo scorrimento è animato. Ora attende che si assesti.

`check_visibility.mjs` merita una nota: verifica che **nessun elemento con
contenuto resti invisibile** — testo o figura che sia — in quattro situazioni:
JavaScript attivo su desktop, su mobile, con `prefers-reduced-motion`, e **con
JavaScript disattivato del tutto**. Nasce per le animazioni allo scorrimento,
che sono state rimosse, ma il controllo è stato reso generale e resta: un
contenuto nascosto per sbaglio non si vede guardando la pagina, si vede solo
quando manca.

---

## 2. Struttura del progetto

```
locanda-seggiovia/
├── src/
│   ├── pages/
│   │   ├── index.astro                    # Homepage
│   │   ├── la-locanda.astro               # Storia e famiglia
│   │   ├── camere.astro                   # Camere e tariffe
│   │   ├── ristorante.astro               # Ristorante e menù
│   │   ├── gnocchi-con-la-fioreta.astro   # Pagina dedicata al piatto De.Co.
│   │   ├── sentieri/
│   │   │   ├── index.astro                # Panoramica + scala CAI
│   │   │   └── [id].astro                 # Scheda di ogni sentiero
│   │   ├── contatti.astro                 # Form + orari + mappa differita
│   │   ├── privacy.astro                  # Privacy Policy
│   │   ├── cookie.astro                   # Cookie Policy
│   │   ├── grazie.astro                   # Conferma invio (noindex)
│   │   └── 404.astro
│   ├── content.config.ts          # ★ schema delle collezioni (Astro 7)
│   ├── content/                   # ★ contenuti gestiti dal CMS
│   │   ├── camere/                #   Singola, Doppia
│   │   ├── menu/                  #   7 piatti, per categoria
│   │   ├── gnocchi/               #   Gnocchi con la Fioreta
│   │   └── sentieri/              #   6 itinerari
│   ├── components/
│   │   ├── Header.astro           # navigazione (menu mobile senza JS)
│   │   ├── Footer.astro           # recapiti, dati societari, link legali
│   │   └── Hero.astro             # apertura della home
│   ├── layouts/
│   │   └── BaseLayout.astro       # <head>, SEO, JSON-LD
│   ├── scripts/
│   │   ├── form-contatti.ts       # invio del modulo via JavaScript
│   │   └── mappa.ts               # caricamento differito della mappa Google
│   ├── data/
│   │   └── site.ts                # ★ dati della struttura + SITE_URL
│   ├── styles/
│   │   └── global.css             # ★ design system: palette, tipografia, componenti
│   └── assets/                    # ★ TUTTE le fotografie del sito (ottimizzate da Astro)
├── public/
│   ├── admin/                     # ★ pannello Sveltia CMS
│   │   ├── index.html             #   carica Sveltia dal CDN
│   │   └── config.yml             #   collezioni e campi
│   ├── favicon.svg, apple-touch-icon.png, og-default.jpg
│   └── robots.txt
├── scripts/
│   ├── generate_placeholders.py    # genera le immagini segnaposto
│   ├── generate_og.py              # genera immagine social e icona iOS
│   ├── verify_build.py             # controlli automatici sull'output
│   ├── check_visibility.mjs        # nessun contenuto nascosto, anche senza JS
│   ├── test_form.mjs               # collaudo del modulo contatti
│   ├── diag.mjs                    # diagnostica dei valori CSS calcolati
│   └── shot.mjs                    # screenshot per la revisione visiva
├── astro.config.mjs
├── tailwind.config.mjs
├── netlify.toml
├── vercel.json
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

### Accenti grafici

I toni sopra sono **spenti di proposito** perché devono funzionare come testo.
Come segno grafico però non si vedevano: `--color-forest-500` è `#5a7a5e`, che su
fondo chiaro sparisce. Esiste quindi una **seconda rampa satura**, usata solo per
linee, fili e bordi:

| Token | Valore | Dove |
|---|---|---|
| `--color-acc-bosco` | `#3f7a4a` | antipasti, sezioni verdi |
| `--color-acc-legno` | `#b57a3c` | primi, territorio, tariffe |
| `--color-acc-alba` | `#c9663f` | secondi, specialità della casa |
| `--color-acc-pietra` | `#9c958a` | dolci, contenuti neutri |

Si usano con le classi `.card-accento--*` (bordo superiore spesso) e
`.filo-accento--*` / `.cat-menu--*` (filo sotto i titoli).

### Fasce colorate

`.sezione-legno`, `.sezione-alba`, `.sezione-bosco-chiara` alternano il fondo di
alcune sezioni. Sono mescolate a sufficienza per vedersi: sotto il 40% di
color-mix il colore scompare nel grigio.

### Angoli

Arrotondati: `--raggio-media: 0.75rem` per immagini e `--raggio-card: 0.5rem`
per le card. La fotografia deve sembrare una fotografia, non un blocco
rettangolare incollato sulla pagina.

### Card colorate

`.card-accento--*` applica insieme tre cose: un bordo superiore spesso, gli
angoli arrotondati e una **tinta di fondo dello stesso accento** (12%). Cos la
card si stacca dal fondo senza bordi n ombre.

### Elemento grafico: `Cresta.astro`

Un profilo di montagna disegnato in linea, usato come pausa fra le sezioni e per
riempire gli spazi vuoti. Riprende la forma del favicon, quindi  coerente con
l'identit invece di essere decorazione casuale.  `aria-hidden`: non porta
informazione.

### Tipografia

- **Titoli**: `Fraunces` (serif variabile con *optical size*). Usato **solo** per
  titoli e wordmark. Le grazie si assottigliano man mano che il testo cresce,
  come nella stampa tipografica.
- **Corpo**: stack di sistema (`system-ui`, `Segoe UI`, …). **Zero richieste di
  rete** per il testo: se il font dei titoli non carica, il contenuto resta
  leggibile con il serif di sistema.

### Movimento

**Non ci sono animazioni allo scorrimento.** Erano state implementate con AOS
(Animate On Scroll) e sono state rimosse su richiesta del committente.

La scelta regge anche sul piano tecnico: le rivelazioni che partono scorrendo
sono fra i pattern sconsigliati dalle linee guida di accessibilità, perché il
contenuto compare in un momento imprevedibile, spesso non viene visto, e senza
JavaScript non comparirebbe affatto. Ora il contenuto è semplicemente presente,
subito.

Resta il **movimento che parte da un'azione dell'utente**, tutto fra 250 e 300
ms: il passaggio del mouse sui pulsanti, la freccia che scorre accanto al testo,
le schede che si sollevano, il contorno del focus da tastiera.

Resta anche la **rete di sicurezza per chi ha chiesto meno movimento dal
sistema**: `@media (prefers-reduced-motion: reduce)` azzera durate e
trasformazioni. La regola è volutamente generale, così vale anche per qualunque
movimento venga aggiunto in futuro senza doversene ricordare.

---

## 4. ⚠️ Dati da confermare prima della pubblicazione

`src/data/site.ts` contiene alcuni **valori segnaposto**. Sono elencati come
`TODO` nel file e **devono** essere verificati prima del go-live:

| Campo | Stato | Perché conta |
|---|---|---|
| `telefono` / `telefonoLink` | ✅ **0445 76162** — dal sito precedente | è la CTA di contatto principale |
| `fiscale.ragioneSociale` | ✅ **Ristorante Asnicar Bertoldi SNC** — dal sito precedente | compare nel footer |
| `annoFondazione` | `null` | finché è `null` il titolo omette l'anno invece di inventarlo |
| `fiscale.partitaIva`, `fiscale.codiceFiscale` | zeri | obbligatori per legge nel footer |
| `orari` | da confermare | informazione operativa |
| `instagram` | `null` | il link compare solo se valorizzato |
| `geo.lat/lng` | centro di Recoaro | da raffinare sul civico esatto |
| `url` (in `astro.config.mjs`) | dominio ipotizzato | canonical, OG e sitemap |

**Altri dati ricavati dal sito precedente** e già applicati:

- la **colazione è compresa** nella tariffa B&B;
- il **Wi-Fi è negli spazi comuni**, non in camera: la pagina Camere non lo
  promette più in camera (prima lo elencava, ed era sbagliato);
- l'attività è **aperta tutto l'anno**;
- il condimento degli gnocchi comprende anche **300 g di formaggio di malga
  stagionato** e il sale;
- la **prima domenica di settembre** si tiene la Festa dei gnocchi con la
  fioreta.

**Nessun dato inventato è stato inserito al posto dei valori reali.** Dove
l'informazione mancava, il sito la omette invece di riempirla. L'anno di
fondazione (1968) compare su un sito **di un'altra attività** presente fra gli
screenshot ed è stato volutamente **non** usato: va confermato dalla cliente.

### Immagini

Le fotografie stanno in `src/assets/`, **divise per sezione**: ognuna nella
cartella della pagina a cui appartiene. Astro le ottimizza da lì (WebP e versioni
ridimensionate), quindi il sito resta leggero.

| Cartella | Contenuto | Sezione del pannello |
|---|---|---|
| `home/` | apertura, panorama, montagne, facciata | Home Page |
| `la-locanda/` | facciata, tavolo di cucina | Pagina La Locanda |
| `camere/` | fotografie delle camere | Camere (elenco) |
| `ristorante/piatti/` | piatti del menù | Menù del ristorante |
| `sentieri/` | copertine dei sentieri, montagne, panorama | Sentieri (elenco), Pagina Sentieri |
| `gnocchi/` | piatto finito, preparazione | Gnocchi con la Fioreta |
| *(radice)* | `locanda-logo.png`, usato ovunque | — |

**Perché per cartella.** La libreria del pannello mostra, per ogni campo, i file
della cartella della sua sezione. Con tutti i file in una cartella sola, la
libreria di una sezione appare vuota e la fotografia già presente non può più
essere né ritrovata né sostituita.

**Perché `immagini.ts` usa un glob ricorsivo.** Il modulo indicizza
`../assets/**/*.{jpg,…}`: con un solo `*` le immagini nelle sottocartelle non
verrebbero nemmeno viste. La ricerca accetta sia il percorso completo
(`/assets/sentieri/gino-solda.jpg`) sia il solo nome file, così i contenuti
scritti prima della riorganizzazione continuano a funzionare.

**Sulle fotografie condivise fra due pagine.** La facciata compare sulla home e
su La Locanda, la preparazione su La Locanda e su Gnocchi: in quei casi il file
è **duplicato**, così ogni sezione è indipendente e si possono avere due scatti
diversi. Attenzione: le copie hanno contenuto identico, quindi Astro le
ottimizza in un unico file e lo intitola a una delle due. La pagina mostra
l'immagine giusta, ma il nome del file costruito può essere quello dell'altra —
`scripts/verify_build.py` lo tiene presente e accetta entrambi i nomi.

Una sola immagine  **generata proceduralmente** perch serve a tutta larghezza e
le foto fornite non bastano: `piccole-dolomiti-large.jpg` (25601440), usata
nella chiusura della home e nella pagina Sentieri. Il panorama reale con il
tricolore  400297: steso su 1440 pixel si sgrana, quindi compare **in piccolo**
nella pagina Sentieri, dove la sua risoluzione basta.

La cartella `foto sito locanda/` è conservata nel repository come archivio degli
originali: è da lì che si rigenerano gli asset.

**Restano segnaposto** le copertine dei sentieri e il panorama: sono disegni
generati proceduralmente da `scripts/generate_placeholders.py`, non fotografie.
**L'etichetta «FOTO IN ARRIVO» è scritta dentro l'immagine**, non nel codice della
pagina: quando la fotografa vera sostituisce il file, l'avviso sparisce da solo.
Dove non c'è nessuna immagine (camere, sala del ristorante) il riquadro è
disegnato in CSS e dichiarato nel testo `alt`.

**I file forniti sono piccoli** (il più grande è 600×450 px, il logo 281×218).
Vanno bene per gli spazi in cui sono usati, ma non reggono un ingrandimento a
schermo intero: per la fotografia di apertura della home serve uno scatto
almeno 2560 px di larghezza.

Le immagini stanno **tutte in `src/assets/`**, in un unico posto: da lì Astro le
converte in WebP e genera le varianti responsive. In `public/` restano solo i
file con URL fisso (favicon, icona iOS, immagine social, robots.txt).

> ⚠️ **La conversione in WebP dentro il pannello è deliberatamente disattivata.**
> `media_libraries.all.transformations.raster_image` è stato rimosso perché
> rendeva impossibile **sostituire** una fotografia: il pannello convertiva il
> file caricato in WebP e poi rifiutava di metterlo al posto di un `.jpg`
> esistente, perché il formato non corrispondeva. Non esiste un'opzione
> documentata per disattivare quel controllo. Il costo è qualche MB in più nel
> repository; il sito pubblicato resta leggero perché **Astro converte comunque
> in WebP in fase di build**. Non riattivare quella opzione senza risolvere prima
> il problema della sostituzione.

---

## 5. Deploy

### Anteprima attiva su Vercel (revisione cliente)

Il sito è pubblicato su Vercel ed è raggiungibile qui:

**https://locanda-seggiovia.vercel.app**

È un indirizzo **temporaneo** di anteprima, non il dominio definitivo.
Non è protetto da login: il link si può mandare direttamente alla cliente.

Il canonical e i tag Open Graph puntano già a `www.locandaseggiovia.com`, quindi
questa anteprima **non entra in concorrenza** con il sito vero nelle ricerche:
Google attribuisce il contenuto al dominio definitivo.

Per ripubblicare dopo una modifica:

```bash
vercel deploy --prod        # aggiorna locanda-seggiovia.vercel.app
vercel deploy               # crea una anteprima separata, con URL usa e getta
```

Il progetto è collegato all'account Vercel: la configurazione locale sta in
`.vercel/`, che è escluso da Git.

> Il file `vercel.json` imposta comandi di build, cartella di output e header di
> sicurezza. Deve contenere **JSON puro**: Vercel non accetta commenti, quindi le
> note stanno qui. Vercel applica i propri valori predefiniti per
> `Referrer-Policy` e `Strict-Transport-Security` e ignora i duplicati: le altre
> intestazioni sono efficaci.

### Netlify (alternativa, o hosting definitivo)

Il file `netlify.toml` è pronto per Netlify, che resta l'hosting previsto dal
progetto per il go-live.

1. Creare un repository su GitHub e caricare il progetto (vedi §7).
2. Su [netlify.com](https://netlify.com) → **Add new site** → **Import an existing project**.
3. Collegare il repository. Netlify legge `netlify.toml`: comando `npm run build`,
   cartella `dist`. Non serve configurare altro.
4. **Site configuration → Environment variables**: aggiungere le variabili
   elencate in `.env.example` (in particolare `PUBLIC_WEB3FORMS_KEY`).
5. **Domain management**: puntare `locandaseggiovia.com` e attivare HTTPS
   (certificato automatico, gratuito).

Da quel momento ogni `git push` sul branch principale ripubblica il sito.

**Cloudflare Pages** funziona allo stesso modo: build command `npm run build`,
output directory `dist`, variabili d'ambiente nella sezione Settings.

---

## 6. Pannello di gestione contenuti (Sveltia CMS)

Il pannello è pubblicato su **`/admin`** e non ha bisogno di alcun server: legge e
scrive direttamente i file Markdown del repository GitHub. Ogni salvataggio è un
commit, quindi ogni modifica è tracciata e sempre annullabile.

| File | Ruolo |
|---|---|
| `public/admin/index.html` | carica Sveltia dal CDN |
| `public/admin/config.yml` | backend GitHub, collezioni e campi |

### ⚠️ Passo obbligatorio prima che il pannello funzioni

In `config.yml` il repository è un **segnaposto**:

```yaml
backend:
  name: github
  repo: TUO-UTENTE/locanda-seggiovia   # ← da sostituire
  branch: main
```

1. Creare il repository su GitHub e caricare il progetto (§7).
2. Sostituire `TUO-UTENTE` con l'account reale.
3. Autorizzare l'applicazione OAuth: il login di Sveltia passa da un servizio
   OAuth (per impostazione predefinita `api.netlify.com/auth`). Serve
   registrare un'app OAuth o usare il servizio indicato nella
   [documentazione del backend GitHub](https://sveltiacms.app/en/docs/backends/github).
4. Aggiungere la collaboratrice come collaboratore del repository, con permesso
   di scrittura.

Fino al punto 2 il pannello si apre ma non trova nessun repository.

### Colonne e collezioni

| Collezione | Cartella | Campi principali |
|---|---|---|
| Camere e tariffe | `src/content/camere` | nome, ordine, descrizione, ospiti, tre tariffe, servizi |
| Menù del ristorante | `src/content/menu` | nome, categoria, ordine, descrizione, prezzo, specialità |
| Gnocchi con la Fioreta | `src/content/gnocchi` | storia, ricetta, lavorazione, condimento, riconoscimenti |
| Sentieri | `src/content/sentieri` | nome, sommario, descrizione, difficoltà, dati tecnici |

I nomi dei campi in `config.yml` **devono** restare allineati a quelli dello
schema in `src/content.config.ts`. Rinominarne uno da una parte sola fa fallire
la compilazione: è il vincolo da tenere presente quando si modifica il CMS.

Il CMS è configurato con `omit_empty_optional_fields: true`. È indispensabile:
senza quella riga Sveltia scriverebbe una stringa vuota per i campi opzionali
lasciati vuoti, e lo schema Zod di Astro rifiuterebbe il contenuto. È anche il
meccanismo che permette di **non inventare dati**: un campo che non si conosce
resta vuoto e semplicemente non compare nel sito.

---

## 7. Modulo di contatto (Web3Forms)

Il modulo è su `/contatti` e invia tramite Web3Forms, senza backend.

| Impostazione | Valore |
|---|---|
| Endpoint | `https://api.web3forms.com/submit` |
| Destinatario | `locandaseggiovia@gmail.com` |
| Chiave | variabile `PUBLIC_WEB3FORMS_KEY` |
| Antispam | campo esca `botcheck` + filtro Web3Forms |
| Dopo l'invio | redirect a `/grazie` |

Senza JavaScript il modulo funziona comunque: è una POST classica e Web3Forms
reindirizza a `/grazie` tramite il campo `redirect`. Con JavaScript attivo
l'invio avviene senza ricaricare la pagina e l'esito compare sotto il modulo.

### Stato del collaudo — da leggere

`node scripts/test_form.mjs` esegue 24 controlli. **Tutti superati**, e
verificano che la richiesta parta con l'endpoint, il metodo e i campi corretti
(`access_key`, `subject`, `from_name`, `redirect`, consenso privacy, campo esca
non compilato).

**Non è però la prova che l'email arrivi.** Due limiti concreti:

1. La chiave configurata è quella dimostrativa di Web3Forms, quindi l'invio
   viene rifiutato per progetto e nessuna email parte.
2. Il browser di collaudo automatico viene bloccato dal filtro anti-bot di
   Cloudflare (risposta 403 con `cf-ray`). È un comportamento atteso verso un
   browser headless, non un difetto del modulo.

Per completare il collaudo serve una prova manuale su un browser reale:

1. Ottenere la Access Key su [web3forms.com](https://web3forms.com) usando
   `locandaseggiovia@gmail.com`.
2. Impostare `PUBLIC_WEB3FORMS_KEY` in `.env` (in locale) e fra le variabili
   d'ambiente di Vercel/Netlify.
3. Ricompilare, aprire `/contatti` e inviare un messaggio vero.
4. Verificare che arrivi a `locandaseggiovia@gmail.com` e che il browser finisca
   su `/grazie`.

### reCAPTCHA v3 — perché è disattivato

Il brief chiedeva reCAPTCHA v3. È implementato e si attiva impostando la site key
in `PUBLIC_RECAPTCHA_SITE_KEY`, ma **di default è spento** per un motivo preciso:
su Web3Forms la verifica reCAPTCHA è una funzione dei **piani a pagamento**.
Inviare il campo `recaptcha_response` senza un token valido fa rifiutare l'invio.

Quindi: con il piano gratuito, attivare reCAPTCHA **romperebbe** il modulo. Con
un piano a pagamento basta impostare la variabile e tutto si attiva da solo,
compresa l'informativa su Google richiesta dal GDPR.

Con il piano gratuito il modulo resta protetto dal campo esca e dal filtro
antispam di Web3Forms, che è quanto offre il servizio a quel livello.

---

## 8. Cosa arriva nella prossima settimana

| Settimana | Contenuto |
|---|---|
| 4 | Audit Lighthouse · test mobile · formazione alla cliente · DNS e go-live |

Tutte le pagine previste dalla roadmap sono realizzate. Restano le attività di
collaudo e pubblicazione, non di sviluppo.

### Decisione sulla mappa di Google

La mappa nella pagina Contatti è a **caricamento differito**: l'iframe di Google
parte solo dopo un clic dell'utente. Non è una scelta estetica.

L'iframe di Google Maps imposta cookie di terze parti appena viene caricato.
Caricandolo automaticamente, il sito avrebbe dovuto mostrare un banner cookie e
chiedere il consenso prima di renderlo visibile. Con il caricamento differito non
c'è nulla da autorizzare, quindi **il sito non ha banner cookie** — coerente con
la scelta di non includere analytics né altri script di terze parti.

Il codice è in `src/scripts/mappa.ts`. Se si volesse caricare la mappa
automaticamente, bisognerebbe anche aggiungere un banner di consenso e
aggiornare la Cookie Policy.

---

## 9. Repository e pubblicazione

Il progetto  su GitHub:

**https://github.com/alpicodewebsites-prog/locanda-seggiovia** (branch `main`)

Vercel  collegato a questo repository: **ogni push ricostruisce il sito da solo**.
Non serve pi pubblicare a mano dal terminale  e soprattutto, quando la
proprietaria salva un contenuto dal pannello `/admin`, quel salvataggio  un
commit, quindi il sito si aggiorna da s in circa un minuto.

### Comandi utili

```bash
git add <file>          # mettere in attesa SOLO i file voluti
git commit -m "..."     # salvare la modifica
git push                # pubblicare (Vercel ricostruisce da solo)
```

> Non usare `git add -A` in questo progetto senza aver controllato `git status`
> prima: in passato ha incluso per errore file temporanei. Meglio indicare i file
> per nome.

---

## 9-bis. Autenticazione su GitHub

Git su questa macchina  autenticato con l'account `alpicodewebsites-prog`
tramite il Credential Manager di Windows. Le credenziali si gestiscono da
**Pannello di controllo ? Gestione credenziali ? Credenziali Windows**, cercando
`git:https://github.com`.

Se un push viene rifiutato con *Permission denied*, quasi sempre significa che
 salvata la credenziale di un **account diverso**: va cancellata, e il push
successivo chieder di accedere di nuovo.

```bash
git init
git add .
git commit -m "Settimana 2: CMS, pagine Camere/Ristorante/Contatti, modulo Web3Forms"
git branch -M main
git remote add origin https://github.com/<utente>/locanda-seggiovia.git
git push -u origin main
```

Il file `.gitignore` esclude già `node_modules/`, `dist/`, `.astro/`, `.vercel/`,
`screenshots/` e i file `.env`.

Dopo il push, aggiornare `repo:` in `public/admin/config.yml` con
`<utente>/locanda-seggiovia` (vedi §6).

---

## 10. Scelte tecniche e compromessi

| Scelta | Motivo |
|---|---|
| Astro, output statico | zero JavaScript non necessario, tempi di caricamento minimi su rete debole |
| Tailwind 4 CSS-first | coerente con Astro 7; un solo posto per i token |
| Un solo webfont, con *optical size* | meno richieste di rete, gerarchia tipografica reale |
| Font di sistema per il corpo | nessuna richiesta di rete, leggibilità immediata |
| Menu mobile in `<details>` | funziona anche senza JavaScript |
| Modulo contatti senza JavaScript | POST classica con redirect: funziona sempre, JS solo come miglioramento |
| Nessuna animazione allo scorrimento | il contenuto è presente subito, non appare in un momento imprevedibile; resta il movimento che parte da un'azione dell'utente |
| Nessun analytics di default | nessun cookie di terze parti, nessun banner necessario |
| JSON-LD `Restaurant` + `LodgingBusiness` | una struttura con cucina e camere è entrambe le cose |
| `Menu` e `OfferCatalog` sulle pagine nuove | menù e tariffe diventano leggibili anche dai motori di ricerca |
| Politiche di soggiorno in `site.ts` | valgono per tutte le camere: nel CMS sarebbero duplicabili e divergenti |
| `/grazie` esclusa da sitemap e robots | è una conferma, non un contenuto: contraddirebbe il suo `noindex` |
| Sentieri come pagina dinamica `[id].astro` | una sola impaginazione per sei schede, e il CMS può aggiungerne altre senza toccare il codice |
| Mappa a caricamento differito | l'iframe di Google imposta cookie: caricandolo su clic, il sito non ha bisogno di un banner |
| Difficoltà CAI in `additionalProperty` | non esiste un campo schema.org equivalente: dichiararla come proprietà aggiuntiva è più onesto che forzarla altrove |
| Nessun anno di fondazione citato | la cliente non l'ha confermato: meglio omettere la data che inventarla |

### Limiti noti di questa consegna

- **Il collaudo end-to-end del modulo non è concluso.** I 24 controlli superano,
  ma con la chiave dimostrativa nessuna email parte e il browser di collaudo viene
  bloccato da Cloudflare. Serve una prova manuale con la chiave reale (§7).
- **I dati societari restano segnaposto** in `src/data/site.ts`: telefono,
  partita IVA, codice fiscale, orari e anno di fondazione. La Privacy Policy li
  mostra esplicitamente come «da confermare».
- **Privacy e Cookie Policy sono testi base da far validare.** Descrivono con
  precisione come il sito tratta i dati, ma non sostituiscono il parere di un
  consulente privacy.
- **I prezzi del menù sono vuoti**: la cliente non li ha forniti, e la pagina lo
  dichiara apertamente invece di inventarli.
- **Le immagini sono segnaposto**, incluse le sei copertine dei sentieri e la
  foto degli ambienti: sono disegni generati proceduralmente, non fotografie.
- **Nessuna verifica con un lettore di schermo reale** è stata eseguita. Sono
  applicati contrasto, focus visibile, ordine dei titoli, skip-link, `alt`
  veritieri e rispetto di `prefers-reduced-motion`, ma un test manuale con
  VoiceOver/NVDA resta da fare prima del go-live.
- Il punteggio **Lighthouse non è stato misurato**: va eseguito sulla build di
  produzione (settimana 4) e non su un server di sviluppo locale.
