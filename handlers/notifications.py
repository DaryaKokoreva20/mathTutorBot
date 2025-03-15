from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from utils.database import load_table
import telebot
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
TUTOR_ID = int(os.getenv("TUTOR_ID"))  # ID репетитора

def send_lesson_reminders(bot):
    """Отправляет напоминания за 1 час до начала занятия."""
    schedule_df = load_table("schedule")
    now = datetime.now()

    for _, row in schedule_df.iterrows():
        lesson_time = datetime.strptime(row["start_time"], "%H:%M")
        lesson_datetime = datetime.combine(now.date(), lesson_time.time())

        reminder_time = lesson_datetime - timedelta(hours=1)

        if reminder_time.hour == now.hour and reminder_time.minute == now.minute:
            student_id = row["telegram_id"]
            bot.send_message(student_id, f"⏳ Напоминание: у тебя занятие через 1 час с репетитором.")
            bot.send_message(TUTOR_ID, f"⏳ Напоминание: Через 1 час занятие с {row['name']} в {row['start_time']}.")

def check_past_lessons(bot):
    """Спрашивает репетитора в 22:00, прошло ли занятие."""
    schedule_df = load_table("schedule")
    today = datetime.now().date()

    for _, row in schedule_df.iterrows():
        lesson_date = today - timedelta(days=1)  # Проверяем вчерашний день

        message = f"❓ Прошло ли занятие с {row['name']} в {row['start_time']}?"
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("✅ Да", callback_data=f"lesson_yes_{row['id']}"),
            telebot.types.InlineKeyboardButton("❌ Нет", callback_data=f"lesson_no_{row['id']}")
        )
        bot.send_message(TUTOR_ID, message, reply_markup=markup)

def start_scheduler(bot):
    """Запускает планировщик задач для напоминаний и проверки занятий."""
    scheduler = BackgroundScheduler()
    
    # Проверяем напоминания каждые 30 минут
    scheduler.add_job(lambda: send_lesson_reminders(bot), "interval", minutes=30)
    
    # Спрашиваем о прошедших занятиях в 22:00
    scheduler.add_job(lambda: check_past_lessons(bot), "cron", hour=22, minute=0)
    
    scheduler.start()
