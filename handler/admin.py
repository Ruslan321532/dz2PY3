from random import choice
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import bot
from database.bot_db import sql_command_all, sql_command_delete


async def game_emoji(message: types.Message):
    a = ["🎰", "🎯", "🏀", "⚽", "🎲", "🎳"]
    i = choice(a)
    await bot.send_dice(message.chat.id, emoji=i)


async def delete_data(message: types.Message):
    users = await sql_command_all()
    for user in users:
        await message.answer(
            f"id ={user[0]} mentor id={user[2]} "
            f"name={user[3]} age={user[4]} course_name={user[5]} group_name{user[6]}",
            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f"delete {user[3]}",
                                 callback_data=f"delete {user[0]}"))
        )


async def complete_delete(callback: types.CallbackQuery):
    await sql_command_delete(callback.data.split()[1])
    await callback.answer("Deleted", show_alert=True)
    await callback.message.delete()


def register_handlers_admin(db: Dispatcher):
    db.register_message_handler(game_emoji, commands=['game'])
    db.register_message_handler(delete_data, commands=['delete'])
    db.register_callback_query_handler(complete_delete,
        lambda callback: callback.data and callback.data.startswith("delete "))
