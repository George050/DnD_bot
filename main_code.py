import random  # Импорт всех библиотек и необходимых функций
import sqlite3

from urllib.request import urlopen
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dices_code import Dices
from Docum import classes_info, books
from Hero import hero
from flags import flags_change
from KeyBoard import books_kb, dices_kb, classes_kb, main_func_kb, hero_func_kb, yes_or_no_kb, spells_page_kb, pages
from html_parser import music_spis, spell_data, spell_spis, lvl_cls_check

TOKEN = "5226221353:AAHIkDyNlZEGVuB6C76w9Iqp9prPYl72HH8"  # Подключаемся к боту
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
# создание кнопок с именами персонажей

current_dice = ''
classes = ['бард', 'варвар', 'воин', 'волшебник', 'друид', 'жрец', 'изобретатель', 'колдун', 'монах', 'паладин', 'плут',
           'следопыт', 'чародей']

dices = ['d2', 'd3', 'd4', 'd6', 'd8', 'd10', 'd20', 'd100']
stats_names = ["сила", "ловкость", "телосложение", "интеллект", "мудрость", "харизма"]


@dp.message_handler(commands=['start', 'help'])
async def start_and_help(message: types.Message):
    # функция для вывода всех команд бота
    await message.reply('Функции бота: \n/books - Книги по D&D \n/roll_dice - Бросить кости \n/choose_profile - Выбрать'
                        ' профиль для изменения вашего героя или просмотра его характеристик\n/create_profile - Создать'
                        ' нового героя\n/classes - Просмотр всех классов\n'
                        '/spell - Просмотр всех заклинаний и заговоров\n'
                        '/music - Бот отправит вам список всей музыки, которую может предложить\n'
                        '/music_random - Бот отправит случайную музыку\n'
                        '/stop - Остановка всех функций', reply_markup=main_func_kb)


@dp.message_handler(commands=['books'])
async def send_books(message: types.Message):
    # функция для отправки справочников
    await message.answer('Напишите название книги, которую хотите получить: \n'
                         'книга игрока \n'
                         'руководство мастера \n'
                         'бестиарий \n'
                         'справочник по монстрам', reply_markup=books_kb)


@dp.message_handler(commands=['roll_dice'])
async def roll_dice(message: types.Message):
    # выбор кубика
    await message.answer('Выберите кость: \n/d2\n/d3\n/d4\n/d6\n/d8\n/d10\n/d20\n/d100', reply_markup=dices_kb)


@dp.message_handler(commands=dices)
async def get_quantity(message: types.Message):
    # вывод значений броска
    global current_dice
    flags_change(message.from_user.id)
    flags_change(message.from_user.id, di=True)
    current_dice = message.text
    await message.answer('Укажите количество бросков и бонус к броску \nПример:\n 3 -5\n 1 +3\n 8 0')


@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    # функция для остановки всех остальных функций
    dice_flag, delete_flag = flags_change(message.from_user.id)['dice_flag'], \
                             flags_change(message.from_user.id)['delete_flag']
    if dice_flag:
        flags_change(message.from_user.id, di=False)
        await message.reply('Была прекращена функция /roll_dice')
    if delete_flag:
        flags_change(message.from_user.id, de=False)
        await message.reply('Была прекращена функция /delete_flag')


@dp.message_handler(commands=["choose_profile"])
async def choose_profile(message: types.Message):
    # выбор имеющихся в базе данных персонажей
    global names_kb
    do = """SELECT * FROM character_profile"""
    heroes = cur.execute(do).fetchall()
    names_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in command_names:
        names_kb.add(KeyboardButton(i))
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
    # создание персонажа и запись в базу данных
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
    # вывод всех классов
    await message.answer("Существующие классы: \n{}".format("\n".join(classes)), reply_markup=classes_kb)
    await message.answer("Введите название любого класса, чтобы получить информацию о нем")


@dp.message_handler(commands=["hero_info"])
async def hero_info(message: types.Message):
    # вывод информации о герое
    if hero(message.from_user.id) == "":
        await message.answer("Чтобы изменять статы персонажа, выберете его при помощи /choose_profile")
    else:
        answer = []
        request = ''
        do = """SELECT * FROM character_profile WHERE name = '{}'""".format(hero(message.from_user.id))
        info = cur.execute(do).fetchall()[0]
        request += "Имя: {}\nУровень: {}\nКласс: {}\nРаса: {}\n\n".format(info[0], info[3], info[1], info[2])
        do = """SELECT stats FROM character_profile WHERE name = '{}'""".format(hero(message.from_user.id))
        if cur.execute(do).fetchall()[0][0] != None:
            stats = cur.execute(do).fetchall()[0][0].split()
            for i in range(6):
                if ((int(stats[i]) - 10) // 2) >= 0:
                    answer.append("{} = {}(+{})".format(stats_names[i], stats[i], ((int(stats[i]) - 10) // 2)))
                else:
                    answer.append("{} = {}({})".format(stats_names[i], stats[i], ((int(stats[i]) - 10) // 2)))
            request += "\n".join(answer)
        else:
            request += "У вашего персонажа не записаны характеристики, вы можете сделать это при помощи\n/stats_roll"
        request += '\n\nЗаклинания и Заговоры:'
        if info[5] is None or info[5] == "":
            request += "У вашего персонажа нет заклинаний или заговоров"
        else:
            spells = info[5].split(',')
            for i in spells:
                request += '\n{}:\n{}'.format(i, spell_data[i])
        await message.answer(request)


@dp.message_handler(commands=["stats_change"])
async def stats_change(message: types.Message):
    # функция для изменения характеристик выбранного персонажа
    if hero(message.from_user.id) == "":
        await message.answer("Чтобы изменять статы персонажа, выберете его при помощи /choose_profile")
    else:
        do = """SELECT stats FROM character_profile WHERE name = '{}'""".format(hero(message.from_user.id))
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
                    do = """SELECT stats FROM character_profile WHERE name = '{}'""".format(hero(message.from_user.id))
                    stats = cur.execute(do).fetchall()[0][0].split()
                    stats[stats_names.index(text[1])] = str(int(stats[stats_names.index(text[1])]) + bonus_number)
                    if int(stats[stats_names.index(text[1])]) > 30:
                        await message.answer("Параметр не может быть выше 30")
                    elif int(stats[stats_names.index(text[1])]) <= 0:
                        await message.answer("Параметр не может быть ниже 1")
                    else:
                        do = """UPDATE character_profile SET stats = '{}'
                         WHERE name = '{}'""".format(" ".join(stats), hero(message.from_user.id))
                        cur.execute(do)
                        if bonus_number >= 0:
                            await message.answer("Параметр '{}' увеличен на {}\n{} = "
                                                 "{}".format(text[1], text[2], text[1],
                                                             stats[stats_names.index(text[1])]))
                        else:
                            await message.answer("Параметр '{}' уменьшен на {}\n{} = "
                                                 "{}".format(text[1], text[2], text[1],
                                                             stats[stats_names.index(text[1])]))
                        con.commit()
        else:
            await message.answer("У вашего персонажа не записаны характеристики, вы можете сделать это при "
                                 "помощи\n/stats_roll")


@dp.message_handler(commands=["stats_roll"])
async def stats_roll(message: types.Message):
    # случайным образом выбирает значение для характеристик персонажа
    if hero(message.from_user.id) == "":
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
        do = """UPDATE character_profile set stats = '{}' 
        WHERE name = '{}'""".format(stats_in_db, hero(message.from_user.id))
        cur.execute(do)
        con.commit()


@dp.message_handler(commands=["stats_lvlup", "stats_lvldown"])
async def level_up_down(message: types.Message):
    # функция для повышения или понижения уровня персонажа
    if hero(message.from_user.id) == "":
        await message.answer("Чтобы изменять статы персонажа, выберете его при помощи /choose_profile")
    else:
        do = """SELECT level FROM character_profile WHERE name = '{}'""".format(hero(message.from_user.id))
        lvl = cur.execute(do).fetchall()[0][0]
        if "up" in message.text:
            lvl += 1
            if lvl > 20:
                await message.answer("Уровень не может быть выше 20")
                lvl -= 1
            else:
                await message.answer("Уровень повышен на 1 единицу"
                                     "\nНынешний уровень персонажа \n{} - {}".format(hero(message.from_user.id), lvl))
        elif "down" in message.text:
            lvl -= 1
            if lvl < 1:
                await message.answer("Уровень не может быть ниже 1")
                lvl += 1
            else:
                await message.answer("Уровень повышен на 1 единицу"
                                     "\nНынешний уровень персонажа \n{} - {}".format(hero(message.from_user.id), lvl))
        do = """UPDATE character_profile SET level = {} WHERE name = '{}'""".format(lvl, hero(message.from_user.id))
        cur.execute(do)
        con.commit()


@dp.message_handler(commands=['delete_profile'])
async def delete_profile(message: types.Message):
    # удаление персонажа
    await message.reply("Вы точно хотите удалить этот профиль?\nДа или Нет", reply_markup=yes_or_no_kb)
    flags_change(message.from_user.id, de=True)


@dp.message_handler(commands=['music_random'])
async def music_random(message: types.Message):
    # отправка случайного трека
    await message.answer("Пожалуйста, немного подождите, идет загрузка")
    music = random.choice(music_spis)
    filedata = urlopen(music[0])
    datatowrite = filedata.read()
    with open(music[1], 'wb') as f:
        f.write(datatowrite)
    await message.answer_audio(open(''.join(music[1]), 'rb'))


@dp.message_handler(commands=['music'])
async def music(message: types.Message):
    # отправка выбранной музыки
    args = message.get_args().split()
    if args == []:
        answer = ""
        count = 1
        for i in music_spis:
            answer += "{} - {}\n".format(count, i[1][:-4])
            count += 1
        await message.answer(answer)
        await message.reply("Чтобы получить песню введите команду /music и номер песни в одном сообщении")
    elif len(args) == 1:
        try:
            music = music_spis[int(args[0]) - 1]
            filedata = urlopen(music[0])
            datatowrite = filedata.read()
            with open(music[1], 'wb') as f:
                f.write(datatowrite)
            await message.answer_audio(open(''.join(music[1]), 'rb'))
        except Exception:
            await message.answer("Номер песни был введен некорректно")
    else:
        await message.answer("Если хотите получить песню, введите ее номер одним числом")


@dp.message_handler(commands=['add_spell'])
async def add_spell(message: types.message):
    # добавление заклинаний персонажу
    args = message.get_args().capitalize()
    if hero(message.from_user.id) == '':
        await message.answer("Чтобы изменять заклинания персонажа, выберете его при помощи /choose_profile")
    else:
        if args == '':
            await message.answer('Для того чтобы добавить заклинание напишите его полное название. Все '
                                 'заклинания можно просмотреть при помощи команды /spell')
        elif args not in spell_data:
            await message.answer('вы напишите пожалуйста правильно! :)')
        else:
            do = """SELECT level FROM character_profile WHERE name = '{}'""".format(hero(message.from_user.id))
            lvl = cur.execute(do).fetchall()[0][0]
            do = """SELECT class FROM character_profile WHERE name = '{}'""".format(hero(message.from_user.id))
            cls = cur.execute(do).fetchall()[0][0]
            request = lvl_cls_check(args, lvl, cls)
            if request == True:
                do = """SELECT spells FROM character_profile WHERE name = '{}'""".format(hero(message.from_user.id))
                chr_spells = cur.execute(do).fetchall()
                if chr_spells[0][0] == None:
                    spell_req = ','.join([args])
                    await message.answer('Вы добавили заклинание {}'.format(args))
                else:
                    spells = chr_spells[0][0].split(',')
                    if args in spells:
                        await message.answer('Ваш герой уже знает такое заклинание')
                    else:
                        spells.append(args)
                        await message.answer('Вы добавили заклинание {}'.format(args))
                    spell_req = ','.join(spells)
                do = """UPDATE character_profile SET spells = '{}'
                 WHERE name = '{}'""".format(spell_req, hero(message.from_user.id))
                cur.execute(do)
                con.commit()
            else:
                try:
                    request = int(request)
                    await message.answer('Извините, но у вашего персонажа слишком низкий уровень.\nНеобходимый уровень '
                                         '- {}. \nВаш уровень - {}'.format(request, lvl))
                except TypeError:
                    await message.answer("Извините, но вашему классу недопступно это заклинание. \nКлассы, которым "
                                         "доступно это заклинание: {}.\nВаш класс: {}".format(", ".join(request[1:]),
                                                                                              cls))


@dp.message_handler(commands=['delete_spell'])
async def delete_spell(message: types.Message):
    # удаление заклинаний
    if hero(message.from_user.id) == '':
        await message.answer("Чтобы изменять заклинания персонажа, выберете его при помощи /choose_profile")
    else:
        args = message.get_args()
        request = ''
        do = """SELECT spells FROM character_profile WHERE name = '{}'""".format(hero(message.from_user.id))
        spells = cur.execute(do).fetchall()[0][0]
        if args == '':
            if spells is None or spells == "":
                request += "У вашего персонажа уже нет заклинаний или заговоров"
            else:
                spells = spells.split(',')
                for i in range(len(spells)):
                    request += "{} - {}\n".format(i + 1, spells[i])
                request += "\nЧтобы удалить заклинание или заговор введите /delete_spell и номер" \
                           "заклинания или заговора"
        else:
            if spells is None or spells == "":
                request += "У вашего персонажа уже нет заклинаний или заговоров"
            else:
                spells = spells.split(',')
                try:
                    nnnn = spells[int(args)]
                    spells.pop(int(args) - 1)
                    spell_req = ','.join(spells)
                    do = """UPDATE character_profile SET spells = '{}'
                                 WHERE name = '{}'""".format(spell_req, hero(message.from_user.id))
                    cur.execute(do)
                    con.commit()
                    request += "Ваш персонаж забыл заклинание/заговор:\n{}".format(nnnn)
                except Exception:
                    request += "Номер заклинания/заговора ввведен неправильно"
        await message.answer(request)


@dp.message_handler(commands=['spell'])
async def spell_finder(message: types.Message):
    # функция для поиска заклинаний
    args = message.get_args()
    if args.split() == []:
        await message.answer("Чтобы получить список заклинаний, выберите кнопку со страницей или введите несколько "
                             "символов после команды /spell, и бот выдаст вам все заклинания "
                             "с этими символами в названии", reply_markup=spells_page_kb)
    elif args.split()[0].lower() == 'страница':
        args = args.split()
        if int(args[1]) > 0:
            if int(args[1]) < pages:
                await message.answer('\n'.join(spell_spis[(int(args[1]) - 1) * 50: int(args[1]) * 50 - 1]))
            elif int(args[1]) == pages:
                await message.answer('\n'.join(spell_spis[(int(args[1]) - 1) * 50:]))
            else:
                await message.answer("Такой страницы нет")
        else:
            await message.answer("Такой страницы нет")
    else:
        request = []
        for i in spell_spis:
            if args.lower() in i.lower():
                request.append(i)
        if len(request) == 0:
            await message.answer("Извините, но по данному запросу никаких заклинаний не найдено")
        elif len(request) == 1:
            await message.answer('{}\n{}'.format(request[0], spell_data[request[0]]))
        elif len(request) <= 50:
            await message.answer('\n'.join(request))
        elif len(request) > 50:
            request = request[:49]
            request.append('...')
            await message.answer('\n'.join(request))


@dp.message_handler(content_types=["text"])
async def get_messages(message: types.Message):
    # взаимодействие с вводом пользователя
    global current_dice, names, command_names
    dice_flag, delete_flag = flags_change(message.from_user.id)['dice_flag'], \
                             flags_change(message.from_user.id)['delete_flag']
    if message.text in command_names:
        hero(message.from_user.id, name=message.text[1:])
        await message.answer("Выбран герой {}\nТеперь вам доступны команды:\n"
                             "/hero_info\n/stats_change\n/stats_roll\n/stats_lvlup\n"
                             "/stats_lvldown\n/add_spell\n/delete_spell\n"
                             "/delete_profile".format(message.text[1:]), reply_markup=hero_func_kb)
    elif dice_flag:
        text = message.text.split(' ')
        try:
            if int(text[0]) > 0:
                dice = Dices(current_dice, text[0], text[1])
                await message.answer(str(dice.get_roll()))
                flags_change(message.from_user.id, di=False)
        except BaseException:
            flags_change(message.from_user.id, di=True)
    elif delete_flag:
        text = message.text
        if text.lower() == "да":
            do = """DELETE FROM character_profile WHERE name = '{}'""".format(hero(message.from_user.id))
            cur.execute(do)
            con.commit()
            await message.reply("Персонаж {} успешно удален".format(hero(message.from_user.id)))
            hero(123)
            flags_change(message.from_user.id, de=False)
            do = """SELECT name FROM character_profile"""
            names = cur.execute(do).fetchall()
            command_names = ["-" + (i[0]) for i in names]
        elif text.lower() == 'нет':
            await message.reply("Персонаж не будет удален")
            flags_change(message.from_user.id, de=False)
        else:
            await message.reply("Да или Нет", reply_markup=yes_or_no_kb)

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

