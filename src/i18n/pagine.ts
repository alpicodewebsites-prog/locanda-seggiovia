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
