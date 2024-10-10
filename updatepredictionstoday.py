import requests
from bs4 import BeautifulSoup
import sqlite3

def updatepredictionstoday():
    signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
             'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
    
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()

    for sign in signs:
        url = f'https://horoscopes.rambler.ru/{sign}/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # предсказание с сайта рамблер гороскопы
        prediction_div = soup.find('div', class_='dGWT9 cidDQ')
        prediction_text_today = prediction_div.find('p').get_text()

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
            INSERT OR REPLACE INTO Predictions (prediction_sign_id, prediction_text_today)
            VALUES (?, ?)
            ''', (zodiac_id, prediction_text_today)
            )
    connection.commit()
        
    connection.close()