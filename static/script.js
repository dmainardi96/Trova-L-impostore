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
    sessionStorage.setItem("nome_utente", nome);

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
        }
        if (data.owner) {
            document.getElementById("inizia-gioco").style.display = "inline";
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
    let nome = document.getElementById("nome").value;

    let response = await fetch("/gestisci_partita", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ codice: codice , nome: nome})
    });

    let data = await response.json();

    if (data.successo) {
        document.getElementById("inizia-gioco").innerText = "Nuova Parola"; // Nasconde il pulsante dopo l'inizio del gioco
        avviaMusica();  // Avvia la musica solo se non sta già suonando
        document.getElementById("punteggio-container").style.display = "inline-block";
        document.getElementById("sei-impostore").style.display = "none";
        document.getElementById("btn-impostore").style.display = "inline-block";
    } else {
        alert(data.errore);
    }
}

// Ricevi la parola segreta dal server
socket.on("parola_segreta", function(data) {
    document.getElementById("parola-container").style.display = "block";
    document.getElementById("categoria").innerText = `Categoria: ${data.categoria}`;
    document.getElementById("parola").innerText = data.parola;
    document.getElementById("ruolo-giocatore").innerText = `Ruolo: ${data.ruolo}`;

    // Mostra la lista dei ruoli disponibili
    let ruoliLista = document.getElementById("lista-ruoli");
    ruoliLista.innerHTML = "<h4>Ruoli disponibili:</h4>";
    for (let ruolo in data.ruoli_partita) {
        let p = document.createElement("p");
        p.innerHTML = `<strong>${ruolo}:</strong> ${data.ruoli_partita[ruolo]}`;
        ruoliLista.appendChild(p);
    }

    document.getElementById("sei-impostore").style.display = "none";
    document.getElementById("btn-impostore").style.display = "inline-block";
    document.getElementById("sei-impostore").innerText = data.imposter;

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

async function apriPopupImpostazioni() {
    // Caricamento delle categorie disponibili
    fetch("/categorie_disponibili")
        .then(response => response.json())
        .then(data => {
            let categorieDiv = document.getElementById("categorie");
            categorieDiv.innerHTML = ""; // Pulisce il div prima di riempirlo

            data.categorie.forEach(categoria => {
                let checkbox = document.createElement("input");
                checkbox.type = "checkbox";
                checkbox.value = categoria;
                checkbox.id = "cat-" + categoria;

                let label = document.createElement("label");
                label.htmlFor = "cat-" + categoria;
                label.textContent = categoria;

                let div = document.createElement("div");
                div.appendChild(checkbox);
                div.appendChild(label);
                categorieDiv.appendChild(div);
            });
        });

    // Caricamento dei ruoli disponibili
    fetch("/ruoli_disponibili")
        .then(response => response.json())
        .then(data => {
            let ruoliDiv = document.getElementById("ruoli-list");
            ruoliDiv.innerHTML = ""; // Pulisce il div prima di riempirlo

            for (let ruolo in data.ruoli) {
                let checkbox = document.createElement("input");
                checkbox.type = "checkbox";
                checkbox.value = ruolo;
                checkbox.id = "ruolo-" + ruolo;

                let label = document.createElement("label");
                label.htmlFor = "ruolo-" + ruolo;
                label.innerHTML = `<strong>${ruolo}</strong> - <span class="descrizione">${data.ruoli[ruolo]}</span>`;

                let div = document.createElement("div");
                div.appendChild(checkbox);
                div.appendChild(label);
                ruoliDiv.appendChild(div);
            }
        });

    // Mostra il popup e l'overlay
    document.getElementById("popup-impostazioni").style.display = "block";
    document.getElementById("overlay").style.display = "block";
}


function chiudiPopup() {
    document.getElementById("popup-impostazioni").style.display = "none";
    document.getElementById("overlay").style.display = "none";
}

async function salvaImpostazioni() {
    let codice = sessionStorage.getItem("stanza_creata");
    if (!codice) {
        alert("Devi prima creare una stanza!");
        return;
    }

    let categorieScelte = Array.from(document.querySelectorAll("#categorie input:checked"))
                               .map(el => el.value);

    let modalitaSelezionata = document.querySelector('input[name="modalita"]:checked').value;

    let numImpostori = parseInt(document.querySelector('input[name="num-impostori"]').value);

    let ruoliScelti = Array.from(document.querySelectorAll("#ruoli-list input:checked"))
                           .map(el => el.value);

    let response = await fetch("/modifica_impostazioni", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            codice: codice,
            impostazioni: {
                categorie_scelte: categorieScelte,
                modalita: modalitaSelezionata,
                num_impostori: numImpostori,
                ruoli_scelti: ruoliScelti
            }
        })
    });

    let data = await response.json();
    chiudiPopup();
}

async function verificaImpostore() {
    document.getElementById("sei-impostore").style.display = "inline-block";
    document.getElementById("btn-impostore").style.display = "none";
}

