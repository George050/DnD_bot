from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from Docum import books

books_kb = ReplyKeyboardMarkup(one_time_keyboard=True)
for i in books:
    books_kb.add(KeyboardButton(i))