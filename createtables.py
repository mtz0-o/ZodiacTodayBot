import sqlite3


connection = sqlite3.connect('projectzodiac.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        user_state TEXT,
        user_sign TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Prediction (
        prediction_id INTEGER PRIMARY KEY,
        sign_name TEXT,
        prediction_text TEXT
    )
''')

connection.commit()
connection.close()