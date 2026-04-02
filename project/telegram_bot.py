import os
from dotenv import load_dotenv
load_dotenv()
import sys
sys.path.append('./project')
import corps_dataset
import forecast
import schedule_handler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler

# Підключення датасету з адресами корпусів
corps = corps_dataset.dataset

# Глобальна змінна для зберігання тексту користувача
user_text = ""

# Дані за замовчуванням для надисалланя запитів
selected_day = "Пн"
selected_group = "sub_1_full"
selected_fraction = "qroup_chys"

# Змінні для зберігання стану кнопок
group_1_text = None
group_2_text = None
numerator_text = None
denominator_text = None

# Глобальну константу для стану розмови
CORPS = 0
WEATHER = 0
START = 0


# Функція для обробки команди /start
def start(update, context):
    global user_text
    user_text = ""
    context.bot.send_message(chat_id=update.effective_chat.id, text="📝Введіть назву групи (наприклад ІК-41)")
    return START


# Функція для зберігання та опрацювання вхідних даних від користувача
def get_start_text(update, context):
    global user_text, corps
    
    user_text = update.message.text

    verify_schedule = update_schedule(update, context)
    # Перевірка чи група була введена вірно
    if verify_schedule is None:
        update.message.reply_text(text="❌Невірна назва групи")
        return START   # Розпочати запит назви групи наново
    else:
        # Початковий стан кнопок меню
        keyboard = [[InlineKeyboardButton(format_day_button("Пн"), callback_data="101"),
                    InlineKeyboardButton(format_day_button("Вт"), callback_data="102"),
                    InlineKeyboardButton(format_day_button("Ср"), callback_data="103"),
                    InlineKeyboardButton(format_day_button("Чт"), callback_data="104"),
                    InlineKeyboardButton(format_day_button("Пт"), callback_data="105")],   
                    [InlineKeyboardButton("⚙️Налаштування", callback_data="settings")]]
        reply_markup_inine_key = InlineKeyboardMarkup(keyboard)

        # Відправити розклад користувачеві
        update.message.reply_text(
                text="Привіт, {0.first_name}! Ось твій розклад!".format(update.message.from_user))
        update.message.reply_text(text=verify_schedule, reply_markup=reply_markup_inine_key,
                                  parse_mode='HTML', disable_web_page_preview=True)

        # Змінити стан діалогу про запит розкладу на завершено
        return ConversationHandler.END


# Функція для оновлення розкладу після взаємодії з меню
def button_callback(update, context):
    global selected_group, selected_fraction, selected_day
    global group_1_text, group_2_text, numerator_text, denominator_text

    query = update.callback_query  # Отримання данних від користувача
    data = query.data              # Кнопки які він натиснув (callback_data)

    if data in ["101", "102", "103", "104", "105"]:  # Визначає який день тижня було обрано
        days = ["Пн", "Вт", "Ср", "Чт", "Пт"]
        day_index = int(data) - 101  # Отримати індекс дня тижня
        selected_day = days[day_index]  # Зберегти обрани день тижня в змінну
        keyboard = [[InlineKeyboardButton(format_day_button("Пн"), callback_data="101"),
                     InlineKeyboardButton(format_day_button("Вт"), callback_data="102"),
                     InlineKeyboardButton(format_day_button("Ср"), callback_data="103"),
                     InlineKeyboardButton(format_day_button("Чт"), callback_data="104"),
                     InlineKeyboardButton(format_day_button("Пт"), callback_data="105")],
                    [InlineKeyboardButton("⚙️Налаштування", callback_data="settings")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        schedule = schedule_handler.display_schedule(selected_day)
        query.edit_message_text(text=("Розклад відсутній" if schedule is None     # Повернути користувачеві розклад
                                      else schedule), reply_markup=reply_markup,
                                parse_mode='HTML', disable_web_page_preview=True)  # який відповідає дню тижня
    elif data == "settings":  # Меню налаштувань
        # Відображення налаштувань меню
        group_1_text = "👉1 група" if selected_group == "sub_1_full" else "1 група"  # Визначаю та зберігаю стан
        group_2_text = "👉2 група" if selected_group == "sub_2_full" else "2 група"  # кнопок, які вибрав користувач
        numerator_text = "👉чисельник" if selected_fraction == "group_chys" else "чисельник"
        denominator_text = "👉знаменник" if selected_fraction == "group_znam" else "знаменник"
        keyboard_settings = [[InlineKeyboardButton(group_1_text, callback_data="group_1"),
                              InlineKeyboardButton(group_2_text, callback_data="group_2")],  # Зберігаю вигляд
                             [InlineKeyboardButton(numerator_text, callback_data="numerator"),
                              InlineKeyboardButton(denominator_text, callback_data="denominator")],  # нової клавіатури
                             [InlineKeyboardButton("❗️Видалити розклад❗️", callback_data="delete"),
                              InlineKeyboardButton("Повернутись назад↩️", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard_settings)      # Повертаю вигляд нової
        query.edit_message_reply_markup(reply_markup=reply_markup)  # клавіатури користувачу
    elif data == "group_1":
        selected_group = "sub_1_full"
        update_settings_menu(query, context)  # Якщо обрана одна з опцій,
    elif data == "group_2":                   # то модифікувати значення змінної,
        selected_group = "sub_2_full"         # яка відповідає за цю кнопку,
        update_settings_menu(query, context)  # викликавши update_settings_menu
    elif data == "numerator":
        selected_fraction = "group_chys"
        update_settings_menu(query, context)
    elif data == "denominator":
        selected_fraction = "group_znam"
        update_settings_menu(query, context)
    elif data == "delete":  # Очистити розклад
        delete_schedule()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Розклад видалено🗑")
    elif data == "back":  # Кнопка виходу з меню налаштувань до розкладу
        keyboard = [[InlineKeyboardButton(format_day_button("Пн"), callback_data="101"),
                     InlineKeyboardButton(format_day_button("Вт"), callback_data="102"),
                     InlineKeyboardButton(format_day_button("Ср"), callback_data="103"),
                     InlineKeyboardButton(format_day_button("Чт"), callback_data="104"),
                     InlineKeyboardButton(format_day_button("Пт"), callback_data="105")],
                    [InlineKeyboardButton("⚙️Налаштування", callback_data="settings")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        schedule = update_schedule(update, context)
        query.edit_message_text(text=("Розклад відсутній" if schedule is None
                                      else schedule), reply_markup=reply_markup,
                                parse_mode='HTML', disable_web_page_preview=True)


# Функція оновлення стану меню налаштувань
def update_settings_menu(query, context):
    global group_1_text, group_2_text, numerator_text, denominator_text
    group_1_text = "👉1 група" if selected_group == "sub_1_full" else "1 група"  # Визначаю та зберігаю стан
    group_2_text = "👉2 група" if selected_group == "sub_2_full" else "2 група"  # кнопок, які вибрав користувач
    numerator_text = "👉чисельник" if selected_fraction == "group_chys" else "чисельник"
    denominator_text = "👉знаменник" if selected_fraction == "group_znam" else "знаменник"
    keyboard = [[InlineKeyboardButton(group_1_text, callback_data="group_1"),
                 InlineKeyboardButton(group_2_text, callback_data="group_2")],  # зберігаю вигляд нової клавіатури
                [InlineKeyboardButton(numerator_text, callback_data="numerator"),
                 InlineKeyboardButton(denominator_text, callback_data="denominator")],
                [InlineKeyboardButton("❗️Видалити розклад❗️", callback_data="delete"),
                 InlineKeyboardButton("Повернутись назад↩️", callback_data="back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_reply_markup(reply_markup=reply_markup)


# Функція, яка отримує розклад та повертає його
def update_schedule(update, context):
    global user_text, selected_group, selected_fraction

    schedule_handler.fetch_schedule(user_text, selected_group, selected_fraction)
    # Логує в консоль запит про розклад
    print(user_text, selected_day, selected_group, selected_fraction)
    return schedule_handler.display_schedule(selected_day)


# Функція яка очищає розклад
def delete_schedule():
    schedule_handler.set_schedule_parameters("", "", "")


# Функція, яка позначає кнопку дня тижня як вибрану
def format_day_button(day):
    return "☑️" + day if selected_day == day else day


# Функція  для обробки команди /weather. Надсилає прогноз погоди
def weather(update, context):
    update.message.reply_text(text=forecast.get_weather_forecast())
    return ConversationHandler.END


# Функція для обробки команди /get_corps. Запитує номер корпусу
def get_corps(update, context):
    global user_text
    user_text = ""
    # Відправляємо сповіщення, що бот обробляє запит
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    # Перевіряємо, чи введена назва місця є в списку
    update.message.reply_text('Введіть номер корпусу, наприклад, головний - "0" і т.д.')
    return CORPS


def get_text_corps(update, context):
    global user_text, corps
    user_text = update.message.text  # Запитувати текст наново
    keyboard_2 = [[KeyboardButton('Розклад занять🗓', callback_data="schedule")],
                  [KeyboardButton('Погода⛅️', callback_data="weather"),
                   KeyboardButton('Карта📍', callback_data="map")]]  # Початковий стан кнопок клавіатури
    reply_markup_reply_key = ReplyKeyboardMarkup(keyboard_2, one_time_keyboard=True)

    if user_text in corps:  # перевірити чи введено номер корпусу
        latitude, longitude, address = corps[user_text]  # отримати широту та довготу
        update.message.reply_text(text=f"Адреса {user_text} корпусу: {address}",
                                  reply_markup=reply_markup_reply_key)
        update.message.reply_location(latitude=latitude, longitude=longitude)  # надіслати мітку локації користувачу
        return ConversationHandler.END
    else:
        update.message.reply_text("Місце не знайдено. Будь ласка, оберіть місце зі списку або введіть інше.")
        return CORPS  # Якщо місце не знайдено повідомити користувачу
    pass


def cancel(update, context):
    # Функція для скасування поточної розмови
    context.bot.send_message(chat_id=update.effective_chat.id, text="Операція скасована.")
    return ConversationHandler.END


def main():
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    # Обробник для команди /start і Розклад занять🗓
    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      MessageHandler(Filters.regex('^(Розклад занять🗓)$'), start)],
        states={
            START: [MessageHandler(Filters.text & ~Filters.command, get_start_text)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(start_handler)

    # Обробник для команди /map і Карта📍
    map_handler = ConversationHandler(
        entry_points=[CommandHandler('map', get_corps),
                      MessageHandler(Filters.regex('^(Карта📍)$'), get_corps)],
        states={
            CORPS: [MessageHandler(Filters.text & ~Filters.command, get_text_corps)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(map_handler)

    # Обробник для команди /weather і тексту "Погода⛅️"
    weather_handler = ConversationHandler(
        entry_points=[CommandHandler('weather', weather),
                      MessageHandler(Filters.regex('^(Погода⛅️)$'), weather)],
        states={},
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(weather_handler)

    # Обробник для взаємодії з inline меню
    dispatcher.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()


if __name__ == '__main__':
    main()
