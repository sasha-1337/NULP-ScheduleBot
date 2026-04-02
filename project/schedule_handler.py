import requests
from bs4 import BeautifulSoup
import corps_dataset
import convert_roman_numerals


# Створюємо словник для зберігання розкладів для кожного дня
schedule_for_week = []
weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт"]
studgroup_name = "ІК-41"
group_stud = "sub_1_full"
group_week = "group_chys"
group_stud_and_week = ""
pair_time = {
    "1": "8:30-9:50",
    "2": "10:05-11:25",
    "3": "11:40-13:00",
    "4": "13:15-14:35",
    "5": "14:50-16:10",
    "6": "16:25-17:45",
    "7": "18:00-19:20",
    "8": "19:30-20:50"
}
num_pair_emoji = {
    "1": "1️⃣",
    "2": "2️⃣",
    "3": "3️⃣",
    "4": "4️⃣",
    "5": "5️⃣",
    "6": "6️⃣",
    "7": "7️⃣",
    "8": "8️⃣"
}
corps = corps_dataset.dataset


def set_schedule_parameters(_studgroup_name, _group_stud=group_stud, _group_week=group_week):
    global studgroup_name, group_stud, group_week, group_stud_and_week
    studgroup_name = _studgroup_name
    group_stud = _group_stud
    group_week = _group_week
    if _group_stud == "sub_1_full" and _group_week == "group_chys":
        group_stud_and_week = "sub_1_chys"
    elif _group_stud == "sub_2_full" and _group_week == "group_chys":
        group_stud_and_week = "sub_2_chys"
    elif _group_stud == "sub_1_full" and _group_week == "group_znam":
        group_stud_and_week = "sub_1_znam"
    elif _group_stud == "sub_2_full" and _group_week == "group_znam":
        group_stud_and_week = "sub_2_znam"
    else:
        group_stud_and_week = ""


def get_schedule_html(response):
    # Отримуємо HTML код сторінки
    html_content = response.text
    # Використовуємо BeautifulSoup для парсингу HTML коду
    soup = BeautifulSoup(html_content, "html.parser")
    # Знаходимо блок з розкладом
    schedule = soup.find("div", class_="view-content")
    return schedule


#
def get_schedule():
    # Підготовка параметрів для запиту
    params_1 = {
        "studygroup_abbrname": studgroup_name,
        "semestr": "1",
        "semestrduration": "1"
    }
    params_2 = {
        "studygroup_abbrname": studgroup_name,
        "semestr": "2",
        "semestrduration": "1"
    }

    # Відправка GET запиту на розклад з вказаними параметрами
    url = "https://student.lpnu.ua/students_schedule"
    response = requests.get(url, params=params_1)

    # Перевіряємо, чи успішно виконано запит
    if response.status_code == 200:
        schedule = get_schedule_html(response)

        if schedule is None:  # якщо розклад пустий виконати запит з іншими параметрами
            response_2 = requests.get(url, params=params_2)
            return create_schedule(str(get_schedule_html(response_2)))
        else:
            return create_schedule(str(schedule))
    else:
        return "Помилка: не вдалося з'єднатися з сервером або вхідні дані хибні."


# Функція створення розкладу з отриманих даних
def create_schedule(str_schedule):
    pair_for_week = {
        "Пн": "",
        "Вт": "",
        "Ср": "",
        "Чт": "",
        "Пт": ""
    }
    res = {
        "Пн": [],
        "Вт": [],
        "Ср": [],
        "Чт": [],
        "Пт": []
    }

    # Створити об'єкт BeautifulSoup
    soup = BeautifulSoup(str_schedule, "html.parser")

    # Знаходження всіх елементів з класом 'view-grouping-header' (відповідає за день тижня)
    headers = soup.find_all(class_="view-grouping-header")

    # Алгоритм парсінгу HTML відповіді для отримання розкладу
    if headers:
        # Цикл, який перебирає кожен отриманий день тижня
        for header in headers:
            schedule_ = header.find_next_sibling()

            # Цикл, який окремо зберігає кожен день
            while schedule_ and schedule_.name != "span" and schedule_.text.strip() != "":
                pair_for_week[header.text.strip()] += str(schedule_)
                schedule_ = schedule_.find_next_sibling()
            soup2 = BeautifulSoup(str(pair_for_week[header.text.strip()]), 'html.parser')

            # Цикл, який окремо сортує розклад для кожного дня за фільтрами: group_stud, group_week, "group_full"
            for div in soup2.find_all('div', {'id': [group_stud_and_week,
                                                                group_stud, group_week,
                                                                "group_full"]}):
                content_div = div.find('div', {'class': 'group_content'})

                # Ділить текст на фрагменти: назва пари + викладач
                fragments = [fragment.strip() for fragment in
                             content_div.get_text(strip=True, separator='<br>').split('<br>')
                             if fragment.strip()]
                lesson_number = div.find_previous("h3").get_text()  # Зберігає номер пари

                if content_div:  # Запис результату у список
                    res[header.text.strip()].append((lesson_number, fragments))
        return res
    else:
        return None


# Функція виведення для розкладу
def display_schedule(_day):
    output = ""
    if schedule_for_week:
        if _day not in schedule_for_week:
            print("Розклад для цього дня не знайдено.")
            return None
        pairs = schedule_for_week[_day]
        if not pairs:
            output += f"Розклад для групи: {studgroup_name}\n"
            output += f"Навчальний тиждень: чисельник\n" if group_week == "group_chys" \
                else f"Навчальний тиждень: знаменник\n"
            output += f"Підгрупа: перша\n\n" if group_stud == "sub_1_full" else f"<b>Підгрупа</b>: друга\n\n"
            output += "\nСьгодні пар немає 🥳\n"
            return output
        elif pairs:
            output += f"<b>Розклад для групи</b>: {studgroup_name}\n"
            output += f"<b>Навчальний тиждень</b>: чисельник\n" if group_week == "group_chys" \
                else f"<b>Навчальний тиждень</b>: знаменник\n"
            output += f"<b>Підгрупа</b>: перша\n\n" if group_stud == "sub_1_full" else f"<b>Підгрупа</b>: друга\n\n"

            for index, (pair_number, subject) in enumerate(schedule_for_week[_day]):
                # Знайти римські числа в тексті розкладу та конвертувати
                arabic_numerals = convert_roman_numerals.find_arabic_numerals(subject[1])
                # Якщо знайдено
                if arabic_numerals:
                    # Отримую поточний номер корпусу
                    arabic_numeral = str(arabic_numerals[0])
                    # Дістаю дані з датасету за номером корпусу
                    latitude, longitude, address = corps[arabic_numeral]
                    output += (f"{num_pair_emoji[pair_number] if pair_number
                                  in num_pair_emoji else pair_number}   "
                               f"{subject[0]}\n"
                               # Залишаю посилання в розкладі з точкою корпусу на гугл мапі
                               f"<a href='http://maps.google.com/maps?q={latitude, longitude}'>📍</a>    {subject[1]}\n"
                               f"🕐   {pair_time[pair_number]}\n")
                    # Якщо номера корпусів відсутні, то не створювати посилання
                else:
                    output += (f"{num_pair_emoji[pair_number] if pair_number
                                  in num_pair_emoji else pair_number}"
                               f"   {subject[0]}\n"
                               f"         {subject[1]}\n"
                               f"🕐   {pair_time[pair_number]}\n")
                # Розділяти кожну пару візуально рисками
                if index != len(schedule_for_week[_day])-1:
                    output += "==== ==== ==== ==== ====\n"
    else:
        return None
    return output


# Функція створення розкладу
def fetch_schedule(_studgroup_name, _group_stud, _group_week):
    global schedule_for_week
    set_schedule_parameters(_studgroup_name, _group_stud, _group_week)
    schedule_for_week = get_schedule()


if __name__ == "__main__":
    # Отримання вхідних даних від користувача
    fetch_schedule("ІК-11", "sub_1_full", "group_chys")
    while True:
        day = input(f"\nВведіть день тижня: ")
        print(display_schedule(day))
