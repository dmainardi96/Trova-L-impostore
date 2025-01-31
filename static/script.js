const socket = io.connect(window.location.origin, { transports: ["websocket"] });
const nome = ''

async function creaStanza() {
    let categorieScelte = JSON.parse(localStorage.getItem("categorie_scelte")) || [];


    let response = await fetch("/crea_stanza", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ categorie: categorieScelte })
    });

    let data = await response.json();
    let codice = data.codice;

    document.getElementById("stanza-codice").innerText = `Codice: ${codice}`;
    document.getElementById("stanza-codice").style.display = "inline";

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
        li.innerText = descrizione;  // Mostra Nome + Emoji + Soprannome + Punteggio
        lista.appendChild(li);
    }
});

async function gestisciPartita() {
    let codice = sessionStorage.getItem("stanza_creata");

    let response = await fetch("/gestisci_partita", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ codice: codice })
    });

    let data = await response.json();

    if (data.successo) {
        document.getElementById("inizia-gioco").innerText = "Nuova Parola"; // Nasconde il pulsante dopo l'inizio del gioco
        avviaMusica();  // Avvia la musica solo se non sta già suonando
        document.getElementById("punteggio-container").style.display = "inline-block";
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

function avviaMusica() {
    let audio = document.getElementById("bg-music");

    if (audio.paused) {  // Controlla se è già in riproduzione
        audio.volume = 0.5;  // Imposta il volume a metà
        audio.play().catch(error => {
            console.log("Errore avvio musica: ", error);
        });
    }
}

function assegnaPunti(esito) {
    let codice = sessionStorage.getItem("stanza_creata");

    fetch("/assegna_punti", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ codice: codice, esito: esito })
    }).then(response => response.json())
      .then(data => {
          if (data.successo) {
              document.getElementById("punteggio-container").style.display = "none";  // Nasconde i bottoni dopo il click
          } else {
              alert(data.errore);
          }
      });
}

document.getElementById("dropdown-btn").addEventListener("click", function() {
    let dropdown = document.getElementById("dropdown-menu");
    dropdown.style.display = (dropdown.style.display === "block") ? "none" : "block";
});

// Chiude il dropdown quando si clicca altrove
document.addEventListener("click", function(event) {
    if (!event.target.matches("#dropdown-btn")) {
        document.getElementById("dropdown-menu").style.display = "none";
    }
});

// Quando si seleziona un'opzione, assegna i punti
document.getElementById("dropdown-menu").addEventListener("click", function(event) {
    let codice = sessionStorage.getItem("stanza_creata");
    let esito = event.target.value;

    fetch("/assegna_punti", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ codice: codice, esito: esito })
    }).then(response => response.json())
      .then(data => {
          if (data.successo) {
              document.getElementById("punteggio-container").style.display = "none";  // Nasconde il bottone dopo l'assegnazione
          } else {
              alert(data.errore);
          }
      });
});

async function mostraPopupCategorie() {
    // Controlla se il popup è già aperto
    if (document.getElementById("popup-categorie")) return;

    let response = await fetch("/categorie_disponibili");
    let data = await response.json();
    let categorie = data.categorie;

    let popup = document.createElement("div");
    popup.id = "popup-categorie";
    popup.innerHTML = `
        <div class="popup-content">
            <h2>Impostazioni della Stanza</h2>
            <div id="categorie-opzioni">
            Categorie:
                ${categorie.map(cat => `
                    <div class="categoria-checkbox">
                        <label><input type="checkbox" value="${cat}" checked> ${cat}</label>
                    </div>
                `).join("")}
            </div>
            <button onclick="salvaImpostazioni()">Salva Impostazioni</button>
            <button onclick="chiudiPopup()">Chiudi</button>
        </div>
    `;

    document.body.appendChild(popup);
}

function chiudiPopup() {
    let popup = document.getElementById("popup-categorie");
    if (popup) popup.remove();
}

// Funzione per salvare le impostazioni selezionate
function salvaImpostazioni() {
    let categorieScelte = [];
    document.querySelectorAll("#categorie-opzioni input:checked").forEach(checkbox => {
        categorieScelte.push(checkbox.value);
    });

    localStorage.setItem("categorie_scelte", JSON.stringify(categorieScelte)); // Salva localmente
    chiudiPopup();
}
