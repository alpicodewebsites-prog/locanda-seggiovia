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

Apri l'indirizzo del sito seguito da `/admin`, per esempio:

```
https://locandaseggiovia.vercel.app/admin
```

Accedi con l'account GitHub che ha accesso al progetto. Da lì trovi quattro sezioni:

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

### Come sostituirle

1. Preparare la fotografia **orizzontale**, almeno **1600 pixel** di larghezza.
2. Rinominarla **esattamente** come il file che sostituisce.
3. Copiarla nella cartella **`src/assets/`**, sovrascrivendo il file esistente.

| Nome file | Dove appare |
|---|---|
| `hero-piccole-dolomiti.jpg` | apertura della home |
| `camere-interno.jpg` | pagina Camere |
| `ristorante-sala.jpg` | pagina Ristorante |
| `gnocchi-fioreta.jpg` | pagina Gnocchi con la Fioreta |
| `sentieri-grandi-alberi.jpg` | scheda del sentiero |
| `sentieri-campogrosso.jpg` | scheda del sentiero |
| `sentieri-ponte-tibetano.jpg` | scheda del sentiero |
| `sentieri-52-gallerie.jpg` | scheda del sentiero |
| `sentieri-mole.jpg` | scheda del sentiero |
| `sentieri-gino-solda.jpg` | scheda del sentiero |

Tutte le fotografie stanno nella **stessa cartella** (`src/assets/`): non ci sono
copie da aggiornare in altri posti. Il sistema si occupa da solo di ridurle e
converterle nel formato giusto per il web.

**Non** usare fotografie scaricate da internet: servono scatti vostri, o foto di
cui avete i diritti.

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
