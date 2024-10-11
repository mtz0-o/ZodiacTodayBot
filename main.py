from functions import getzodiacid, checkinput, get_day, get_month, localizeSignRU
from db import save_user, get_prediction_today, get_prediction_tomorrow, update_user_state, get_user_state, get_user_sign, update_user_sign_id
from updatepredictionstoday import updatepredictionstoday
from updatepredictionstomorrow import updatepredictionstomorrow

import json

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from apscheduler.schedulers.asyncio import AsyncIOScheduler


# открытие конфиг файла с токеном бота
with open('config.txt', 'r') as cfg:
  # получение токена бота
  data = json.load(cfg)


def start_keyboard(): #начальная клавиатура пользователя
    return ReplyKeyboardMarkup([
        ['Узнать свой знак зодиака', 'Помощь'],
        ['ТЫК (только для викули)', '/start']
    ], one_time_keyboard=True)

def getPredictionKeyboard(): #процедура для изменения клавиатуры
   return ReplyKeyboardMarkup( [
     ['Предсказание на сегодня', 'Предсказание на завтра'], 
      ['Помощь', '/start']
], one_time_keyboard=True)

def vikaKeyboard(): #процедура для изменения клавиатуры
   return ReplyKeyboardMarkup( [
     ['ЛЮБЛЮ тебя', 'ОБОЖАЮ тебя'], ['/start']
], one_time_keyboard=True)

def schedule_scraping(scheduler): # ежедневное обновление бд
    scheduler.add_job(updatepredictionstoday, 'cron', hour=1, minute=0)  # Запускать ежедневно в 1:00 утра
    scheduler.add_job(updatepredictionstomorrow, 'cron', hour=1, minute=5)


async def start(update: Update, context):
    user_id = update.message.from_user.id
    await update.message.reply_text("Приветик! Я твой бот для астрологических предсказаний или же гороскопов :) Выбери действие: ", reply_markup = start_keyboard())  
   #приветственное сообщение и отправка стартовой клавиатуры
    update_user_state(user_id, None) #ресет статуса юзера в таблице users (при нажатии /start)


async def handle_message(update: Update, context):
   user_id = update.message.from_user.id #запись id пользователя
   user_text = update.message.text #входящее сообщение от пользователя
   user_state = get_user_state(user_id) #статус пользователя из таблицы users

   if user_text == 'Узнать свой знак зодиака': # обработка нажатия на кнопку1
      await update.message.reply_text("Напиши пожалуйста день и месяц своего рождения через точку \
                                       Например, 14.04")
      save_user(user_id, 'awaiting birthdate') #запись пользователя в таблицу Users со статусом ожидания ввода др

   elif user_state=='awaiting birthdate': #обработка др, у пользователей со статусом = awaiting birthdate
      if checkinput(user_text) == 0: # проверка корректности ввода даты см. functions.py
         await update.message.reply_text("Ты ввёл дату в неправильном формате, попробуй ещё раз!")
      else:
         if get_day(user_text) == 11 and get_month(user_text) == 5:
            await update.message.reply_text("Привет, любимая!!!!!")
         user_sign_id = getzodiacid(get_day(user_text), get_month(user_text)) # получение зз пользователя
         update_user_sign_id(user_id, user_sign_id) #запись зз пользователя в таблицу
         update_user_state(user_id, 'zodiac_chosen') # изменение статуса пользователя на "зз выбран"
         usersignRU = localizeSignRU(get_user_sign(user_id))
         await update.message.reply_text(f"Твой знак зодиака - {usersignRU}!")
         await update.message.reply_text(f"Тебе доступны предсказания для {usersignRU}!", reply_markup = getPredictionKeyboard())
         # отправка клавиатуры для получения предсказания



   elif user_state=='zodiac_chosen' and user_text == 'Предсказание на сегодня':
      await update.message.reply_text(get_prediction_today(user_id)) # выдача предсказания соответствующего зз пользователя из таблицы Prediction 

   elif user_state=='zodiac_chosen' and user_text == 'Предсказание на завтра':
      await update.message.reply_text(get_prediction_tomorrow(user_id)) # выдача предсказания на завтра



   elif user_text == 'Помощь': # обработка нажатия на кнопку2
      await update.message.reply_text("Бота разрабатывает @timofeevzakharov, по всем вопросам обращаться туда")
      

   elif user_text == 'ТЫК (только для викули)': # секретное взаимодействие 0_o
      await update.message.reply_text("Я ничево не понимаю в этих человеческих чувствах, но мой создатель хотел передать тебе, что очень сильно тебя любит <33", reply_markup=vikaKeyboard())

   elif user_text == 'ЛЮБЛЮ тебя': # секретное взаимодействие 0_o
      await update.message.reply_text("Если ты - @iits_wiki, то это взаимно...")

   elif user_text == 'ОБОЖАЮ тебя': # секретное взаимодействие 0_o
      await update.message.reply_text("прости, но моё сердце принадлежит вике тищенко (моей обожульке) ")

   elif user_text == 'я люблю макара' or user_text == 'Я ЛЮБЛЮ МАКАРА': # секретное взаимодействие 0_o
      await update.message.reply_text("я тоже тебя люблю!!!!! (если ты @iits_wiki)")

   

if __name__ == '__main__':
    app = ApplicationBuilder().token(data["token"]).build() #создание и вызов экземпляра класса Application
    app.add_handler(CommandHandler('start', start)) #обработчик команды /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) #обработчик поступающих сообщений
    

   # Создание и настройка планировщика
    scheduler = AsyncIOScheduler()
    schedule_scraping(scheduler)
    scheduler.start()
    print ('Бот работает!')
    app.run_polling() #постоянный мониторинг поступающих в бота сообщений