import random


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

dices = ['d2', 'd3', 'd4', 'd6', 'd8', 'd10', 'd20', 'd100']


class Dices:
    def __init__(self, dice, quantity, bonus):
        self.dice = dice
        self.quantity = int(quantity)
        self.bonus = bonus

    def get_roll(self):
        dice_number = int(self.dice[1:])
        if "-" in self.bonus:
            bonus_number = -(int(self.bonus[1:]))
        elif "+" in self.bonus:
            bonus_number = int(self.bonus[1:])
        else:
            bonus_number = int(self.bonus)
        result = int(bonus_number)
        for i in range(self.quantity):
            result += random.randint(1, dice_number)
        return result


@dp.message_handler(commands=['start', 'help'])
async def start_and_help(message: types.Message):
    await message.reply('Функции бота: \n'
                        '/книги\n'
                        '/бросить_кости')

@dp.message_handler(commands=['книги'])
async def send_books(message: types.Message):
    await message.answer('-книга игрока \n'
                         '-руководство мастера \n'
                         '-бестиарий \n'
                         '-справочник по монстрам')

@dp.message_handler(commands=['бросить_кости'])
async def roll_dice(message: types.Message):
    await message.answer('Выберите кость: \n /d2\n /d3\n /d4\n /d6\n /d8\n /d10\n /d20\n /d100')
    @dp.message_handler(commands=dices)
    async def get_quantity(message: types.Message):
        await message.answer('Укажите количество бросков (напишите число больше 0)')
      #  @dp.message_handler(content_types=["text"])
      #  async def get_messages(message: types.Message):
       #     if message.text in books:


@dp.message_handler(content_types=["text"])
async def get_messages(message: types.Message):
    if message.text in books:
        await message.answer("Подождите минутку")
        await message.answer_animation(open("fff.gif", 'rb'))
        await message.answer_document(open("books\{}".format(books[message.text]), 'rb'))
    else:
        await message.answer("Команда не распознана, напишите /help")

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)