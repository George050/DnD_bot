import telebot


bot = telebot.TeleBot('5226221353:AAHIkDyNlZEGVuB6C76w9Iqp9prPYl72HH8')


@bot.message_handler(commands=["start", "help"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Мы можем отправить вам основную документацию. Для этого напишите: \n'
                                '-книга игрока \n'
                                '-руководство мастера \n'
                                '-бестиарий \n'
                                '-справочник по монстрам \n')

@bot.message_handler(content_types=["text"])
def handle_text(message):

    bot.send_message(message.chat.id, 'Я неготов, поэтому выведу вам это: \n Вы написали: ' + message.text)

bot.polling(none_stop=True, interval=0)