/**
 * I testi scritti dentro le pagine, uno per lingua.
 *
 * ----------------------------------------------------------------------------
 * PERCHÉ UN FILE SEPARATO DA `ui.ts`
 *
 * `ui.ts` contiene l'interfaccia condivisa: voci di menu, pulsanti, etichette
 * che compaiono in più pagine. Qui invece sta la copia di una singola pagina —
 * titoli, paragrafi, didascalie — che non serve a nessun'altra.
 *
 * Tenerle separate evita che il file dell'interfaccia diventi un elenco di
 * centinaia di voci in cui non si trova più niente. La regola per scegliere:
 * se il testo compare in due pagine, va in `ui.ts`; se è di una sola, sta qui.
 *
 * Quello che modifica la cliente (storia, piatti, sentieri) non sta né qui né
 * lì: sta nelle collezioni, e si modifica dal pannello.
 * ----------------------------------------------------------------------------
 */
import type { Lingua } from './index';

export interface TestiPagine {
  locanda: {
    metaTitolo: string;
    metaDescrizione: string;
    etichetta: string;
    titolo: string;
    lede: string;
    altCucina: string;
    didascaliaCucina: string;
    /** «La famiglia Asnicar Bertoldi» / «The Asnicar Bertoldi family». */
    titoloFamiglia: string;
    paragrafiFamiglia: string[];
    etichettaCarattere: string;
    titoloCarattere: string;
    carattere: string[];
    altFacciata: string;
    etichettaCasa: string;
    titoloCasa: string;
    paragrafiCasa: string[];
    notaFoto: string;
    titoloDove: string;
    testoDove: string;
    apriMappa: string;
    voci: {
      indirizzo: string;
      altitudine: string;
      gruppi: string;
      camere: string;
      ristorante: string;
    };
    altitudine: string;
    gruppi: string;
    camereLink: string;
    ristoranteLink: string;
    titoloChiusura: string;
    testoChiusura: string;
    pulsanteCamere: string;
    pulsanteContatti: string;
  };
  cookie: {
    metaTitolo: string;
    metaDescrizione: string;
    etichetta: string;
    titolo: string;
    lede: string;
    titoloElenco: string;
    captionTabella: string;
    tabella: { voce: string; tipo: string; durata: string };
    elenco: { nome: string; tipo: string; durata: string; nota: string }[];
    notaElenco: string;
    titoloGestione: string;
    testoGestione: string;
    titoloBanner: string;
    /** Il testo del banner si spezza per la parola in corsivo. */
    testoBannerPrima: string;
    testoBannerCorsivo: string;
    testoBannerDopo: string;
    linkPrivacy: string;
    linkContatti: string;
    notaPrevalenza: string;
  };
  privacy: {
    metaTitolo: string;
    metaDescrizione: string;
    etichetta: string;
    titolo: string;
    lede: string;
    avvisoTitolo: string;
    avvisoTesto: string;
    titoloTitolare: string;
    vociTitolare: {
      ragioneSociale: string;
      partitaIva: string;
      sedeLegale: string;
      recapito: string;
      titolare: string;
    };
    daConfermare: string;
    titoloTrattamenti: string;
    campi: {
      finalita: string;
      dati: string;
      base: string;
      conservazione: string;
      destinatari: string;
    };
    trattamenti: {
      nome: string;
      finalita: string;
      dati: string;
      base: string;
      conservazione: string;
      destinatari: string;
    }[];
    titoloDiritti: string;
    /** Il testo si spezza per inserire il collegamento all'email. */
    testoDirittiPrima: string;
    testoDirittiDopo: string;
    testoGarantePrima: string;
    testoGaranteDopo: string;
    titoloTrasferimenti: string;
    testoTrasferimenti: string;
    titoloModifiche: string;
    testoModifiche: string;
    linkCookie: string;
    /** Chi prevale se le due versioni dicono cose diverse. */
    notaPrevalenza: string;
  };
  contatti: {
    metaTitolo: string;
    metaDescrizione: string;
    etichetta: string;
    titolo: string;
    lede: string;
    avvisoDemoTitolo: string;
    avvisoDemoTesto: string;
    nome: string;
    email: string;
    telefono: string;
    telefonoAiuto: string;
    messaggio: string;
    placeholderNome: string;
    placeholderEmail: string;
    placeholderTelefono: string;
    placeholderMessaggio: string;
    consenso: string;
    invia: string;
    campiObbligatori: string;
    recaptcha: string;
    titoloRecapiti: string;
    etichettaTelefono: string;
    etichettaEmail: string;
    etichettaOrari: string;
    notaOrari: string;
    titoloMappa: string;
    notaMappa: string;
    caricaMappa: string;
    apriMaps: string;
  };
  ristorante: {
    metaTitolo: string;
    metaDescrizione: string;
    etichetta: string;
    titolo: string;
    lede: string;
    altSala: string;
    segnapostoTitolo: string;
    segnapostoSoggetto: string;
    etichettaSpecialita: string;
    titoloSpecialita: string;
    testoSpecialita: string;
    linkRicettaGnocchi: string;
    titoloMenu: string;
    testoMenu: string;
    notaPrezzi: string;
    /** Le quattro categorie, nell'ordine in cui si mangiano. */
    categorie: { antipasti: string; primi: string; secondi: string; dolci: string };
    titoloOrari: string;
    testoOrari: string;
    pulsantePrenota: string;
  };
  gnocchi: {
    metaTitolo: string;
    metaDescrizione: string;
    etichetta: string;
    altPiatto: string;
    titoloStoria: string;
    etichettaRicetta: string;
    titoloRicetta: string;
    testoRicetta: string;
    altIngredienti: string;
    didascaliaIngredienti: string;
    titoloLavorazione: string;
    titoloCondimento: string;
    riconoscimenti: string;
    pulsanteRistorante: string;
    pulsantePrenota: string;
    /** Come si compone un ingrediente per i dati strutturati. */
    ingredienteSchema: string;
    categoriaSchema: string;
    cucinaSchema: string;
    paroleChiaveSchema: string;
  };
  sentiero: {
    /** «{nome} — Sentieri». */
    titoloDocumento: string;
    altCopertina: string;
    briciola: string;
    etichettaDati: string;
    notaDati: string;
    titoloPercorso: string;
    titoloCondizioni: string;
    webcamVoce: string;
    webcamDefault: string;
    webcamNota: string;
    titoloChiusura: string;
    testoChiusura: string;
    pulsanteScrivici: string;
    pulsanteCamere: string;
  };
  sentieriPagina: {
    metaTitolo: string;
    metaDescrizione: string;
    etichetta: string;
    titolo: string;
    lede: string;
    etichettaElenco: string;
    etichettaDifficolta: string;
    titoloScala: string;
    testoScala: string;
    scala: { sigla: string; nome: string; nota: string }[];
    altMontagne: string;
    didascaliaMontagne: string;
    etichettaTerritorio: string;
    titoloMontagna: string;
    testoMontagna: string;
    linkConsiglio: string;
    altPanorama: string;
    titoloChiusura: string;
    testoChiusura: string;
    pulsanteCamere: string;
    pulsanteInfo: string;
  };
  camere: {
    metaTitolo: string;
    metaDescrizione: string;
    etichetta: string;
    titolo: string;
    titoloCamere: string;
    /** Testo alternativo: «La camera singola della Locanda Seggiovia». */
    altCamera: string;
    segnapostoAlt: string;
    segnapostoTitolo: string;
    notaColazione: string;
    etichettaPrezzi: string;
    titoloTariffe: string;
    ledeTariffe: string;
    tabella: { camera: string; bnb: string; mezzaPensione: string; pensioneCompleta: string };
    captionTabella: string;
    doppiaUsoSingola: string;
    supplemento: string;
    /** «+ 15 € / giorno». */
    valoreSupplemento: string;
    notaTariffe: string;
    prenotazioneTitolo: string;
    prenotazioneDescrizione: string;
    etichettaRegole: string;
    titoloRegole: string;
    testoRegole: string;
    politiche: {
      bambini03: string;
      bambini410: string;
      animali: string;
      soggiornoMinimo: string;
      doppiaUsoSingola: string;
    };
    valori: {
      gratuiti: string;
      sconto30: string;
      animali: string;
      soggiorno: string;
      supplementoDus: string;
    };
    chiusuraTitolo: string;
    chiusuraTesto: string;
    pulsanteScrivici: string;
  };
  home: {
    /** Titolo per i lettori di schermo del carosello. */
    titoloCarosello: string;
    /** Il verbo del collegamento sotto ogni diapositiva. */
    invitoCarosello: string;
    precedente: string;
    successiva: string;
    altFacciata: string;
    etichettaCucina: string;
    titoloCucina: string;
    testoCucina: string;
    linkRistorante: string;
    /** Invito nelle schede delle specialità. */
    invitoGnocchi: string;
    invitoPiatto: string;
    titoloLegenda: string;
    testoLegenda: string;
    legenda: { sigla: string; nome: string; nota: string }[];
    pulsanteTuttiSentieri: string;
    titoloChiusura: string;
    testoChiusura: string;
    pulsanteScrivici: string;
  };
}

const IT: TestiPagine = {
  locanda: {
    metaTitolo: 'La Locanda — storia e famiglia',
    metaDescrizione:
      'La Locanda Seggiovia a Recoaro Terme: una casa di pietra e legno in piazza, gestita dalla famiglia Asnicar Bertoldi, ai piedi delle Piccole Dolomiti.',
    etichetta: 'La Locanda',
    titolo: 'Una casa di pietra in piazza, ai piedi delle Piccole Dolomiti',
    lede:
      'La Locanda Seggiovia non è nata come albergo e non lo è diventata. È la casa di una famiglia che ha scelto di restare in montagna e di aprirla a chi la montagna la viene a cercare.',
    altCucina:
      'Il tavolo di lavoro della cucina con la fioreta, la farina e il burro di malga',
    didascaliaCucina: 'Il tavolo di cucina: la fioreta, la farina e il burro di malga.',
    titoloFamiglia: 'La famiglia {cognome}',
    paragrafiFamiglia: [
      'La locanda la portano {gestori}. Non è una gestione delegata: chi cucina, chi accoglie e chi consiglia il sentiero sono le stesse persone che vivono qui tutto l’anno. È la differenza che si sente appena si varca la porta.',
      'Recoaro Terme è un paese di fondovalle che nel Novecento è stato terme e industria, e che oggi vive soprattutto di montagna. Restare qui, e tenere aperta una locanda in piazza, è una scelta precisa: significa credere che il turismo di queste valli sia quello di chi cammina, non quello di chi passa.',
      'Da quella scelta viene tutto il resto. Si conoscono i sentieri perché si percorrono, si conoscono le malghe perché ci si compra il formaggio, e la cucina segue le stagioni di quello che le malghe hanno da offrire.',
    ],
    etichettaCarattere: 'Il carattere della casa',
    titoloCarattere: 'Perché diciamo rifugio e non albergo',
    carattere: [
      'Chi sale qui per camminare lascia l’auto in piazza e comincia a camminare: i sentieri partono dal paese, non da un parcheggio.',
      'La mattina la colazione è pronta prima dell’alba, perché chi va in montagna parte presto — e sa già che cosa lo aspetta, visto che i sentieri li conosciamo uno per uno.',
      'La sera si torna affamati, e la cucina è quella di casa: non un servizio in più, ma il motivo per cui molti tornano.',
    ],
    altFacciata:
      'La facciata della Locanda Seggiovia con i balconi in legno, nel centro di Recoaro Terme',
    etichettaCasa: 'La casa',
    titoloCasa: 'Pietra, legno e una piazza davanti',
    paragrafiCasa: [
      'L’edificio è in piazza, con i balconi in legno che guardano le Piccole Dolomiti. Le camere sono ai piani, il ristorante al piano terra: si entra dalla porta e si è già dentro la giornata.',
    ],
    notaFoto:
      'Altre fotografie degli interni sono in arrivo: gli ambienti sono in fase di ristrutturazione.',
    titoloDove: 'In piazza, nel centro del paese',
    testoDove:
      'Recoaro Terme sta in Valle dell’Agno, ai piedi delle Piccole Dolomiti e del Gruppo del Pasubio. La locanda è in piazza, a due passi dalle fonti e dal punto da cui partono i sentieri.',
    apriMappa: 'Apri la mappa',
    voci: {
      indirizzo: 'Indirizzo',
      altitudine: 'Altitudine',
      gruppi: 'Gruppi montuosi',
      camere: 'Camere',
      ristorante: 'Ristorante',
    },
    altitudine: 'circa 450 m s.l.m.',
    gruppi: 'Piccole Dolomiti, Pasubio, Carega',
    camereLink: 'Singole e doppie',
    ristoranteLink: 'Cucina alto-vicentina',
    titoloChiusura: 'Vieni a vedere',
    testoChiusura:
      'Le camere sono semplici e curate, il ristorante è aperto a pranzo e a cena. Scrivici e ti diciamo tutto quello che serve.',
    pulsanteCamere: 'Le camere',
    pulsanteContatti: 'Contatti',
  },
  cookie: {
    metaTitolo: 'Cookie Policy',
    metaDescrizione:
      'Cookie Policy del sito della Locanda Seggiovia: il sito non imposta cookie prima di un’azione dell’utente, e la mappa di Google si carica solo su richiesta.',
    etichetta: 'Informativa',
    titolo: 'Cookie Policy',
    lede:
      'Questo sito non ti chiede di accettare cookie che non usa. Ecco esattamente cosa viene impostato e quando.',
    titoloElenco: 'Cosa viene impostato, in concreto',
    captionTabella: 'Elenco dei cookie e delle memorizzazioni tecniche del sito',
    tabella: { voce: 'Voce', tipo: 'Tipo', durata: 'Durata' },
    elenco: [
      {
        nome: 'Cookie tecnici propri',
        tipo: 'Nessuno',
        durata: '—',
        nota: 'Il sito non imposta cookie propri: non ci sono sessioni, carrelli o preferenze da ricordare.',
      },
      {
        nome: 'Cookie di Google Maps',
        tipo: 'Di terze parti',
        durata: 'Stabilita da Google',
        nota:
          'Vengono impostati solo dopo che l’utente ha premuto «Carica la mappa» nella pagina Contatti. Se non si preme il pulsante, nessun cookie di Google viene impostato.',
      },
      {
        nome: 'Cookie di reCAPTCHA (Google)',
        tipo: 'Di terze parti',
        durata: 'Stabilita da Google',
        nota:
          'Presenti solo se è attiva la verifica reCAPTCHA sul modulo di contatto. Al momento l’opzione è disattivata, quindi questi cookie non vengono impostati.',
      },
      {
        nome: 'Log tecnici dell’hosting',
        tipo: 'Non sono cookie',
        durata: 'Breve periodo',
        nota:
          'Il fornitore di hosting registra indirizzo IP e richieste per sicurezza e diagnostica. Non sono cookie e non servono a profilare.',
      },
    ],
    notaElenco:
      'L’elenco è aggiornato alla data di pubblicazione e viene rivisto quando cambia qualcosa nel sito. Se in futuro venisse attivato uno strumento di statistica, verrebbe indicato qui e il sito chiederebbe il consenso prima di attivarlo.',
    titoloGestione: 'Come gestirli dal browser',
    testoGestione:
      'Puoi bloccare o cancellare i cookie dalle impostazioni del tuo browser. Bloccare i cookie di terze parti non impedisce di usare questo sito: l’unica cosa che non funzionerebbe è la mappa incorporata, che puoi comunque aprire in una nuova scheda.',
    titoloBanner: 'Perché non c’è un banner',
    testoBannerPrima:
      'Il banner serve quando un sito imposta cookie non necessari',
    testoBannerCorsivo: 'prima',
    testoBannerDopo:
      'che l’utente acconsenta. Qui non accade: la mappa di Google si carica solo dopo un clic, e non ci sono altri script di terze parti. Senza cookie da autorizzare, un banner sarebbe solo un ostacolo in più.',
    linkPrivacy: 'Leggi la Privacy Policy',
    linkContatti: 'Contatti',
    notaPrevalenza:
      'Questa è la traduzione inglese della cookie policy. In caso di divergenza fa fede la versione italiana.',
  },
  privacy: {
    metaTitolo: 'Privacy Policy',
    metaDescrizione:
      'Informativa sul trattamento dei dati personali del sito della Locanda Seggiovia: quali dati raccogliamo, perché, per quanto tempo e come esercitare i tuoi diritti.',
    etichetta: 'Informativa',
    titolo: 'Privacy Policy',
    lede:
      'Questa pagina spiega quali dati personali raccoglie il sito, perché li raccoglie e che fine fanno. È scritta per essere letta, non per essere saltata.',
    avvisoTitolo: 'Documento in fase di completamento.',
    avvisoTesto:
      'Il testo descrive correttamente come il sito tratta i dati, ma i dati societari contrassegnati come «da confermare» devono essere verificati con la proprietaria prima della pubblicazione.',
    titoloTitolare: 'Titolare del trattamento',
    vociTitolare: {
      ragioneSociale: 'Ragione sociale completa',
      partitaIva: 'Partita IVA / Codice fiscale',
      sedeLegale: 'Sede legale',
      recapito: 'Recapito per la privacy',
      titolare: 'Titolare del trattamento',
    },
    daConfermare: '(da confermare)',
    titoloTrattamenti: 'Quali dati trattiamo e perché',
    campi: {
      finalita: 'Finalità',
      dati: 'Dati raccolti',
      base: 'Base giuridica',
      conservazione: 'Conservazione',
      destinatari: 'Destinatari',
    },
    trattamenti: [
      {
        nome: 'Modulo di contatto',
        finalita: 'Rispondere alla richiesta di informazioni, prenotazione o preventivo.',
        dati: 'Nome e cognome, indirizzo email, numero di telefono (facoltativo), contenuto del messaggio.',
        base: 'Consenso dell’interessato, espresso con la casella di conferma prima dell’invio.',
        conservazione:
          'Per il tempo necessario a gestire la richiesta e gli eventuali obblighi di legge collegati.',
        destinatari:
          'Web3Forms (servizio di inoltro del modulo) e Google se è attiva la verifica reCAPTCHA. Il messaggio arriva all’indirizzo email della struttura.',
      },
      {
        nome: 'Prenotazione e soggiorno',
        finalita:
          'Gestire la prenotazione, l’accoglienza e gli obblighi di legge (comunicazione degli alloggiati).',
        dati: 'Dati anagrafici degli ospiti, documento d’identità, date del soggiorno.',
        base: 'Esecuzione del contratto e obblighi di legge.',
        conservazione: 'Per i termini previsti dalla normativa fiscale e di pubblica sicurezza.',
        destinatari: 'Autorità competenti, quando la legge lo richiede.',
      },
      {
        nome: 'Log tecnici dell’hosting',
        finalita: 'Garantire il funzionamento e la sicurezza del sito.',
        dati: 'Indirizzo IP, tipo di browser, pagina richiesta, data e ora.',
        base: 'Legittimo interesse alla sicurezza del servizio.',
        conservazione: 'Per brevi periodi, secondo le politiche del fornitore di hosting.',
        destinatari: 'Fornitore di hosting (Vercel e/o Netlify).',
      },
    ],
    titoloDiritti: 'I tuoi diritti',
    testoDirittiPrima:
      'Puoi chiedere in qualsiasi momento di accedere ai tuoi dati, correggerli, cancellarli, limitarne il trattamento o opporti al trattamento, e puoi richiedere la portabilità dei dati che ci hai fornito. Per esercitare questi diritti scrivi a',
    testoDirittiDopo: '.',
    testoGarantePrima:
      'Se ritieni che il trattamento non rispetti la normativa, puoi rivolgerti al Garante per la protezione dei dati personali',
    testoGaranteDopo: '.',
    titoloTrasferimenti: 'Trasferimenti fuori dall’Unione Europea',
    testoTrasferimenti:
      'Il servizio di inoltro del modulo e i servizi dell’hosting possono trattare i dati anche negli Stati Uniti. In quel caso il trasferimento avviene sulla base delle clausole contrattuali standard o di decisioni di adeguatezza della Commissione Europea.',
    titoloModifiche: 'Modifiche a questa informativa',
    testoModifiche:
      'Se l’informativa cambia, la versione aggiornata sostituisce questa pagina. Non usiamo i dati per finalità diverse da quelle descritte qui.',
    linkCookie: 'Leggi la Cookie Policy',
    notaPrevalenza:
      'Questa è la traduzione inglese dell’informativa. In caso di divergenza fa fede la versione italiana.',
  },
  contatti: {
    metaTitolo: 'Contatti',
    metaDescrizione:
      'Scrivi o chiama la Locanda Seggiovia a Recoaro Terme per prenotare una camera, un tavolo al ristorante o chiedere informazioni sui sentieri delle Piccole Dolomiti.',
    etichetta: 'Contatti',
    titolo: 'Scrivici',
    lede:
      'Per prenotare una camera, un tavolo o per chiedere informazioni su un sentiero. Rispondiamo noi, di solito entro la giornata.',
    avvisoDemoTitolo: 'Modulo in modalità dimostrativa.',
    avvisoDemoTesto:
      'La chiave di Web3Forms non è ancora configurata, quindi l’invio non recapita email. Impostare la variabile PUBLIC_WEB3FORMS_KEY per attivarlo.',
    nome: 'Nome e cognome',
    email: 'Email',
    telefono: 'Telefono',
    telefonoAiuto: 'Facoltativo, ma utile se preferisci essere richiamato.',
    messaggio: 'Messaggio',
    placeholderNome: 'Maria Rossi',
    placeholderEmail: 'maria.rossi@esempio.it',
    placeholderTelefono: '+39 333 000 0000',
    placeholderMessaggio: 'Vorrei prenotare una camera doppia per il fine settimana del…',
    consenso:
      'Ho letto l’informativa e acconsento al trattamento dei dati per rispondere alla mia richiesta. I dati non vengono usati per altro.',
    invia: 'Invia il messaggio',
    campiObbligatori: 'I campi con * sono obbligatori.',
    recaptcha:
      'Questo modulo è protetto da reCAPTCHA v3 di Google. L’uso di reCAPTCHA è soggetto all’informativa sulla privacy e ai termini di servizio di Google.',
    titoloRecapiti: 'Dove siamo',
    etichettaTelefono: 'Telefono',
    etichettaEmail: 'Email',
    etichettaOrari: 'Orari',
    notaOrari:
      'Gli orari sono indicativi e possono cambiare in stagione. Per un tavolo conviene sempre una telefonata.',
    titoloMappa: 'Come raggiungerci',
    notaMappa:
      'La mappa è fornita da Google. Caricandola accetti i termini di Google e i suoi cookie. Se preferisci, puoi aprirla in una nuova scheda.',
    caricaMappa: 'Carica la mappa',
    apriMaps: 'Apri in Google Maps',
  },
  ristorante: {
    metaTitolo: 'Ristorante',
    metaDescrizione:
      'Cucina tradizionale alto-vicentina a Recoaro Terme: bacalà alla vicentina, sopressa fatta in casa, trota affumicata e gnocchi con la fioreta De.Co.',
    etichetta: 'Ristorante',
    titolo: 'La cucina di queste valli',
    lede:
      'Il menù segue le stagioni e le malghe, non le mode. Il bacalà arriva da una tradizione lunga, la sopressa si fa in casa, la trota si affumica qui.',
    altSala: 'Fotografia in arrivo: la sala del ristorante apparecchiata',
    segnapostoTitolo: 'Foto in arrivo',
    segnapostoSoggetto: 'La sala del ristorante',
    etichettaSpecialita: 'Le specialità',
    titoloSpecialita: 'Quello che ci identifica',
    testoSpecialita:
      'Pochi piatti, sempre gli stessi, perché sono quelli che sappiamo fare. Il resto del menù cambia con le stagioni.',
    linkRicettaGnocchi: 'La storia e la ricetta',
    titoloMenu: 'Il menù',
    testoMenu:
      'Il menù cambia con le stagioni e con quello che le malghe hanno da offrire. Questi sono i piatti che trovate tutto l’anno.',
    notaPrezzi:
      'I prezzi non sono ancora pubblicati: chiediceli direttamente, oppure consultali in locanda.',
    categorie: {
      antipasti: 'Antipasti',
      primi: 'Primi',
      secondi: 'Secondi',
      dolci: 'Dolci',
    },
    titoloOrari: 'Orari e prenotazioni',
    testoOrari:
      'Il tavolo si prenota per tempo, soprattutto nei fine settimana e in stagione. Per gruppi e per esigenze particolari, chiamateci.',
    pulsantePrenota: 'Prenota un tavolo',
  },
  gnocchi: {
    metaTitolo: 'Gnocchi con la Fioreta — prodotto De.Co.',
    metaDescrizione:
      'Storia, ricetta De.Co. e lavorazione degli Gnocchi con la Fioreta di Recoaro Terme: 1,5 litri di fioreta, 1 kg di farina bianca, burro di malga rosolato.',
    etichetta: 'Prodotto bandiera',
    altPiatto:
      'Gli gnocchi con la fioreta serviti nel piatto, conditi con il burro di malga rosolato',
    titoloStoria: 'Da dove viene la fioreta',
    etichettaRicetta: 'Ricetta De.Co.',
    titoloRicetta: 'Due ingredienti, nessuna scorciatoia',
    testoRicetta:
      'La ricetta depositata è breve perché non c’è molto da aggiungere: quello che conta è la qualità della fioreta e la mano di chi impasta.',
    altIngredienti:
      'Gli ingredienti disposti sul tavolo di cucina: la fioreta, la farina, il burro e il formaggio di malga',
    didascaliaIngredienti:
      'Gli ingredienti sul tavolo di cucina: fioreta, farina bianca, burro e formaggio di malga.',
    titoloLavorazione: 'La lavorazione',
    titoloCondimento: 'Il condimento',
    riconoscimenti: 'Riconoscimenti',
    pulsanteRistorante: 'Il ristorante',
    pulsantePrenota: 'Prenota un tavolo',
    ingredienteSchema: '{quantita} di {ingrediente}',
    categoriaSchema: 'Primi piatti',
    cucinaSchema: 'Cucina alto-vicentina',
    paroleChiaveSchema: 'gnocchi con la fioreta, De.Co., Recoaro Terme, cucina vicentina',
  },
  sentiero: {
    titoloDocumento: '{nome} — Sentieri',
    altCopertina: 'Segnaposto grafico in attesa della fotografia del {nome}',
    briciola: 'Sentieri',
    etichettaDati: 'Dati tecnici del percorso',
    notaDati:
      'Difficoltà secondo la scala del CAI. I dati sono indicativi: prima di partire verifica le condizioni del sentiero.',
    titoloPercorso: 'Il percorso',
    titoloCondizioni: 'Condizioni',
    webcamVoce: 'Webcam',
    webcamDefault: 'Guarda la webcam',
    webcamNota: 'Immagine aggiornata dalla fonte, in una nuova scheda ↗',
    titoloChiusura: 'Hai bisogno di informazioni?',
    testoChiusura:
      'Se ci scrivi ti diciamo com’è il sentiero in questo periodo e dove conviene lasciare l’auto.',
    pulsanteScrivici: 'Scrivici',
    pulsanteCamere: 'Le camere',
  },
  sentieriPagina: {
    metaTitolo: 'Sentieri',
    metaDescrizione:
      'Sette itinerari escursionistici da Recoaro Terme: Piccole Dolomiti, Gruppo del Carega e Pasubio, con distanze, dislivelli e difficoltà CAI.',
    etichetta: 'Territorio e sentieri',
    titolo: 'I sentieri cominciano dal centro del paese',
    lede:
      'Sette itinerari fra Piccole Dolomiti, Gruppo del Carega e Pasubio. Difficoltà dal turistico all’escursionistico esposto, con i dati tecnici di ciascuno.',
    etichettaElenco: 'Elenco degli itinerari',
    etichettaDifficolta: 'Difficoltà',
    titoloScala: 'Come si leggono le difficoltà',
    testoScala:
      'Le sigle sono la classificazione ufficiale del Club Alpino Italiano. Non sono un giudizio: dicono cosa aspettarsi dal terreno.',
    scala: [
      {
        sigla: 'T',
        nome: 'Turistico',
        nota: 'Sentieri facili, adatti anche alle famiglie.',
      },
      {
        sigla: 'E',
        nome: 'Escursionistico',
        nota: 'Serve un minimo di allenamento e scarpe adatte.',
      },
      {
        sigla: 'EE',
        nome: 'Escursionisti esperti',
        nota: 'Terreno impervio, attrezzatura adeguata.',
      },
    ],
    altMontagne:
      'Le creste delle Piccole Dolomiti sopra Recoaro Terme, con il tricolore',
    didascaliaMontagne: 'Il gruppo delle Piccole Dolomiti sopra Recoaro Terme.',
    etichettaTerritorio: 'Il territorio',
    titoloMontagna: 'Un gruppo montuoso a misura d’uomo',
    testoMontagna:
      'Le Piccole Dolomiti non hanno l’altezza delle grandi, ed è proprio questo il loro pregio: si cammina tutto il giorno e si torna in paese la sera. Il Gruppo del Carega e il Pasubio sono a pochi chilometri.',
    linkConsiglio: 'Chiedi un consiglio sul percorso',
    altPanorama: 'Disegno di creste montuose con foschia nelle valli',
    titoloChiusura: 'Dove si dorme, prima di partire',
    testoChiusura:
      'La Locanda è in piazza a Recoaro Terme: colazione presto, consigli su misura, e i sentieri che cominciano fuori dalla porta.',
    pulsanteCamere: 'Le camere',
    pulsanteInfo: 'Chiedi informazioni',
  },
  camere: {
    metaTitolo: 'Camere e tariffe',
    metaDescrizione:
      'Camere singole e doppie a Recoaro Terme con TV, cassaforte e set di cortesia. Tariffe per persona da 55 €. Soggiorno minimo 3 giorni.',
    etichetta: 'Camere e tariffe',
    titolo: 'Camere semplici ed accoglienti',
    titoloCamere: 'Due tipi di camera',
    altCamera: 'La {camera} della Locanda Seggiovia',
    segnapostoAlt: 'Fotografia in arrivo: {camera}',
    segnapostoTitolo: 'Foto in arrivo',
    notaColazione:
      'La colazione è compresa nella tariffa B&B. La linea Wi-Fi è disponibile su richiesta negli spazi comuni.',
    etichettaPrezzi: 'Prezzi',
    titoloTariffe: 'Tariffe',
    ledeTariffe:
      'Prezzi per persona, per giorno. Invariati sia in stagione estiva (1 giugno – 15 settembre) sia in stagione invernale (16 settembre – 31 maggio).',
    tabella: {
      camera: 'Camera',
      bnb: 'B&B',
      mezzaPensione: 'Mezza pensione',
      pensioneCompleta: 'Pensione completa',
    },
    captionTabella: 'Tariffe per camera e trattamento, in euro per persona al giorno',
    doppiaUsoSingola: 'Doppia uso singola',
    supplemento: 'supplemento',
    valoreSupplemento: '+ {valore} € / giorno',
    notaTariffe:
      'Le tariffe si intendono per persona e per giorno. Il soggiorno minimo è di {giorni} giorni.',
    prenotazioneTitolo: 'Verifica le date',
    prenotazioneDescrizione:
      'Dicci quando vorresti venire e quante persone siete. Ti rispondiamo noi, di solito entro un giorno.',
    etichettaRegole: 'Regole',
    titoloRegole: 'Bambini, animali e regole',
    testoRegole:
      'Poche regole, chiare. Se avete esigenze particolari — un lettino, una cena anticipata, un cane di taglia grande — ditecelo al momento della prenotazione.',
    politiche: {
      bambini03: 'Bambini 0–3 anni',
      bambini410: 'Bambini 4–10 anni',
      animali: 'Animali domestici',
      soggiornoMinimo: 'Soggiorno minimo',
      doppiaUsoSingola: 'Doppia uso singola',
    },
    valori: {
      gratuiti: 'Gratuiti',
      sconto30: 'Sconto 30%',
      animali: '{giorno} € al giorno + {pulizie} € di pulizie finali',
      soggiorno: '{giorni} giorni',
      supplementoDus: 'Supplemento {valore} € al giorno',
    },
    chiusuraTitolo: 'Verifica le date',
    chiusuraTesto:
      'Scrivici o chiamaci: ti diciamo subito disponibilità e prezzo esatto per il tuo soggiorno.',
    pulsanteScrivici: 'Scrivici',
  },
  home: {
    titoloCarosello: 'Cosa trovi qui',
    invitoCarosello: 'Scopri di più',
    precedente: 'Diapositiva precedente',
    successiva: 'Diapositiva successiva',
    altFacciata:
      'La Locanda Seggiovia in piazza a Recoaro Terme, con i balconi in legno e le Piccole Dolomiti sullo sfondo',
    etichettaCucina: 'Cucina',
    titoloCucina: 'Quello che si cucina in vallata',
    testoCucina:
      'Il menù segue le stagioni e le malghe, non le mode. Il bacalà arriva da una tradizione lunga, la sopressa si fa in casa.',
    linkRistorante: 'Il ristorante',
    invitoGnocchi: 'La storia e la ricetta',
    invitoPiatto: 'Vedi il menù',
    titoloLegenda: 'Come si leggono le difficoltà',
    testoLegenda:
      'È la scala del Club Alpino Italiano, quella che si trova sui cartelli lungo i sentieri.',
    legenda: [
      { sigla: 'T', nome: 'Turistico', nota: 'Sentieri pianeggianti o poco ripidi, adatti a tutti.' },
      {
        sigla: 'E',
        nome: 'Escursionistico',
        nota: 'Serve allenamento e scarpe adatte. Sentieri su terreno anche ripido.',
      },
      {
        sigla: 'EE',
        nome: 'Escursionisti esperti',
        nota: 'Terreno impervio, a tratti esposto. Serve esperienza e passo sicuro.',
      },
    ],
    pulsanteTuttiSentieri: 'Tutti i sentieri',
    titoloChiusura: 'Ti aspettiamo in piazza',
    testoChiusura:
      'Per prenotare una camera, un tavolo o per chiedere informazioni su un sentiero, scrivici o chiamaci. Rispondiamo noi.',
    pulsanteScrivici: 'Scrivici',
  },
};

const EN: TestiPagine = {
  locanda: {
    metaTitolo: 'The Inn — its story and the family',
    metaDescrizione:
      'Locanda Seggiovia in Recoaro Terme: a house of stone and wood on the square, kept by the Asnicar Bertoldi family, at the foot of the Piccole Dolomiti.',
    etichetta: 'The Inn',
    titolo: 'A house of stone on the square, at the foot of the Piccole Dolomiti',
    lede:
      'Locanda Seggiovia was not built as a hotel and has not become one. It is the home of a family that chose to stay in the mountains and to open it to those who come looking for them.',
    altCucina: 'The kitchen work table with fioreta, flour and malga butter',
    didascaliaCucina: 'The kitchen table: fioreta, flour and malga butter.',
    titoloFamiglia: 'The {cognome} family',
    paragrafiFamiglia: [
      'The inn is run by {gestori}. It is not a management company: the people who cook, who welcome you and who suggest the trail are the same people who live here all year. It is the difference you notice the moment you come through the door.',
      'Recoaro Terme is a valley town that in the twentieth century was spas and industry, and that today lives mainly on the mountain. Staying here, and keeping an inn open on the square, is a precise choice: it means believing that the tourism of these valleys belongs to those who walk, not to those who pass through.',
      'Everything else follows from that choice. We know the trails because we walk them, we know the malghe because we buy cheese there, and the kitchen follows the seasons of what the malghe have to give.',
    ],
    etichettaCarattere: 'The character of the house',
    titoloCarattere: 'Why we say refuge and not hotel',
    carattere: [
      'Anyone who comes up here to walk leaves the car on the square and starts walking: the trails begin in the village, not in a car park.',
      'In the morning breakfast is ready before dawn, because people heading for the mountains leave early — and they already know what awaits them, since we know the trails one by one.',
      'In the evening you come back hungry, and the cooking is the cooking of the house: not an extra service, but the reason many people come back.',
    ],
    altFacciata:
      'The façade of Locanda Seggiovia with its wooden balconies, in the centre of Recoaro Terme',
    etichettaCasa: 'The house',
    titoloCasa: 'Stone, wood, and a square in front',
    paragrafiCasa: [
      'The building is on the square, with wooden balconies facing the Piccole Dolomiti. The rooms are on the upper floors, the restaurant on the ground floor: you come in through the door and you are already inside the day.',
    ],
    notaFoto:
      'More photographs of the interiors are on their way: the rooms are being refurbished.',
    titoloDove: 'On the square, in the centre of the village',
    testoDove:
      'Recoaro Terme lies in the Valle dell’Agno, at the foot of the Piccole Dolomiti and the Pasubio group. The inn is on the square, a short walk from the springs and from the point where the trails begin.',
    apriMappa: 'Open the map',
    voci: {
      indirizzo: 'Address',
      altitudine: 'Altitude',
      gruppi: 'Mountain groups',
      camere: 'Rooms',
      ristorante: 'Restaurant',
    },
    altitudine: 'about 450 m above sea level',
    gruppi: 'Piccole Dolomiti, Pasubio, Carega',
    camereLink: 'Single and double',
    ristoranteLink: 'Cooking of the upper Vicenza valleys',
    titoloChiusura: 'Come and see',
    testoChiusura:
      'The rooms are simple and carefully kept, the restaurant is open at lunch and in the evening. Write to us and we will tell you everything you need.',
    pulsanteCamere: 'The rooms',
    pulsanteContatti: 'Contact',
  },
  cookie: {
    metaTitolo: 'Cookie Policy',
    metaDescrizione:
      'Cookie Policy of the Locanda Seggiovia website: the site sets no cookies before you act, and the Google map loads only when you ask for it.',
    etichetta: 'Privacy notice',
    titolo: 'Cookie Policy',
    lede:
      'This site does not ask you to accept cookies it never uses. Here is exactly what is set, and when.',
    titoloElenco: 'What is actually set',
    captionTabella: 'Cookies and technical storage used by the site',
    tabella: { voce: 'Item', tipo: 'Type', durata: 'Duration' },
    elenco: [
      {
        nome: 'Our own technical cookies',
        tipo: 'None',
        durata: '—',
        nota: 'The site sets no cookies of its own: there are no sessions, baskets or preferences to remember.',
      },
      {
        nome: 'Google Maps cookies',
        tipo: 'Third party',
        durata: 'Set by Google',
        nota:
          'They are set only after you press “Load the map” on the Contact page. If you do not press the button, no Google cookie is set.',
      },
      {
        nome: 'reCAPTCHA cookies (Google)',
        tipo: 'Third party',
        durata: 'Set by Google',
        nota:
          'Present only if the reCAPTCHA check on the contact form is active. At the moment that option is off, so these cookies are not set.',
      },
      {
        nome: 'Technical hosting logs',
        tipo: 'Not cookies',
        durata: 'Short period',
        nota:
          'The hosting provider records IP address and requests for security and diagnostics. These are not cookies and are not used to profile anyone.',
      },
    ],
    notaElenco:
      'This list is up to date as of publication and is reviewed whenever something changes on the site. If a statistics tool were ever enabled, it would be listed here and the site would ask for consent before switching it on.',
    titoloGestione: 'How to manage them in your browser',
    testoGestione:
      'You can block or delete cookies in your browser settings. Blocking third-party cookies does not stop you using this site: the only thing that would not work is the embedded map, which you can still open in a new tab.',
    titoloBanner: 'Why there is no banner',
    testoBannerPrima:
      'A banner is needed when a site sets unnecessary cookies',
    testoBannerCorsivo: 'before',
    testoBannerDopo:
      'the visitor agrees. That does not happen here: the Google map loads only after a click, and there are no other third-party scripts. With no cookies to authorise, a banner would only be one more obstacle.',
    linkPrivacy: 'Read the Privacy Policy',
    linkContatti: 'Contact',
    notaPrevalenza:
      'This is the English translation of the cookie policy. In case of discrepancy, the Italian version prevails.',
  },
  privacy: {
    metaTitolo: 'Privacy Policy',
    metaDescrizione:
      'How the Locanda Seggiovia website processes personal data: what we collect, why, for how long, and how to exercise your rights.',
    etichetta: 'Privacy notice',
    titolo: 'Privacy Policy',
    lede:
      'This page explains what personal data the site collects, why it collects it and what becomes of it. It is written to be read, not to be skipped.',
    avvisoTitolo: 'This document is still being completed.',
    avvisoTesto:
      'The text describes correctly how the site handles data, but the company details marked “to be confirmed” must be checked with the owner before publication.',
    titoloTitolare: 'Data controller',
    vociTitolare: {
      ragioneSociale: 'Full registered name',
      partitaIva: 'VAT number / tax code',
      sedeLegale: 'Registered office',
      recapito: 'Contact for privacy matters',
      titolare: 'Data controller',
    },
    daConfermare: '(to be confirmed)',
    titoloTrattamenti: 'What data we process, and why',
    campi: {
      finalita: 'Purpose',
      dati: 'Data collected',
      base: 'Legal basis',
      conservazione: 'Retention',
      destinatari: 'Recipients',
    },
    trattamenti: [
      {
        nome: 'Contact form',
        finalita: 'To answer a request for information, a booking or a quotation.',
        dati: 'Name and surname, email address, telephone number (optional), the content of the message.',
        base: 'The consent of the person concerned, given with the confirmation box before sending.',
        conservazione:
          'For as long as it takes to deal with the request and any legal obligations connected with it.',
        destinatari:
          'Web3Forms (the service that forwards the form) and Google if the reCAPTCHA check is active. The message arrives at the email address of the inn.',
      },
      {
        nome: 'Bookings and stays',
        finalita:
          'To manage the booking, the welcome, and the legal obligations (reporting of guests to the authorities).',
        dati: 'Identity details of guests, identity document, dates of the stay.',
        base: 'Performance of the contract, and legal obligations.',
        conservazione: 'For the periods required by tax and public-safety law.',
        destinatari: 'The competent authorities, where the law requires it.',
      },
      {
        nome: 'Technical hosting logs',
        finalita: 'To keep the site working and secure.',
        dati: 'IP address, browser type, page requested, date and time.',
        base: 'Legitimate interest in the security of the service.',
        conservazione: 'For short periods, according to the policies of the hosting provider.',
        destinatari: 'The hosting provider (Vercel and/or Netlify).',
      },
    ],
    titoloDiritti: 'Your rights',
    testoDirittiPrima:
      'You may ask at any time to see your data, correct it, delete it, restrict how it is processed or object to the processing, and you may ask for the data you gave us to be transferred. To exercise these rights, write to',
    testoDirittiDopo: '.',
    testoGarantePrima:
      'If you believe the processing does not comply with the law, you may turn to the Italian data protection authority, the Garante per la protezione dei dati personali',
    testoGaranteDopo: '.',
    titoloTrasferimenti: 'Transfers outside the European Union',
    testoTrasferimenti:
      'The service that forwards the form, and the hosting services, may also process data in the United States. Where that happens, the transfer relies on the standard contractual clauses or on adequacy decisions of the European Commission.',
    titoloModifiche: 'Changes to this notice',
    testoModifiche:
      'If this notice changes, the updated version replaces this page. We do not use the data for any purpose other than the ones described here.',
    linkCookie: 'Read the Cookie Policy',
    notaPrevalenza:
      'This is the English translation of the privacy notice. In case of discrepancy, the Italian version prevails.',
  },
  contatti: {
    metaTitolo: 'Contact',
    metaDescrizione:
      'Write to or call Locanda Seggiovia in Recoaro Terme to book a room, a table in the restaurant, or to ask about the trails of the Piccole Dolomiti.',
    etichetta: 'Contact',
    titolo: 'Write to us',
    lede:
      'To book a room, a table, or to ask about a trail. We answer ourselves, usually within the day.',
    avvisoDemoTitolo: 'The form is in demonstration mode.',
    avvisoDemoTesto:
      'The Web3Forms key is not configured yet, so sending it does not deliver any email. Set the PUBLIC_WEB3FORMS_KEY variable to enable it.',
    nome: 'Full name',
    email: 'Email',
    telefono: 'Phone',
    telefonoAiuto: 'Optional, but useful if you would rather be called back.',
    messaggio: 'Message',
    placeholderNome: 'Maria Rossi',
    placeholderEmail: 'maria.rossi@example.com',
    placeholderTelefono: '+39 333 000 0000',
    placeholderMessaggio: 'I would like to book a double room for the weekend of…',
    consenso:
      'I have read the privacy notice and I agree to my data being used to answer my enquiry. The data are not used for anything else.',
    invia: 'Send the message',
    campiObbligatori: 'Fields marked * are required.',
    recaptcha:
      'This form is protected by Google reCAPTCHA v3. Use of reCAPTCHA is subject to Google’s privacy notice and terms of service.',
    titoloRecapiti: 'Where we are',
    etichettaTelefono: 'Phone',
    etichettaEmail: 'Email',
    etichettaOrari: 'Opening hours',
    notaOrari:
      'These hours are indicative and may change with the season. For a table, a phone call is always best.',
    titoloMappa: 'How to find us',
    notaMappa:
      'The map is provided by Google. Loading it means accepting Google’s terms and cookies. If you prefer, you can open it in a new tab.',
    caricaMappa: 'Load the map',
    apriMaps: 'Open in Google Maps',
  },
  ristorante: {
    metaTitolo: 'Restaurant',
    metaDescrizione:
      'Traditional cooking from the upper Vicenza valleys in Recoaro Terme: bacalà alla vicentina, house-made sopressa, smoked trout and gnocchi with fioreta De.Co.',
    etichetta: 'Restaurant',
    titolo: 'The cooking of these valleys',
    lede:
      'The menu follows the seasons and the malghe, not fashions. The bacalà comes from a long tradition, the sopressa is made at home, the trout is smoked here.',
    altSala: 'Photograph to come: the restaurant dining room, laid for service',
    segnapostoTitolo: 'Photo to come',
    segnapostoSoggetto: 'The dining room',
    etichettaSpecialita: 'Our specialities',
    titoloSpecialita: 'What sets us apart',
    testoSpecialita:
      'A few dishes, always the same, because they are the ones we know how to cook. The rest of the menu changes with the seasons.',
    linkRicettaGnocchi: 'The story and the recipe',
    titoloMenu: 'The menu',
    testoMenu:
      'The menu changes with the seasons and with what the malghe have to offer. These are the dishes you will find all year.',
    notaPrezzi:
      'Prices are not published yet: ask us directly, or look at them when you are here.',
    categorie: {
      antipasti: 'Starters',
      primi: 'First courses',
      secondi: 'Main courses',
      dolci: 'Desserts',
    },
    titoloOrari: 'Opening hours and bookings',
    testoOrari:
      'Tables are best booked ahead, especially at weekends and in season. For groups and particular needs, give us a ring.',
    pulsantePrenota: 'Book a table',
  },
  gnocchi: {
    metaTitolo: 'Gnocchi con la Fioreta — a De.Co. product',
    metaDescrizione:
      'The story, the De.Co. recipe and how Gnocchi con la Fioreta are made in Recoaro Terme: 1.5 litres of fioreta, 1 kg of white flour, browned malga butter.',
    etichetta: 'Flagship product',
    altPiatto: 'Gnocchi with fioreta served on the plate, dressed with browned malga butter',
    titoloStoria: 'Where fioreta comes from',
    etichettaRicetta: 'The De.Co. recipe',
    titoloRicetta: 'Two ingredients, no shortcuts',
    testoRicetta:
      'The registered recipe is short because there is not much to add: what matters is the quality of the fioreta and the hand of the person mixing it.',
    altIngredienti:
      'The ingredients laid out on the kitchen table: fioreta, flour, butter and malga cheese',
    didascaliaIngredienti:
      'The ingredients on the kitchen table: fioreta, white flour, butter and malga cheese.',
    titoloLavorazione: 'How it is made',
    titoloCondimento: 'The dressing',
    riconoscimenti: 'Recognition',
    pulsanteRistorante: 'The restaurant',
    pulsantePrenota: 'Book a table',
    /*
      In inglese «1.5 litres of fioreta» va bene ma «of salt: to taste» no: qui
      l'ordine si rovescia e diventa «Salt: to taste». Il modello tiene conto
      della lingua invece di concatenare parole.
    */
    ingredienteSchema: '{ingrediente}: {quantita}',
    categoriaSchema: 'First courses',
    cucinaSchema: 'Cooking of the upper Vicenza valleys',
    paroleChiaveSchema:
      'gnocchi with fioreta, De.Co., Recoaro Terme, cooking of the Vicenza valleys',
  },
  sentiero: {
    titoloDocumento: '{nome} — Trails',
    altCopertina: 'Placeholder drawing, waiting for a photograph of {nome}',
    briciola: 'Trails',
    etichettaDati: 'Technical data for the route',
    notaDati:
      'Difficulty according to the CAI scale. The figures are indicative: check the condition of the trail before you set off.',
    titoloPercorso: 'The route',
    titoloCondizioni: 'Conditions',
    webcamVoce: 'Webcam',
    webcamDefault: 'Open the webcam',
    webcamNota: 'The image is updated by the source, in a new tab ↗',
    titoloChiusura: 'Do you need information?',
    testoChiusura:
      'Write to us and we will tell you how the trail is at this time of year, and where it is best to leave the car.',
    pulsanteScrivici: 'Write to us',
    pulsanteCamere: 'The rooms',
  },
  sentieriPagina: {
    metaTitolo: 'Trails',
    metaDescrizione:
      'Seven hiking itineraries from Recoaro Terme: the Piccole Dolomiti, the Carega group and Monte Pasubio, with distances, ascents and CAI difficulty grades.',
    etichetta: 'The area and its trails',
    titolo: 'The trails begin in the centre of the village',
    lede:
      'Seven itineraries between the Piccole Dolomiti, the Carega group and Monte Pasubio. Grades from easy walking to exposed mountain paths, with the technical data for each.',
    etichettaElenco: 'List of itineraries',
    etichettaDifficolta: 'Difficulty',
    titoloScala: 'How to read the difficulty grades',
    testoScala:
      'These letters are the official classification of the Club Alpino Italiano. They are not a judgement: they tell you what to expect from the ground.',
    scala: [
      {
        sigla: 'T',
        nome: 'Tourist',
        nota: 'Easy paths, suitable for families too.',
      },
      {
        sigla: 'E',
        nome: 'Hiking',
        nota: 'You need some fitness and proper boots.',
      },
      {
        sigla: 'EE',
        nome: 'Experienced hikers',
        nota: 'Rough ground, proper equipment.',
      },
    ],
    altMontagne:
      'The ridges of the Piccole Dolomiti above Recoaro Terme, with the Italian flag',
    didascaliaMontagne: 'The Piccole Dolomiti group above Recoaro Terme.',
    etichettaTerritorio: 'The area',
    titoloMontagna: 'A mountain group on a human scale',
    testoMontagna:
      'The Piccole Dolomiti do not have the height of the great ranges, and that is precisely their virtue: you walk all day and you are back in the village by evening. The Carega group and Monte Pasubio are a few kilometres away.',
    linkConsiglio: 'Ask us about a route',
    altPanorama: 'Drawing of mountain ridges with haze in the valleys',
    titoloChiusura: 'Where you sleep, before you set off',
    testoChiusura:
      'The inn is on the square in Recoaro Terme: breakfast early, advice to suit you, and the trails beginning outside the door.',
    pulsanteCamere: 'The rooms',
    pulsanteInfo: 'Ask for information',
  },
  camere: {
    metaTitolo: 'Rooms and rates',
    metaDescrizione:
      'Single and double rooms in Recoaro Terme with TV, safe and toiletries. Rates from €55 per person. Minimum stay 3 days.',
    etichetta: 'Rooms and rates',
    titolo: 'Simple, welcoming rooms',
    titoloCamere: 'Two kinds of room',
    altCamera: 'The {camera} at Locanda Seggiovia',
    segnapostoAlt: 'Photograph to come: {camera}',
    segnapostoTitolo: 'Photo to come',
    notaColazione:
      'Breakfast is included in the bed and breakfast rate. Wi-Fi is available on request in the shared areas.',
    etichettaPrezzi: 'Prices',
    titoloTariffe: 'Rates',
    ledeTariffe:
      'Prices per person, per day. The same in summer (1 June – 15 September) and in winter (16 September – 31 May).',
    tabella: {
      camera: 'Room',
      bnb: 'B&B',
      mezzaPensione: 'Half board',
      pensioneCompleta: 'Full board',
    },
    captionTabella: 'Rates by room and board, in euros per person per day',
    doppiaUsoSingola: 'Double for single use',
    supplemento: 'supplement',
    valoreSupplemento: '+ €{valore} / day',
    notaTariffe:
      'Rates are per person and per day. The minimum stay is {giorni} days.',
    prenotazioneTitolo: 'Check your dates',
    prenotazioneDescrizione:
      'Tell us when you would like to come and how many of you there are. We answer ourselves, usually within a day.',
    etichettaRegole: 'House rules',
    titoloRegole: 'Children, pets and house rules',
    testoRegole:
      'Few rules, and clear ones. If you have particular needs — a cot, an early dinner, a large dog — tell us when you book.',
    politiche: {
      bambini03: 'Children 0–3',
      bambini410: 'Children 4–10',
      animali: 'Pets',
      soggiornoMinimo: 'Minimum stay',
      doppiaUsoSingola: 'Double for single use',
    },
    valori: {
      gratuiti: 'Free',
      sconto30: '30% off',
      animali: '€{giorno} per day + €{pulizie} for final cleaning',
      soggiorno: '{giorni} days',
      supplementoDus: '€{valore} per day supplement',
    },
    chiusuraTitolo: 'Check your dates',
    chiusuraTesto:
      'Write to us or call: we will tell you straight away whether we have room, and the exact price for your stay.',
    pulsanteScrivici: 'Write to us',
  },
  home: {
    titoloCarosello: 'What you will find here',
    invitoCarosello: 'Find out more',
    precedente: 'Previous slide',
    successiva: 'Next slide',
    altFacciata:
      'Locanda Seggiovia on the square in Recoaro Terme, with its wooden balconies and the Piccole Dolomiti behind',
    etichettaCucina: 'Kitchen',
    titoloCucina: 'What is cooked in the valley',
    testoCucina:
      'The menu follows the seasons and the malghe, not fashions. The bacalà comes from a long tradition, the sopressa is made at home.',
    linkRistorante: 'The restaurant',
    invitoGnocchi: 'The story and the recipe',
    invitoPiatto: 'See the menu',
    titoloLegenda: 'How to read the difficulty grades',
    testoLegenda:
      'It is the scale of the Club Alpino Italiano, the one you find on the signs along the trails.',
    legenda: [
      { sigla: 'T', nome: 'Tourist', nota: 'Level or gently sloping paths, suitable for everyone.' },
      {
        sigla: 'E',
        nome: 'Hiking',
        nota: 'You need fitness and proper boots. Paths on ground that may be steep.',
      },
      {
        sigla: 'EE',
        nome: 'Experienced hikers',
        nota: 'Rough ground, exposed in places. You need experience and a sure foot.',
      },
    ],
    pulsanteTuttiSentieri: 'All trails',
    titoloChiusura: 'We will see you on the square',
    testoChiusura:
      'To book a room, a table, or to ask about a trail, write to us or give us a ring. We answer ourselves.',
    pulsanteScrivici: 'Write to us',
  },
};

export const PAGINE: Record<Lingua, TestiPagine> = { it: IT, en: EN };

/** I testi delle pagine nella lingua richiesta. */
export function testiPagina(lingua: Lingua): TestiPagine {
  return PAGINE[lingua];
}
