import random
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime, time as dtime
from uptime import manter_online
from twilio.rest import Client

print("Executando bot.py...")

TOKEN = '7556007084:AAGiPr6S7ZMAq-E5_nsqsRDVFD-urU2bYQ0'
CHAT_ID = '-1001234567890'

TWILIO_ACCOUNT_SID = 'AC990443fa5f1dd456d1a8fc4bf7f323c8'
TWILIO_AUTH_TOKEN = 'c16f3d425d2936647924f19bd8d3acf3'
TWILIO_PHONE_NUMBER = '+14155238886'
DESTINO_SMS = '+244932071284'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

try:
    manter_online()
except Exception as e:
    print("Erro ao iniciar uptime:", e)

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
    print("Comando /start recebido.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot Camuanha Sinais ativo!")

def enviar_alerta(context: CallbackContext):
    agora = datetime.now()
    hora = agora.hour
    dia_semana = agora.weekday()
    print(f"Enviando alerta... Hora: {hora}, Dia: {dia_semana}")

    if dia_semana < 5:
        if hora in [7, 11, 14]:
            slots = ["Golden Coins", "Moeda do Dia", "Cash Rain", "Tesouro do Ouro"]
            foco = "Moedas e ganhos consistentes"
        else:
            slots = ["Free Spin Fever", "Bônus Mania", "Rodada Secreta", "Mega Chance"]
            foco = "Rodadas grátis e bônus padrão"
        slot = random.choice(slots)
        mensagem = f"🔥 SLOT EM ALTA AGORA 🔥\n🎰 Jogo: {slot}\n🎯 Foco: {foco}\nGanhe: https://bit.ly/449TH4F"
    else:
        slots = ["Super Bônus Final", "Roda da Fortuna", "Camuanha Premium", "Jackpot Veloz"]
        slot = random.choice(slots)
        mensagem = f"🎉 FIM DE SEMANA DE GANHOS 🎉\n🔥 SLOT ESPECIAL: {slot}\nAposte agora na GoldenBet!"

    try:
        context.bot.send_message(chat_id=CHAT_ID, text=mensagem)
        enviar_sms(mensagem)
    except Exception as e:
        print("Erro ao enviar alerta:", e)

    with open("log_alertas.txt", "a", encoding="utf-8") as log:
        log.write(f"[{agora}] Alerta enviado: {slot} - Dia: {dia_semana}\n")

try:
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    horarios = [dtime(7, 0), dtime(11, 0), dtime(14, 0), dtime(18, 30), dtime(21, 0), dtime(0, 0)]
    for h in horarios:
        updater.job_queue.run_daily(enviar_alerta, h)
    print("Iniciando polling...")
    updater.start_polling()
except Exception as e:
    print("Erro geral no bot:", e)
