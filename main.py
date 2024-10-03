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

reply_keyboard = [ # стартовая клавиатура пользователя
     ['Узнать свой знак зодиака', 'Помощь'], 
['ТЫК (только для викули)', '/start']
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True) # создание клавиатуры с кнопками

def getPredictionKeyboard(): #процедура для изменения клавиатуры
   return ReplyKeyboardMarkup( [
     ['Предсказание на сегодня', 'Помощь'], 
['ТЫК (только для викули)', '/start']
], one_time_keyboard=True)

def vikaKeyboard(): #процедура для изменения клавиатуры
   return ReplyKeyboardMarkup( [
     ['ЛЮБЛЮ тебя', 'ОБОЖАЮ тебя'], ['/start']
], one_time_keyboard=True)

async def start(update: Update, context):
    user_id = update.message.from_user.id
    await update.message.reply_text("Приветик! Я твой бот для астрологических предсказаний или же гороскопов :) Выбери действие: ", reply_markup = markup)  
    user_state[user_id] = None #ресет статуса юзера (при нажатии /start)
    # приветственное сообщение и отправка стартовой клавиатуры

async def handle_message(update: Update, context):
   user_id = update.message.from_user.id #запись id пользователя
   user_text = update.message.text #входящее сообщение от пользователя

   if user_text == 'Узнать свой знак зодиака': # обработка нажатия на кнопку1
      await update.message.reply_text("Напиши пожалуйста день и месяц своего рождения через точку \
                                       Например, 14.04")
      user_state[user_id] = 'awaiting birthdate' #присвоение пользовтелю (от которого ожидается ввод др) статуса awaiting birthdate

   elif user_state.get(user_id)=='awaiting birthdate': #обработка др, у пользователей со статусом = awaiting birthdate
      if checkinput(user_text) == 0:
         await update.message.reply_text("Ты ввёл дату в неправильном формате, попробуй ещё раз!")
      else:
         user_zodiac[user_id] = getzodiac(get_day(user_text), get_month(user_text))
         await update.message.reply_text(f"Твой знак зодиака - {user_zodiac[user_id]}!")
         user_state[user_id] = 'zodiac_chosen' #статус юзера - зз выбран
         await update.message.reply_text(f"Теперь тебе доступно предсказание для {user_zodiac[user_id]} на сегодня!", reply_markup = getPredictionKeyboard())

   elif user_text == 'Предсказание на сегодня': 
      await update.message.reply_text("Тут пока ничево нет, но скоро обязательно что-то будет!!!")

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
    app.run_polling() #постоянный мониторинг поступающих в бота сообщений