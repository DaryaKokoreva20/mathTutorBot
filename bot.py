import telebot
from dotenv import load_dotenv
import os
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"

# Загружаем список пользователей
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {"tutor_ids": [], "students": []}


# Функция для сохранения данных
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


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
        KeyboardButton("👤 Добавить ученика")
    )
    return keyboard


# Клавиатура для ученика
def student_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("📩 Отправить ДЗ на проверку"))
    keyboard.add(KeyboardButton("🔄 Запросить перенос занятия"))
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    # Проверяем, кто пользователь
    if user_id == data["tutor_id"]:
        bot.send_message(
            user_id,
            "Привет, репетитор! Ты авторизован.",
            reply_markup=tutor_menu()
        )
    elif user_id in data["students"]:
        bot.send_message(
            user_id,
            "Привет, ученик! Ты авторизован.",
            reply_markup=student_menu()
        )
    else:
        bot.send_message(user_id, "Ты не в списке учеников. Доступ запрещен.")


# Обработчики кнопок (пока заглушки)
@bot.message_handler(func=lambda message: message.text == "Отправить ДЗ")
def send_homework(message):
    bot.send_message(
        message.chat.id, "Функция отправки ДЗ еще не реализована."
    )


@bot.message_handler(
        func=lambda message: message.text == "Отправить ДЗ на проверку")
def hand_in_homework(message):
    bot.send_message(
        message.chat.id,
        "Функция отправки ДЗ на проверку еще не реализована."
    )


@bot.message_handler(
        func=lambda message: message.text == "Изменить расписание")
def change_schedule(message):
    bot.send_message(
        message.chat.id,
        "Функция изменения расписания еще не реализована."
    )


@bot.message_handler(func=lambda message: message.text == "Перенести занятие")
def reschedule_lesson(message):
    bot.send_message(
        message.chat.id,
        "Функция переноса занятия еще не реализована."
    )


@bot.message_handler(
        func=lambda message: message.text == "Запросить перенос занятия")
def request_lesson_reschedule(message):
    bot.send_message(
        message.chat.id,
        "Функция запроса на перенос занятия еще не реализована."
    )


@bot.message_handler(
        func=lambda message: message.text == "Отчет о прошедших занятиях")
def report_lessons(message):
    bot.send_message(
        message.chat.id,
        "Функция отчетов еще не реализована."
    )


@bot.message_handler(func=lambda message: message.text == "Общее сообщение")
def general_message(message):
    bot.send_message(
        message.chat.id,
        "Функция массовых сообщений еще не реализована."
    )


@bot.message_handler(func=lambda message: message.text == "Добавить ученика")
def add_student(message):
    user_id = message.chat.id
    if user_id != data["tutor_id"]:
        bot.send_message(user_id, "Только репетитор может добавлять учеников.")
        return

    bot.send_message(user_id, "Введи Telegram ID ученика:")
    bot.register_next_step_handler(message, save_student)


def save_student(message):
    try:
        student_id = int(message.text)
        if student_id in data["students"]:
            bot.send_message(message.chat.id, "Этот ученик уже добавлен.")
        else:
            data["students"].append(student_id)
            save_data()
            bot.send_message(message.chat.id, f"Ученик {student_id} добавлен!")
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ID. Введи число.")


bot.polling()
