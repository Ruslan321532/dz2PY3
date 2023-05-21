from decouple import config, Csv
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

TOKEN = config("TOKEN")

bot = Bot(token=TOKEN)
db = Dispatcher(bot=bot, storage=storage)

ADMINS = config("ADMINS", cast=Csv(post_process=tuple, cast=int))