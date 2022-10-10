from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


skargy_list = KeyboardButton("/Скарги")
delete_list = KeyboardButton("/Видалити")

skargy_button = ReplyKeyboardMarkup(resize_keyboard=True).add(skargy_list).add(delete_list)


