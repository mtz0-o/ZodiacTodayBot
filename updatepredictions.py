import requests
from bs4 import BeautifulSoup
import sqlite3

signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
             'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']

def parse_html(sign):
    url_today = f'https://horoscopes.rambler.ru/{sign}/'
    url_tomorrow = f'https://horoscopes.rambler.ru/{sign}/tomorrow/'

    response_today = requests.get(url_today)
    response_tomorrow = requests.get(url_tomorrow)

    soup_today = BeautifulSoup(response_today.text, 'html.parser')
    soup_tomorrow = BeautifulSoup(response_tomorrow.text, 'html.parser')

    # предсказание с сайта рамблер гороскопы
    prediction_div1 = soup_today.find('div', class_='dGWT9 cidDQ')
    prediction_div2 = soup_tomorrow.find('div', class_='dGWT9 cidDQ')

    prediction_text_today = prediction_div1.find('p').get_text()
    prediction_text_tomorrow = prediction_div2.find('p').get_text()

    predictions_text = [prediction_text_today, prediction_text_tomorrow]
    
    return predictions_text

def updatepredictions():
    
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()

    for sign in signs:
        
        prediction_text_today = parse_html(sign)[0]
        prediction_text_tomorrow = parse_html(sign)[1]

        #получение id соответствующего знака зодиака
        cursor.execute('''
            SELECT zodiac_id FROM ZodiacSigns
            WHERE zodiac_name = ?
        ''', (sign,)
        )
        result = cursor.fetchone()
        zodiac_id = result[0]

        # Обновление предсказаний в таблице
        cursor.execute('''
            INSERT OR REPLACE INTO Predictions (prediction_sign_id, prediction_text_today, prediction_text_tomorrow)
            VALUES (?, ?, ?)
        ''', (zodiac_id, prediction_text_today, prediction_text_tomorrow))

        
    connection.commit()
    connection.close()