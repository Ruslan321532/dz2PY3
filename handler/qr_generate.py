from aiogram import types, Dispatcher
import pyqrcode as pq

from config import bot


async def qr_create(message: types.Message):

    url = message.text

    qr_code = pq.create(url)
    qr_code.png('code.png', scale=6)

    with open('code.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)


def register_handlers_generate_qr(db: Dispatcher):
    db.register_message_handler(qr_create, commands='qr')



