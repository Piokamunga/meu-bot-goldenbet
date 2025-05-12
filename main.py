
from dashboard import app
from uptime import manter_online
from threading import Thread
from time import sleep
from bot import enviar_alerta_simples, iniciar_bot

def enviar_automaticamente():
    while True:
        enviar_alerta_simples()
        sleep(300)

if __name__ == "__main__":
    manter_online()
    Thread(target=iniciar_bot).start()
    Thread(target=enviar_automaticamente).start()
    app.run(host='0.0.0.0', port=8080)
