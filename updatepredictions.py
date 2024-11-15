import requests
from bs4 import BeautifulSoup
import sqlite3

def updatepredictions():
    signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
             'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
    
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()

    for sign in signs:
        url1 = f'https://horoscopes.rambler.ru/{sign}/'
        url2 = f'https://horoscopes.rambler.ru/{sign}/tomorrow'

        response1 = requests.get(url1)
        response2 = requests.get(url2)

        soup1 = BeautifulSoup(response1.text, 'html.parser')
        soup2 = BeautifulSoup(response2.text, 'html.parser')

        # предсказание с сайта рамблер гороскопы
        prediction_div1 = soup1.find('div', class_='dGWT9 cidDQ')
        prediction_div2 = soup2.find('div', class_='dGWT9 cidDQ')

        prediction_text_today = prediction_div1.find('p').get_text()
        prediction_text_tomorrow = prediction_div2.find('p').get_text()

        #получение id соответствующего знака зодиака
        cursor.execute('''
            SELECT zodiac_id FROM ZodiacSigns
            WHERE zodiac_name = ?
        ''', (sign,)
        )
        result = cursor.fetchone()
        zodiac_id = result[0]

        # Обновление бд
        cursor.execute('''
            INSERT OR REPLACE INTO Predictions (prediction_sign_id, prediction_text_today, prediction_text_tomorrow)
            VALUES (?, ?)
            ''', (zodiac_id, prediction_text_today, prediction_text_tomorrow)
            )
    connection.commit()
        
    connection.close()