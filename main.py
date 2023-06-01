from aiogram.utils import executor
import logging

from config import db, bot, ADMINS

from handler import commands, callback, admin, forms, fsmAdminMentor, extra, notifications, qr_generate
from database.bot_db import sql_create


async def on_startup(db):
    await notifications.set_scheduler()
    await bot.send_message(ADMINS[0], "Я родился!")
    sql_create()


async def on_shutdown(db):
    await bot.send_message(ADMINS[0], "Пока пока!")

commands.register_handlers_commands(db)
callback.register_handlers_callback(db)
admin.register_handlers_admin(db)
fsmAdminMentor.register_handlers_forms(db)

forms.register_handlers_forms(db)

qr_generate.register_handlers_generate_qr(db)



# extra.register_handlers_extra(db)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(db, skip_updates=True, on_startup=on_startup,
                           on_shutdown=on_shutdown)