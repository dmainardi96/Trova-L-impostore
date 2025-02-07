from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, emit
import random

from config import CATEGORIE, stanze, EMOJIS, SOPRANNOMI, DEBUG, client_sessions, RUOLI_DISPONIBILI, DOMANDE

app = Flask(__name__)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"  # Usa "eventlet" per supporto WebSocket su Render
)

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/ruoli_disponibili", methods=["GET"])
def ruoli_disponibili():
    return jsonify({"ruoli": RUOLI_DISPONIBILI})


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
        "num_impostori": 1,
        "owner": None
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
            "nome": nome,
            "owner": stanze[codice]['owner'] == nome
        })

    # Genera emoji e soprannome casuale
    emoji = random.choice(EMOJIS)
    soprannome = random.choice(SOPRANNOMI)

    # **AGGIORNA il dizionario PRIMA di emettere il messaggio**
    stanze[codice]["giocatori"][nome] = {"emoji": emoji, "soprannome": soprannome}

    # Notifica tutti gli utenti della stanza, incluso il nuovo giocatore
    aggiorna_giocatori(codice)

    return jsonify({"successo": True, "soprannome": soprannome, "owner": stanze[codice]['owner'] == nome})


@app.route("/gestisci_partita", methods=["POST"])
def gestisci_partita():
    data = request.json
    codice = data["codice"]
    owner = data["nome"]
    stanze[codice]['owner'] = owner

    if codice not in stanze:
        return jsonify({"errore": "Stanza inesistente"}), 400

    # Filtra le categorie disponibili in base a quelle scelte dall'host
    if not stanze[codice]["categorie_scelte"] or stanze[codice]["categorie_scelte"] == []:
        stanze[codice]["categorie_scelte"] = CATEGORIE

    categorie_disponibili = [c for c in stanze[codice]["categorie_scelte"] if c in CATEGORIE]

    if not categorie_disponibili:
        return jsonify({"errore": "Nessuna categoria valida selezionata!"}), 400

    vere_domande = ""
    if stanze[codice].get("modalita") == "domande":
        categorie_domande = random.sample(list(DOMANDE.keys()), 3)  # Seleziona 3 categorie casuali
        domande_associate = [(categoria, random.choice(DOMANDE[categoria])) for categoria in categorie_domande]

        parola_segreta = "\n".join([f"{cat}: {dom}" for cat, dom in domande_associate])  # Associa domande e categorie
        categoria = ", ".join(categorie_domande)  # L'impostore vede solo le categorie
        vere_domande = parola_segreta
    else:
        # Seleziona una categoria casuale
        categoria = random.choice(categorie_disponibili)

        # Seleziona una coppia di parole (parola normale, variante impostore)
        parola_coppia = list(random.choice(CATEGORIE[categoria]))  # Converte la tupla in una lista
        random.shuffle(parola_coppia)  # Mescola la coppia
        parola_segreta, parola_variante = parola_coppia[0], parola_coppia[1]  # Ora è casuale

    stanze[codice]["parola"] = parola_segreta
    stanze[codice]["categoria"] = categoria
    stanze[codice]["parole_usate"].append(parola_segreta)

    # Riassegna un nuovo impostore
    giocatori = list(stanze[codice]["giocatori"].keys())
    if len(giocatori) < 2 and not DEBUG:
        return jsonify({"errore": "Servono almeno 2 giocatori per iniziare"}), 400

    num_impostori = min(stanze[codice]["num_impostori"], len(giocatori) - 1)
    stanze[codice]["impostori"] = random.sample(giocatori, num_impostori)
    stanze[codice]["punteggio_assegnato"] = False

    # Assegna ruoli casuali con descrizione (solo se ci sono abbastanza giocatori)
    ruoli_disponibili = list(stanze[codice].get("ruoli_scelti", []))
    random.shuffle(ruoli_disponibili)

    ruoli_giocatori = {}
    traditori = []
    veggenti = []

    for giocatore in giocatori:
        if giocatore in stanze[codice]["impostori"]:
            continue  # Gli impostori non ricevono ruoli speciali

        if ruoli_disponibili:
            ruolo = ruoli_disponibili.pop()
            descrizione = RUOLI_DISPONIBILI.get(ruolo, "Nessuna descrizione disponibile")
            ruoli_giocatori[giocatore] = {"nome": ruolo, "descrizione": descrizione}

            # Aggiorna gli array traditori e veggenti direttamente
            if "Traditore" in ruolo:
                traditori.append(giocatore)
            elif "Veggente" in ruolo:
                veggenti.append(giocatore)
        else:
            ruoli_giocatori[giocatore] = {"nome": "Nessun ruolo", "descrizione": "Gioca senza abilità speciali"}

    # Salva i ruoli nella stanza
    stanze[codice]["ruoli_giocatori"] = ruoli_giocatori

    # Creiamo la lista dei ruoli disponibili per tutti
    ruoli_partita = {ruolo: RUOLI_DISPONIBILI.get(ruolo, "Nessuna descrizione disponibile") for ruolo in stanze[codice].get("ruoli_scelti", [])}

    impostori = stanze[codice]["impostori"]

    # Se esiste un veggente, scegli un giocatore buono a caso (che non sia impostore)
    buoni = [g for g in giocatori if g not in impostori and g not in traditori and g not in veggenti]

    # Il veggente vede un buono casuale tra quelli validi
    veggente_vede = random.choice(buoni) if buoni else None

    # Invia le parole, i ruoli dei giocatori e la lista dei ruoli scelti a tutti
    for sid, info in client_sessions.items():
        if info["codice"] == codice:
            nome_giocatore = info["nome"]

            ruolo_info = stanze[codice]["ruoli_giocatori"].get(info["nome"], {"nome": "Nessun ruolo", "descrizione": "Gioca senza abilità speciali"})
            ruolo_nome = ruolo_info["nome"]
            ruolo_descrizione = ruolo_info["descrizione"]

            if info["nome"] in stanze[codice]["impostori"]:
                parola = parola_variante if stanze[codice].get("modalita") == "little_secret" else " 👀 Sei l'IMPOSTORE! Non conosci una sega. 👀"
            else:
                parola = parola_segreta

            info_extra = ""
            if nome_giocatore in traditori:
                info_extra = f" - Impostore/i: {', '.join(impostori)}!"
            elif nome_giocatore in veggenti and veggente_vede:
                info_extra = f" - Hai avuto una visione: {veggente_vede} è un buono!"

            imposter_string = "Sei un impostore! " + vere_domande if info["nome"] in stanze[codice]["impostori"] else "Sei buono!"
            socketio.emit("parola_segreta", {
                "categoria": categoria,
                "parola": parola,
                "ruolo": f"{ruolo_nome} {info_extra}".strip(),
                "descrizione": ruolo_descrizione,
                "ruoli_partita": ruoli_partita,
                "imposter": imposter_string
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
    esito = data["esito"]

    if codice not in stanze or stanze[codice]["punteggio_assegnato"]:
        return jsonify({"errore": "Punti già assegnati o stanza inesistente"}), 400

    impostori = stanze[codice]["impostori"]
    giocatori = stanze[codice]["giocatori"]
    ruoli_giocatori = stanze[codice]["ruoli_giocatori"]

    if esito == "clown_eliminato":
        print(ruoli_giocatori)
        clown = [g for g, ruolo in ruoli_giocatori.items() if "Clown" in ruolo["nome"]]
        print(clown)
        if clown:
            for c in clown:
                stanze[codice]["punteggi"][c] = stanze[codice]["punteggi"].get(c, 0) + 2
    elif esito == "impostore_fugge":
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

    if codice not in stanze:
        return jsonify({"errore": "Stanza inesistente"}), 400

    for chiave, valore in nuove_impostazioni.items():
        if chiave == "num_impostori":
            stanze[codice][chiave] = int(valore) if valore else 1  # Cast a int qui
        elif chiave in ["categorie_scelte", "modalita", "ruoli_scelti"]:
            stanze[codice][chiave] = valore  # Memorizza anche i ruoli scelti

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
