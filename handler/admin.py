from random import choice
from aiogram import types, Dispatcher

from config import bot, ADMINS


async def game_emoji(message: types.Message):
    a = ["🎰", "🎯", "🏀", "⚽","🎲","🎳"]
    i = choice(a)
    await bot.send_dice(message.chat.id, emoji=i)


def register_handlers_admin(db: Dispatcher):
    db.register_message_handler(game_emoji, commands=['game'])