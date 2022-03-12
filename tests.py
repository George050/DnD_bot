from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import time
import random

TOKEN = "5226221353:AAHIkDyNlZEGVuB6C76w9Iqp9prPYl72HH8"
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

button_dice = KeyboardButton('/dice')
button_time = KeyboardButton('/timer')

greet_kb = ReplyKeyboardMarkup(one_time_keyboard=True)
greet_kb.add(button_dice)
greet_kb.add(button_time)

dice_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
dice_kb.add(KeyboardButton("кинуть один шестигранный кубик"), KeyboardButton("кинуть 2 шестигранных кубика одновременно"),
            KeyboardButton("кинуть 20-гранный кубик"), KeyboardButton("вернуться назад"))

timer_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
timer_kb.add(KeyboardButton("30 секунд"), KeyboardButton("1 минута"), KeyboardButton("5 минут"),
             KeyboardButton("вернуться назад"))


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Начнем?", reply_markup=greet_kb)


@dp.message_handler(commands=['dice'])
async def dice_command(message: types.Message):
    await message.reply("Что делать?", reply_markup=dice_kb)


@dp.message_handler(commands=['timer'])
async def timer_command(message: types.Message):
    await message.reply("Что делать?", reply_markup=timer_kb)


@dp.message_handler(content_types=['text'])
async def answers(message: types.Message):
    tt = message.text
    if tt == "кинуть один шестигранный кубик":
        await message.reply("{}".format(random.randint(1, 6)))
    elif tt == "кинуть 2 шестигранных кубика одновременно":
        await message.reply('{}'.format(random.randint(2, 12)))
    elif tt == "кинуть 20-гранный кубик":
        await message.reply('{}'.format(random.randint(1, 20)))
    elif tt == "30 секунд":
        await message.reply("Отсчет пошел")
        tt1 = time.time()
        tt2 = time.time()
        while tt2 - tt1 < 30:
            tt2 = time.time()
        await message.reply("Время вышло")
    elif tt == "1 минута":
        await message.reply("Отсчет пошел")
        tt1 = time.time()
        tt2 = time.time()
        while tt2 - tt1 < 60:
            tt2 = time.time()
        await message.reply("Время вышло")
    elif tt == "5 минут":
        await message.reply("Отсчет пошел")
        tt1 = time.time()
        tt2 = time.time()
        while tt2 - tt1 < 300:
            tt2 = time.time()
        await message.reply("Время вышло")
    elif tt == "вернуться назад":
        await message.reply("Еще разок?", reply_markup=greet_kb)


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)