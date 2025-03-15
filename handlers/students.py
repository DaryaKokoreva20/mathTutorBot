from utils.database import save_data, load_users

data = load_users()

def register_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == "👤 Добавить ученика")
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
                save_data(data)
                bot.send_message(message.chat.id, f"Ученик {student_id} добавлен!")
        except ValueError:
            bot.send_message(message.chat.id, "Некорректный ID. Введи число.")
