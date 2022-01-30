import telebot


bot = telebot.TeleBot('5226221353:AAHIkDyNlZEGVuB6C76w9Iqp9prPYl72HH8')

books = {'-руководство мастера': 'Dungeon Masters Guide - Руководство Мастера RUS 5e .pdf',
         '-книга игрока': 'Players Handbook - Книга игрока RUS 5e .pdf',
         '-бестиарий': 'Monsters Manual - Бестиарий RUS 5e .pdf',
         '-справочник по монстрам': 'Volo_s Guide to Monsters RUS.pdf'}


@bot.message_handler(commands=["start", "help"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Мы можем отправить вам основную документацию. Для этого напишите: \n'
                                '-книга игрока \n'
                                '-руководство мастера \n'
                                '-бестиарий \n'
                                '-справочник по монстрам \n')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text in books:
        bot.send_message(message.chat.id, "Подождите минутку")
        bot.send_animation(message.chat.id, open("truck.gif", 'rb'))
        bot.send_document(message.chat.id, open("books\{}".format(books[message.text]), 'rb'))
    else:
        bot.send_message(message.chat.id, "Команда не распознана, напишите /help")

bot.polling(none_stop=True, interval=0)
