def register_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == "🗓 Изменить расписание")
    def change_schedule(message):
        bot.send_message(message.chat.id, "Функция изменения расписания еще не реализована.")

    @bot.message_handler(func=lambda message: message.text == "🔄 Перенести занятие")
    def reschedule_lesson(message):
        bot.send_message(message.chat.id, "Функция переноса занятия еще не реализована.")

    @bot.message_handler(func=lambda message: message.text == "🔄 Запросить перенос занятия")
    def request_lesson_reschedule(message):
        bot.send_message(message.chat.id, "Функция запроса на перенос занятия еще не реализована.")
