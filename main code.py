from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


TOKEN = "5226221353:AAHIkDyNlZEGVuB6C76w9Iqp9prPYl72HH8"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


books = {'-руководство мастера': 'Dungeon Masters Guide - Руководство Мастера RUS 5e .pdf',
         '-книга игрока': 'Players Handbook - Книга игрока RUS 5e .pdf',
         '-бестиарий': 'Monsters Manual - Бестиарий RUS 5e .pdf',
         '-справочник по монстрам': 'Volo_s Guide to Monsters RUS.pdf'}


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply('Мы можем отправить вам основную документацию. Для этого напишите: \n'
                                '-книга игрока \n'
                                '-руководство мастера \n'
                                '-бестиарий \n'
                                '-справочник по монстрам \n')

@dp.message_handler(content_types=["text"])
async def get_text_messages(message: types.Message):
    if message.text in books:
        await message.answer("Подождите минутку")
        await message.answer_animation(open("truck.gif", 'rb'))
        await message.answer_document(open("books\{}".format(books[message.text]), 'rb'))
    else:
        await message.answer("Команда не распознана, напишите /help")

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
