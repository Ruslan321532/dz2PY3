from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot


async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_2 = InlineKeyboardButton("NEXT", callback_data="button_2")
    markup.add(button_2)

    question = "В каком году был создан Телеграмм?"
    answers = [
        "1991",
        "2001",
        "2013",
        "2019",
        "2032",
        "3232",
    ]
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        open_period=10,
        reply_markup=markup

    )


async def quiz_3(call: types.CallbackQuery):
    question = "Какая компания разработала Телеграмм?"
    answers = [
        "Start Fellows",
        "MTProto",
        "Durov’s Android Challenge",
        "WhatsApp",
        "Digital Fortress",
        "Telegram",
    ]
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=4,
        open_period=10,
    )

def register_handlers_callback(db: Dispatcher):
    db.register_callback_query_handler(quiz_2, text="button_1")
    db.register_callback_query_handler(quiz_3, text="button_2")