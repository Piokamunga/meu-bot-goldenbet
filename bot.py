
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from datetime import datetime
import pytz
import random
import os

TOKEN = "8067025267:AAGkiP6F68X3FvqaTcCuTCKMM1FHFy_zHkg"
CHAT_ID = "-1002479614516"

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

def start(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="GoldenAlertasBot está ativo!")

def enviar_alerta_automatico():
    agora = datetime.now(pytz.timezone('Africa/Luanda'))
    hora = agora.strftime("%H:%M")
    slots = ["Golden Coins", "Moeda do Dia", "Cash Rain", "Tesouro do Ouro", "Camuanha Premium", "Jackpot Veloz"]
    slot = random.choice(slots)
    mensagem = f"Slot em alta agora!\nJogo: {slot}\nHora: {hora}\nAlta chance de ganho.\nCadastre-se: https://goldenbet.co.ao"
    bot.send_message(chat_id=CHAT_ID, text=mensagem)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

@app.route('/')
def index():
    return "GoldenAlertasBot com OCR e alertas automáticos está rodando!"

# Configura o dispatcher
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))

# Disparar alerta de exemplo no boot (para teste)
enviar_alerta_automatico()
