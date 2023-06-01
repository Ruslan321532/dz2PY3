from aiogram import types, Dispatcher
from config import bot


async def echo(message: types.Message):
    a = message.text
    print(a)
    if a.isnumeric():
        a = int(a) ** 2
    await bot.send_message(message.chat.id, a)





def register_handlers_extra(db: Dispatcher):
    db.register_message_handler(echo)

