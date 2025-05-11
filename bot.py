from telegram.ext import Updater, CommandHandler
from uptime import manter_online

TOKEN = 'SEU_TOKEN_AQUI'  # Substitua pelo seu token real
CHAT_ID = 'SEU_CHAT_ID'   # Substitua pelo seu ID real

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot de alertas iniciado com sucesso!")

def enviar_alerta(context):
    mensagem = "🔥 SLOT EM ALTA AGORA 🔥\nAposte com sabedoria!"
    context.bot.send_message(chat_id=CHAT_ID, text=mensagem)

manter_online()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
job = updater.job_queue
job.run_repeating(enviar_alerta, interval=3600, first=5)
updater.start_polling()
