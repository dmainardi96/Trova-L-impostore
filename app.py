from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, emit
import random

from config import CATEGORIE, stanze, EMOJIS, SOPRANNOMI, DEBUG, client_sessions

app = Flask(__name__)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"  # Usa "eventlet" per supporto WebSocket su Render
)

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
    codice = str(random.randint(1000, 9999))

    # Salva solo le categorie scelte nella stanza
    stanze[codice] = {
        "categorie_scelte": list(CATEGORIE.keys()),
        "parola": None,
        "categoria": None,
        "giocatori": {},
        "impostore": None,
        "parole_usate": [],
        "punteggi": {},
        "punteggio_assegnato": False,
        "modalita": None,
        "num_impostori": 1
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

    # Se il nome esiste già, semplicemente lo ricolleghiamo alla stanza
    if nome in stanze[codice]["giocatori"]:
        return jsonify({
            "successo": True,
            "soprannome": stanze[codice]["giocatori"][nome]["soprannome"],
            "emoji": stanze[codice]["giocatori"][nome]["emoji"],
            "nome": nome
        })

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
    data = request.json
    codice = data["codice"]

    if codice not in stanze:
        return jsonify({"errore": "Stanza inesistente"}), 400

    # Filtra le categorie disponibili in base a quelle scelte dall'host
    categorie_disponibili = [c for c in stanze[codice]["categorie_scelte"] if c in CATEGORIE]

    if not categorie_disponibili:
        return jsonify({"errore": "Nessuna categoria valida selezionata!"}), 400

    # Seleziona una categoria casuale
    categoria = random.choice(categorie_disponibili)

    # Seleziona una coppia di parole (parola normale, variante impostore)
    parola_coppia = random.choice(CATEGORIE[categoria])
    parola_segreta, parola_variante = parola_coppia

    stanze[codice]["parola"] = parola_segreta
    stanze[codice]["categoria"] = categoria
    stanze[codice]["parole_usate"].append(parola_segreta)

    # Riassegna un nuovo impostore
    giocatori = list(stanze[codice]["giocatori"].keys())
    if len(giocatori) < 2 and not DEBUG:
        return jsonify({"errore": "Servono almeno 2 giocatori per iniziare"}), 400

    num_impostori = min(stanze[codice]["num_impostori"], len(giocatori) - 1)
    stanze[codice]["impostori"] = random.sample(giocatori, num_impostori)
    stanze[codice]["punteggio_assegnato"] = False  # Resetta la possibilità di assegnare punti

    # Se modalità "Little Secret", impostore riceve una parola diversa
    parola_impostore = parola_segreta
    if stanze[codice].get("modalita") == "little_secret":
        parola_impostore = parola_variante

    # Invia le parole ai giocatori
    for sid, info in client_sessions.items():
        if info["codice"] == codice:
            if info["nome"] in stanze[codice]["impostori"]:
                parola = parola_impostore if stanze[codice].get("modalita") == "little_secret" else " 👀 Sei l'IMPOSTORE! Non conosci la parola. 👀"
            else:
                parola = parola_segreta

            socketio.emit("parola_segreta", {"categoria": categoria,
                                             "parola": parola,
                                             "imposter": info["nome"] in stanze[codice]["impostori"]}, to=sid)


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
    esito = data["esito"]

    if codice not in stanze or stanze[codice]["punteggio_assegnato"]:
        return jsonify({"errore": "Punti già assegnati o stanza inesistente"}), 400

    impostori = stanze[codice]["impostori"]
    giocatori = stanze[codice]["giocatori"]

    if esito == "impostore_fugge":
        for impostore in impostori:
            stanze[codice]["punteggi"][impostore] = stanze[codice]["punteggi"].get(impostore, 0) + 2
    elif esito == "impostore_indovina":
        for impostore in impostori:
            stanze[codice]["punteggi"][impostore] = stanze[codice]["punteggi"].get(impostore, 0) + 1
    elif esito == "impostore_non_indovina":
        for impostore in impostori:
            stanze[codice]["punteggi"][impostore] = stanze[codice]["punteggi"].get(impostore, 0)
        for giocatore in giocatori:
            if giocatore not in impostori:
                stanze[codice]["punteggi"][giocatore] = stanze[codice]["punteggi"].get(giocatore, 0) + 2

    stanze[codice]["punteggio_assegnato"] = True

    aggiorna_giocatori(codice)

    return jsonify({"successo": True})


@app.route("/modifica_impostazioni", methods=["POST"])
def modifica_impostazioni():
    data = request.json
    codice = data.get("codice")
    nuove_impostazioni = data.get("impostazioni")
    print(nuove_impostazioni)
    if codice not in stanze:
        return jsonify({"errore": "Stanza inesistente"}), 400

    for chiave, valore in nuove_impostazioni.items():
        if chiave == "num_impostori":
            stanze[codice][chiave] = int(valore)  # Cast a int qui
        elif chiave in ["categorie_scelte", "modalita"]:
            stanze[codice][chiave] = valore

    socketio.emit("aggiorna_impostazioni", {"impostazioni": nuove_impostazioni}, room=codice)
    return jsonify({"successo": True, "messaggio": "Impostazioni aggiornate"})


@app.route("/verifica_impostore", methods=["POST"])
def verifica_impostore():
    data = request.json
    codice = data["codice"]
    nome = data["nome"]

    if codice not in stanze or nome not in stanze[codice]["giocatori"]:
        return jsonify({"errore": "Giocatore o stanza non trovati."}), 400

    impostore = stanze[codice]["impostore"]
    e_impostore = (nome == impostore)

    return jsonify({"successo": True, "impostore": e_impostore})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
