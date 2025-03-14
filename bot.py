import telebot
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

bot = telebot.TeleBot(TOKEN)
