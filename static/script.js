const socket = io.connect(window.location.origin, { transports: ["websocket"] });
const nome = ''

async function creaStanza() {
    let response = await fetch("/crea_stanza", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    });

    let data = await response.json();
    let codice = data.codice;

    document.getElementById("stanza-codice").innerText = `Codice: ${codice}`;

    document.getElementById("stanza-codice").style.display = "inline";
    document.getElementById("copy-btn").style.display = "inline";
    document.getElementById("inizia-gioco").style.display = "inline";

    document.getElementById("codice").value = codice;
    sessionStorage.setItem("stanza_creata", codice);
}

function copiaCodice() {
    let codice = document.getElementById("stanza-codice").innerText.replace("Codice: ", "");
    navigator.clipboard.writeText(codice);
    document.getElementById("codice").value = codice;
}

function getCookie(name) {
    let match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
}

function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

async function unisciti() {
    let codice = document.getElementById("codice").value;
    let nome = document.getElementById("nome").value;

    let playerId = getCookie("player_id");
    if (!playerId) {
        playerId = Math.random().toString(36).substr(2, 9);
        setCookie("player_id", playerId, 7);
    }

    let response = await fetch("/unisciti", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ codice: codice, nome: nome, player_id: playerId })
    });

    let data = await response.json();

    if (data.successo) {
        document.getElementById("gioco").style.display = "block";
        socket.emit("join_room", { codice: codice, nome: nome });

        if (data.messaggio === "Utente già loggato") {
            document.getElementById("nome").value = data.nome;
            alert("Utente già loggato, rientrato nella stanza!");
        }
    } else {
        alert("Errore: " + data.errore);
    }
}

// Ascolta aggiornamenti dei giocatori in tempo reale
socket.on("aggiorna_giocatori", function(data) {
    let lista = document.getElementById("giocatori-lista");
    lista.innerHTML = "";

    for (const [nome, descrizione] of Object.entries(data.giocatori)) {
        let li = document.createElement("li");
        li.innerText = descrizione;  // Mostra Nome + Emoji + Soprannome
        lista.appendChild(li);
    }
});

async function iniziaGioco() {
    let codice = sessionStorage.getItem("stanza_creata");

    let response = await fetch("/inizia_gioco", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ codice: codice })
    });

    let data = await response.json();

    if (data.successo) {
        document.getElementById("inizia-gioco").style.display = "none"; // Nasconde il pulsante dopo l'inizio del gioco

        // Fai partire la musica
        let audio = document.getElementById("bg-music");
        audio.volume = 0.5; // Imposta il volume a metà
        audio.play().catch(error => {
            console.log("Errore avvio musica: ", error);
        });
        
    } else {
        alert(data.errore);
    }
}

// Ricevi la parola segreta dal server
socket.on("parola_segreta", function(data) {
    document.getElementById("parola-container").style.display = "block";
    document.getElementById("categoria").innerText = `Categoria: ${data.categoria}`;
    document.getElementById("parola").innerText = data.parola;
});
