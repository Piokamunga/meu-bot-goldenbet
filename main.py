
from flask import Flask
from bot import app, configurar_webhook
from threading import Thread
from time import sleep
from bot import enviar_alerta_automatico

if __name__ == "__main__":
    configurar_webhook()

    def loop_alertas():
        while True:
            enviar_alerta_automatico()
            sleep(300)

    Thread(target=loop_alertas).start()
    app.run(host="0.0.0.0", port=8080)
