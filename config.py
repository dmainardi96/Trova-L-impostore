stanze = {}

CATEGORIE = {
    "Animali": [
        ("Leone", "Tigre"),
        ("Giraffa", "Cammello"),
        ("Panda", "Orso Polare"),
        ("Tigre", "Leopardo"),
        ("Elefante", "Rinoceronte"),
        ("Canguro", "Koala"),
        ("Lupo", "Volpe"),
        ("Pinguino", "Foca"),
        ("Delfino", "Squalo"),
        ("Aquila", "Falco"),
        ("Gatto", "Lince"),
        ("Cane", "Lupo"),
        ("Ippopotamo", "Rinoceronte"),
        ("Cobra", "Vipera"),
        ("Corvo", "Gazza Ladra"),
        ("Formica", "Termite"),
        ("Cavallo", "Zebra"),
        ("Gufo", "Civetta"),
        ("Orso", "Tasso"),
        ("Squalo", "Barracuda")
    ],
    "Oggetti": [
        ("Telefono", "Tablet"),
        ("Orologio", "Bracciale"),
        ("Zaino", "Borsa"),
        ("Sedia", "Poltrona"),
        ("Computer", "Tablet"),
        ("Lampada", "Torcia"),
        ("Chitarra", "Violino"),
        ("Bicicletta", "Monopattino"),
        ("Forbici", "Coltello"),
        ("Microonde", "Forno"),
        ("Mouse", "Touchpad"),
        ("Tastiera", "Pianoforte"),
        ("Cuffie", "Auricolari"),
        ("Bicchiere", "Tazza"),
        ("Telecomando", "Joystick"),
        ("Specchio", "Vetro"),
        ("Cuscino", "Piumone"),
        ("Bottiglia", "Caraffa"),
        ("Martello", "Mazza"),
        ("Cacciavite", "Chiave Inglese")
    ],
    "Cibi": [
        ("Pizza", "Calzone"),
        ("Pasta", "Riso"),
        ("Gelato", "Sorbetto"),
        ("Hamburger", "Hot Dog"),
        ("Sushi", "Onigiri"),
        ("Lasagna", "Cannelloni"),
        ("Torta", "Muffin"),
        ("Insalata", "Verdure Grigliate"),
        ("Patatine", "Chips"),
        ("Frittata", "Omelette"),
        ("Cioccolato", "Nutella"),
        ("Kebab", "Gyros"),
        ("Bistecca", "Filetto"),
        ("Mozzarella", "Burrata"),
        ("Caffè", "Espresso"),
        ("Vino", "Spumante"),
        ("Whiskey", "Cognac"),
        ("Brioche", "Cornetto"),
        ("Tonno", "Salmone"),
        ("Yogurt", "Budino")
    ],
    "Sport": [
        ("Calcio", "Rugby"),
        ("Basket", "Pallavolo"),
        ("Tennis", "Ping Pong"),
        ("Nuoto", "Pallanuoto"),
        ("Sci", "Snowboard"),
        ("Golf", "Mini Golf"),
        ("Boxe", "MMA"),
        ("Motociclismo", "Automobilismo"),
        ("Pallavolo", "Pallamano"),
        ("Atletica", "Maratona"),
        ("Surf", "Windsurf"),
        ("Ciclismo", "BMX"),
        ("Equitazione", "Polo"),
        ("Tiro con l’arco", "Balestra"),
        ("Karate", "Judo"),
        ("Snooker", "Biliardo"),
        ("Freccette", "Bowling"),
        ("Scherma", "Kendo"),
        ("Skateboard", "Longboard"),
        ("Paracadutismo", "Bungee Jumping")
    ],
    "Film": [
        ("Titanic", "Avatar"),
        ("Inception", "Interstellar"),
        ("Matrix", "Blade Runner"),
        ("Jurassic Park", "King Kong"),
        ("Star Wars", "Star Trek"),
        ("Pulp Fiction", "Il Padrino"),
        ("Forrest Gump", "Rain Man"),
        ("The Shining", "It"),
        ("Fight Club", "American Psycho"),
        ("The Dark Knight", "Joker"),
        ("Harry Potter", "Il Signore degli Anelli"),
        ("Frozen", "Rapunzel"),
        ("Shrek", "Madagascar"),
        ("Il Gladiatore", "Troy"),
        ("The Avengers", "Justice League"),
        ("Kill Bill", "John Wick"),
        ("C'era una volta in America", "The Irishman"),
        ("The Truman Show", "Black Mirror"),
        ("La La Land", "Moulin Rouge"),
        ("Bohemian Rhapsody", "Rocketman"),
        ("Il Re Leone", "Bambi"),
        ("Toy Story", "Coco"),
        ("Frozen", "Rapunzel"),
        ("La città incantata", "Il Castello Errante di Howl"),
        ("Akira", "Perfect Blue"),
        ("L'era glaciale", "Alla ricerca di Nemo"),
        ("Inside Out", "Soul"),
        ("Wall-E", "Up"),
        ("Kung Fu Panda", "Dragon Trainer"),
    ],
    "Personaggi di Finzione": [
        ("Batman", "Superman"),
        ("Sherlock Holmes", "Poirot"),
        ("Harry Potter", "Gandalf"),
        ("Darth Vader", "Kylo Ren"),
        ("Topolino", "Paperino"),
        ("Homer Simpson", "Peter Griffin"),
        ("Indiana Jones", "Lara Croft"),
        ("Dracula", "Frankenstein"),
        ("Freddy Krueger", "Saw l'enigmista"),
        ("Wolverine", "Hulk"),
        ("James Bond", "Ethan Hunt"),
        ("Goku", "Vegeta"),
        ("Naruto", "Sasuke"),
        ("Rick Sanchez", "Bender"),
        ("Joker", "Pennywise"),
        ("Geralt di Rivia", "Legolas"),
        ("Zorro", "Robin Hood")
    ],
    "Volgare & Hot": [
        ("Velina", "Playgirl"),
        ("Vibratore", "Dildo"),
        ("Troia", "Zoccola"),
        ("Stripper", "Escort"),
        ("Scopata", "Petting"),
        ("Orgasmo", "Squirting"),
        ("69", "Missionario"),
        ("Nudista", "Esibizionista"),
        ("Sadomaso", "BDSM"),
        ("Pompino", "Leccata di passera"),
        ("Triplo Penetration", "Gang Bang"),
        ("Seno", "Tette"),
        ("Culo", "Chiappe"),
        ("Vagina", "Figa"),
        ("Sesso anale", "Doppia Penetrazione"),
        ("Shemale", "Trans"),
        ("Camgirl", "OnlyFans"),
        ("Masturbazione", "Dito in culo"),
        ("Pene", "Cazzo"),
        ("Latex", "Catwoman")
    ],
    "Musica - Generi": [
        ("Rock", "Hard Rock"),
        ("Metal", "Heavy Metal"),
        ("Jazz", "Blues"),
        ("Hip-Hop", "Rap"),
        ("Reggae", "Ska"),
        ("Techno", "House"),
        ("Trap", "Drill"),
        ("Classica", "Sinfonica"),
        ("Pop", "Synthpop"),
        ("Punk", "Grunge")
    ],
    "Musica - Strumenti": [
        ("Chitarra", "Basso"),
        ("Pianoforte", "Clavicembalo"),
        ("Batteria", "Percussioni"),
        ("Sassofono", "Clarinetto"),
        ("Violino", "Viola"),
        ("Tromba", "Trombone"),
        ("Ukulele", "Mandolino"),
        ("Flauto", "Oboe"),
        ("Arpa", "Liuto"),
        ("Fisarmonica", "Organetto")
    ],
    "Personaggi Famosi": [
        ("Elon Musk", "Jeff Bezos"),
        ("Cristiano Ronaldo", "Lionel Messi"),
        ("Steve Jobs", "Bill Gates"),
        ("Freddie Mercury", "David Bowie"),
        ("Madonna", "Lady Gaga"),
        ("Charlie Chaplin", "Buster Keaton"),
        ("Michael Jackson", "Prince"),
        ("Elvis Presley", "Frank Sinatra"),
        ("Marilyn Monroe", "Audrey Hepburn"),
        ("Robert Downey Jr.", "Johnny Depp"),
        ("Quentin Tarantino", "Christopher Nolan"),
        ("Pablo Picasso", "Vincent van Gogh"),
        ("Kanye West", "Drake"),
        ("Leonardo DiCaprio", "Brad Pitt"),
        ("Roger Federer", "Rafael Nadal"),
        ("Usain Bolt", "Carl Lewis"),
        ("Cristiano Ronaldo", "Diego Maradona"),
        ("Serena Williams", "Maria Sharapova"),
        ("Muhammad Ali", "Mike Tyson"),
        ("Angelina Jolie", "Scarlett Johansson"),
        ("Denzel Washington", "Morgan Freeman"),
        ("Jennifer Lopez", "Shakira"),
        ("Taylor Swift", "Ariana Grande"),
        ("Rihanna", "Beyoncé"),
        ("Drake", "The Weeknd"),
        ("Eminem", "Snoop Dogg"),
        ("Stephen King", "J.K. Rowling"),
        ("Arnold Schwarzenegger", "Sylvester Stallone"),
        ("Tom Hanks", "Harrison Ford"),
        ("Jennifer Aniston", "Courteney Cox"),
        ("Emma Watson", "Anne Hathaway"),
        ("Brad Pitt", "George Clooney"),
        ("Cristiano Ronaldo", "Pelé"),
        ("Lewis Hamilton", "Max Verstappen"),
        ("Mark Zuckerberg", "Larry Page"),
        ("Jay-Z", "Kanye West"),
        ("Justin Bieber", "Harry Styles"),
        ("Post Malone", "Travis Scott"),
        ("Hugh Jackman", "Chris Hemsworth"),
        ("Dwayne Johnson", "Jason Momoa"),
        ("Céline Dion", "Whitney Houston"),
        ("Ed Sheeran", "Shawn Mendes"),
        ("Lady Gaga", "Katy Perry"),
        ("Gordon Ramsay", "Jamie Oliver"),
        ("Jimmy Fallon", "James Corden"),
        ("Emma Stone", "Margot Robbie"),
        ("Bruce Lee", "Jackie Chan"),
        ("Tom Cruise", "Keanu Reeves"),
        ("Cristiano Ronaldo", "Kylian Mbappé"),
        ("Zlatan Ibrahimovic", "Erling Haaland"),
        ("Andrea Bocelli", "Luciano Pavarotti")
    ],
    "Personaggi Storici": [
        ("Giuseppe Garibaldi", "Camillo Benso di Cavour"),
        ("Cristoforo Colombo", "Amerigo Vespucci"),
        ("Charles Darwin", "Gregor Mendel"),
        ("Socrate", "Platone"),
        ("Aristotele", "Pitagora"),
        ("Julius Caesar", "Augusto"),
        ("Gengis Khan", "Attila"),
        ("Cleopatra", "Nefertiti"),
        ("Giovanna d'Arco", "Maria Antonietta"),
        ("Abramo Lincoln", "George Washington"),
        ("Benito Mussolini", "Adolf Hitler"),
        ("Karl Marx", "Friedrich Engels"),
        ("Mahatma Gandhi", "Nelson Mandela"),
        ("Winston Churchill", "Theodore Roosevelt"),
        ("Martin Luther King", "Malcolm X"),
        ("John F. Kennedy", "Richard Nixon"),
        ("Niccolò Machiavelli", "Sun Tzu"),
        ("Leonardo da Vinci", "Galileo Galilei"),
        ("Marie Curie", "Rosalind Franklin"),
        ("Nikola Tesla", "Thomas Edison"),
        ("Albert Einstein", "Max Planck"),
        ("Sigmund Freud", "Carl Jung"),
        ("Ludwig van Beethoven", "Wolfgang Amadeus Mozart"),
        ("Johann Sebastian Bach", "Franz Schubert"),
        ("Marco Polo", "Ferdinando Magellano"),
        ("James Cook", "Vasco da Gama"),
        ("Giulio Verne", "Isaac Asimov"),
        ("Napoleone Bonaparte", "Luigi XIV"),
        ("Fidel Castro", "Che Guevara"),
        ("Joseph Stalin", "Lenin"),
        ("Robespierre", "Danton"),
        ("San Francesco d’Assisi", "Sant’Agostino"),
        ("René Descartes", "Immanuel Kant"),
        ("John Locke", "Jean-Jacques Rousseau"),
        ("Simón Bolívar", "José de San Martín"),
        ("Antonio Gramsci", "Enrico Berlinguer"),
        ("Otto von Bismarck", "Francisco Franco"),
        ("William Shakespeare", "Dante Alighieri"),
        ("Voltaire", "Montesquieu"),
        ("Galileo Galilei", "Johannes Kepler"),
        ("Barack Obama", "Donald Trump"),
        ("Angela Merkel", "Margaret Thatcher"),
        ("Cleopatra", "Caterina la Grande"),
        ("Giordano Bruno", "Niccolò Copernico"),
        ("Tito", "Josip Broz"),
        ("John Maynard Keynes", "Adam Smith"),
        ("Francisco Goya", "Salvador Dalí"),
        ("Friedrich Nietzsche", "Arthur Schopenhauer"),
        ("Otto von Bismarck", "Mao Zedong"),
    ],

    "Giochi da Tavolo": [
        ("Scacchi", "Dama"),
        ("Risiko", "Monopoly"),
        ("Twister", "Jenga"),
        ("Trivial Pursuit", "Pictionary"),
        ("Battaglia Navale", "Forza 4"),
        ("Taboo", "Indovina Chi"),
        ("Backgammon", "Mahjong"),
        ("Uno", "Poker")
    ],
    "Supereroi": [
        ("Batman", "Daredevil"),
        ("Superman", "Shazam"),
        ("Iron Man", "War Machine"),
        ("Spiderman", "Miles Morales"),
        ("Thor", "Odino"),
        ("Hulk", "Abominio"),
        ("Deadpool", "Deathstroke"),
        ("Wolverine", "Sabretooth"),
        ("Doctor Strange", "Mandarino"),
        ("Black Panther", "Killmonger")
    ],
    "Miti e Leggende": [
        ("Zeus", "Giove"),
        ("Thor", "Odino"),
        ("Medusa", "Gorgone"),
        ("Achille", "Ettore"),
        ("Minotauro", "Centauro"),
        ("Fenice", "Drago"),
        ("Bigfoot", "Yeti"),
        ("Kraken", "Leviatano"),
        ("Pegaso", "Unicorno"),
        ("Chimera", "Grifone")
    ],
    "Cultura Pop": [
        ("Star Wars", "Star Trek"),
        ("Harry Potter", "Il Signore degli Anelli"),
        ("Marvel", "DC Comics"),
        ("Game of Thrones", "The Witcher"),
        ("Pokemon", "Digimon"),
        ("Dragon Ball", "Naruto"),
        ("One Piece", "Fairy Tail"),
        ("Disney", "Pixar"),
        ("Netflix", "Amazon Prime"),
        ("Facebook", "Instagram")
    ],
    "Cultura Generale": [
        ("Astronomia", "Astrologia"),
        ("Psicologia", "Psichiatria"),
        ("Filosofia", "Teologia"),
        ("Economia", "Finanza"),
        ("Letteratura", "Poesia"),
        ("Biologia", "Chimica"),
        ("Fisica", "Ingegneria"),
        ("Matematica", "Statistica"),
        ("Geografia", "Geologia"),
        ("Archeologia", "Storia")
    ],
    "Cose Inutili ma Divertenti": [
        ("Fidget Spinner", "Cubo di Rubik"),
        ("Slime", "Pallina Antistress"),
        ("Scherzi Telefonici", "Prank su YouTube"),
        ("Memes", "GIF"),
        ("Emoji", "Sticker"),
        ("ASMR", "Mukbang"),
        ("Tamagotchi", "Game Boy"),
        ("Fidget Cube", "Hand Spinner"),
        ("Selfie Stick", "Droni"),
        ("Troll", "Shitposting")
    ],
    "Parole Difficili": [
        ("Dodecaedro", "Ettagono"),
        ("Ossimoro", "Paradosso"),
        ("Idiosincrasia", "Apatia"),
        ("Antonomasia", "Metonimia"),
        ("Ellissi", "Sinestesia"),
        ("Tautologia", "Pleonasmo"),
        ("Eteroclito", "Omogeneo"),
        ("Disparato", "Dispotico"),
        ("Ortografia", "Grafia"),
        ("Apoftegma", "Massima")
    ],
    "Città": [
        ("Roma", "Milano"),
        ("Parigi", "Marsiglia"),
        ("New York", "Los Angeles"),
        ("Tokyo", "Osaka"),
        ("Londra", "Manchester"),
        ("Madrid", "Barcellona"),
        ("Berlino", "Monaco"),
        ("Mosca", "San Pietroburgo"),
        ("Buenos Aires", "Rio de Janeiro"),
        ("Sydney", "Melbourne"),
        ("Toronto", "Vancouver"),
        ("Pechino", "Shanghai"),
        ("Dubai", "Abu Dhabi"),
        ("Amsterdam", "Rotterdam"),
        ("Bangkok", "Phuket"),
        ("Chicago", "San Francisco"),
        ("Atene", "Salonicco"),
        ("Seul", "Busan"),
        ("Dublino", "Belfast"),
        ("Vienna", "Praga")
    ],
    "Geografia": [
        ("Everest", "Kilimangiaro"),
        ("Sahara", "Gobi"),
        ("Amazzonia", "Foresta Nera"),
        ("Caspio", "Baikal"),
        ("Mississippi", "Nilo"),
        ("Alpi", "Ande"),
        ("Siberia", "Alaska"),
        ("Antartide", "Groenlandia"),
        ("Himalaya", "Rocciose"),
        ("Bermuda", "Maldive"),
        ("Fiordi", "Geyser"),
        ("Deserto del Nevada", "Death Valley"),
        ("Isola di Pasqua", "Galapagos"),
        ("Tundra", "Taiga"),
        ("Grand Canyon", "Niagara Falls"),
        ("Mediterraneo", "Adriatico"),
        ("Suez", "Panama"),
        ("Tibet", "Nepal"),
        ("Amazzoni", "Gange"),
        ("Savane", "Steppe")
    ],
    "Nazioni": [
        ("Italia", "Francia"),
        ("Germania", "Austria"),
        ("Brasile", "Argentina"),
        ("Russia", "Ucraina"),
        ("Cina", "Giappone"),
        ("India", "Pakistan"),
        ("Messico", "Spagna"),
        ("Canada", "Stati Uniti"),
        ("Corea del Sud", "Vietnam"),
        ("Sudafrica", "Egitto"),
        ("Grecia", "Turchia"),
        ("Portogallo", "Brasile"),
        ("Norvegia", "Svezia"),
        ("Finlandia", "Danimarca"),
        ("Colombia", "Venezuela"),
        ("Cuba", "Giamaica"),
        ("Israele", "Palestina"),
        ("Arabia Saudita", "Iran"),
        ("Thailandia", "Indonesia"),
        ("Nuova Zelanda", "Australia")
    ],
    "Videogiochi": [
        ("Super Mario", "Sonic"),
        ("Minecraft", "Terraria"),
        ("Call of Duty", "Battlefield"),
        ("GTA", "Red Dead Redemption"),
        ("The Legend of Zelda", "Elden Ring"),
        ("The Sims", "Animal Crossing"),
        ("Final Fantasy", "Dragon Quest"),
        ("Dark Souls", "Bloodborne"),
        ("Pokémon", "Digimon"),
        ("FIFA", "PES"),
        ("Resident Evil", "Silent Hill"),
        ("Fallout", "Skyrim"),
        ("Metal Gear Solid", "Splinter Cell"),
        ("God of War", "Devil May Cry"),
        ("Cyberpunk 2077", "The Witcher 3"),
        ("Tetris", "Pac-Man")
    ],
    "Serie TV": [
        ("Breaking Bad", "Better Call Saul"),
        ("Game of Thrones", "House of the Dragon"),
        ("Stranger Things", "Dark"),
        ("The Office", "Parks and Recreation"),
        ("Friends", "How I Met Your Mother"),
        ("Sherlock", "Luther"),
        ("Westworld", "Black Mirror"),
        ("The Mandalorian", "Obi-Wan Kenobi"),
        ("The Witcher", "Vikings"),
        ("Squid Game", "Alice in Borderland"),
        ("The Boys", "Invincible"),
        ("Lost", "Prison Break"),
        ("Dexter", "Hannibal"),
        ("Rick and Morty", "Futurama"),
        ("Lucifer", "Supernatural"),
        ("Arrow", "The Flash"),
        ("Daredevil", "Jessica Jones"),
        ("BoJack Horseman", "Big Mouth"),
        ("Brooklyn Nine-Nine", "Scrubs")
    ],
"Parole Miste": [
    ("Sole", "Stella"),
    ("Luna", "Maree"),
    ("Montagna", "Neve"),
    ("Fiume", "Delta"),
    ("Foresta", "Liane"),
    ("Sabbia", "Deserto"),
    ("Onda", "Marea"),
    ("Piuma", "Cuscino"),
    ("Cristallo", "Vetro"),
    ("Fiamma", "Cenere"),
    ("Vento", "Aquilone"),
    ("Fumo", "Profumo"),
    ("Orologio", "Sveglia"),
    ("Labirinto", "Enigma"),
    ("Tramonto", "Crepuscolo"),
    ("Ombra", "Silhouette"),
    ("Silenzio", "Sussurro"),
    ("Speranza", "Promessa"),
    ("Ricordo", "Fotografia"),
    ("Segreto", "Diario"),
    ("Verità", "Confessione"),
    ("Destino", "Oracolo"),
    ("Caos", "Tornado"),
    ("Euforia", "Brivido"),
    ("Bussola", "Mappa"),
    ("Fossile", "Era"),
    ("Libro", "Manoscritto"),
    ("Storia", "Leggenda"),
    ("Museo", "Collezione"),
    ("Arte", "Pittura"),
    ("Scultura", "Statua"),
    ("Danza", "Balletto"),
    ("Teatro", "Sipario"),
    ("Attore", "Maschera"),
    ("Autore", "Romanzo"),
    ("Poeta", "Versi"),
    ("Melodia", "Sinfonia"),
    ("Canzone", "Ritornello"),
    ("Flauto", "Orchestra"),
    ("Tamburo", "Battito"),
    ("Gusto", "Aromi"),
    ("Cioccolato", "Fondente"),
    ("Spezie", "Zenzero"),
    ("Miele", "Dolcezza"),
    ("Tè", "Infusione"),
    ("Caffè", "Espresso"),
    ("Pane", "Forno"),
    ("Marmellata", "Confettura"),
    ("Olio", "Frantoio"),
    ("Bistecca", "Griglia"),
    ("Riso", "Sushi"),
    ("Pasta", "Tagliatelle"),
    ("Pizza", "Impasto"),
    ("Fontana", "Acquedotto"),
    ("Ponte", "Arco"),
    ("Cattedrale", "Campanile"),
    ("Castello", "Bastioni"),
    ("Grattacielo", "Vetrate"),
    ("Vicolo", "Acciottolato"),
    ("Metropolitana", "Tunnel"),
    ("Treno", "Binari"),
    ("Aereo", "Turbina"),
    ("Nave", "Bussola"),
    ("Automobile", "Motore"),
    ("Bicicletta", "Pedali"),
    ("Autostrada", "Casello"),
    ("Semaforo", "Strisce pedonali"),
    ("Moneta", "Tesoro"),
    ("Borsa", "Mercato"),
    ("Bancomat", "PIN"),
    ("Tesoro", "Scrigno"),
    ("Economia", "Finanza"),
    ("Scienza", "Esperimento"),
    ("Chimica", "Reazione"),
    ("Matematica", "Equazione"),
    ("Fisica", "Particelle"),
    ("Elettricità", "Conduttore"),
    ("Astronomia", "Telescopio"),
    ("Biologia", "Cellula"),
    ("Medicina", "Diagnosi"),
    ("Farmaco", "Ricetta"),
    ("Virus", "Vaccino"),
    ("Informatica", "Codice"),
    ("Videogioco", "Controller"),
    ("Internet", "Browser"),
    ("Social", "Hashtag"),
    ("Smartphone", "App"),
    ("Computer", "Processore"),
    ("Robot", "Automazione"),
    ("Saturno", "Anelli"),
    ("Marte", "Crateri"),
    ("Terra", "Continenti"),
    ("Oceano", "Abissi"),
    ("Foresta", "Radici"),
    ("Vulcano", "Magma"),
    ("Ghiacciaio", "Scioglimento"),
    ("Uragano", "Tifone"),
    ("Fulmine", "Saetta"),
    ("Luce", "Riflesso"),
    ("Specchio", "Immagine"),
    ("Vetro", "Trasparenza"),
    ("Pittura", "Pennello"),
    ("Musica", "Armonia"),
    ("Emozione", "Lacrime"),
    ("Risata", "Divertimento"),
    ("Bacio", "Passione"),
    ("Abbraccio", "Affetto"),
    ("Nostalgia", "Passato"),
    ("Segreto", "Sospetto"),
    ("Bugia", "Menzogna"),
    ("Destino", "Coincidenza"),
    ("Sogno", "Immaginazione"),
    ("Paura", "Brividi"),
    ("Fiducia", "Lealtà"),
    ("Avventura", "Esplorazione"),
    ("Nave", "Bussola"),
    ("Terremoto", "Scossa"),
    ("Cometa", "Meteorite"),
    ("Orologio", "Lancette"),
    ("Tempo", "Momento"),
    ("Galassia", "Nebulosa"),
    ("Mistero", "Enigma"),
    ("Indovinello", "Soluzione"),
    ("Veleno", "Antidoto"),
    ("Fuga", "Libertà"),
    ("Ombrello", "Pioggia"),
    ("Oasi", "Dune"),
    ("Biblioteca", "Enciclopedia"),
    ("Scaffale", "Libri"),
    ("Scenario", "Paesaggio"),
    ("Teatro", "Palcoscenico"),
    ("Statua", "Bronzo"),
    ("Dipinto", "Tela"),
    ("Murales", "Graffiti"),
    ("Racconto", "Paragrafo"),
    ("Romanzo", "Protagonista"),
    ("Autunno", "Foglie"),
    ("Primavera", "Boccioli"),
    ("Estate", "Sole"),
    ("Inverno", "Ghiaccio"),
    ("Viaggio", "Cartolina"),
    ("Strada", "Segnale"),
    ("Labirinto", "Mistero"),
    ("Biglietto", "Ingresso"),
    ("Salotto", "Divano"),
    ("Cucina", "Pentola"),
    ("Bagno", "Asciugamano"),
    ("Camera", "Cuscino"),
    ("Cantina", "Bottiglia"),
    ("Soffitta", "Bauli"),
    ("Muro", "Mattone"),
    ("Finestra", "Vista"),
    ("Cortile", "Giardino"),
    ("Terrazza", "Panorama"),
    ("Spazio", "Stazione orbitante"),
    ("Molecola", "Atomo"),
    ("Genetica", "DNA"),
    ("Neurone", "Cervello"),
    ("Ghiacciaio", "Artico"),
    ("Isola", "Arcipelago"),
    ("Fiume", "Affluente"),
    ("Fossile", "Dinosauro"),
    ("Astronave", "Missione"),
    ("Sottomarino", "Profondità"),
    ("Razzo", "Propulsione"),
    ("Porto", "Ancora"),
    ("Foresta", "Ecosistema"),
    ("Vulcano", "Eruzione"),
    ("Pianeta", "Orbita"),
    ("Burrasca", "Tornado"),
    ("Diga", "Centrale idroelettrica"),
    ("Radio", "Frequenza"),
    ("Fotografia", "Obiettivo"),
    ("Cinema", "Proiezione"),
    ("Pista", "Automobilismo"),
    ("Olimpiadi", "Medaglia"),
    ("Scultura", "Marmo")
]
}

EMOJIS = [
    "🕵️", "🕶️", "🧐", "👻", "🎭", "😎", "🦹", "🥷", "🤖", "👀", "🦸", "👺", "🐱‍👤", "🐲", "🐸", "🐍", "🐒", "🎭",
    "🦉", "🦡", "🦦", "🦘", "🦨", "🦩", "🦚", "🦜", "🦢", "🐉", "🐺", "🐙", "🐠", "🦈", "🐬", "🐲", "🦏", "🐘", "🦛",
    "🤡", "🎃", "🦹‍♂️", "🦹‍♀️", "🦸‍♂️", "🦸‍♀️", "😈", "👾", "💀", "👽", "👑", "👁️", "🦄", "🐧", "🐼", "🐨", "🦔"
]

SOPRANNOMI = [
    "se c’è da rubare, è già lì",
    "venderebbe sua madre per 5 euro (e lo ha fatto)",
    "ha più truffe aperte di un call center nigeriano",
    "l’unico che riesce a perdere soldi a rubare",
    "ha più condanne di un dittatore africano",
    "se fosse più falso, sarebbe un orgasmo femminile",
    "campione mondiale di fuga dalle responsabilità",
    "più tossico di un gruppo Telegram di incel",
    "ruberebbe pure i fiori a un funerale",
    "quello che ti chiede un favore e sparisce",
    "ladro di cuore… e di carte di credito",
    "ha più bugie in canna di una escort sposata",
    "campione olimpico di farla franca",
    "sa cambiare più facce di una camgirl in live",
    "il peggior errore dei suoi genitori (dopo il fratello)",
    "potrebbe corrompere un prete con due birre",
    "se c'è un errore genetico, è lui",
    "la sua fedeltà dura meno di un’erezione a pagamento",
    "sembra innocente, ma ha più amanti di Rocco Siffredi",
    "mentirebbe sul nome della madre per una birra gratis",
    "il motivo per cui il papà è andato a comprare le sigarette",
    "truffatore di vecchie sole e di MILF facili",
    "ladro di baci… e di portafogli",
    "ha venduto l’anima per il Wi-Fi gratis",
    "la moralità gli fa schifo più dei preliminari",
    "se gli offri una botta, accetta anche se sei suo cugino",
    "troppo stronzo per stare simpatico, ma ci prova lo stesso",
    "ha più scheletri nell’armadio di un serial killer",
    "farebbe sesso con un cactus per 10 euro",
    "ha fregato più soldi di una chiesa evangelica",
    "se c’è da fregare qualcuno, lui ha già fatto il bonifico",
    "mentirebbe su un test di paternità per sport",
    "si fa le ex degli amici per principio",
    "ha più mogli nascoste di un emiro arabo",
    "potrebbe vendere ghiaccio agli eschimesi e scappare coi soldi",
    "farebbe un porno solo per non pagare l’affitto",
    "se c'è da sparare una cazzata, è già in mira",
    "campione mondiale di ghosting e fregature",
    "venderebbe il suo culo, ma a caro prezzo",
    "noto per scappare prima di pagare il taxi… e il figlio",
    "fa più danni di un vibratore senza batterie",
    "la sua coscienza è in ferie da quando è nato",
    "quando dice 'ti amo', sta già fregando qualcun altro",
    "venderebbe sua sorella per una ricarica Vodafone",
    "vive a scrocco come una suocera in vacanza",
    "se fosse più stronzo, lo scagionerebbero per eccesso di bastardaggine",
    "ha più debiti di un casinò in bancarotta",
    "se ti dice 'fidati', nascondi il portafogli e le figlie",
    "se c'è un colpevole, ha un alibi migliore",
    "se ti giura amore eterno, cambia casa",
    "più bugiardo di un uomo sposato in trasferta",
    "ha lasciato più ragazze incinte che i film di Rocco Siffredi",
    "la sua firma è già su troppi assegni scoperti",
    "se vedi il suo nome su un contratto, è truffa",
    "ha più ex che rimorsi, e nessuno dei due gli interessa",
    "sembra onesto, ma ha più lati oscuri di un porno giapponese",
    "potrebbe insegnare all’FBI come sparire nel nulla",
    "ha fregato così tante donne che Tinder gli ha dato il ban a vita",
    "se c'è una figa, lui è già lì (e l’ha già rovinata)",
    "più paraculo di un oroscopo personalizzato",
    "la sua promessa di fedeltà è una barzelletta in 12 lingue",
    "ha più nomi falsi di un agente sotto copertura",
    "sembra un amico, ma ha già il coltello pronto",
    "ha più doppie vite di un browser in incognito",
    "se lo vedi con la tua ragazza, è già tardi",
    "potrebbe convincerti che tua madre è adottata",
    "se c'è un prete, gli confessa una bugia per allenamento",
    "più ambiguo di un messaggio alle 3 di notte",
    "se gli presti soldi, è come regalarli alla mafia",
    "ha più segreti di un’avvocatessa divorzista",
    "se c'è un bar, è già ubriaco e senza portafoglio",
    "ha più cazzate in bocca di un televenditore di pentole",
    "nato per mentire, cresciuto per imbrogliare",
    "può venderti la sabbia del Sahara come spiaggia privata",
    "se dice che è gay, sta solo cercando di farsi tua sorella"
]

RUOLI_DISPONIBILI = {
    "Clown 🤡": "Conosce la parola e vince solo se viene eliminato.",
    "Traditore 🕵️‍♂️": "Sa chi è l’impostore e cerca di aiutarlo di nascosto. - Vince se gli impostori rimangono in vita",
    "Veggente 🔮": "Conosce il nome di uno dei giocatori buoni. - Vince se i buoni rimangono in vita",
    "Vendicatore ⚔️": "Se viene eliminato, sceglie un giocatore da portare con sé nella sconfitta."
}

DOMANDE = {
    # 🎵 MUSICA
    "Cantanti": [
        "Qual è il tuo cantante preferito?",
        "Se potessi cenare con un cantante, chi sceglieresti?",
        "Quale cantante non sopporti?",
        "Se potessi avere la voce di un cantante, chi sceglieresti?",
        "Quale cantante ha la migliore presenza scenica?"
    ],
    "Canzoni": [
        "Qual è l'ultima canzone che hai ascoltato?",
        "Quale canzone ti fa sempre emozionare?",
        "Se dovessi scegliere una canzone per descrivere la tua vita, quale sarebbe?",
        "Quale canzone odi di più?",
        "Qual è la colonna sonora perfetta per un viaggio in auto?"
    ],
    "Generi Musicali": [
        "Qual è il tuo genere musicale preferito?",
        "Quale genere musicale non ti piace?",
        "Se potessi eliminare un genere musicale, quale sarebbe?",
        "Quale genere musicale è sopravvalutato?",
        "Qual è il miglior decennio per la musica?"
    ],
    "Strumenti Musicali": [
        "Quale strumento musicale vorresti saper suonare?",
        "Quale strumento ti rappresenta di più?",
        "Quale strumento ha il suono più fastidioso?",
        "Se potessi essere un maestro in uno strumento, quale sceglieresti?"
    ],

    # 🍕 CIBO
    "Primi Piatti": [
        "Qual è il tuo primo piatto preferito?",
        "Qual è il peggior condimento per la pasta?",
        "Quale primo piatto cucini meglio?"
    ],
    "Secondi Piatti": [
        "Qual è il secondo piatto più sopravvalutato?",
        "Qual è il piatto che odi di più?",
        "Il secondo più strano che hai mangiato.",
    ],
    "Dolci": [
        "Qual è il tuo dolce preferito?",
        "Qual è il peggior dolce che hai mai assaggiato?",
        "Se potessi mangiare solo un dolce per il resto della vita, quale sarebbe?"
    ],
    "Bevande": [
        "Qual è la tua bevanda preferita?",
        "Quale cocktail ordini più spesso?",
        "Quale bevanda non berresti mai?"
    ],
    "Fast Food": [
        "Qual è la tua catena di fast food preferita?",
        "Quale panino del McDonald's è il migliore?",
        "Qual è la catena di fast food peggiore?",
    ],

    # 🎥 CINEMA E SERIE TV
    "Film": [
        "Qual è il tuo film preferito?",
        "Qual è stato il film che ti ha fatto piangere?",
        "Qual è il film più sopravvalutato di sempre?",
        "Qual è il film peggiore che tu abbia mai visto?",
    ],
    "Serie TV": [
        "Qual è la serie TV che hai amato di più?",
        "Quale serie TV ti ha deluso?",
        "Quale serie TV hai mollato dopo poche puntate?",
    ],
    "Registi": [
        "Chi è il tuo regista preferito?",
        "Quale regista ha cambiato la storia del cinema?",
        "Quale regista è sopravvalutato?",
        "Quale regista dovrebbe smettere di fare film?"
    ],
    "Attori": [
        "Chi è il tuo attore/attrice preferito/a?",
        "Qual è l’attore/attrice più bravo/a secondo te?",
        "Quale attore/attrice odi?",
        "Quale attore/attrice ha il miglior carisma?",
        "Se potessi essere un attore/attrice per un giorno, chi saresti?"
    ],

    # ✈️ VIAGGI E LUOGHI
    "Destinazioni da sogno": [
        "Qual è stato il viaggio più bello che hai fatto?",
        "Quale città visiteresti subito se potessi?"
    ],
    "Luoghi da evitare": [
        "Qual è stato il peggior viaggio della tua vita?",
        "Quale città non visiteresti mai?",
        "Quale meta turistica è sopravvalutata?",
        "Quale luogo non visiteresti nemmeno se ti pagassero?"
    ],

    # 🎮 HOBBY E PASSIONI
    "Videogiochi": [
        "Qual è il tuo videogioco preferito?",
        "Quale gioco odi ma tutti amano?",
        "Qual è stato il primo videogioco che hai giocato?"
    ],
    "Sport e attività": [
        "Qual è il tuo sport preferito?",
        "Se potessi essere un campione in uno sport, quale sceglieresti?"
    ],

    # 🔥 HOT E ARGOMENTI TABÙ
    "Sesso": [
        "Il peggior posto dove fare sesso?",
        "Qual è la tua fantasia più strana?",
        "Qual è la posizione più sopravvalutata?"
    ],
}

# Mappa per associare gli utenti alle loro sessioni di Socket.IO
client_sessions = {}

DEBUG = True
