from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime
import pytesseract
from PIL import Image
import random
import os

TOKEN = '8067025267:AAGkiP6F68X3FvqaTcCuTCKMM1FHFy_zHkg'
CHAT_ID = '-1002479614516'
bot = Bot(token=TOKEN)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot ativo! Envie uma imagem de slot para análise OCR.")

def receber_imagem(update: Update, context: CallbackContext):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    foto = update.message.photo[-1]
    arquivo = foto.get_file()
    caminho = f"imagem_{agora.replace(':','-').replace(' ','_')}.jpg"
    arquivo.download(caminho)

    try:
        imagem = Image.open(caminho)
        texto = pytesseract.image_to_string(imagem, lang='eng')
        resumo = texto.strip()[:400]
        resposta = f"Resultado OCR:\n{resumo if resumo else 'Nenhum texto detectado.'}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=resposta)

        with open("ocr_results.txt", "a", encoding="utf-8") as log:
            log.write(f"[{agora}]\n{resumo}\n\n")

    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Erro ao analisar a imagem.")
    finally:
        os.remove(caminho)

def enviar_alerta_simples(context: CallbackContext = None):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    slots = ["Golden Coins", "Moeda do Dia", "Cash Rain", "Tesouro do Ouro", "Mega Spin", "Roda Milionária"]
    slot = random.choice(slots)
    chance = round(random.uniform(87.1, 98.4), 2)
    mensagem = (
        "ALERTA DE SLOT\n"
        f"Jogo: {slot}\n"
        f"Chance estimada de acerto: {chance}%\n\n"
        "Ganhe com os meus sinais: https://bit.ly/449TH4F\n"
        "goldenbet.co.ao"
    )
    bot.send_message(chat_id=CHAT_ID, text=mensagem)
    with open("log_alertas.txt", "a", encoding="utf-8") as log:
        log.write(f"[{agora}] {slot} - Chance: {chance}%\n")

def iniciar_bot():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, receber_imagem))
    updater.start_polling()
    return updater