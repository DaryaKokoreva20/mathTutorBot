from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура для репетитора
def tutor_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("📚 Отправить ДЗ"),
        KeyboardButton("🗓 Изменить расписание")
    )
    keyboard.add(
        KeyboardButton("🔄 Перенести занятие"),
        KeyboardButton("📢 Общее сообщение")
    )
    keyboard.add(
        KeyboardButton("📊 Отчет о прошедших занятиях"),
    )
    return keyboard

# Клавиатура для ученика
def student_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("📩 Отправить ДЗ на проверку"))
    keyboard.add(KeyboardButton("🔄 Запросить перенос занятия"))
    return keyboard
