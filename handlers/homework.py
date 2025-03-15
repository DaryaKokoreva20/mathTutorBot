def register_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == "📚 Отправить ДЗ")
    def send_homework(message):
        bot.send_message(message.chat.id, "Функция отправки ДЗ еще не реализована.")

    @bot.message_handler(func=lambda message: message.text == "📩 Отправить ДЗ на проверку")
    def hand_in_homework(message):
        bot.send_message(message.chat.id, "Функция отправки ДЗ на проверку еще не реализована.")
