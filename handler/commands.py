from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot

from database.bot_db import sql_command_random



async def start_handler(message: types.Message):
    with open(r'C:\Users\Admin\Pictures\mem.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)

async  def to_pin(message: types.Message):
    await message.reply_to_message.pin()

async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("NEXT", callback_data="button_1")
    markup.add(button_1)
    question = "Кто создал Телеграмм?"
    answers = [
        "Гарри Поттер",
        "Путин",
        "Дуров, Павел Валерьевич",
        "Guido Van Rossum",
        "Griffin",
        "Linus Torvalds",
    ]

    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        open_period=10,
        reply_markup=markup

    )


async def get_user(message: types.Message):
    user: tuple = await sql_command_random()
    await message.answer(
        f"Имя: {user[3]} Возраст: {user[4]} "
        f"Направлние: {user[5]} Группа: {user[6]} "
    )



def register_handlers_commands(db: Dispatcher):
    db.register_message_handler(start_handler, commands=['mem'])
    db.register_message_handler(quiz_1, commands=['quiz'])
    db.register_message_handler(to_pin, commands=['pin'], commands_prefix='!')
    db.register_message_handler(get_user, commands=['get'])


