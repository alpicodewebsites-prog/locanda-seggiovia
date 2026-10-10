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
| **Sentieri** | gli itinerari escursionistici |

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

## 3. Sostituire le fotografie

Le fotografie attuali sono **segnaposto**, non foto reali. Si riconoscono perché
sono disegni astratti oppure riquadri con la scritta «FOTO IN ARRIVO».

Per sostituirle:

1. Preparare la fotografia in formato **orizzontale**, almeno **1920 pixel** di
   larghezza, in formato `.jpg`.
2. Rinominarla **esattamente** come il file che sostituisce.
3. Copiarla nella cartella **`src/assets/`**, sovrascrivendo il file esistente.

| Nome file | Dove appare | Soggetto ideale |
|---|---|---|
| `hero-piccole-dolomiti.jpg` | apertura della home | le Piccole Dolomiti viste da Recoaro |
| `locanda-facciata.jpg` | sezione «Un rifugio, non un albergo» | la facciata della locanda |
| `sentieri-piccole-dolomiti.jpg` | fascia finale della home | un sentiero o un panorama |
| `camere-interno.jpg` | pagina Camere | una camera rifatta |
| `ristorante-sala.jpg` | pagina Ristorante | la sala del ristorante |
| `gnocchi-fioreta.jpg` | pagina Gnocchi con la Fioreta | il piatto |
| `sentieri-pasubio.jpg` | pagina Sentieri | il Pasubio |
| `territorio-malghe.jpg` | pagina Territorio | una malga |

Tutte le fotografie stanno nella **stessa cartella** (`src/assets/`): non ci sono
copie da aggiornare in altri posti. Il sistema si occupa da solo di ridurle e
converterle nel formato giusto per il web.

**Non** usare fotografie scaricate da internet: servono scatti vostri, o foto di
cui avete i diritti.

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

**Come si aggiunge un nuovo piatto o una nuova camera?**
Dal pannello: apri la sezione, premi **New**, compila i campi e pubblica. Per una
camera nuova servono le tre tariffe; per un piatto basta il nome e la categoria,
il prezzo si può aggiungere dopo.

**Come si aggiunge un nuovo sentiero?**
La sezione **Sentieri** esiste già nel pannello e i sentieri si possono creare da
subito. Le pagine di dettaglio, con la scheda completa di ogni itinerario,
arrivano nella prossima consegna.

**Il modulo di contatto dove manda le email?**
A `locandaseggiovia@gmail.com`. Il modulo è pronto e funzionante nel suo
meccanismo, ma per ricevere davvero i messaggi va inserita la chiave di
Web3Forms: è un'operazione da fare una volta sola, chiedi assistenza.

**Cosa succede se il modulo non funziona?**
Chi scrive vede un messaggio di errore che invita a scrivere direttamente a
`locandaseggiovia@gmail.com`, quindi nessun messaggio va perso in silenzio.
