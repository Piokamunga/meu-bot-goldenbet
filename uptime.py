from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/uptime')
def uptime():
    return "OK"

def manter_online():
    def run():
        app.run(host='0.0.0.0', port=8081)
    Thread(target=run).start()
