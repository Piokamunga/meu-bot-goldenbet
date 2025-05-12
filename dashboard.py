
from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

def ler_logs():
    if not os.path.exists("log_alertas.txt"):
        return []
    with open("log_alertas.txt", encoding="utf-8") as f:
        linhas = f.readlines()[-10:]
    return [linha.strip() for linha in linhas[::-1]]

def registrar_feedback(slot, status):
    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write(f"{slot}|{status}\n")

def calcular_ranking():
    if not os.path.exists("feedback.txt"):
        return []
    with open("feedback.txt", encoding="utf-8") as f:
        dados = [linha.strip().split("|") for linha in f if "|" in linha]
    contagem = {}
    for slot, status in dados:
        if slot not in contagem:
            contagem[slot] = {"bom": 0, "ruim": 0}
        if status == "bom":
            contagem[slot]["bom"] += 1
        else:
            contagem[slot]["ruim"] += 1
    ranking = []
    for slot, val in contagem.items():
        total = val["bom"] + val["ruim"]
        if total == 0: continue
        perc = round((val["bom"] / total) * 100)
        ranking.append((slot, perc))
    ranking.sort(key=lambda x: -x[1])
    return ranking[:5]

@app.route("/", methods=["GET", "POST"])
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    logs = ler_logs()
    ranking = calcular_ranking()

    if request.method == "POST":
        from bot import enviar_alerta_simples
        enviar_alerta_simples()
        logs = ler_logs()
        ranking = calcular_ranking()

    if request.args.get("slot") and request.args.get("f"):
        registrar_feedback(request.args["slot"], request.args["f"])
        return redirect("/dashboard")

    return render_template("dashboard.html", logs=logs, ranking=ranking)
