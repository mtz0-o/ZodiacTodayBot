import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# Opens the file in read-only mode and assigns the contents to the variable cfg to be accessed further down
with open('config.json', 'r') as cfg:
  # Deserialize the JSON data (essentially turning it into a Python dictionary object so we can use it in our code) 
  data = json.load(cfg) 

async def start(update: Update, context):
    await update.message.reply_text("Приветик! Я твой бот для астрологических предсказаний или же гороскопов :) /n Для начала я должен узнать твой день и месяц рождения!)")

if __name__ == '__main__':
    app = ApplicationBuilder().token(data["token"]).build() #создание и вызов экземпляра бота
    app.add_handler(CommandHandler('start', start)) #обработчик команды /start
    app.run_polling() #мониторинг поступающих в бота сообщений