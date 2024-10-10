import sqlite3


def save_user(user_id, user_state):
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()
    # SQL-запрос для внесения данных о пользователе
    cursor.execute('''
        INSERT OR REPLACE INTO Users (user_id, user_state)
        VALUES (?, ?)
    ''', (user_id, user_state))
    connection.commit()
    connection.close()

def update_user_state(user_id, new_state):
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()
    # SQL-запрос для обновления статуса пользователя
    query = """
    UPDATE Users
    SET user_state = ?
    WHERE user_id = ?
    """
    cursor.execute(query, (new_state, user_id))
    connection.commit()
    connection.close()

def update_user_sign_id(user_id, new_sign_id):
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()
    # SQL-запрос для обновления поля знак зодиака пользователя
    query = """
    UPDATE Users
    SET user_sign_id = ?
    WHERE user_id = ?
    """
    cursor.execute(query, (new_sign_id, user_id))
    connection.commit()
    connection.close()

def get_user_state(user_id):
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()
    # SQL-запрос для получения статуса пользователя
    query = """
    SELECT user_state
    FROM Users
    WHERE user_id = ?
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    connection.close()
    # Если результат есть, вернуть статус, иначе вернуть None
    if result:
        return result[0]
    else:
        return None
    
def get_user_sign(user_id):
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()
    # SQL-запрос для получения знака зодиака пользователя
    query = """
    SELECT zodiac_name FROM ZodiacSigns 
    INNER JOIN Users 
    ON Users.user_sign_id = ZodiacSigns.zodiac_id
    WHERE Users.user_id = ?
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    else:
        return None

def get_prediction_today(user_id):
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()
    # запрос для получения предсказания из таблицы Predictions
    cursor.execute('''
        SELECT prediction_text_today FROM Predictions
        INNER JOIN Users
        ON Users.user_sign_id = Predictions.prediction_sign_id
        WHERE user_id = ?
    ''', (user_id,))
    prediction = cursor.fetchone()
    connection.close()
    if prediction:
        return prediction[0]
    else:
        return "Предсказание не найдено."
    
def get_prediction_tomorrow(user_id):
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()
    # запрос для получения предсказания из таблицы Predictions
    cursor.execute('''
        SELECT prediction_text_tomorrow FROM Predictions
        INNER JOIN Users
        ON Users.user_sign_id = Predictions.prediction_sign_id
        WHERE user_id = ?
    ''', (user_id,))
    prediction = cursor.fetchone()
    connection.close()
    if prediction:
        return prediction[0]
    else:
        return "Предсказание не найдено."
   

