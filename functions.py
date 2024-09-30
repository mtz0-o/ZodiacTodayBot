def getzodiac(day: int, month: int):
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
    
def transformtext(word1, word2):
    if word1<1 | word1>31 | word2<1 | word2>12:
        return 0
    else:
        return 1