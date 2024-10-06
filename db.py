import sqlite3


def save_user(user_id, user_state, user_sign):
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO Users (user_id, user_state, user_sign)
        VALUES (?, ?, ?)
    ''', (user_id, user_state, user_sign))
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

def update_user_sign(user_id, new_sign):
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()
    query = """
    UPDATE Users
    SET user_sign = ?
    WHERE user_id = ?
    """
    cursor.execute(query, (new_sign, user_id))
    connection.commit()
    connection.close()

def get_user_state(user_id):
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()
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
    query = """
    SELECT user_sign
    FROM Users
    WHERE user_id = ?
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    else:
        return None

def get_prediction(user_sign):
    connection = sqlite3.connect('projectzodiac.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT prediction_text FROM Prediction
        WHERE sign_name = ?
    ''', (user_sign,))
    prediction = cursor.fetchone()
    connection.close()
    if prediction:
        return prediction[0]
    else:
        return "Предсказание не найдено."
   

