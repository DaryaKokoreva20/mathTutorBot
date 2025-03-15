import telebot
import json
import os
from handlers.menu import tutor_menu, student_menu
from utils.database import save_data, load_users

DATA_FILE = "users.json"
data = load_users()

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        user_id = message.chat.id

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
