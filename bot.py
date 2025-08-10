import telebot

# ضع التوكن الخاص بك هنا
TOKEN = "8062995274:AAErOwOGL090cuu9ZOjWeBOt7ym9ydrRV9w"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def reply_message(message):
    bot.send_message(message.chat.id, "Done!")

print("Bot is running...")
bot.polling()
