
from flask import Flask
from threading import Thread

app_uptime = Flask(__name__)

@app_uptime.route('/uptime')
def home():
    return "<h1>GoldenAlertasBot rodando</h1>"

def manter_online():
    def run():
        app_uptime.run(host='0.0.0.0', port=8081)
    Thread(target=run).start()
