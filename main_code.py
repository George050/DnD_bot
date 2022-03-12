import sqlite3


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dices_code import Dices
from Docum import classes_info, books
from Hero import hero
from KeyBoard import books_kb, dices_kb, classes_kb, main_func_kb, hero_func_kb

TOKEN = "5226221353:AAHIkDyNlZEGVuB6C76w9Iqp9prPYl72HH8"
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

con = sqlite3.connect("dnd_base.db")  # Подключаемся к базам данных
cur = con.cursor()

do = """SELECT name FROM character_profile"""
names = cur.execute(do).fetchall()
command_names = ["-"+(i[0]) for i in names]
names_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for i in command_names:
    names_kb.add(KeyboardButton(i))

dice_flag = False
current_dice = ''
classes = ['бард', 'варвар', 'воин', 'волшебник', 'друид', 'жрец', 'изобретатель', 'колдун', 'монах', 'паладин', 'плут',
           'следопыт', 'чародей']

dices = ['d2', 'd3', 'd4', 'd6', 'd8', 'd10', 'd20', 'd100']
stats_names = ["сила", "ловкость", "телосложение", "интеллект", "мудрость", "харизма"]


@dp.message_handler(commands=['start', 'help'])
async def start_and_help(message: types.Message):
    await message.reply('Функции бота: \n/books - Книги по D&D \n/roll_dice - Бросить кости \n/choose_profile - Выбрать'
                        ' профиль для изменения вашего героя или просмотра его характеристик\n/create_profile - Создать'
                        ' нового героя\n/classes - Просмотр всех классов\n'
                        '/stop - Остановка всех функций', reply_markup=main_func_kb)


@dp.message_handler(commands=['books'])
async def send_books(message: types.Message):
    await message.answer('Напишите название книги, которую хотите получить: \n'
                         'книга игрока \n'
                         'руководство мастера \n'
                         'бестиарий \n'
                         'справочник по монстрам', reply_markup=books_kb)


@dp.message_handler(commands=['roll_dice'])
async def roll_dice(message: types.Message):
    await message.answer('Выберите кость: \n/d2\n/d3\n/d4\n/d6\n/d8\n/d10\n/d20\n/d100', reply_markup=dices_kb)


@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    global dice_flag
    if dice_flag:
        dice_flag = False
        await message.reply('Была прекращена функция /roll_dice')


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
        await message.answer("Чтобы выбрать героя введите его имя через тире '-'", reply_markup=names_kb)
        for i in range(len(heroes)):
            await message.answer("-{} {} {} {} уровня".format(heroes[i][0], heroes[i][1], heroes[i][2], heroes[i][3]))
        await message.answer("Если хотите создать нового персонажа напишите\n/create_profile")


@dp.message_handler(commands=["create_profile"])
async def create_profile(message: types.Message):
    global names, command_names, names_kb
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
            VALUES('{}', '{}', '{}', 1)""".format(text[1],
                                                  text[2].lower(),
                                                  text[3])
            cur.execute(do)
            con.commit()
            await message.answer("Ваш персонаж успешно создан и сохранен в базе данных!\nВы можете его выбрать,"
                                 " введя команду\n/choose_profile")
    do = """SELECT name FROM character_profile"""
    names = cur.execute(do).fetchall()
    command_names = ["-"+(i[0]) for i in names]
    names_kb = ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in command_names:
        names_kb.add(KeyboardButton(i))


@dp.message_handler(commands=["classes"])
async def classes_list(message: types.Message):
    await message.answer("Существующие классы: \n{}".format("\n".join(classes)), reply_markup=classes_kb)
    await message.answer("Введите название любого класса, чтобы получить информацию о нем")


@dp.message_handler(commands=["stats_get"])
async def stats_get(message: types.Message):
    if hero() == "":
        await message.answer("Чтобы изменять статы персонажа, выберете его при помощи /choose_profile")
    else:
        answer = []
        do = """SELECT stats FROM character_profile WHERE name = '{}'""".format(hero())
        if cur.execute(do).fetchall()[0][0] != None:
            stats = cur.execute(do).fetchall()[0][0].split()
            for i in range(6):
                if ((int(stats[i]) - 10) // 2) >= 0:
                    answer.append("{} = {}(+{})".format(stats_names[i], stats[i], ((int(stats[i]) - 10) // 2)))
                else:
                    answer.append("{} = {}({})".format(stats_names[i], stats[i], ((int(stats[i]) - 10) // 2)))
            await message.answer("\n".join(answer))
        else:
            await message.answer("У вашего персонажа не записаны характеристики, вы можете сделать это при "
                                 "помощи\n/stats_roll")


@dp.message_handler(commands=["stats_change"])
async def stats_change(message: types.Message):
    if hero() == "":
        await message.answer("Чтобы изменять статы персонажа, выберете его при помощи /choose_profile")
    else:
        do = """SELECT stats FROM character_profile WHERE name = '{}'""".format(hero())
        if cur.execute(do).fetchall()[0][0] != None:
            text = message.text.split()
            if len(text) != 3:
                await message.answer("Чтобы изменить статы вашего героя, введите:\n/stats_change *характеристика* "
                                     "*количество очков*\n/stats_change сила 2\n/stats_change ловкость -1")
            else:
                if text[1] in stats_names:
                    if "-" in text[2]:
                        bonus_number = -(int(text[2][1:]))
                    elif "+" in text[2]:
                        bonus_number = int(text[2][1:])
                    else:
                        bonus_number = int(text[2])
                    do = """SELECT stats FROM character_profile WHERE name = '{}'""".format(hero())
                    stats = cur.execute(do).fetchall()[0][0].split()
                    stats[stats_names.index(text[1])] = str(int(stats[stats_names.index(text[1])]) + bonus_number)
                    if int(stats[stats_names.index(text[1])]) > 30:
                        await message.answer("Параметр не может быть выше 30")
                    elif int(stats[stats_names.index(text[1])]) <= 0:
                        await message.answer("Параметр не может быть ниже 1")
                    else:
                        do = """UPDATE character_profile SET stats = '{}' WHERE name = '{}'""".format(" ".join(stats), hero())
                        cur.execute(do)
                        if bonus_number >= 0:
                            await message.answer("Параметр '{}' увеличен на {}\n{} = "
                                                 "{}".format(text[1], text[2], text[1], stats[stats_names.index(text[1])]))
                        else:
                            await message.answer("Параметр '{}' уменьшен на {}\n{} = "
                                                 "{}".format(text[1], text[2], text[1], stats[stats_names.index(text[1])]))
                        con.commit()
        else:
            await message.answer("У вашего персонажа не записаны характеристики, вы можете сделать это при "
                                 "помощи\n/stats_roll")


@dp.message_handler(commands=["stats_roll"])
async def stats_roll(message: types.Message):
    if hero() == "":
        await message.answer("Чтобы изменять статы персонажа, выберете его при помощи /choose_profile")
    else:
        stats = []
        dice_class = Dices(6, 4, 0)
        for i in range(6):
            stats.append(dice_class.create_stats())
        answer = []
        for i in range(6):
            if stats[i][1] >= 0:
                answer.append("{} = {}(+{})".format(stats_names[i], stats[i][0], stats[i][1]))
            else:
                answer.append("{} = {}({})".format(stats_names[i], stats[i][0], stats[i][1]))
        await message.answer("\n".join(answer))
        stats_in_db = " ".join(str(i[0]) for i in stats)
        do = """UPDATE character_profile set stats = '{}' WHERE name = '{}'""".format(stats_in_db, hero())
        cur.execute(do)
        con.commit()


@dp.message_handler(commands=["stats_lvlup", "stats_lvldown"])
async def level_up_down(message: types.Message):
    if hero() == "":
        await message.answer("Чтобы изменять статы персонажа, выберете его при помощи /choose_profile")
    else:
        do = """SELECT level FROM character_profile WHERE name = '{}'""".format(hero())
        lvl = cur.execute(do).fetchall()[0][0]
        if "up" in message.text:
            lvl += 1
            if lvl > 20:
                await message.answer("Уровень не может быть выше 20")
                lvl -= 1
            else:
                await message.answer("Уровень повышен на 1 единицу"
                                     "\nНынешний уровень персонажа \n{} - {}".format(hero(), lvl))
        elif "down" in message.text:
            lvl -= 1
            if lvl < 1:
                await message.answer("Уровень не может быть ниже 1")
                lvl += 1
            else:
                await message.answer("Уровень повышен на 1 единицу"
                                     "\nНынешний уровень персонажа \n{} - {}".format(hero(), lvl))
        do = """UPDATE character_profile SET level = {} WHERE name = '{}'""".format(lvl, hero())
        cur.execute(do)
        con.commit()


@dp.message_handler(content_types=["text"])
async def get_messages(message: types.Message):
    global current_dice, command_names
    global dice_flag
    if message.text in command_names:
        hero(name=message.text[1:])
        await message.answer("Выбран герой {}\nТеперь вам доступны команды:\n"
                             "/stats_get\n/stats_change\n/stats_roll\n/stats_lvlup\n/stats_lvldown".format(message.text[1:]), reply_markup=hero_func_kb)
    elif dice_flag:
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

