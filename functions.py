def getzodiac(day: int, month: int): #функция для определения зз
    if ((month==3) and (day>=21)) or ((month==4) and (day<=20)):
        return "Овен"
    elif ((month==4) and (day>=21)) or ((month==5) and (day<=20)):
        return "Телец"
    elif ((month==5) and (day>=21)) or ((month==6) and (day<=21)):
        return "Близнецы"
    elif ((month==6) and (day>=22)) or ((month==7) and (day<=22)):
        return "Рак"
    elif ((month==7) and (day>=23)) or ((month==8) and (day<=23)):
        return "Лев"
    elif ((month==8) and (day>=24)) or ((month==9) and (day<=23)):
        return "Дева"
    elif ((month==9) and (day>=24)) or ((month==10) and (day<=23)):
        return "Весы"
    elif ((month==10) and (day>=24)) or ((month==11) and (day<=22)):
        return "Скорпион"
    elif ((month==11) and (day>=23)) or ((month==12) and (day<=21)):
        return "Стрелец"
    elif ((month==12) and (day>=22)) or ((month==1) and (day<=20)):
        return "Козерог"
    elif ((month==1) and (day>=21)) or ((month==2) and (day<=20)):
        return "Водолей"
    else:
        return "Рыбы"
    
def checkdate(word1, word2):
    if word1<1 or word1>31 or word2<1 or word2>12:
        return 0
    else:
        return 1
    
def get_day(message):
    message_words = message.split('.') #разбиение сообщения на список строк с разделителем "."
    return int(message_words[0])

def get_month(message):
    message_words = message.split('.') 
    return int(message_words[1])
    
def checkinput(message):
    message_words = message.split('.') 
    if len(message_words)!=2 or not(message_words[0].isdigit()) or not(message_words[1].isdigit()):
      #длина списка должна быть = 2, т.к. (14 и 04) - дата и месяц, /n
      #проверка, что обе части сообщения состоят из цифр 
      return 0
    elif checkdate(get_day(message), get_month(message)) == 0:
      return 0 # обработка случая когда введенная дата выходит за рамки
    else:
      return 1