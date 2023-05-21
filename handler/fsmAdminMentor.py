from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import ADMINS
from . import keyboards


class FSMAdmin(StatesGroup):
    id_mentor = State()
    name = State()
    age = State()
    course_name= State()
    group = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private' and message.from_user.id in ADMINS:
        await FSMAdmin.id_mentor.set()
        await message.answer("Какой у вас id?")

    else:
        await message.answer("Ты не админ!")


async def load_id_mentor(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['username'] = f"@{message.from_user.username}" if message.from_user.username else None
        data['id_mentor'] = message.text
    await FSMAdmin.next()
    await message.answer('Как вас зовут? Имя/Фамилия')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer('Сколько вам лет?')

async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пиши числа!")
    elif not 16 < int(message.text) < 60:
        await message.answer("Доступ воспрещен!")
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer('Ваше направление?')


async def load_course_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['course_name'] = message.text
    await FSMAdmin.next()
    await message.answer('Какая группа?')


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await message.answer(f"{data['id_mentor']} {data['name']} {data['age']} "
                    f"{data['course_name']} {data['group']}")
    await FSMAdmin.next()
    await message.answer('Все верно?', reply_markup=keyboards.submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.finish()
        await message.answer("Регистрация прошла успешно!")
    elif message.text.lower() == "заново":
        await FSMAdmin.id_mentor.set()
        await message.answer("Какой у вас id?")


async def cancel_form(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await message.answer("Вы прервали регистрацию!")


def register_handlers_forms(db: Dispatcher):
    db.register_message_handler(cancel_form, state='*', commands=['cancel'])
    db.register_message_handler(
        cancel_form,
        Text(equals='отмена', ignore_case=True), state='*')

    db.register_message_handler(fsm_start,
                                Text(equals='регистрация', ignore_case=True))
    db.register_message_handler(load_id_mentor, state=FSMAdmin.id_mentor)
    db.register_message_handler(load_name, state=FSMAdmin.name)
    db.register_message_handler(load_age, state=FSMAdmin.age)
    db.register_message_handler(load_course_name, state=FSMAdmin.course_name)
    db.register_message_handler(load_group, state=FSMAdmin.group)
    db.register_message_handler(submit, state=FSMAdmin.submit)