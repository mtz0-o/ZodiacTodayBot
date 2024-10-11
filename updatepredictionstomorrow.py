import requests
from bs4 import BeautifulSoup
import sqlite3

def updatepredictionstomorrow():
    signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
             'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
    
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()
  
    for sign in signs:
        url = f'https://horoscopes.rambler.ru/{sign}/tomorrow/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # предсказание с сайта рамблер гороскопы
        prediction_div = soup.find('div', class_='dGWT9 cidDQ')
        prediction_text = prediction_div.find('p').get_text()

        #получение id соответствующего знака зодиака
        cursor.execute('''
            SELECT zodiac_id FROM ZodiacSigns
            WHERE zodiac_name = ?
        ''', (sign,)
        )
        result = cursor.fetchone()
        zodiac_id = result[0]

        #создание записи если не существует
        cursor.execute('''
            INSERT OR IGNORE INTO Predictions (prediction_sign_id)
            VALUES (?)
        ''', (zodiac_id,))

        # Обновление предсказания
        cursor.execute('''
            UPDATE Predictions
            SET prediction_text_tomorrow = ?
            WHERE prediction_sign_id = ?               
            ''', (prediction_text, zodiac_id)
            )
    
    connection.commit()
    connection.close()