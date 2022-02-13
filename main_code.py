import sqlite3


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dices_code import Dices
from Docum import classes_info, books
from Hero import hero_name, hero

TOKEN = "5226221353:AAHIkDyNlZEGVuB6C76w9Iqp9prPYl72HH8"
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

con = sqlite3.connect("dnd_base.db")  # Подключаемся к базам данных
cur = con.cursor()

do = """SELECT name FROM character_profile"""
names = cur.execute(do).fetchall()

dice_flag = False
current_dice = ''
classes = ['бард', 'варвар', 'воин', 'волшебник', 'друид', 'жрец', 'изобретатель', 'колдун', 'монах', 'паладин', 'плут',
           'следопыт', 'чародей']

dices = ['d2', 'd3', 'd4', 'd6', 'd8', 'd10', 'd20', 'd100']


@dp.message_handler(commands=['start', 'help'])
async def start_and_help(message: types.Message):
    await message.reply('Функции бота: \n/books \n/roll_dice \n/choose_profile \n/create_profile \n/classes')


@dp.message_handler(commands=['books'])
async def send_books(message: types.Message):
    await message.answer('Напишите название книги, которую хотите получить: \n'
                         'книга игрока \n'
                         'руководство мастера \n'
                         'бестиарий \n'
                         'справочник по монстрам')


@dp.message_handler(commands=['roll_dice'])
async def roll_dice(message: types.Message):
    await message.answer('Выберите кость: \n/d2\n/d3\n/d4\n/d6\n/d8\n/d10\n/d20\n/d100')


@dp.message_handler(commands=dices)
async def get_quantity(message: types.Message):
    global current_dice
    global dice_flag
    dice_flag = True
    current_dice = message.text
    await message.answer('Укажите количество бросков и бонус к броску \nПример:\n 3 -5\n 1 +3\n 8 0')


@dp.message_handler(commands=["choose_profile"])
async def choose_profile(message: types.Message):
    do = """SELECT * FROM character_profile"""
    heroes = cur.execute(do).fetchall()
    if heroes == []:
        await message.answer("К сожалению, на данный момент в базе данных нет никаких персонажей( \nХотите его "
                             "создать?\n/create_profile")
    else:
        await message.answer("Чтобы выбрать героя введите его имя через слэш")
        for i in range(len(heroes)):
            await message.answer("/{} {} {} {} уровня".format(heroes[i][0], heroes[i][1], heroes[i][2], heroes[i][3]))


@dp.message_handler(commands=["create_profile"])
async def create_profile(message: types.Message):
    global names
    do = """SELECT name FROM character_profile"""
    names = cur.execute(do).fetchall()
    text = message.text.split()
    if len(text) != 4:
        await message.answer("Чтобы создать персонажа вы должны написать \n/create_profile *имя*"
                             " *класс* *раса*\nИмя и раса должны содержать минимум 2 символа, в них не должны быть "
                             "пробелы, имя должно быть написано на английском языке \nЧтобы получить весь список"
                             " классов введите"
                             " /classes")
    else:
        if not (text[2].lower() in classes):
            await message.answer("Ваш класс не входит в список допустимых\nЧтобы получить весь список, "
                                 "напишите\n/classes")
        elif len(text[1]) < 2:
            await message.answer("Ошибка в имени, слишком короткое")
        elif text[1] in names:
            await message.answer("Такое имя уже существует, введите другое")
        else:
            do = """INSERT INTO character_profile(name, class, species, level) 
            VALUES('{}', '{}', '{}', 0)""".format(text[1],
                                                  text[2].lower(),
                                                  text[3])
            cur.execute(do)
            con.commit()
            await message.answer("Ваш персонаж успешно создан и сохранен в базе данных!\n Вы можете его выбрать, введя команду\n/choose_profile")


@dp.message_handler(commands=[i[0] for i in names])
async def hero_choose(message: types.Message):
    hero(name=message.text[1:])
    await message.answer("Выбран герой {}".format(message.text[1:]))


@dp.message_handler(commands=["classes"])
async def classes_list(message: types.Message):
    await message.answer("\n".join(classes))
    await message.answer("Введите название любого класса, чтобы получить информацию о нем")


@dp.message_handler(content_types=["text"])
async def get_messages(message: types.Message):
    global current_dice
    global dice_flag
    if dice_flag:
        text = message.text.split(' ')
        try:
            if int(text[0]) > 0:
                dice = Dices(current_dice, text[0], text[1])
                await message.answer(str(dice.get_roll()))
                dice_flag = False
        except BaseException:
            dice_flag = True
    elif message.text in books:
        await message.answer("Подождите минутку")
        await message.answer_animation(open("truck.gif", 'rb'))
        await message.answer_document(open("books\{}".format(books[message.text]), 'rb'))
        await message.answer_animation(open("fff.gif", 'rb'))
    elif message.text.lower() in classes_info:
        await message.answer("{}".format(classes_info[message.text.lower()]))
    else:
        await message.answer("Команда не распознана, напишите /help")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

