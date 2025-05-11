from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Bot rodando normalmente!</h1><p>Status: Online com logs ativos.</p>"

def manter_online():
    def run():
        print("Iniciando Flask para uptime...")
        app.run(host='0.0.0.0', port=8080)
    Thread(target=run).start()
