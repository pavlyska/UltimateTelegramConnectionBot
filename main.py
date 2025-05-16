from config import *


# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для хранения соответствий между сообщениями
message_to_user = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, STARTMS)

# Обработчик текстовых сообщений от пользователей
@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID, content_types=['text', 'photo', 'video', 'document', 'audio'])
def forward_message_to_admin(message):
    try:
        if not message.text and not message.caption and not (message.photo or message.video or message.document or message.audio):
            bot.reply_to(message, TAKEMS)
            return
            
        # Пересылаем сообщение администратору
        forwarded_msg = bot.forward_message(chat_id=ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
        
        # Сохраняем соответствие между ID пересланного сообщения и ID пользователя
        message_to_user[forwarded_msg.message_id] = message.chat.id
        
        if message.content_type == 'text':
            bot.reply_to(message, GIFTMS)
        else:
            bot.reply_to(message, FGIFTMS)
            
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при отправке сообщения. Попробуйте позже.")
        print(f"Ошибка: {e}")

# Обработчик ответов администратора
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID, content_types=['text'])
def reply_to_user(message):
    try:
        # Проверяем, является ли сообщение администратора ответом на другое сообщение
        if message.reply_to_message:
            original_message_id = message.reply_to_message.message_id
            if original_message_id in message_to_user:
                user_id = message_to_user[original_message_id]
                # Отправляем ответ пользователю
                bot.send_message(chat_id=user_id, text=f"OTVET\n{message.text}")
                bot.reply_to(message, AREPLY)
            else:
                bot.reply_to(message, AEROR)
        else:
            bot.reply_to(message, AR)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при отправке ответа.")
        print(f"Ошибка: {e}")

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)