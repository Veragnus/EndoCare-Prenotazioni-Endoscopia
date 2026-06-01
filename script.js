document.addEventListener("DOMContentLoaded", () => {

    const selectOrario = document.getElementById("orario");
    const inputData = document.getElementById("data");

    // blocco date passate
    const today = new Date().toISOString().split("T")[0];
    inputData.setAttribute("min", today);

    // Generazione automatica degli slot orari disponibili
    // genera orari
    for (let h = 9; h <= 17; h++) {
        selectOrario.innerHTML += `<option>${h}:00</option>`;
        selectOrario.innerHTML += `<option>${h}:30</option>`;
    }

    // submit
    document.getElementById("form").addEventListener("submit", async (e) => {
        e.preventDefault();

        console.log("CLICK OK"); // test

        // Invio dei dati al backend tramite API REST

        const res = await fetch("http://127.0.0.1:5001/prenotazioni", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                nome: document.getElementById("nome").value,
                cognome: document.getElementById("cognome").value,
                data_nascita: document.getElementById("data_nascita").value,
                tipo_esame: document.getElementById("tipo_esame").value,
                data: document.getElementById("data").value,
                orario: document.getElementById("orario").value
            })
        });

        const data = await res.json();

        if (data.errore) {
            alert("❌ " + data.errore);
        } else {
            alert("✅ Prenotazione effettuata!");
        }

        caricaPrenotazioni();
    });

    // Recupera tutte le prenotazioni registrate dal backend
    // carica lista
    async function caricaPrenotazioni() {
        const res = await fetch("http://127.0.0.1:5001/prenotazioni");
        const data = await res.json();

        const lista = document.getElementById("lista");
        lista.innerHTML = "";

        data.forEach(p => {
            const li = document.createElement("li");

            li.innerHTML = `
                <strong>${p.nome} ${p.cognome}</strong><br>
                ${p.tipo_esame}<br>
                ${p.data} - ${p.orario}<br>
                <button onclick="elimina(${p.id})">Elimina</button>
            `;

            lista.appendChild(li);
        });
    }

    // Elimina una prenotazione e aggiorna la lista
    // elimina
    window.elimina = async function(id) {
        await fetch(`http://127.0.0.1:5001/prenotazioni/${id}`, {
            method: "DELETE"
        });

        caricaPrenotazioni();
    }

    // avvio
    caricaPrenotazioni();

});
