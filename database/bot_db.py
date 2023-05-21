# SQL - Structured Querry Language
# СУБД - Система Управления Базой Данных
import random
import sqlite3


def sql_create():
    global cursor, ments
    ments = sqlite3.connect("bot.sqlite3")
    cursor = ments.cursor()

    if ments:
        print("База данных подключена!")

    ments.execute("CREATE TABLE IF NOT EXISTS mentors "
        "(id_db INTEGER PRIMARY KEY AUTOINCREMENT,"
        "username VARCHAR (100),"
        "id_mentor INTEGER UNIQUE,"  
        "name VARCHAR (100),"   
        "age INTEGER,"
        "course_name VARCHAR (50),"
        "group_name VARCHAR (50))")

    ments.commit()
async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute(
            "INSERT INTO mentors "
            "(username, id_mentor, name, age, course_name, group_name) "
            "VALUES (?, ?, ?, ?, ?,?)",
            tuple(data.values())
        )
        ments.commit()


async def sql_command_random():
    users = cursor.execute("SELECT * FROM mentors").fetchall()
    random_user = random.choice(users)
    return random_user


async def sql_command_delete(id_db: str):
    cursor.execute("DELETE FROM mentors WHERE id_db= ?", (id_db,))
    ments.commit()


async def sql_command_all():
    return cursor.execute("SELECT * FROM mentors").fetchall()