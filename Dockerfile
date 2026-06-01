# Используем легкую версию Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# Выполняем миграции при старте (чтобы база db.sqlite3 была готова)
RUN python manage.py migrate

# Приложение внутри контейнера будет работать на стандартном порту 8000
EXPOSE 8000

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]