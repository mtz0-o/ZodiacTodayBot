FROM python:3.10-slim

WORKDIR /app

# Копируем файлы в контейнер
COPY config.txt requirements.txt db.py createtables.py functions.py main.py updatepredictionstoday.py updatepredictionstomorrow.py ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 5000
EXPOSE 5000

# Выполняем команды для создания таблиц и запуска основного скрипта
CMD ["bash", "-c", "python createtables.py && python main.py"]