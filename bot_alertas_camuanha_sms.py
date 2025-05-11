from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime, time as dtime
from uptime import manter_online
from twilio.rest import Client
import random

# Telegram
TOKEN = '7556007084:AAGiPr6S7ZMAq-E5_nsqsRDVFD-urU2bYQ0'
CHAT_ID = '-1001234567890'  # Substituir pelo ID do grupo ou canal

# Twilio (substitua pelos seus dados)
TWILIO_ACCOUNT_SID = 'SEU_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'SEU_AUTH_TOKEN'
TWILIO_PHONE_NUMBER = '+1XXXXXXXXXX'  # Número do Twilio
DESTINO_SMS = '+244XXXXXXXXX'  # Número de destino real

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
manter_online()

def enviar_sms(mensagem):
    try:
        message = client.messages.create(
            body=mensagem,
            from_=TWILIO_PHONE_NUMBER,
            to=DESTINO_SMS
        )
        print("SMS enviado:", message.sid)
    except Exception as e:
        print("Erro ao enviar SMS:", e)

def start(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot Camuanha Sinais ativo com alertas semanais e especiais de fim de semana!")

def enviar_alerta(context: CallbackContext):
    agora = datetime.now()
    hora = agora.hour
    dia_semana = agora.weekday()

    if dia_semana < 5:
        if hora in [7, 11, 14]:
            slots = ["Golden Coins", "Moeda do Dia", "Cash Rain", "Tesouro do Ouro"]
            foco = "Moedas e ganhos consistentes"
        else:
            slots = ["Free Spin Fever", "Bônus Mania", "Rodada Secreta", "Mega Chance"]
            foco = "Rodadas grátis e bônus padrão"

        slot = random.choice(slots)
        mensagem = f"""🔥 SLOT EM ALTA AGORA 🔥
🎰 Jogo: {slot}
🎯 Foco: {foco}

Ganhe com os meus sinais: https://bit.ly/449TH4F
Site oficial: www.goldenbet.co.ao
Cadastre-se e teste já!
"""
    else:
        slots = ["Super Bônus Final", "Roda da Fortuna", "Camuanha Premium", "Jackpot Veloz"]
        slot = random.choice(slots)
        mensagem = f"""🎉 FIM DE SEMANA DE GANHOS 🎉
🔥 SLOT ESPECIAL: {slot}
💰 Hora de apostar mais, ganhar mais!

Ganhe com os meus sinais: https://bit.ly/449TH4F
Aposte agora na GoldenBet!
Cadastre-se e aproveite o fim de semana!
"""

    context.bot.send_message(chat_id=CHAT_ID, text=mensagem)
    enviar_sms(mensagem)

    with open("log_alertas.txt", "a", encoding="utf-8") as log:
        log.write(f"[{agora}] Alerta enviado: {slot} - Dia: {dia_semana}\n")

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))

horarios = [dtime(7, 0), dtime(11, 0), dtime(14, 0), dtime(18, 30), dtime(21, 0), dtime(0, 0)]
for h in horarios:
    updater.job_queue.run_daily(enviar_alerta, h)

updater.start_polling()
