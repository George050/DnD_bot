import random


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


TOKEN = "5226221353:AAHIkDyNlZEGVuB6C76w9Iqp9prPYl72HH8"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dice_flag = False
current_dice = ''

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
        dice_number = int(self.dice[2:])
        #if "-" in self.bonus:
        #    bonus_number = -(int(self.bonus[1:]))
        #elif "+" in self.bonus:
        #    bonus_number = int(self.bonus[1:])
        #else:
        #    bonus_number = int(self.bonus)
        result = int(0)
        for i in range(self.quantity):
            result += random.randint(1, dice_number)
        return result


@dp.message_handler(commands=['start', 'help'])
async def start_and_help(message: types.Message):
    await message.reply('Функции бота: \n /books \n /roll_dice')


@dp.message_handler(commands=['books'])
async def send_books(message: types.Message):
    await message.answer('-книга игрока \n'
                         '-руководство мастера \n'
                         '-бестиарий \n'
                         '-справочник по монстрам')


@dp.message_handler(commands=['roll_dice'])
async def roll_dice(message: types.Message):
    await message.answer('Выберите кость: \n /d2\n /d3\n /d4\n /d6\n /d8\n /d10\n /d20\n /d100')


@dp.message_handler(commands=dices)
async def get_quantity(message: types.Message):
    global current_dice
    global dice_flag
    dice_flag = True
    current_dice = message.text
    await message.answer('Укажите количество бросков (напишите число больше 0)')


@dp.message_handler(content_types=["text"])
async def get_messages(message: types.Message):
    global current_dice
    global dice_flag
    if dice_flag:
        dice_flag = False
        dice = Dices(current_dice, int(message.text), 0)
        await message.answer(str(dice.get_roll()))
    elif message.text in books:
        await message.answer("Подождите минутку")
        await message.answer_animation(open("truck.gif", 'rb'))
        await message.answer_document(open("books\{}".format(books[message.text]), 'rb'))
        await message.answer_animation(open("fff.gif", 'rb'))
    else:
        await message.answer("Команда не распознана, напишите /help")

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)