from functions import getzodiac, checkinput, get_day, get_month
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# открытие конфиг файла с токеном бота
with open('config.txt', 'r') as cfg:
  # получение токена бота
  data = json.load(cfg)

reply_keyboard = [
     ['Узнать свой знак зодиака', 'Помощь'], 
['ТЫК (только для вики тищенко)']
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True) # создание клавиатуры с кнопками
async def start(update: Update, context):
    await update.message.reply_text("Приветик! Я твой бот для астрологических предсказаний или же гороскопов :) \
                                    Выбери действие: ", reply_markup = markup)  # приветственное сообщение и отправка клавиатуры

async def handle_message(update: Update, context):
   user_text = update.message.text
   if user_text == 'Узнать свой знак зодиака':
      await update.message.reply_text("Напиши пожалуйста день и месяц своего рождения через точку \
                                       Например, 14.04")
      user_text = update.message.text
      if checkinput(user_text) == 0:
         await update.message.reply_text("Ты ввёл дату в неправильном формате, попробуй ещё раз!")
      else:
         zodiac_sign = getzodiac(int(get_day(user_text)), int(get_month(user_text)))
         await update.message.reply_text(f"Твой знак зодиака - {zodiac_sign}!")
   elif user_text == 'Помощь':
      await update.message.reply_text("Бота разрабатывает @timofeevzakharov, по всем вопросам обращаться туда")
   elif user_text == 'ТЫК (только для вики тищенко)':
      await update.message.reply_text("Я ничево не понимаю в этих человеческих чувствах, \
                                      но мой создатель 'Макар' хотел передать тебе, \
                                      что очень сильно тебя любит <33")
      
if __name__ == '__main__':
    app = ApplicationBuilder().token(data["token"]).build() #создание и вызов экземпляра класса Application
    app.add_handler(CommandHandler('start', start)) #обработчик команды /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) #обработчик поступающих сообщений
    app.run_polling() #мониторинг поступающих в бота сообщений