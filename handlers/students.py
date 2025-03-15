from utils.database import save_data, load_users, load_table, save_table
import telebot

data = load_users()

def add_student(bot, message):
    """Функция добавления ученика (запрашивает данные после добавления ID)"""
    user_id = message.chat.id
    if user_id != data["tutor_id"]:
        bot.send_message(user_id, "❌ Только репетитор может добавлять учеников.")
        return

    bot.send_message(user_id, "✏️ Введи Telegram ID ученика:")
    bot.register_next_step_handler(message, process_student_id, bot)

def process_student_id(message, bot):
    """Проверяет, есть ли ученик в JSON, если нет – добавляет и запрашивает данные"""
    try:
        student_id = int(message.text)
        if student_id in data["students"]:
            bot.send_message(message.chat.id, "⚠️ Этот ученик уже добавлен.")
        else:
            data["students"].append(student_id)
            save_data(data)
            bot.send_message(message.chat.id, "✅ Ученик добавлен! Теперь введи его имя:")
            bot.register_next_step_handler(message, process_student_name, bot, student_id)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Некорректный ID. Введи число.")

def process_student_name(message, bot, student_id):
    """Запрашивает фамилию после имени"""
    student_name = message.text.strip()
    bot.send_message(message.chat.id, "✏️ Введи фамилию ученика:")
    bot.register_next_step_handler(message, process_student_last_name, bot, student_id, student_name)

def process_student_last_name(message, bot, student_id, student_name):
    """Запрашивает предмет обучения после фамилии"""
    student_last_name = message.text.strip()
    bot.send_message(message.chat.id, "✏️ Введи предмет (например, 'ЕГЭ'/'ОГЭ'/'Подтянуть'):")
    bot.register_next_step_handler(message, process_student_role, bot, student_id, student_name, student_last_name)

def process_student_role(message, bot, student_id, student_name, student_last_name):
    """Запрашивает цену за час после предмета"""
    student_role = message.text.strip()
    bot.send_message(message.chat.id, "💰 Введи цену за час занятий:")
    bot.register_next_step_handler(message, process_student_price, bot, student_id, student_name, student_last_name, student_role)

def process_student_price(message, bot, student_id, student_name, student_last_name, student_role):
    """Запрашивает ID родителя (если есть)"""
    try:
        student_price = float(message.text)
        bot.send_message(message.chat.id, "📞 Введи Telegram ID родителя (если нет – напиши 0):")
        bot.register_next_step_handler(message, process_student_parent, bot, student_id, student_name, student_last_name, student_role, student_price)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Некорректная цена. Введи число.")

def process_student_parent(message, bot, student_id, student_name, student_last_name, student_role, student_price):
    """Сохраняет ученика во все Excel-таблицы"""
    try:
        parent_id = int(message.text) if message.text.strip() != "0" else None

        # Обновляем students.xlsx
        students_df = load_table("students")
        new_student = {
            "telegram_id": student_id,
            "first_name": student_name,
            "last_name": student_last_name,
            "role": student_role,
            "hourly_rate": student_price,
            "parent_id": parent_id
        }
        students_df = students_df.append(new_student, ignore_index=True)
        save_table("students", students_df)

        # Обновляем parents.xlsx (если есть родитель)
        if parent_id:
            parents_df = load_table("parents")
            if parent_id not in parents_df["telegram_id"].values:
                bot.send_message(message.chat.id, "👨‍👩‍👦 Теперь введи ФИО родителя:")
                bot.register_next_step_handler(message, process_parent_name, bot, parent_id, student_name)
            else:
                bot.send_message(message.chat.id, "✅ Ученик успешно добавлен!")
        else:
            bot.send_message(message.chat.id, "✅ Ученик успешно добавлен!")

    except ValueError:
        bot.send_message(message.chat.id, "❌ Некорректный ID родителя. Введи число.")

def process_parent_name(message, bot, parent_id, student_name):
    """Запрашивает номер телефона родителя и сохраняет"""
    parent_name = message.text.strip()
    bot.send_message(message.chat.id, "📞 Введи номер телефона родителя:")
    bot.register_next_step_handler(message, process_parent_phone, bot, parent_id, parent_name, student_name)

def process_parent_phone(message, bot, parent_id, parent_name, student_name):
    """Сохраняет родителя в таблицу"""
    parent_phone = message.text.strip()
    parents_df = load_table("parents")
    new_parent = {
        "telegram_id": parent_id,
        "full_name": parent_name,
        "child_name": student_name,
        "phone_number": parent_phone
    }
    parents_df = parents_df.append(new_parent, ignore_index=True)
    save_table("parents", parents_df)

    bot.send_message(message.chat.id, "✅ Родитель успешно добавлен!")
