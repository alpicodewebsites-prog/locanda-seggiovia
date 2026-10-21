# Meteo e webcam nei sentieri

## Il meteo

### Da dove arrivano i dati

[Open-Meteo](https://open-meteo.com/). Si interroga **dal browser** di chi visita,
non da un server: il sito resta statico, non c'è niente da mantenere acceso e non
serve nessuna chiave.

L'alternativa sarebbe stata chiedere il meteo durante la compilazione e scriverlo
nell'HTML. Più semplice, ma il dato invecchierebbe: il sito si ricompila quando
qualcuno modifica un contenuto, non ogni ora. Un meteo di tre giorni fa è peggio
di nessun meteo.

### ⚠️ La licenza: da leggere prima di andare in produzione

Il piano gratuito di Open-Meteo è **per uso non commerciale**. Il sito di una
locanda è un sito commerciale.

Non è un blocco tecnico — funziona lo stesso — ma è un punto da decidere:

| Strada | Costo | Cosa comporta |
|---|---|---|
| Piano gratuito | 0 € | Funziona, ma tecnicamente fuori dai termini |
| Abbonamento Open-Meteo | ~29 €/mese | Tutto in regola, stessa implementazione |
| Togliere il meteo | 0 € | Le schede non lo mostrano: basta svuotare il campo «località» |

**Da decidere con la proprietà.** Se il sito resta una vetrina senza prenotazioni
online, il rischio pratico è basso; se diventa uno strumento commerciale a tutti
gli effetti, l'abbonamento è la strada pulita.

### Dove si misura — e perché è scritto

Il riquadro dichiara sempre **il luogo** accanto ai numeri: «Meteo a Bocchetta
Campiglia», non «il meteo del sentiero».

Il motivo è che un sentiero è lungo chilometri e sale di quota: la temperatura
alla partenza e in vetta possono differire di dieci gradi. Mostrare un solo
numero senza dire dove è stato preso sarebbe stato comodo e falso.

Le coordinate sono quelle del punto di partenza verificato, non del percorso.

### Come si cambia

Nel pannello, scheda del sentiero:

| Campo | Cosa mettere |
|---|---|
| **Meteo, località** | Il nome del posto: «Bocchetta Campiglia» |
| **Meteo, latitudine** | `45.778657` — col punto, non con la virgola |
| **Meteo, longitudine** | `11.227940` |

**Se il campo «località» è vuoto, il meteo non compare.** Non c'è un valore di
riserva: senza sapere dove, il numero non ha senso.

### Cosa succede se non funziona

Se Open-Meteo non risponde entro dieci secondi, o la rete è assente, il riquadro
mostra un messaggio leggibile con il collegamento a un bollettino vero. Non resta
mai un riquadro vuoto o un «Caricamento…» eterno.

I dati restano in memoria per **15 minuti** nella scheda del browser: è il passo
con cui Open-Meteo aggiorna le previsioni, quindi chiedere più spesso non darebbe
un dato più fresco, darebbe solo più richieste.

---

## Le webcam

### Come sono state messe

Il campo **Webcam, indirizzo della pagina** contiene l'indirizzo della **pagina**
della webcam, non dell'immagine.

La scheda del sentiero mostra una scheda cliccabile che rimanda alla fonte, che
apre in una nuova scheda.

### Perché non è l'immagine dentro la pagina

Sarebbe stato più bello, ma tre motivi lo sconsigliano:

1. **L'indirizzo dell'immagine cambia.** I gestori delle webcam riorganizzano i
   file: un collegamento diretto si rompe, e ci si accorge mesi dopo.
2. **Non è pensata per essere incorporata.** Mostrare l'immagine di qualcun altro
   dentro il proprio sito consuma la sua banda e, senza permesso, è scorretto.
3. **Non si può verificare.** Un riquadro con l'immagine rotta è peggio di un
   collegamento che funziona.

### Se si vuole l'immagine dentro il sito

Serve il **codice di incorporamento** dal gestore della webcam (spesso i rifugi o
i consorzi turistici lo forniscono). Con quel codice si aggiunge in un minuto.

**Non inventare indirizzi**: un `<img>` con un indirizzo sbagliato non dà errore,
mostra un riquadro vuoto.

### Webcam attualmente collegate

| Sentiero | Webcam | Fonte |
|---|---|---|
| Anello Storico di Campogrosso | Rifugio Campogrosso | [rifugiocampogrosso.com](https://www.rifugiocampogrosso.com/webcam/) |

---

## I dati dei sentieri: da dove vengono

Le schede sono state verificate sulle pagine outdooractive gestite dal **Comune di
Recoaro Terme** e da **UM.PASUBIO**, entrambi marcati «Partner verificato»:

- [Escursioni a Recoaro Terme](https://www.outdooractive.com/it/escursioni/recoaro-terme/escursioni-a-recoaro-terme/2519741/) — Comune di Recoaro Terme
- [6 Sentiero Italo Soldà](https://www.outdooractive.com/it/route/escursione/vicenza/6-sentiero-italo-solda-/265535981/)
- [Ponte Tibetano Avis](https://www.outdooractive.com/it/route/escursione/trentino/ponte-tibetano-avis-anello-del-sengio-alto/807164021/)
- [Strada delle 52 Gallerie, CAI 366](https://www.outdooractive.com/it/route/escursione/vicenza/strada-delle-52-gallerie-sentiero-cai-366/809413184/)

**Non è stato copiato il testo delle schede**: è protetto. Sono stati presi i
numeri — distanze, dislivelli, durate, quote, coordinate — che sono fatti e non
appartengono a nessuno, e sono state tenute le descrizioni già scritte per il
sito.

### Il nome del sentiero

Si chiama **Sentiero Italo Soldà**, non «Gino». La scheda ufficiale del Comune lo
intitola «6 SENTIERO ITALO SOLDA'», e lo stesso fa il CAI Chioggia.

**Gino Soldà** è l'alpinista recoarese, decorato «Giusto tra le Nazioni»: è una
persona diversa. Il controllo automatico del sito pretendeva «Gino» ed è stato
corretto: per due volte era stato segnalato alla proprietà come se fosse un
refuso, e non lo era.

### Dati ancora da confermare

| Sentiero | Cosa manca |
|---|---|
| Sentiero delle Mole | Coordinate del Rifugio La Guardia: il meteo usa quelle del Passo Pian delle Fugazze, l'unico punto verificato della zona |
| Anello Storico di Campogrosso | Distanza («circa 10 km») e dislivello (300 m) non trovati su fonte ufficiale |
| 6 Sentiero Italo Soldà | Il numero «CAI 133» non è confermato dalle schede del Comune, che lo indicano come percorso «6» |
