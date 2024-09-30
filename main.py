from functions import getzodiac
from functions import transformtext
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# открытие конфиг файла с токеном
with open('config.txt', 'r') as cfg:
  # получение токена бота
  data = json.load(cfg)

async def start(update: Update, context):
    await update.message.reply_text("Приветик! Я твой бот для астрологических предсказаний или же гороскопов :) \
                                    Для начала работы я должен узнать твой день и месяц рождения! (например: 14.04).") # приветственное сообщение

async def handle_message(update: Update, context):
   user_text = update.message.text
   message_words = user_text.split('.') #разбиение ввода на массив с разделителем "."

   if len(message_words)!=2 or not(message_words[0].isdigit) or not(message_words[1].isdigit):
      await update.message.reply_text("Ты ввёл дату в неправильном формате, попробуй ещё раз!") #проверка длины массива из строк, проверка на числа
      return
   
   day = message_words[0]
   month = message_words[1]

   if transformtext(int(day), int(month)) == 0:
      await update.message.reply_text("Ты ввёл дату в неправильном формате, попробуй ещё раз!") # обработка случая когда дата выходит за рамки
   else:
      zodiac_sign = getzodiac(int(day), int(month))
      await update.message.reply_text(f"Твой знак зодиака - {zodiac_sign}!")
      
      
if __name__ == '__main__':
    app = ApplicationBuilder().token(data["token"]).build() #создание и вызов экземпляра класса Application
    app.add_handler(CommandHandler('start', start)) #обработчик команды /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) #обработчик поступающих сообщений
    app.run_polling() #мониторинг поступающих в бота сообщений