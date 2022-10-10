from aiogram import types, Dispatcher
from createbot import bot
from db.sql_db import sql_add_command
from keyboards import client_button, phonenumb_button
#from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from datetime import datetime


n = datetime.now()

#Формуємо складові машини станів
class FSMAdmin(StatesGroup):
    pib = State()
    opys = State()
    photovideo = State()
    address = State()
    phonenumb = State()


#Запускаємо бот
async def start_bot(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вас вітає Святошинський Помічник 💚\nНаш Бот створений для швидкого зв’язку між Вами та Державними чи Комунальними структурами.',
    reply_markup=client_button)

#Ловимо першу відповідь
async def start_skarga(message: types.Message):
    await FSMAdmin.pib.set()
    await message.reply('🧑🏻‍💻 Підкажіть, як до Вас звертатися (бажано у форматі ПІБ):')

#Ловимо другу відповідь
async def get_pib(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pib'] = message.text
    await FSMAdmin.next()
    await message.reply('🙋🏻‍♂️ Опишіть проблему з якою Ви звертаєтесь:')

#Ловимо третю відповідь
async def get_problem(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['opys_problemy'] = message.text
    await FSMAdmin.next()
    await message.reply('📷 Додайте фото/відео матеріали, щоб доповнити звернення:')

#Ловимо четверту відповідь
async def get_photovideo(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            if message.content_type == 'photo':
                data['photo'] = message.photo[0].file_id
            elif message.content_type == 'video':
                data['video'] = message.video.file_id
            else:
                raise AttributeError("No photo or video")
        await FSMAdmin.next()
        await message.reply('🧭 Введіть адресу проблеми:')
    except AttributeError:
        await message.reply("Надішліть фото або відео!")

#Ловимо п'яту відповідь
async def get_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await FSMAdmin.next()
    await message.reply('📲 Надішліть Ваш номер телефону, задля контакту з Вами:', reply_markup=phonenumb_button)

#Ловимо шосту відповідь й завершуємо машину станів
async def get_phonenumber(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['phonenumber'] = message.contact.phone_number
            data['time'] = str(f'{n.day}.{n.month}.{n.year}---{n.hour}:{n.minute}:{n.second}')
        await sql_add_command(state)
        await message.reply('💚 Дякуємо за Ваше звернення, очікуйте на відповідь по вашому зверненню в найближчий час).\nГарного дня 🙋🏻‍♂️', reply_markup=client_button)
        await state.finish()
    except AttributeError:
        await message.reply("Надішліть свій номер телефону натиснувши на кнопку знизу 💚")

#Вихід з машини стану
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Надіслання скарги відмінено.')

#"Реєстрація" обробників повідомлень (хендлерів)
def rhc(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(start_skarga, commands=['Надіслати_скаргу'], state=None)
    dp.register_message_handler(get_pib, state=FSMAdmin.pib)
    dp.register_message_handler(get_problem, state=FSMAdmin.opys)
    dp.register_message_handler(get_photovideo, content_types=['photo'], state=FSMAdmin.photovideo)
    dp.register_message_handler(get_photovideo, content_types=['video'], state=FSMAdmin.photovideo)
    dp.register_message_handler(get_photovideo, state=FSMAdmin.photovideo)
    dp.register_message_handler(get_address, state=FSMAdmin.address)
    dp.register_message_handler(get_phonenumber, content_types=ContentType.CONTACT, state=FSMAdmin.phonenumb)
    dp.register_message_handler(get_phonenumber, state=FSMAdmin.phonenumb)
    dp.register_message_handler(cancel_handler, state="*", commands='Відміна')
    dp.register_message_handler(cancel_handler, Text(equals='відміна', ignore_case=True), state="*")

    