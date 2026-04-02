# Використовуємо офіційний образ Python
FROM python:3.12

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /tg_bot

# Копіюємо requirements.txt для встановлення залежностей
COPY requirements.txt .

# Встановлюємо залежності Python
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь вихідний код проекту у контейнер
COPY . .

# Відкриваємо порт для Telegram бота (якщо потрібно)
EXPOSE 8080

# Команда для запуску Telegram бота
CMD ["python", "main.py"]