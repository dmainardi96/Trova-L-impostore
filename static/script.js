const socket = io.connect("http://localhost:5000");  // Cambia con il tuo server se deployato

function creaStanza() {
    let parola = document.getElementById("parola").value;
    fetch("/crea_stanza", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ parola: parola })
    })
    .then(response => response.json())
    .then(data => {
        alert("Stanza creata! Codice: " + data.codice);
    });
}

function unisciti() {
    let codice = document.getElementById("codice").value;
    let nome = document.getElementById("nome").value;

    fetch("/unisciti", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ codice: codice, nome: nome })
    })
    .then(response => response.json())
    .then(data => {
        if (data.successo) {
            document.getElementById("gioco").style.display = "block";
            socket.emit("join", { codice: codice, nome: nome });
        } else {
            alert("Errore: " + data.errore);
        }
    });
}

function iniziaGioco() {
    let codice = document.getElementById("codice").value;
    socket.emit("start_game", { codice: codice });
}

socket.on("word", function(data) {
    document.getElementById("stato").innerText = "Parola: " + data.parola;
});
