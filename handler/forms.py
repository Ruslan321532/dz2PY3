from sqlite3 import IntegrityError

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from . import keyboards
from database.bot_db import sql_command_insert


class FSMAdmin(StatesGroup):
    name = State()
    age = State()
    gender = State()
    region = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        await FSMAdmin.name.set()
        await message.answer("Как звать?", reply_markup=keyboards.cancel_markup)
    else:
        await message.answer("Пиши в личке!")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['username'] = f"@{message.from_user.username}" if message.from_user.username else None
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer('Сколько лет?')


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пиши числа!")
    elif not 16 < int(message.text) < 60:
        await message.answer("Доступ воспрещен!")
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer('Какого пола?', reply_markup=keyboards.gender_markup)


async def load_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await FSMAdmin.next()
    await message.answer('Откуда будищь?', reply_markup=keyboards.cancel_markup)


async def load_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['region'] = message.text
    await FSMAdmin.next()
    await message.answer('Скинь фотку)?')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await message.answer_photo(
            data['photo'],
            caption=f"{data['name']} {data['age']} "
                    f"{data['gender']} {data['region']}\n{data['username']}"
        )
    await FSMAdmin.next()
    await message.answer('Все верно?', reply_markup=keyboards.submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        try:
            await sql_command_insert(state)
            await message.answer("Все свободен!")
        except IntegrityError:
            await message.answer("У тебя уже есть анкета йоу!")
        await state.finish()

    elif message.text.lower() == "заново":
        await FSMAdmin.name.set()
        await message.answer("Как звать?")
    else:
        await message.answer("Нипонял!?")


async def cancel_form(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await message.answer("Ну и пошел ты!")


def register_handlers_forms(db: Dispatcher):
    db.register_message_handler(cancel_form, state='*', commands=['cancel'])
    db.register_message_handler(
        cancel_form,
        Text(equals='отмена', ignore_case=True), state='*')

    db.register_message_handler(fsm_start,
                                Text(equals='регистрация', ignore_case=True))
    db.register_message_handler(load_name, state=FSMAdmin.name)
    db.register_message_handler(load_age, state=FSMAdmin.age)
    db.register_message_handler(load_gender, state=FSMAdmin.gender)
    db.register_message_handler(load_region, state=FSMAdmin.region)
    db.register_message_handler(load_photo, state=FSMAdmin.photo,
                                content_types=['photo'])
    db.register_message_handler(submit, state=FSMAdmin.submit)