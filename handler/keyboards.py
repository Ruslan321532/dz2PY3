from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=3
)

register = KeyboardButton("РЕГИСТРАЦИЯ")
quiz = KeyboardButton("/quiz")
help = KeyboardButton("/help")
contact = KeyboardButton("Share contact", request_contact=True)
location = KeyboardButton("Share location", request_location=True)

start_markup.add(register, quiz, help, contact, location)

cancel_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
)
cancel = KeyboardButton("отмена")
cancel_markup.add(cancel)


gender_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
).add(
    KeyboardButton("MAN"),
    KeyboardButton("WOMAN"),
    KeyboardButton("OTHER"),
    cancel
)

submit_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
).add(
    KeyboardButton("ДА"),
    KeyboardButton("ЗАНОВО"),
    cancel
)

