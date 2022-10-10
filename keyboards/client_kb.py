from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_load = KeyboardButton('/Надіслати_скаргу')
phonenumb_load = KeyboardButton('Надіслати номер телефону', request_contact=True)


client_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_load)
phonenumb_button = ReplyKeyboardMarkup(resize_keyboard=True).add(phonenumb_load)
