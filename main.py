from functions import getzodiac, checkinput, get_day, get_month
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# открытие конфиг файла с токеном бота
with open('config.txt', 'r') as cfg:
  # получение токена бота
  data = json.load(cfg)

user_state = {} # таблица для хранения статуса пользователя
user_zodiac = {} # таблица для хранения зз пользователя

reply_keyboard = [
     ['Узнать свой знак зодиака', 'Помощь'], 
['ТЫК (только для викули)', '/start']
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True) # создание клавиатуры с кнопками
async def start(update: Update, context):
    user_id = update.message.from_user.id
    await update.message.reply_text("Приветик! Я твой бот для астрологических предсказаний или же гороскопов :) Выбери действие: ", reply_markup = markup)  
    user_state[user_id] = None
    # приветственное сообщение и отправка клавиатуры

async def handle_message(update: Update, context):
   user_id = update.message.from_user.id #запись id пользователя
   user_text = update.message.text #входящее сообщение от пользователя


   if user_text == 'Узнать свой знак зодиака': # обработка нажатия на кнопку1
      await update.message.reply_text("Напиши пожалуйста день и месяц своего рождения через точку \
                                       Например, 14.04")
      user_state[user_id] = 'awaiting birthdate' #присвоение пользовтелю статус: ожидание ввода даты


   elif user_state.get(user_id)=='awaiting birthdate': #обработка др, у пользователей со статусом 'awaiting birthdate'
      if checkinput(user_text) == 0:
         await update.message.reply_text("Ты ввёл дату в неправильном формате, попробуй ещё раз!")
      else:
         zodiac_sign = getzodiac(get_day(user_text), get_month(user_text))
         await update.message.reply_text(f"Твой знак зодиака - {zodiac_sign}!")
         user_state[user_id] = None #обнуление статуса пользователя


   elif user_text == 'Помощь': # обработка нажатия на кнопку2
      await update.message.reply_text("Бота разрабатывает @timofeevzakharov, по всем вопросам обращаться туда")


   elif user_text == 'ТЫК (только для викули)': # обработка нажатия на кнопку3
      await update.message.reply_text("Я ничево не понимаю в этих человеческих чувствах, но мой создатель хотел передать тебе, что очень сильно тебя любит <33")
      


if __name__ == '__main__':
    app = ApplicationBuilder().token(data["token"]).build() #создание и вызов экземпляра класса Application
    app.add_handler(CommandHandler('start', start)) #обработчик команды /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) #обработчик поступающих сообщений
    app.run_polling() #мониторинг поступающих в бота сообщений