import telebot
from handlers.students import add_student  # Импортируем функцию добавления ученика
from utils.database import load_table

def register_handlers(bot):
    @bot.message_handler(commands=['schedule'])
    def send_schedule(message):
        """Команда /schedule – показать расписание занятий"""
        df = load_table("schedule")
        if df.empty:
            bot.send_message(message.chat.id, "📅 Расписание пустое.")
        else:
            bot.send_message(message.chat.id, f"📅 Расписание:\n{df.to_string(index=False)}")

    @bot.message_handler(commands=['students'])
    def send_students_list(message):
        """Команда /students – список учеников"""
        df = load_table("students")
        if df.empty:
            bot.send_message(message.chat.id, "👨‍🎓 Список учеников пуст.")
        else:
            bot.send_message(message.chat.id, f"👨‍🎓 Ученики:\n{df.to_string(index=False)}")

    @bot.message_handler(commands=['parents'])
    def send_parents_list(message):
        """Команда /parents – список родителей"""
        df = load_table("parents")
        if df.empty:
            bot.send_message(message.chat.id, "👨‍👩‍👦 Список родителей пуст.")
        else:
            bot.send_message(message.chat.id, f"👨‍👩‍👦 Родители:\n{df.to_string(index=False)}")

    @bot.message_handler(commands=['add_student'])
    def handle_add_student(message):
        """Команда /add_student – вызывает функцию из students.py"""
        add_student(bot, message)
