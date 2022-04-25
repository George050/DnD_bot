from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from Docum import books
from html_parser import spell_data

books_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for i in books:
    books_kb.add(KeyboardButton(i))

dices = ['d2', 'd3', 'd4', 'd6', 'd8', 'd10', 'd20', 'd100', 'stop']
dices_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for i in dices:
    dices_kb.add(KeyboardButton("/{}".format(i)))

classes = ['бард', 'варвар', 'воин', 'волшебник', 'друид', 'жрец', 'изобретатель', 'колдун', 'монах', 'паладин', 'плут',
           'следопыт', 'чародей', '/stop']
classes_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for i in classes:
    classes_kb.add(KeyboardButton(i))

main_func = ['/books', '/roll_dice', '/choose_profile', '/create_profile', '/classes', '/stop', '/spell',
             '/music', '/music_random']
main_func_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for i in main_func:
    main_func_kb.add(i)

hero_func = ['/hero_info', '/stats_change', '/stats_roll', '/stats_lvlup', '/stats_lvldown', '/add_spell',
             'delete_spell', '/delete_profile', '/stop']
hero_func_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for i in hero_func:
    hero_func_kb.add(i)

yes_or_no_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
yes_or_no_kb.add(KeyboardButton("Да"), KeyboardButton("Нет"))

spells_page_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
pages = len(spell_data) / 50
if pages >= len(spell_data) // 50:
    pages = int(pages) + 1
for i in range(pages):
    spells_page_kb.add(KeyboardButton("/spell Страница {}".format(i + 1)))