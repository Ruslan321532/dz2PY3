import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger


from config import bot
from database.bot_db import sql_command_id


async def go_to_sleep():
    users = await sql_command_id()
    for user in users:
        await bot.send_message(user[0],"С Новым годом!!!С Новым счастьем!!")


async def set_scheduler():
    scheduler = AsyncIOScheduler(timezone="Asia/Bishkek")

    scheduler.add_job(
        go_to_sleep,
        trigger=CronTrigger(
            month=12,
            day=31,
            hour=23,
            minute=59,
            start_date=datetime.datetime.now()
        )
    )
    scheduler.start()

