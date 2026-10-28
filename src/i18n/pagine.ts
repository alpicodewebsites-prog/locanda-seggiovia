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
