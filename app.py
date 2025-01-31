from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, emit
import random

app = Flask(__name__)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"  # Usa "eventlet" per supporto WebSocket su Render
)
stanze = {}

CATEGORIE = {
    "Animali": ["Leone", "Giraffa", "Panda", "Tigre", "Elefante", "Canguro", "Lupo", "Volpe", "Pinguino", "Orso Polare",
                "Delfino", "Aquila"],
    "Oggetti": ["Telefono", "Orologio", "Zaino", "Sedia", "Computer", "Lampada", "Chitarra", "Bicicletta", "Forbici",
                "Microonde", "Telecomando"],
    "Cibi": ["Pizza", "Pasta", "Gelato", "Hamburger", "Sushi", "Cioccolato", "Lasagna", "Hot Dog", "Torta", "Insalata",
             "Patatine", "Frittata"],
    "Film": ["Titanic", "Inception", "Matrix", "Interstellar", "Pulp Fiction", "Il Padrino", "Avatar", "Jurassic Park",
             "Star Wars", "Harry Potter"],
    "Personaggi Famosi": ["Albert Einstein", "Leonardo da Vinci", "Elvis Presley", "Michael Jackson", "Napoleone",
                          "Cristoforo Colombo", "Cleopatra"],
    "Personaggi di Finzione": ["Batman", "Superman", "Sherlock Holmes", "Harry Potter", "Darth Vader", "Spiderman",
                               "Topolino", "Gandalf", "Homer Simpson"],
    "Luoghi": ["Roma", "New York", "Tokyo", "Parigi", "Londra", "Sydney", "Pechino", "Mosca", "Rio de Janeiro", "Dubai",
               "Berlino", "Los Angeles"],
    "Sport": ["Calcio", "Basket", "Tennis", "Nuoto", "Atletica", "Sci", "Golf", "Boxe", "Motociclismo", "Rugby",
              "Pallavolo"],
    "Videogiochi": ["Super Mario", "Minecraft", "Fortnite", "The Legend of Zelda", "GTA", "League of Legends",
                    "Call of Duty", "Pac-Man", "Doom", "Tetris"],
    "Miti e Leggende": ["Medusa", "Thor", "Zeus", "Pegaso", "Fenice", "Bigfoot", "Dracula", "Nessie", "Minotauro",
                        "Ciclopi", "Chupacabra"],
    "Emozioni e Sentimenti": ["Felicità", "Tristezza", "Paura", "Rabbia", "Amore", "Noia", "Gelosia", "Ansia",
                              "Sorpresa", "Timidezza"]
}

EMOJIS = [
    "🕵️", "🕶️", "🧐", "👻", "🎭", "😎", "🦹", "🥷", "🤖", "👀", "🦸", "👺", "🐱‍👤", "🐲", "🐸", "🐍", "🐒", "🎭",
    "🦉", "🦡", "🦦", "🦘", "🦨", "🦩", "🦚", "🦜", "🦢", "🐉", "🐺", "🐙", "🐠", "🦈", "🐬", "🐲", "🦏", "🐘", "🦛",
    "🤡", "🎃", "🦹‍♂️", "🦹‍♀️", "🦸‍♂️", "🦸‍♀️", "😈", "👾", "💀", "👽", "👑", "👁️", "🦄", "🐧", "🐼", "🐨", "🦔"
]

SOPRANNOMI = [
    "sarà sicuro l'impostore...",
    "tranquilli, non sa bluffare",
    "il cacciatore di passere",
    "la piccola fiammiferaia",
    "agente 00 tette",
    ", la mia fatina preferita",
    "mangia spaghetti professionista",
    "il ninja delle fogne",
    "il finto vegano",
    "re dei bidoni",
    "campione mondiale di nascondino",
    "ladro di patatine",
    "più lento di una tartaruga",
    "la volpe astuta",
    "il detective senza indizi",
    "quello che non capisce le battute",
    "lo stratega dell'ultimo secondo",
    "l’ombra nella notte",
    "quello che fa sempre finta di sapere",
    "il maestro dei tranelli",
    "il bugiardo più onesto",
    "non ha mai visto un film di spionaggio",
    "il re del bluff (o forse no?)",
    "il fuggitivo senza meta",
    "sempre sospetto ma mai colpevole",
    "quello che dice sempre 'non sono io!'",
    "il mago delle scuse",
    "fa finta di capire il gioco",
    "quello che dimentica sempre le regole",
    "la mente criminale (o solo casualità?)"
]

# Mappa per associare gli utenti alle loro sessioni di Socket.IO
client_sessions = {}

DEBUG = True


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/categorie_disponibili", methods=["GET"])
def categorie_disponibili():
    """Restituisce la lista delle categorie disponibili"""
    return jsonify({"categorie": list(CATEGORIE.keys())})


@socketio.on("connect")
def handle_connect():
    print(f"Nuova connessione: {request.sid}")  # Log della connessione


@app.route("/crea_stanza", methods=["POST"])
def crea_stanza():
    data = request.json
    categorie_scelte = data.get("categorie", list(CATEGORIE.keys()))  # Se nessuna scelta, usa tutte

    if not categorie_scelte:
        return jsonify({"errore": "Devi selezionare almeno una categoria!"}), 400

    codice = str(random.randint(1000, 9999))

    # Salva solo le categorie scelte nella stanza
    stanze[codice] = {
        "categorie_scelte": categorie_scelte,
        "parola": None,
        "categoria": None,
        "giocatori": {},
        "impostore": None,
        "parole_usate": [],
        "punteggi": {},
        "punteggio_assegnato": False
    }

    return jsonify({"codice": codice})



def aggiorna_giocatori(codice):
    """Aggiorna la lista dei giocatori e classifica per tutti nella stanza"""
    if codice not in stanze:
        return  # Evita errori se la stanza non esiste più

    # Ordina i giocatori per punteggio (dal più alto al più basso)
    classifica = sorted(stanze[codice]["giocatori"].keys(), key=lambda x: stanze[codice]["punteggi"].get(x, 0), reverse=True)

    # Emoji per la classifica (🥇, 🥈, 🥉, nessuna medaglia dal 4° posto in poi)
    MEDAGLIE = ["🥇", "🥈", "🥉"]

    # Costruisce la classifica con medaglie
    giocatori_classifica = {
        n: f"{MEDAGLIE[i] if i < len(MEDAGLIE) else '🏅'} {info['emoji']} {n}, {info['soprannome']} - {stanze[codice]['punteggi'].get(n, 0)} punti"
        for i, n in enumerate(classifica)
        for info in [stanze[codice]["giocatori"][n]]
    }

    # Manda la classifica aggiornata a tutti nella stanza
    socketio.emit("aggiorna_giocatori", {"giocatori": giocatori_classifica}, room=codice)



@app.route("/unisciti", methods=["POST"])
def unisciti():
    data = request.json
    codice = data["codice"]
    nome = data["nome"]

    if codice not in stanze:
        return jsonify({"errore": "Stanza inesistente"}), 400

    if nome in stanze[codice]["giocatori"]:
        return jsonify({"errore": "Nome già usato nella stanza"}), 400

    # Genera emoji e soprannome casuale
    emoji = random.choice(EMOJIS)
    soprannome = random.choice(SOPRANNOMI)

    # **AGGIORNA il dizionario PRIMA di emettere il messaggio**
    stanze[codice]["giocatori"][nome] = {"emoji": emoji, "soprannome": soprannome}

    # Notifica tutti gli utenti della stanza, incluso il nuovo giocatore
    aggiorna_giocatori(codice)

    return jsonify({"successo": True, "soprannome": soprannome})


@app.route("/gestisci_partita", methods=["POST"])
def gestisci_partita():
    """Avvia la partita (se prima volta) o genera una nuova parola per la stanza"""
    data = request.json
    codice = data["codice"]

    if codice not in stanze:
        return jsonify({"errore": "Stanza inesistente"}), 400

    # Filtra le categorie disponibili in base a quelle scelte dall'host
    categorie_disponibili = {c: CATEGORIE[c] for c in stanze[codice]["categorie_scelte"] if c in CATEGORIE}
    if not categorie_disponibili:
        return jsonify({"errore": "Nessuna categoria valida selezionata!"}), 400

    categoria, parole = random.choice(list(categorie_disponibili.items()))

    # Evita parole già usate
    parole_disponibili = [p for p in parole if p not in stanze[codice]["parole_usate"]]
    if not parole_disponibili:
        return jsonify({"errore": "Nessuna parola disponibile, cambia categoria!"}), 400

    parola_segreta = random.choice(parole_disponibili)
    stanze[codice]["parola"] = parola_segreta
    stanze[codice]["categoria"] = categoria
    stanze[codice]["parole_usate"].append(parola_segreta)

    # Riassegna un nuovo impostore
    giocatori = list(stanze[codice]["giocatori"].keys())
    if len(giocatori) < 2 and not DEBUG:
        return jsonify({"errore": "Servono almeno 2 giocatori per iniziare"}), 400

    impostore = random.choice(giocatori)
    stanze[codice]["impostore"] = impostore
    stanze[codice]["punteggio_assegnato"] = False  # Resetta la possibilità di assegnare punti

    # Invia la parola segreta a tutti i giocatori della stanza
    for sid, info in client_sessions.items():
        if info["codice"] == codice:
            if info["nome"] == impostore:
                socketio.emit("parola_segreta", {
                    "categoria": categoria,
                    "parola": " 👀 Sei l'IMPOSTORE! Non conosci la parola. 👀"
                }, to=sid)
            else:
                socketio.emit("parola_segreta", {
                    "categoria": categoria,
                    "parola": parola_segreta
                }, to=sid)

    return jsonify({"successo": True, "parola": parola_segreta, "categoria": categoria})


@socketio.on("join_room")
def join_room_event(data):
    codice = data["codice"]
    nome = data["nome"]

    join_room(codice)  # Il client entra nella stanza
    client_sessions[request.sid] = {"nome": nome, "codice": codice}

    # Invia la lista aggiornata anche al nuovo giocatore
    aggiorna_giocatori(codice)


@app.route("/assegna_punti", methods=["POST"])
def assegna_punti():
    data = request.json
    codice = data["codice"]
    esito = data["esito"]  # "impostore_fugge", "impostore_indovina", "impostore_non_indovina"

    if codice not in stanze or stanze[codice]["punteggio_assegnato"]:
        return jsonify({"errore": "Punti già assegnati o stanza inesistente"}), 400

    impostore = stanze[codice]["impostore"]
    giocatori = stanze[codice]["giocatori"]

    if esito == "impostore_fugge":
        stanze[codice]["punteggi"][impostore] = stanze[codice]["punteggi"].get(impostore, 0) + 2
    elif esito == "impostore_indovina":
        stanze[codice]["punteggi"][impostore] = stanze[codice]["punteggi"].get(impostore, 0) + 1
    elif esito == "impostore_non_indovina":
        stanze[codice]["punteggi"][impostore] = stanze[codice]["punteggi"].get(impostore, 0)
        for giocatore in giocatori:
            if giocatore != impostore:
                stanze[codice]["punteggi"][giocatore] = stanze[codice]["punteggi"].get(giocatore, 0) + 2

    stanze[codice]["punteggio_assegnato"] = True  # Blocca doppia assegnazione

    aggiorna_giocatori(codice)

    return jsonify({"successo": True})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
