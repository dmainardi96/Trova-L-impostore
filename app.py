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
    "Animali": ["Leone", "Giraffa", "Panda", "Tigre", "Elefante", "Canguro", "Lupo", "Volpe", "Pinguino", "Orso Polare", "Delfino", "Aquila"],
    "Oggetti": ["Telefono", "Orologio", "Zaino", "Sedia", "Computer", "Lampada", "Chitarra", "Bicicletta", "Forbici", "Microonde", "Telecomando"],
    "Cibi": ["Pizza", "Pasta", "Gelato", "Hamburger", "Sushi", "Cioccolato", "Lasagna", "Hot Dog", "Torta", "Insalata", "Patatine", "Frittata"],
    "Film": ["Titanic", "Inception", "Matrix", "Interstellar", "Pulp Fiction", "Il Padrino", "Avatar", "Jurassic Park", "Star Wars", "Harry Potter"],
    "Personaggi Famosi": ["Albert Einstein", "Leonardo da Vinci", "Elvis Presley", "Michael Jackson", "Napoleone", "Cristoforo Colombo", "Cleopatra"],
    "Personaggi di Finzione": ["Batman", "Superman", "Sherlock Holmes", "Harry Potter", "Darth Vader", "Spiderman", "Topolino", "Gandalf", "Homer Simpson"],
    "Luoghi": ["Roma", "New York", "Tokyo", "Parigi", "Londra", "Sydney", "Pechino", "Mosca", "Rio de Janeiro", "Dubai", "Berlino", "Los Angeles"],
    "Sport": ["Calcio", "Basket", "Tennis", "Nuoto", "Atletica", "Sci", "Golf", "Boxe", "Motociclismo", "Rugby", "Pallavolo"],
    "Videogiochi": ["Super Mario", "Minecraft", "Fortnite", "The Legend of Zelda", "GTA", "League of Legends", "Call of Duty", "Pac-Man", "Doom", "Tetris"],
    "Miti e Leggende": ["Medusa", "Thor", "Zeus", "Pegaso", "Fenice", "Bigfoot", "Dracula", "Nessie", "Minotauro", "Ciclopi", "Chupacabra"],
    "Emozioni e Sentimenti": ["Felicità", "Tristezza", "Paura", "Rabbia", "Amore", "Noia", "Gelosia", "Ansia", "Sorpresa", "Timidezza"]
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

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on("connect")
def handle_connect():
    print(f"Nuova connessione: {request.sid}")  # Log della connessione

@app.route("/crea_stanza", methods=["POST"])
def crea_stanza():
    codice = str(random.randint(1000, 9999))
    categoria, parole = random.choice(list(CATEGORIE.items()))
    parola_segreta = random.choice(parole)

    stanze[codice] = {
        "parola": parola_segreta,
        "categoria": categoria,
        "giocatori": {},
        "impostore": None
    }

    return jsonify({"codice": codice})

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
    socketio.emit("aggiorna_giocatori", {
        "giocatori": {n: f"{info['emoji']} {n}, {info['soprannome']}" for n, info in stanze[codice]["giocatori"].items()}
    }, room=codice)

    return jsonify({"successo": True, "soprannome": soprannome})

@app.route("/inizia_gioco", methods=["POST"])
def inizia_gioco():
    data = request.json
    codice = data["codice"]

    if codice not in stanze:
        return jsonify({"errore": "Stanza inesistente"}), 400

    # Se non è stato scelto un impostore, sceglilo ora
    if stanze[codice]["impostore"] is None:
        giocatori = list(stanze[codice]["giocatori"].keys())
        if len(giocatori) < 2:
            return jsonify({"errore": "Servono almeno 2 giocatori per iniziare"}), 400

        impostore = random.choice(giocatori)
        stanze[codice]["impostore"] = impostore  # Salviamo l'impostore per tutta la partita

    impostore = stanze[codice]["impostore"]
    parola = stanze[codice]["parola"]
    categoria = stanze[codice]["categoria"]

    # Invia un messaggio personalizzato a ogni giocatore nella stanza
    for sid, info in client_sessions.items():
        if info["codice"] == codice:  # Verifica che l'utente sia nella stanza
            if info["nome"] == impostore:
                socketio.emit("parola_segreta", {
                    "categoria": categoria,
                    "parola": "Sei l'IMPOSTORE! Non conosci la parola."
                }, to=sid)
            else:
                socketio.emit("parola_segreta", {
                    "categoria": categoria,
                    "parola": parola
                }, to=sid)

    return jsonify({"successo": True, "impostore": impostore})

@socketio.on("join_room")
def join_room_event(data):
    codice = data["codice"]
    nome = data["nome"]

    join_room(codice)  # Il client entra nella stanza
    client_sessions[request.sid] = {"nome": nome, "codice": codice}

    # Invia la lista aggiornata anche al nuovo giocatore
    emit("aggiorna_giocatori", {
        "giocatori": {n: f"{info['emoji']} {n}, {info['soprannome']}" for n, info in stanze[codice]["giocatori"].items()}
    }, to=request.sid)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
