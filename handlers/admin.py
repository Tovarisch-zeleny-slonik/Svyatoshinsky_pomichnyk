from aiogram import types, Dispatcher
from createbot import bot
from keyboards import skargy_button
from db import sql_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = None

async def start_skargy(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Активований режим для перегляду скарг', reply_markup=skargy_button)
    await message.delete()

async def get_skargy(message: types.Message):
    if message.from_user.id == ID:
        await sql_db.sql_read(message)


async def delete_skarga(message: types.Message):
    if message.from_user.id == ID:
        read = await sql_db.sql_read_buffer()
        if read:
            for ret in read:
                await bot.send_photo(message.from_user.id, ret[2], f'Скаржник: {ret[0]}\nПроблема: {ret[1]}\nАдреса: {ret[3]}\nНомер телефону: {ret[4]}\nДата: {ret[5]}', reply_markup=\
                    InlineKeyboardMarkup().add(InlineKeyboardButton(f'Видалити скаргу {ret[0]}', callback_data=f'delete {ret[0]}'))) 
        elif read == None:
            await bot.send_message(message.from_user.id, 'На даний момент скарги відсутні.')

async def del_callback_run(callback_query: types.CallbackQuery):
    await sql_db.sql_delete_command(callback_query.data.replace('delete ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("delete ", "")} видалена.', show_alert=True)

def rhc(dp: Dispatcher):
    dp.register_message_handler(start_skargy, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(get_skargy, commands=['Скарги'])
    dp.register_message_handler(delete_skarga, commands=['Видалити'])
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('delete '))
