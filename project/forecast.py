import os
from dotenv import load_dotenv
load_dotenv()
import requests
from datetime import datetime, timedelta
from googletrans import Translator


# Встановлення API-ключа та міста
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
CITY = os.getenv('CITY', 'Lviv')


# Переклад з англійської на українську
def translate_en_to_uk(description):
    translator = Translator()
    translate_text = translator.translate(description, src='en', dest='uk')
    return translate_text.text


# Функція для отримання JSON прогнозу погоди
def get_weather_forecast():
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)  # Надсилання запиту по АРІ
    data = response.json()  # Отримання JSON відповіді

    if response.status_code == 200:  # Перевірка чи відповідь прийшла успішно
        today = datetime.now().date()  # Отримати дату сьогодні
        tomorrow = today + timedelta(days=1)  # Отримати дату завтра

        today_forecast = next((item for item in data["list"]  # Перевірка чи є прогноз погоди на сьогодні
                               if datetime.fromtimestamp(item["dt"]).date() == today), None)
        tomorrow_forecast = next((item for item in data["list"]  # та запис даних з відповіді
                                  if datetime.fromtimestamp(item["dt"]).date() == tomorrow), None)

        if today_forecast and tomorrow_forecast:  # Перевірка чи є прогноз на сьогодні і завтра
            return format_weather_forecast(today_forecast, tomorrow_forecast)  # Відправити якщо є
        elif today_forecast:  # Перевірка чи є прогноз на сьогодні
            return format_today_weather_forecast(today_forecast)  # Відправити якщо є
        else:
            return "Не вдалося отримати прогноз погоди."
    else:
        return "Помилка при отриманні даних погоди."


def format_today_weather_forecast(today_forecast):
    # Отримання даних прогнозу погоди на сьогодні з JSON
    today_date = datetime.fromtimestamp(today_forecast["dt"]).strftime("%d/%m/%Y")
    today_description = today_forecast["weather"][0]["description"].capitalize()
    today_temp_min = today_forecast["main"]["temp_min"]
    today_temp_max = today_forecast["main"]["temp_max"]
    today_humidity = today_forecast["main"]["humidity"]
    today_rain = today_forecast["rain"]["3h"] if "rain" in today_forecast else 0

    # Створення виводу прогнозу
    output = f"📍Прогноз погоди Львів:\n\n" \
             f"📅Сьогодні ({today_date}):\n" \
             f"📃Опис: {translate_en_to_uk(today_description)}\n" \
             f"🌡Температура: {today_temp_min}-{today_temp_max}°C\n" \
             f"💧Вологість: {today_humidity}%\n" \
             f"☔️Опади: {today_rain} мм\n"
    return output


# Функція для форматування прогнозу погоди
def format_weather_forecast(today_forecast, tomorrow_forecast):
    tomorrow_date = datetime.fromtimestamp(tomorrow_forecast["dt"]).strftime("%d/%m/%Y")

    tomorrow_description = tomorrow_forecast["weather"][0]["description"].capitalize()
    tomorrow_temp_min = tomorrow_forecast["main"]["temp_min"]
    tomorrow_temp_max = tomorrow_forecast["main"]["temp_max"]
    tomorrow_humidity = tomorrow_forecast["main"]["humidity"]
    tomorrow_rain = tomorrow_forecast["rain"]["3h"] if "rain" in tomorrow_forecast else 0

    forecast = f"{format_today_weather_forecast(today_forecast)}\n" \
               f"== == == == ==\n"\
               f"📅Завтра ({tomorrow_date}):\n"\
               f"📃Опис: {translate_en_to_uk(tomorrow_description)}\n"\
               f"🌡Температура: {tomorrow_temp_min}-{tomorrow_temp_max}°C\n"\
               f"💧Вологість: {tomorrow_humidity}%\n"\
               f"☔️Опади: {tomorrow_rain} мм"
    return forecast


# Виклик функції для отримання прогнозу погоди
# weather_forecast = get_weather_forecast()
# print(weather_forecast)
