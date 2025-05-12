from telegram import Bot
from datetime import datetime
import random

TOKEN = '8067025267:AAGkiP6F68X3FvqaTcCuTCKMM1FHFy_zHkg'
CHAT_ID = '-1001234567890'
bot = Bot(token=TOKEN)

def enviar_alerta_simples():
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    slots = ["Golden Coins", "Moeda do Dia", "Cash Rain", "Tesouro do Ouro", "Mega Spin", "Roda Milionária"]
    slot = random.choice(slots)
    chance = round(random.uniform(87.1, 98.4), 2)
    mensagem = (
        f"ALERTA DE SLOT\n"
        f"Jogo: {slot}\n"
        f"Chance estimada de acerto: {chance}%\n\n"
        "Ganhe com os meus sinais: https://bit.ly/449TH4F\n"
        "goldenbet.co.ao"
    )
    bot.send_message(chat_id=CHAT_ID, text=mensagem)
    with open("log_alertas.txt", "a", encoding="utf-8") as log:
        log.write(f"[{agora}] {slot} - Chance: {chance}%\n")