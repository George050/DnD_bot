from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from Docum import books

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

main_func = ['/books', '/roll_dice', '/choose_profile', '/create_profile', '/classes', '/stop']
main_func_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for i in main_func:
    main_func_kb.add(i)

hero_func = ['/stats_get', '/stats_change', '/stats_roll', '/stats_lvlup', '/stats_lvldown', '/stop']
hero_func_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for i in hero_func:
    hero_func_kb.add(i)