from dashboard import app
from uptime import manter_online
from threading import Thread
from time import sleep
from bot import enviar_alerta_simples

def enviar_automaticamente():
    while True:
        enviar_alerta_simples()
        sleep(300)  # 5 minutos

if __name__ == "__main__":
    manter_online()
    Thread(target=enviar_automaticamente).start()
    app.run(host='0.0.0.0', port=8080)