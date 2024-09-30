import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# открытие конфиг файла с токеном
with open('config.txt', 'r') as cfg:
  # получение токена бота
  data = json.load(cfg) 

async def start(update: Update, context):
    await update.message.reply_text("Приветик! Я твой бот для астрологических предсказаний или же гороскопов :) Для начала работы я должен узнать твой день и месяц рождения!)")

if __name__ == '__main__':
    app = ApplicationBuilder().token(data["token"]).build() #создание и вызов экземпляра бота
    app.add_handler(CommandHandler('start', start)) #обработчик команды /start
    app.run_polling() #мониторинг поступающих в бота сообщений