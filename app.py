from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room, send
import random
import string

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Dizionario per tenere traccia delle stanze
stanze = {}


# Funzione per generare codici di stanza casuali
def genera_codice():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/crea_stanza", methods=["POST"])
def crea_stanza():
    codice = genera_codice()
    parola = request.json.get("parola")

    stanze[codice] = {
        "giocatori": {},
        "parola": parola,
        "impostore": None
    }
    return jsonify({"codice": codice})


@app.route("/unisciti", methods=["POST"])
def unisciti():
    data = request.json
    codice = data.get("codice")
    nome = data.get("nome")

    if codice not in stanze:
        return jsonify({"errore": "Stanza inesistente"}), 400

    stanze[codice]["giocatori"][nome] = None
    return jsonify({"successo": True})


@socketio.on("start_game")
def start_game(data):
    codice = data["codice"]
    if codice in stanze:
        impostore = random.choice(list(stanze[codice]["giocatori"].keys()))
        stanze[codice]["impostore"] = impostore

        for giocatore in stanze[codice]["giocatori"]:
            if giocatore == impostore:
                socketio.emit("word", {"parola": "Sei l'impostore!"}, room=giocatore)
            else:
                socketio.emit("word", {"parola": stanze[codice]["parola"]}, room=giocatore)


@socketio.on("join")
def handle_join(data):
    codice = data["codice"]
    nome = data["nome"]
    join_room(nome)  # Usa il nome come "stanza" personale
    send(f"{nome} si è unito alla stanza {codice}", to=codice)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
