from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from datetime import datetime
import pytesseract
from PIL import Image
import os
import random

TOKEN = "8067025267:AAGkiP6F68X3FvqaTcCuTCKMM1FHFy_zHkg"
CHAT_ID = "-1002479614516"
URL = "https://meu-bot-goldenbet.onrender.com"

bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="GoldenAlertasBot com OCR ativo!")

def receber_imagem(update, context):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    foto = update.message.photo[-1]
    arquivo = foto.get_file()
    caminho = f"imagem_{agora.replace(':','-').replace(' ','_')}.jpg"
    arquivo.download(caminho)

    try:
        imagem = Image.open(caminho)
        texto = pytesseract.image_to_string(imagem)
        resposta = texto.strip()[:400] or "Nenhum texto detectado."
        context.bot.send_message(chat_id=update.effective_chat.id, text="Resultado OCR:\n" + resposta)

        with open("ocr_results.txt", "a", encoding="utf-8") as log:
            log.write(f"[{agora}]\n{resposta}\n\n")

    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Erro ao analisar a imagem.")
    finally:
        os.remove(caminho)

def enviar_alerta_automatico():
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    slot = random.choice(["Golden Coins", "Cash Rain", "Roda da Fortuna", "Moeda do Dia"])
    chance = round(random.uniform(89.5, 98.9), 2)
    texto = (
        "SLOT ALERTA\n"
        "Jogo: " + slot + "\n"
        "Chance de vitória: " + str(chance) + "%\n\n"
        "goldenbet.co.ao\n"
        "https://bit.ly/449TH4F"
    )
    bot.send_message(chat_id=CHAT_ID, text=texto)
    with open("log_alertas.txt", "a", encoding="utf-8") as log:
        log.write(f"[{agora}] {slot} - {chance}%\n")

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

@app.route('/')
def index():
    return "GoldenAlertasBot com OCR - Ativo"

def configurar_webhook():
    bot.set_webhook(f"{URL}/webhook")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.photo, receber_imagem))