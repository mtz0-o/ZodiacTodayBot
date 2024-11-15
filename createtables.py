import sqlite3
from updatepredictionstoday import updatepredictionstoday
from updatepredictionstomorrow import updatepredictionstomorrow 


connection = sqlite3.connect('projectzodiac.db')
cursor = connection.cursor()


cursor.execute('''
        CREATE TABLE IF NOT EXISTS ZodiacSigns (
        zodiac_id INTEGER PRIMARY KEY,
        zodiac_name TEXT UNIQUE
        )
''')
connection.commit()

signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
             'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']

for sign in signs:
    cursor.execute('''
    INSERT OR IGNORE INTO ZodiacSigns (zodiac_name) VALUES (?)
    ''', (sign,)
    )
connection.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        user_state TEXT,
        user_sign_id TEXT,
        FOREIGN KEY (user_sign_id) REFERENCES ZodiacSigns(zodiac_id)
    )
''')
connection.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Predictions (
        prediction_sign_id TEXT PRIMARY KEY,
        prediction_text_today TEXT,
        prediction_text_tomorrow TEXT,
        FOREIGN KEY (prediction_sign_id) REFERENCES ZodiacSigns(zodiac_id)
    )
''')


connection.commit()
connection.close()

updatepredictionstoday()
updatepredictionstomorrow()