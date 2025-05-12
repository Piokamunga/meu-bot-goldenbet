from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = "feedback.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot TEXT NOT NULL,
            resultado TEXT NOT NULL,
            data TEXT NOT NULL
        )''')
        conn.commit()

def registrar_feedback(slot, resultado):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO feedback (slot, resultado, data) VALUES (?, ?, ?)",
                  (slot, resultado, datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()

def obter_ranking():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT slot, COUNT(*) as total, SUM(CASE WHEN resultado = 'bom' THEN 1 ELSE 0 END) as bons FROM feedback GROUP BY slot")
        dados = c.fetchall()
    ranking = []
    for slot, total, bons in dados:
        if total == 0: continue
        perc = round((bons / total) * 100)
        ranking.append((slot, perc, total))
    ranking.sort(key=lambda x: -x[1])
    return ranking

@app.route("/")
def dashboard():
    ranking = obter_ranking()
    slots = [r[0] for r in ranking]
    percentuais = [r[1] for r in ranking]
    return render_template("dashboard.html", ranking=ranking, slots=slots, percentuais=percentuais)

@app.route("/feedback", methods=["POST"])
def feedback():
    slot = request.form.get("slot")
    resultado = request.form.get("resultado")
    if slot and resultado:
        registrar_feedback(slot, resultado)
    return redirect("/")