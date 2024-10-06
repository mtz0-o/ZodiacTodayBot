import requests
from bs4 import BeautifulSoup
import sqlite3

def scrape_and_update_predictions():
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
        prediction_text = prediction_div.find('p').get_text()

        # Обновление бд
        cursor.execute('''
            INSERT OR REPLACE INTO Prediction (sign_name, prediction_text)
            VALUES (?, ?)
        ''', (sign, prediction_text))
    
    connection.commit()
    connection.close()