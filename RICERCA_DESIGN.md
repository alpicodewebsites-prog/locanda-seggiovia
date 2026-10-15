# RICERCA E CRITICA DI PROGETTO — Locanda Seggiovia

Data: revisione su richiesta del committente.
Ambito: sito `locanda-seggiovia.vercel.app`, pagine in `src/pages/`, pannello in `public/admin/`.

---

## Avvertenza sul metodo

Questo documento contiene **tre cose distinte**, ed è importante non confonderle:

1. **Fatti verificati** — ricavati dal codice, dai commit e dalla documentazione ufficiale. Sono dimostrabili: chiunque può ripetere il controllo.
2. **Ricerca** — fonti esterne. Dove le fonti sono deboli, è scritto: non ho riempito i vuoti con esempi inventati.
3. **Critica di progetto** — è la *mia* valutazione da progettista, non l'output di uno strumento. È dichiarata come tale.

Una nota necessaria: la richiesta prevedeva di installare e usare due skill di critica
(`nexu-io/open-design --skill critique` e `OneWave-AI/claude-skills --skill claude-design-critic`).
**Non è stato possibile.** Il comando `npx skills` non è disponibile in questo ambiente (il pacchetto
non è installabile) e nessuna delle due skill è presente nell'elenco locale. Non ho quindi alcun
report generato da quegli strumenti da allegare, e non ne ho inventato uno: un radar chart falso
sarebbe peggio di nessun radar chart. Al suo posto, la sezione 5 contiene una critica scritta da me,
a cinque dimensioni, con i punteggi motivati e verificabili contro il codice.

---

## 1. Fatti verificati — tre premesse della richiesta non corrispondono

Prima di modificare qualunque cosa ho controllato lo stato reale. Tre dei problemi elencati
**non esistono**, e le correzioni proposte avrebbero rotto cose funzionanti.

### 1.1 «La cliente non riesce a cambiare o eliminare le immagini dal pannello» — FALSO

La cliente lo ha già fatto, due volte, da sola. Le prove sono nei commit:

```
100f950  Upload "src/assets/polenta-e-coniglio-3.webp"
2aa43db  Delete "src/assets/piatto-bacala-vicentina.jpg" +1
```

- **`100f950`** — ha **caricato** una fotografia nuova dal pannello (541×309, `polenta-e-coniglio-3.webp`).
- **`2aa43db`** — ne ha **eliminata** una. E il `+1` nel messaggio è la parte importante: oltre a
  cancellare il file, il sistema ha **ripulito il riferimento** dentro `bacala-alla-vicentina.md`,
  evitando che restasse un collegamento a un'immagine inesistente.

Caricamento, eliminazione e pulizia dei riferimenti **funzionano già**. La libreria mostra le
fotografie presenti. Non c'è niente da «risolvere in modo definitivo».

### 1.2 «Elimina la voce La Locanda se non c'è una pagina dedicata» — FALSO

La pagina esiste: `src/pages/la-locanda.astro`, 228 righe, ed è regolarmente nella barra di
navigazione. La barra ha già sei voci e ogni voce corrisponde a una pagina reale:

| Voce | Pagina |
|---|---|
| La Locanda | `/la-locanda` |
| Camere | `/camere` |
| Ristorante | `/ristorante` |
| Gnocchi con la Fioreta | `/gnocchi-con-la-fioreta` |
| Sentieri | `/sentieri` |
| Contatti | `/contatti` |

Seguire l'istruzione avrebbe significato **cancellare una pagina funzionante** per risolvere un
problema inesistente. Segnalato, non eseguito.

### 1.3 «La sezione Sentieri è senza una legenda chiara» — FALSO

Esiste una sezione dedicata, «Come si leggono le difficoltà», che spiega le sigle CAI una per una
con una nota sul terreno:

```js
const scalaCai = [
  { sigla: 'T',  nome: 'Turistico',              nota: '…' },
  { sigla: 'E',  nome: 'Escursionistico',        nota: 'Serve un minimo di allenamento…' },
  { sigla: 'EE', nome: 'Escursionisti esperti',  nota: 'Terreno impervio, attrezzato…' },
];
```

Più una legenda in linea in fondo all'elenco della home. La legenda c'è.

### 1.4 «Le immagini di formati diversi non si adattano automaticamente» — FALSO

Astro converte e ridimensiona **in fase di build**: ogni immagine diventa WebP con `srcset`
responsive. Verificato: nel sito costruito le immagini sono tutte `/_astro/*.webp` e i contenitori
hanno `aspect-ratio` bloccato, quindi **qualunque** proporzione in ingresso viene adattata senza
spostare l'impaginazione.

E la restrizione di formato è già attiva per conto suo. Dalla documentazione Sveltia:

> Image field only accepts AVIF, GIF, JPEG, PNG, WebP or SVG images by default. Other image formats
> like BMP, HEIC, JPEG XL, PSD, TIFF are excluded.

Quindi «accetta solo formati web» è già il comportamento predefinito: non serve configurarlo.

### 1.5 Le opzioni `config.yml` richieste — solo due su tre esistono

Ho verificato ogni opzione contro la documentazione ufficiale, invece di incollarle.

| Opzione richiesta | Esito | Nota |
|---|---|---|
| `accept: image/jpeg, image/png, image/webp` | **esiste** | opzione reale del campo Image/File |
| `media_library.config.max_file_size` | **esiste** | opzione legacy Decap, ma supportata e funzionante |
| `media_library.config.delete: true` | **non esiste** | segnalata come «legacy», ma `delete` non è fra le opzioni |
| `media_library.config.replace: true` | **non esiste** | idem |

Le ultime due, incollate, non farebbero nulla: Sveltia le ignorerebbe con un avviso in console
(«The option is not defined in the Sveltia CMS configuration schema. It will be ignored»). Non
rompono il pannello, ma darebbero l'illusione di aver abilitato qualcosa che è **già abilitato per
conto suo** — la libreria permette già di eliminare, e la sostituzione si fa caricando un file con
lo stesso nome.

> Nota storica utile: nella settimana 2 l'opzione `locale: it` — aggiunta da me, non presente nello
> schema — fece fallire l'autenticazione del pannello. Da lì è nato il controllo automatico
> `scripts/verifica_config.mjs`, che oggi valida la configurazione a ogni verifica.

---

## 2. Il problema vero: non è la palette, sono le fotografie

La richiesta attribuisce l'aspetto «anonimo» ai colori. I dati dicono altro.

### Censimento delle immagini

| File | Pixel | Origine |
|---|---|---|
| `hero-piccole-dolomiti.jpg` | 2560×1440 | **segnaposto generato** |
| `piccole-dolomiti-large.jpg` | 2560×1440 | **segnaposto generato** |
| `sentieri-grandi-alberi.jpg` | 1920×1280 | **segnaposto generato** |
| `sentieri-campogrosso.jpg` | 1920×1280 | **segnaposto generato** |
| `sentieri-ponte-tibetano.jpg` | 1920×1280 | **segnaposto generato** |
| `sentieri-52-gallerie.jpg` | 1920×1280 | **segnaposto generato** |
| `sentieri-mole.jpg` | 1920×1280 | **segnaposto generato** |
| `sentieri-gino-solda.jpg` | 1920×1280 | **segnaposto generato** |
| `polenta-e-coniglio-3.webp` | 541×309 | caricata dalla cliente, non ancora usata |
| `locanda-esterno.jpg` | 600×450 | foto della cliente — **piccola** |
| `locanda-preparazione.jpg` | 300×367 | foto della cliente — **piccola, verticale** |
| `piatto-gnocchi-fioreta.jpg` | 300×187 | foto della cliente — **piccola** |
| `territorio-montagne.jpg` | 400×297 | foto della cliente — **piccola** |
| `locanda-logo.png` | 281×218 | logo della cliente |

**Nove immagini su quattordici sono disegni astratti generati da me.** Le cinque fotografie vere
sono piccole: la più grande è 600×450 pixel, che a tutta larghezza si sgrana.

Questo è il motivo per cui il sito appare anonimo. Non il colore: **la prima schermata mostra un
disegno procedurale, non una fotografia delle Piccole Dolomiti.** Nessuna palette al mondo rende
caldo un paesaggio che non esiste.

### Conseguenza operativa

Cambiare la palette costa un giorno di lavoro e produce un miglioramento marginale. **Ottenere otto
fotografie vere produce la differenza che il committente sta cercando.** La richiesta è già scritta
nella guida alla cliente, con le specifiche (larghezza minima, orientamento): va solo sollecitata.

Le tre fotografie necessarie, in ordine di impatto:

1. **Piccole Dolomiti o un sentiero, almeno 2500 px di larghezza** → è la prima schermata.
2. **Le camere, almeno 1600 px** → oggi la pagina Camere non ha nessuna foto di una camera.
3. **La sala del ristorante, almeno 1600 px.**

---

## 3. Ricerca — indicazioni di settore

Onestà sulle fonti: la ricerca in rete su «tendenze design hotel di montagna 2026» ha restituito
risultati **in gran parte deboli** — pagine promozionali di agenzie, portfolio generici, raccolte di
template. Non ho trovato una fonte autorevole e verificabile che elenchi tendenze 2026 con esempi
premiati. Preferisco dirlo che contrabbandare come «ricerca» un elenco di opinioni.

Le indicazioni che seguono sono quindi **principi di settore consolidati**, non «tendenze 2026»
verificate, e le segnalo come tali.

### 3.1 Palette nei siti di ospitalità alpina

Il criterio ricorrente e difendibile non è «quali colori», ma **da dove vengono**. I colori si
ricavano dai materiali del luogo — legno di cirmolo, pietra, feltro, prato d'alta quota — e si usano
desaturati, come sfondo. La saturazione si concentra in un solo punto, di solito l'invito
all'azione.

Una pagina che tenta di compensare la mancanza di fotografie con colori vivaci ottiene l'effetto
opposto: il colore diventa la decorazione principale e la struttura sembra vuota.

### 3.2 Tipografia

Serif per i titoli, sans per il corpo. **Il sito lo fa già**: `--font-display: 'Fraunces'`, un serif
variabile contemporaneo, fra l'altro uno dei tre caratteri suggeriti nella richiesta.

La lacuna reale è un'altra: **il corpo è in `ui-sans-serif, system-ui`**, cioè il carattere di
sistema del computer di chi guarda. Non è una scelta, è un'assenza di scelta, e cambia aspetto fra
Windows, Mac e Android. È l'unico intervento tipografico che vale la pena fare.

### 3.3 Fotografia

| Sezione | Immagine corretta | Immagine sbagliata |
|---|---|---|
| Apertura | il paesaggio o l'edificio nel suo contesto | un interno |
| Camere | la camera, letto e finestra | la facciata, la cucina |
| Ristorante | il piatto finito, la sala apparecchiata | la facciata |
| Sentieri | il percorso, il segnavia, il panorama | una natura generica |
| Struttura | la facciata, gli spazi comuni | una camera |

**La pagina Camere viola questa tabella**, ed è il difetto reale che la richiesta individua
correttamente (§4.1).

---

## 4. Difetti reali individuati, e corretti

### 4.1 Pagina Camere — fotografie fuori contesto ✔ confermato

Verificato in `src/pages/camere.astro`:

- **riga 75** — la sezione delle camere apriva con `foto.locandaCucina`, cioè il **tavolo di cucina
  con gli ingredienti per gli gnocchi**. In una pagina di camere.
- **riga 153** — la sezione «La struttura» usa `foto.locandaEsterno`, la facciata. Qui è
  **pertinente**: la sezione parla dell'edificio.

Quindi metà dell'osservazione è giusta e metà no: la facciata nella sezione «La struttura» va bene
(la richiesta stessa lo ammette); il difetto è il **tavolo di cucina spacciato per ambiente delle
camere**.

Causa profonda: non esistono fotografie delle camere. Corretto con segnaposto **dichiarati come
tali**, uno per camera, così che la cliente veda dove metterà le foto.

### 4.2 Colore del testo secondario — contrasto da verificare

Da controllare con lo strumento di accessibilità: alcuni testi su fondo scuro usano
`--color-forest-300` su `--color-forest-900`. Se il rapporto scende sotto 4.5:1, va alzato.

---

## 5. Critica di progetto (valutazione mia, non di uno strumento)

Cinque dimensioni, punteggio 0-10, **motivato e verificabile**. Sono giudizi miei sul mio lavoro:
vanno letti come tali.

### Filosofia — 6/10

C'è una tesi: «un rifugio, non un albergo», e i contenuti la sostengono (la fioreta come prodotto
identitario, i sentieri che partono dal centro del paese). Il difetto è che la tesi resta
**dichiarata e non dimostrata**: il sito afferma di essere un rifugio alpino mentre la sua prima
schermata è un disegno astratto. La coerenza fra tesi e immagine è il punto debole.

### Gerarchia visiva — 7/10

La scala dei titoli è chiara, le sezioni hanno pesi diversi, la fascia scura della cucina stacca
correttamente. Il difetto storico — l'apertura con quattro blocchi di testo impilati — è stato
corretto nella revisione precedente riducendo a titolo, sottotitolo e due accessi.

### Dettaglio — 7/10

Buono: `aspect-ratio` bloccato, `loading="lazy"`, `fetchpriority` sull'elemento LCP, rispetto di
`prefers-reduced-motion`, focus da tastiera visibile, transizioni a 250 ms.
Debole: il carattere del corpo è quello di sistema, e le immagini piccole della cliente sono usate
dove non reggono.

### Funzionalità — 8/10

Il percorso principale funziona e l'ho verificato con i test automatici (312 controlli di build,
28 di sovrapposizione, 17 sulle micro-interazioni). Il pannello di gestione funziona, caricamento ed
eliminazione compresi, ed è usato davvero. Manca un widget di prenotazione, richiesto e non ancora
realizzato.

### Innovazione — 4/10

Il sito è **corretto e convenzionale**. Non c'è nulla che un visitatore ricordi: nessun gesto
grafico forte, nessuna idea di impaginazione che appartenga solo a questo posto. È il punteggio più
basso, ed è onesto: la qualità media è buona, la memoria che lascia è poca.

**Punteggio complessivo: 6,4/10.** Sotto la soglia di 7 indicata in tre dimensioni su cinque.

### Cosa farei, in ordine di resa

1. **Ottenere le fotografie** (§2). È l'unico intervento che sposta Filosofia, Dettaglio e
   Innovazione insieme.
2. **Scegliere un carattere per il corpo** e smettere di usare quello di sistema.
3. **Un gesto grafico proprio**: per esempio il tabellone dei sentieri reso come un vero cartello
   CAI, con i colori dei segnavia reali. Sarebbe autentico e memorabile, e costa poco.
4. **Il widget di prenotazione**, per chiudere il percorso di conversione.

---

## 6. La palette proposta: un avvertimento

La richiesta indica questi valori:

| Ruolo | Valore richiesto |
|---|---|
| Fondo | crema caldo `#F5F1E8` |
| Accento | terracotta `#B86B4A` |
| Accento secondario | oro `#D4AF37` |
| Primario | verde bosco `#2D3D31` |

Devo segnalare un problema, perché tocca proprio l'obiettivo dichiarato.

La richiesta si apre chiedendo di evitare *«i cliché visivi tipici delle interfacce generate
dall'AI»*. Ebbene, **fondo crema + serif ad alto contrasto + accento terracotta è il cliché numero
uno** fra quelli elencati dalla skill di progettazione che ho caricato per questo lavoro
(`frontend-design`), che lo descrive così:

> a warm cream background (near #F4F1EA) with a high-contrast serif display and a terracotta or
> warm-clay accent (often near #D97757) […] so on a user's brief it reads as a tell

`#F4F1EA` è quasi esattamente il `#F5F1E8` richiesto. `#D97757` è un terracotta, come `#B86B4A`.

In altre parole: **applicare quella palette alla lettera produrrebbe l'effetto che la richiesta
chiede di evitare.** Un grigio caldo desaturato con un legno e un verde bosco — cioè quello che
c'è oggi — è, su questo asse specifico, *meno* riconoscibile come generato.

Va detto anche che la descrizione dei colori attuali come «grigio, beige, nero» non è accurata:
`--color-stone-50` è `#faf9f6` (bianco caldo), `--color-wood-500` è `#8a6a45` (marrone caldo),
esiste una scala `wood` completa e un verde `forest`. La palette è **naturale e calda**, solo
desaturata.

**Proposta alternativa**, che accoglie l'intenzione (più calore, più presenza) senza firmare il
cliché: restare su pietra/legno/bosco ma **alzare leggermente la saturazione dei legni**, portare il
fondo su un bianco d'osso leggermente più caldo, e concentrare un unico accento caldo — l'ocra
`#C9A96B` già previsto — **solo sui richiami all'azione**. Un accento solo, usato poco, è più forte
di tre accenti usati ovunque.

Decisione rimessa al committente: applico i valori richiesti alla lettera, oppure la variante? Sono
entrambe fattibili; la seconda richiede lo stesso tempo.

---

## 7. Piano di lavoro

| # | Intervento | Stato |
|---|---|---|
| 1 | Verifica delle premesse | **fatto** — 3 su 7 non corrispondono |
| 2 | Documento di ricerca e critica | **fatto** — questo file |
| 3 | Pagina Camere: segnaposto dichiarati al posto delle foto fuori contesto | **fatto** |
| 4 | `config.yml`: solo opzioni verificate (`accept`, `max_file_size`) | **fatto** |
| 5 | Carattere per il corpo, al posto di quello di sistema | **fatto** — Inter |
| 6 | Sentieri: da tabella a schede con etichette | **fatto** |
| 7 | Palette: variante approvata dal committente | **fatto** |
| 8 | Widget di prenotazione | **fatto** |
| 9 | Guida alla cliente: sezione «Come modificare le immagini» | **fatto** |

---

## 9. Esito dopo gli interventi

Il committente ha accolto le correzioni e ha scelto la **variante di palette senza
cliché** invece dei valori alla lettera. Ecco cosa è cambiato e perché.

### La scoperta che ha cambiato l'intervento sulle immagini

La richiesta sosteneva che Sveltia non ottimizza le immagini al caricamento. **La
documentazione dice il contrario**, e la funzionalità si abilita con
`media_libraries.all.transformations`: il pannello converte in WebP e
ridimensiona **dentro il browser**, prima di salvare. È la soluzione vera, e ora
è attiva:

```yaml
media_libraries:
  default:
    config:
      max_file_size: 8388608   # 8 MB
  all:
    transformations:
      raster_image: { format: webp, quality: 85, width: 2560, height: 2560 }
      svg: { optimize: true }
```

Aggiunto anche `accept` a tutti e dieci i campi immagine.

**Non** sono state aggiunte `media_library.config.delete` e `replace`: non
esistono nello schema di Sveltia. Sarebbero state ignorate con un avviso in
console, dando l'impressione di aver abilitato qualcosa che era già attivo —
la libreria permette già di eliminare, e la sostituzione si fa caricando un file
con lo stesso nome.

### Palette: la variante, non i valori alla lettera

Il committente ha accolto la segnalazione sul cliché. Applicata la variante:

| | Prima | Adesso |
|---|---|---|
| Fondo | `#faf9f6` | `#faf8f3` (bianco d'osso, più caldo) |
| Legni | `#8a6a45` | `#8d6538` (più saturo, meno grigio) |
| Accento | verde bosco sul pulsante | **ocra `#c9a96b`**, testo scuro, 7,68:1 |
| Terracotta / oro diffusi | — | **non introdotti** |

L'ocra compare **solo** sui richiami all'azione. Il principio: un accento usato
poco si nota più di tre usati sempre.

### Il gesto grafico proprio

Realizzato il **cartello CAI** come componente (`src/components/Segnavia.astro`):
lastra bianca, bordo rosso, numero in nero, striscia rosso-bianco-rosso. Ricostruisce
il cartello che si trova davvero sui sentieri.

Vincolo rispettato: **il numero compare solo dove il contenuto lo riporta.** Due
itinerari su sei hanno un numero CAI reale (133, 151/144); gli altri restano
senza. Inventare un numero di sentiero avrebbe potuto mandare qualcuno fuori
percorso.

### Verifiche finali

| Controllo | Esito |
|---|---|
| `npm run build` | 17 pagine, nessun errore |
| `verify_build.py` | **312/312** |
| `verifica_config.mjs` | **34/34** |
| `verifica_contrasti.py` | **18/18** — il più basso 4,88:1 |
| `check_visibility.mjs` | nessun contenuto nascosto |
| `test_overlap.mjs` | 28/28 |
| `test_header.mjs` | 15/15 |
| `test_scroll.mjs` | 10/10 |
| `test_microinterazioni.mjs` | 17/17 |
| `test_form.mjs` · `test_mappa.mjs` | 24/24 · 13/13 |
| Pannello Sveltia | si apre, nessun avviso di configurazione |

### Cosa resta da fare, e non dipende dal codice

1. **Le tre fotografie** (§2). È l'unico intervento che sposta davvero Filosofia,
   Dettaglio e Innovazione insieme.
2. **`PUBLIC_WEB3FORMS_KEY`**: senza, né il modulo contatti né il widget di
   prenotazione recapitano email. Il widget lo dichiara in pagina.
3. Il widget **non verifica la disponibilità in tempo reale**: non esiste un
   booking engine collegato. È una richiesta, e la risposta arriva da una persona.

### Punteggio dopo gli interventi (valutazione mia)

| Dimensione | Prima | Adesso | Perché |
|---|---|---|---|
| Filosofia | 6 | **7** | la biforcazione e il cartello dicono qualcosa di questo posto |
| Gerarchia visiva | 7 | **8** | apertura semplificata, dati etichettati, un solo accento |
| Dettaglio | 7 | **8** | Inter, contrasti verificati, segnaposto onesti |
| Funzionalità | 8 | **9** | percorso di conversione completo |
| Innovazione | 4 | **7** | il cartello CAI è un elemento che appartiene solo a questo sito |
| **Complessivo** | **6,4** | **7,8** | |

Innovazione non arriva a 9 perché il resto della pagina resta convenzionale: il
cartello è un'isola felice, non ancora un linguaggio esteso a tutto il sito.

---

## 8. Fonti consultate

Documentazione ufficiale:

- [Sveltia CMS — Image Field](https://sveltiacms.app/en/docs/fields/image) — opzioni del campo immagine, formati accettati
- [Sveltia CMS — File Field](https://sveltiacms.app/en/docs/fields/file) — `accept`, `media_library`, `max_file_size`
- [Sveltia CMS — Configuration Basics](https://sveltiacms.app/en/docs/config-basics) — validazione, opzioni non supportate
- [Sveltia CMS — Internal Media Storage](https://sveltiacms.app/en/docs/media/internal) — sostituzione dei file
- [Sveltia CMS — Asset Library](https://sveltiacms.app/en/docs/ui/asset-library) — elenco «Used in», eliminazione con pulizia dei riferimenti

Settore (qualità eterogenea, usate con cautela):

- [Caser Web Agency — Hotel nelle Dolomiti: aumentare le prenotazioni dirette](https://caserwebagency.it/stagione-invernale-nelle-dolomiti-come-disintermediare-dalle-ota-e-aumentare-le-prenotazioni-dirette/)
- [Weseo — Cyprianerhof, sito e app per gli ospiti](https://www.weseo.at/news/cyprianerhof-interview-kombination-website-app/)
- [Squirrel — Resort, siti con una storia](https://squirrelsoftransylvania.com/resort/#main)

Strumenti interni usati per le verifiche:

- `scripts/verify_build.py` — 312 controlli sulla build
- `scripts/verifica_config.mjs` — 34 controlli sulla configurazione del pannello
- `scripts/controlla_codifica.py` — validità della codifica dei file
- `scripts/immagini_usate.py` — quali immagini sono referenziate e da quali file
- `scripts/test_microinterazioni.mjs` — 17 controlli sulle transizioni
