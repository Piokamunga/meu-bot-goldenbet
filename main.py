from flask import Flask
from bot import app as bot_app, configurar_webhook
from uptime import manter_online
from threading import Thread
from time import sleep
from bot import enviar_alerta_automatico

# Start uptime server
manter_online()

# Configure webhook
configurar_webhook()

# Start sending alerts
def loop_alertas():
    while True:
        enviar_alerta_automatico()
        sleep(300)

Thread(target=loop_alertas).start()

# Run bot Flask app (webhook)
bot_app.run(host='0.0.0.0', port=8080)
