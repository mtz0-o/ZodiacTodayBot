def get_zodiac_sign(day, month):
    if ((month==3) and (day>=21)) or ((month==4) and (day<=20)):
        return "овен"
    elif ((month==4) and (day>=21)) or ((month==5) and (day<=20)):
        return "телец"
    elif ((month==5) and (day>=21)) or ((month==6) and (day<=21)):
        return "близнецы"
    elif ((month==6) and (day>=22)) or ((month==7) and (day<=22)):
        return "рак"
    elif ((month==7) and (day>=23)) or ((month==8) and (day<=23)):
        return "лев"
    elif ((month==8) and (day>=24)) or ((month==9) and (day<=23)):
        return "дева"
    elif ((month==9) and (day>=24)) or ((month==10) and (day<=23)):
        return "весы"
    elif ((month==10) and (day>=24)) or ((month==11) and (day<=22)):
        return "скорпион"
    elif ((month==11) and (day>=23)) or ((month==12) and (day<=21)):
        return "стрелец"
    elif ((month==12) and (day>=22)) or ((month==1) and (day<=20)):
        return "козерог"
    elif ((month==1) and (day>=21)) or ((month==2) and (day<=20)):
        return "водолей"
    else:
        return "рыбы"
    