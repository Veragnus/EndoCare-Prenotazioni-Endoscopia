from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_NAME = "prenotazioni.db"

# =========================
# DATABASE
# =========================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS prenotazioni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cognome TEXT,
        data_nascita TEXT,
        tipo_esame TEXT,
        data TEXT,
        orario TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# CLASSE (OOP)
# =========================
class Prenotazione:
    def __init__(self, nome, cognome, data_nascita, tipo_esame, data, orario):
        self.nome = nome
        self.cognome = cognome
        self.data_nascita = data_nascita
        self.tipo_esame = tipo_esame
        self.data = data
        self.orario = orario

# =========================
# API
# =========================

# GET tutte
@app.route("/prenotazioni", methods=["GET"])
def get_prenotazioni():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM prenotazioni")
    rows = c.fetchall()

    conn.close()

    prenotazioni = []
    for r in rows:
        prenotazioni.append({
            "id": r[0],
            "nome": r[1],
            "cognome": r[2],
            "data_nascita": r[3],
            "tipo_esame": r[4],
            "data": r[5],
            "orario": r[6]
        })

    return jsonify(prenotazioni)


# POST crea
@app.route("/prenotazioni", methods=["POST"])
def crea_prenotazione():
    data = request.json

    # controllo domenica
    giorno = datetime.strptime(data["data"], "%Y-%m-%d").weekday()
    if giorno == 6:
        return jsonify({"errore": "Non si può prenotare di domenica"}), 400

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # controllo slot occupato
    c.execute("""
        SELECT * FROM prenotazioni
        WHERE data=? AND orario=?
    """, (data["data"], data["orario"]))

    if c.fetchone():
        conn.close()
        return jsonify({"errore": "Slot già occupato"}), 400

    # crea oggetto (OOP)
    p = Prenotazione(
        data["nome"],
        data["cognome"],
        data["data_nascita"],
        data["tipo_esame"],
        data["data"],
        data["orario"]
    )

    # salva DB
    c.execute("""
        INSERT INTO prenotazioni (nome, cognome, data_nascita, tipo_esame, data, orario)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (p.nome, p.cognome, p.data_nascita, p.tipo_esame, p.data, p.orario))

    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione creata"}), 201


# DELETE
@app.route("/prenotazioni/<int:id>", methods=["DELETE"])
def elimina_prenotazione(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("DELETE FROM prenotazioni WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Eliminata"})


# PUT modifica
@app.route("/prenotazioni/<int:id>", methods=["PUT"])
def modifica_prenotazione(id):
    data = request.json

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        UPDATE prenotazioni
        SET nome=?, cognome=?, data_nascita=?, tipo_esame=?, data=?, orario=?
        WHERE id=?
    """, (
        data["nome"],
        data["cognome"],
        data["data_nascita"],
        data["tipo_esame"],
        data["data"],
        data["orario"],
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Modificata"})


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5001)