# Locanda Seggiovia — guida per chi gestisce il sito

Questa guida è pensata per chi **non** ha competenze tecniche.
Descrive come modificare i contenuti del sito e come pubblicare le modifiche.

---

## 1. Come funziona, in due righe

Il sito è una raccolta di file di testo e immagini. Ogni volta che modifichi un
contenuto, il sito si **ricostruisce da solo** e diventa visibile online dopo
circa un minuto. Non c'è niente da installare e niente da aggiornare.

Ci sono due modi per modificare i contenuti:

| Modo | Quando usarlo | Serve saper programmare? |
|---|---|---|
| **Pannello di amministrazione** (`/admin`) | modifiche di tutti i giorni: menù, prezzi, tariffe, descrizioni | No |
| Modifica diretta dei file | solo per telefono, orari e dati fiscali | Un po' |

> **Il pannello `/admin` si attiva dopo il collegamento a GitHub.** Fino a quel
> momento le modifiche si fanno sui file. La procedura è descritta nella
> documentazione tecnica.

---

## 2. Modificare i contenuti dal pannello

Apri questo indirizzo nel browser:

```
https://locanda-seggiovia.vercel.app/admin
```

> ⚠️ **Attenzione al trattino.** L'indirizzo ha un trattino fra «locanda» e
> «seggiovia»: `locanda-seggiovia.vercel.app`. Se lo dimentichi, il browser
> risponde che la pagina non esiste — non è un guasto, è solo l'indirizzo
> sbagliato.

Compare la schermata di accesso con un solo pulsante, **«Sign In with Token»**.
Incolla il token che ti è stato consegnato e premi conferma. **Va fatto una volta
sola**: da quel momento il pannello ti riconosce e non te lo chiede più.

Da lì trovi quattro sezioni:

| Sezione | Cosa contiene |
|---|---|
| **Camere e tariffe** | i tipi di camera, le tre tariffe, i servizi in camera |
| **Menù del ristorante** | i piatti, divisi per antipasti, primi, secondi, dolci |
| **Gnocchi con la Fioreta** | la pagina del piatto: storia, ricetta, lavorazione, condimento |
| **Sentieri** | i sei itinerari, con dati tecnici e difficoltà CAI |

Apri la voce che ti interessa, modifica quello che serve e premi **Publish**.
Dopo circa un minuto le modifiche sono online.

### Tre cose da sapere

**Se un'informazione non la conosci, lascia il campo vuoto.** Il sito è
costruito per non mostrare i campi vuoti. Scrivere un prezzo a caso è peggio che
non scriverlo: chi prenota si aspetta che sia quello vero.

**I prezzi del menù possono restare vuoti.** In quel caso il piatto compare
senza cifra, e la pagina avvisa che i prezzi si chiedono in locanda. Quando li
avrai, compilali e compariranno da soli.

**Il numero di telefono e la partita IVA non sono nel pannello.** Sono dati
della struttura, non contenuti: si cambiano dal file `src/data/site.ts`
(vedi §4). Chiedi assistenza la prima volta.

---

## 3. Modificare i dati della struttura (telefono, orari, indirizzo)

Tutto quello che riguarda la struttura è raccolto in un unico file:

**`src/data/site.ts`**

Qui si trovano telefono, email, indirizzo, orari, partita IVA e i link.
Aprendo il file si legge subito cosa cambiare: ogni riga ha un'etichetta chiara.

Esempio — cambiare il numero di telefono:

```ts
  telefono: '+39 0445 123456',
  telefonoLink: 'tel:+390445123456',
```

⚠️ **Attenzione**: il numero va scritto **due volte**, in due formati diversi.

- `telefono` è come appare sullo schermo: `+39 0445 123456`
- `telefonoLink` è la versione che il telefono compone: `tel:+390445123456`
  (senza spazi, senza parentesi)

### I campi da riempire prima della pubblicazione

Nel file ci sono alcuni valori **segnaposto**, scritti come `000`. Vanno
sostituiti con i dati reali:

- `telefono` e `telefonoLink`
- `fiscale.partitaIva` e `fiscale.codiceFiscale`
- `orari` (gli orari di ristorante e reception)
- `annoFondazione` — l'anno in cui è nata la locanda; finché è vuoto il titolo
  della home non lo cita
- `instagram` — l'indirizzo del profilo; il link compare solo se compilato

---

## 3. Le fotografie

Sul sito sono già installate le fotografie che hai fornito: la facciata della
locanda, le montagne, il tavolo di cucina con gli ingredienti, i due piatti e il
logo nel footer.

**Le foto che hai dato sono piccole** (la più grande è 600×450 pixel). Vanno
bene dove sono adesso, ma non si possono ingrandire: se le ingrandisci si
vedono sfocate. Per questo **l'immagine di apertura della home è ancora un
segnaposto**: serve uno scatto di almeno 2500 pixel di larghezza.

### Cosa serve ancora

| Serve una foto di | Dove andrà | Requisito |
|---|---|---|
| Le Piccole Dolomiti o un sentiero | apertura della home | almeno 2500 px di larghezza |
| Le camere | pagina Camere | orizzontale, almeno 1600 px |
| La sala del ristorante | pagina Ristorante | orizzontale, almeno 1600 px |
| I sentieri (6 foto) | schede dei sentieri | orizzontale, almeno 1600 px |

Finché non arrivano, al loro posto ci sono riquadri neutri con la scritta
«FOTO IN ARRIVO»: si vede subito che è un segnaposto e non una foto sbagliata.

### Come vedere dove appare una fotografia

Nella libreria, **clicca una fotografia** e poi l'icona **`i`** (l'ultima a
destra, accanto alle icone per cambiare la vista). Si apre il pannello **Info**,
che contiene l'elenco **«Used in»**: lì è scritto in quali contenuti e in quali
campi quella fotografia viene usata.

È il modo più rapido per rispondere alla domanda «questa foto dove finisce?».

### Dove appare ogni fotografia

Il pannello è diviso in due gruppi. Le **pagine** stanno in alto, le **schede**
(elenchi) in basso.

Nelle pagine, ogni campo dice già a cosa serve:

| Voce del pannello | Campo | Dove si vede |
|---|---|---|
| **Home Page** | Fotografia 1 — Apertura | la prima schermata del sito |
| **Home Page** | Fotografia 2 — Fascia panoramica | la fascia a tutta larghezza della home |
| **Home Page** | Fotografia 3 — Le montagne | la sezione Territorio della home |
| **Home Page** | Fotografia 4 — La locanda vista da fuori | la sezione «La locanda» della home |
| **Pagina La Locanda** | La locanda vista da fuori | la pagina La Locanda |
| **Pagina La Locanda** | Il tavolo di cucina | la pagina La Locanda |
| **Pagina Sentieri** | Le montagne, Panorama | la pagina con l'elenco dei sentieri |

> **La facciata compare in due posti diversi, e sono due campi separati.** Puoi
> mettere la stessa fotografia in entrambi, oppure due scatti diversi — per
> esempio uno d'estate sulla home e uno d'inverno nella pagina La Locanda.
> Cambiando uno **non** cambia l'altro: è voluto, così decidi tu.

Le altre si cambiano **dentro la scheda a cui appartengono**:

| Dove | Cosa cambia |
|---|---|
| Camere (elenco) → una camera | la foto di quella camera |
| Menù del ristorante → un piatto | la foto di quel piatto |
| Gnocchi con la Fioreta | la foto del piatto finito e quella degli ingredienti |
| Sentieri (elenco) → un sentiero | la foto di copertina di quel percorso |

### Dove finiscono le fotografie che carichi

Ogni sezione ha la **sua cartella**. Caricando una fotografia mentre sei dentro
una sezione, finisce lì e non si mescola con le altre:

| Sezione | Cartella |
|---|---|
| Home Page | `src/assets/home/` |
| Pagina La Locanda | `src/assets/la-locanda/` |
| Pagina Sentieri e Sentieri (elenco) | `src/assets/sentieri/` |
| Gnocchi con la Fioreta | `src/assets/gnocchi/` |
| Camere (elenco) | `src/assets/camere/` |
| Menù del ristorante | `src/assets/ristorante/piatti/` |

Aprendo il selettore di un campo vedi **prima** i file di quella sezione. Se ti
serve riusare una foto già caricata altrove, la trovi nelle altre schede del
selettore.

### Come sostituire una fotografia

Non c'è un pulsante «sostituisci»: si fa **caricando un file con lo stesso nome e
nello stesso formato** di quello da cambiare.

1. Guarda il nome e il formato della fotografia da cambiare: per esempio
   `hero.jpg` è un **.jpg**.
2. Prepara la fotografia nuova e **rinominala esattamente come quella vecchia**,
   **mantenendo lo stesso formato** (`hero.jpg`).
3. Nel pannello apri il **campo della fotografia** e premi **Carica**.
4. Scegli il file. Il sistema avverte che esiste già un file con quel nome:
   **conferma**.
5. Il vecchio viene sostituito, e **tutti i punti del sito dove compariva si
   aggiornano da soli**.

Il motivo è che i contenuti non contengono la fotografia, ma il suo **nome**: se
il nome resta lo stesso, il sito la ritrova ovunque.

> ⚠️ **Il formato deve essere lo stesso.** Se provi a sostituire un `.jpg` con un
> file `.webp` (o viceversa), il pannello rifiuta e dice:
> *«Questo file non può sostituire … perché è in un formato diverso»*.
>
> **Non è un guasto**: cambiando formato cambierebbe anche il nome del file, e il
> sito perderebbe il collegamento alla fotografia. Il pannello ti sta proteggendo
> da un'immagine che sparirebbe.

**Se il tuo file ha un formato diverso da quello da sostituire**, ci sono due
strade. La prima è la più semplice:

**Converti il file nello stesso formato.** Su Windows: apri la fotografia con
**Paint** → *File* → *Salva con nome* → in *Tipo* scegli **JPEG** → salva con lo
stesso nome. Su Mac: apri con **Anteprima** → *File* → *Esporta* → formato
**JPEG**.

Oppure, se preferisci non convertire niente:

1. Nella libreria, **elimina** la fotografia vecchia (il sistema sistema da solo
   i collegamenti).
2. **Carica** la nuova, con il nome che vuoi.
3. Apri la scheda dove deve comparire e scegli la nuova fotografia dal campo.

È un passaggio in più, ma funziona sempre.

### Caricare una fotografia nuova

1. Nel pannello apri la scheda dove deve comparire (per esempio **Camere e
   tariffe** → una camera).
2. Nel campo della fotografia premi **Scegli immagine**.
3. Nella finestra che si apre, trascina il file oppure premi **Carica** e
   scegliilo dal computer.
4. Salva.

La fotografia finisce nella libreria e resta disponibile per tutti gli altri
campi: non va caricata due volte.

### Togliere una fotografia (senza perdere il campo)

Il campo **non sparisce mai**: resta lì, vuoto, pronto a ricevere una fotografia
nuova. È il modo giusto di togliere una foto da una pagina.

1. Apri la pagina (per esempio **Home Page**).
2. Vai al campo della fotografia che vuoi togliere.
3. Passa il puntatore sull'anteprima della foto e premi la **×** per toglierla.
4. Salva.

Da quel momento la pagina **non mostra più quella fotografia**, e al suo posto
non compare un riquadro rotto: la sezione si riordina da sola.

Per rimetterne una, riapri lo stesso campo e carica il file. **Il campo è ancora
lì, nello stesso punto**: non devi ricreare niente.

> **Se il campo fosse vuoto perché hai svuotato la pagina sbagliata**, non
> succede nulla di irreparabile: le fotografie restano nella cartella della
> sezione e le ritrovi nel selettore.

### Eliminare una fotografia dal disco

Diverso dal punto sopra: qui il file viene **cancellato davvero**.

1. Apri il campo di una fotografia e apri il selettore.
2. Passa il puntatore sulla fotografia e premi **Elimina**.
3. Il sistema avvisa **in quanti punti del sito** quella fotografia è usata, e
   sistema da solo i collegamenti: dove compariva, il campo resta vuoto invece di
   puntare a un file che non c'è più.
4. Conferma.

> **Non puoi sbagliare**: ogni modifica è registrata, e si può sempre tornare
> indietro. Se elimini una fotografia per errore, scrivi e la recuperiamo.

> **Attenzione a una sola cosa.** Se elimini il file **e** il campo continua a
> contenere il suo percorso, il campo punta a un file che non esiste più: la
> pagina resta senza fotografia finché non ne carichi una nuova. Il pannello
> avvisa in quanti punti è usata proprio per questo. Nel dubbio, usa il metodo
> qui sopra (svuotare il campo), che è sempre sicuro.

### Che caratteristiche devono avere

| | |
|---|---|
| **Formato** | `.jpg` per le fotografie, `.png` solo se serve lo sfondo trasparente (il logo) |
| **Orientamento** | orizzontale, tranne il logo |
| **Larghezza consigliata** | **almeno 1920 pixel** — **2500** per l'apertura della home |
| **Peso** | fino a **8 MB** |

**Puoi caricare la fotografia così come esce dalla macchina fotografica.** Non
serve ridimensionarla: **il sito la alleggerisce da solo in fase di
pubblicazione**, producendo il formato WebP e le versioni di dimensione adatta a
telefoni, tablet e schermi grandi.

> **Perché non la converte il pannello, allora?** Perché abbiamo provato, e
> bloccava la sostituzione delle fotografie: se il pannello converte in WebP
> mentre carichi, poi non riesce più a mettere il file al posto di un `.jpg`
> esistente — i formati non corrispondono. Meglio un file un po' più pesante nel
> magazzino e la possibilità di cambiare le foto quando vuoi.

> ⚠️ **Una fotografia piccola non viene ingrandita.** Se carichi un'immagine di
> 600 pixel di larghezza, resta di 600 pixel: il sito non può inventare i
> dettagli che non ci sono, e ingrandirla la farebbe sembrare sfocata. Per
> questo, quando possibile, usa lo scatto originale e non una copia ridotta.

**Non** usare fotografie scaricate da internet: servono scatti vostri, o foto di
cui avete i diritti.

### 📷 Servono tre fotografie, e sono le più importanti

Il sito oggi funziona, ma **le fotografie sono la cosa che fa la differenza** fra
un sito che sembra vero e uno che sembra vuoto. Al momento le immagini mancanti
sono riquadri dichiarati «FOTO IN ARRIVO»: si vede che sono provvisori.

**Queste tre cambierebbero tutto, in quest'ordine:**

| # | Fotografia | Dove va | Come deve essere |
|---|---|---|---|
| 1 | **Le Piccole Dolomiti, o un sentiero** | la prima schermata della home | almeno **2500 px** di larghezza |
| 2 | **Le camere** | pagina Camere | almeno **1600 px**, orizzontale |
| 3 | **La sala del ristorante** | pagina Ristorante | almeno **1600 px**, orizzontale |

La numero 1 è la più importante di tutte: è **la prima cosa che si vede** aprendo
il sito. Oggi lì c'è un disegno, non una fotografia delle vostre montagne.

Bastano anche scatti fatti con il telefono, purché siano **orizzontali** e alla
massima risoluzione. Le fotografie verticali dei telefoni vanno bene per le
camere, non per l'apertura.

### Il logo

Il logo è nel footer, con lo sfondo bianco reso trasparente. La versione che
abbiamo è piccola (281 pixel): se ne esiste una **vettoriale** (file `.svg`,
`.ai` o `.eps`) o una versione molto più grande, vale la pena sostituirla — sul
footer si nota.

---

## 4. Cosa significano le sigle dei sentieri

Nella sezione Territorio compaiono delle sigle. Sono la classificazione
ufficiale del CAI (Club Alpino Italiano):

| Sigla | Significato | Per chi è |
|---|---|---|
| **T** | Turistico | sentieri facili, anche per famiglie |
| **E** | Escursionistico | serve un minimo di allenamento |
| **EE** | Escursionisti Esperti | terreno impervio, attrezzatura adeguata |

---

## 5. Pubblicare le modifiche

1. Aprire il pannello `/admin`, oppure modificare i file.
2. Salvare. Se si usa il pannello, premere **Publish**.
3. Attendere circa un minuto.
4. Ricaricare il sito per vedere le modifiche.

Se qualcosa non appare subito, ricaricare la pagina con **Ctrl + F5**
(Windows) o **Cmd + Shift + R** (Mac): svuota la copia salvata nel browser.

### Se qualcosa va storto

Il sito tiene uno storico di tutte le modifiche. Una modifica sbagliata si può
sempre annullare tornando alla versione precedente: **niente è irreversibile**.
In caso di dubbio, non toccare altro e chiedere assistenza.

---

## 6. Domande frequenti

**Il sito è lento da modificare?**
No. Si salva e dopo circa un minuto è online. Non serve ricostruire nulla a mano.

**Si può rompere il sito?**
Le modifiche ai testi e alle immagini sono sempre reversibili. Le uniche
operazioni delicate sono rinominare i file e modificare le cartelle.

**Serve un abbonamento?**
No. L'unico costo ricorrente è il dominio (circa 15–20 € all'anno). Hosting,
pannello di amministrazione e certificato HTTPS sono gratuiti.

**Come si aggiunge un nuovo sentiero?**
Dal pannello, sezione **Sentieri**: premi **New**, compila nome, sommario,
descrizione, difficoltà e i dati tecnici che conosci, poi pubblica. La scheda si
crea da sola e compare subito nell'elenco. **Compila solo i dati che conosci**:
i campi vuoti non vengono mostrati, mentre un dato sbagliato resta sbagliato.

**Come si aggiunge un nuovo piatto o una nuova camera?**
Dal pannello: apri la sezione, premi **New**, compila i campi e pubblica. Per una
camera nuova servono le tre tariffe; per un piatto basta il nome e la categoria,
il prezzo si può aggiungere dopo.

**Il modulo di contatto dove manda le email?**
A `locandaseggiovia@gmail.com`. Il modulo è pronto e funzionante nel suo
meccanismo, ma per ricevere davvero i messaggi va inserita la chiave di
Web3Forms: è un'operazione da fare una volta sola, chiedi assistenza.

**Cosa succede se il modulo non funziona?**
Chi scrive vede un messaggio di errore che invita a scrivere direttamente a
`locandaseggiovia@gmail.com`, quindi nessun messaggio va perso in silenzio.

**Perché la mappa non si vede subito?**
Perché il sito non vuole caricare i cookie di Google senza che l'utente lo
decida. C'è un pulsante «Carica la mappa»: chi lo preme vede la mappa, chi non
lo preme non riceve cookie di terze parti. È il motivo per cui il sito non ha
quei banner fastidiosi da accettare a ogni visita.

**Il sito raccoglie statistiche sulle visite?**
No. Non ci sono analytics e non ci sono cookie di profilazione. L'unico cookie
possibile è quello di Google Maps, e solo se l'utente decide di caricare la mappa.
