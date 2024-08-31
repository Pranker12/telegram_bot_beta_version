from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb_location = ReplyKeyboardBuilder()

kb_location.row(types.KeyboardButton(text='Ввести автоматически с текущего местоположения', request_location=True))
kb_location.row(types.KeyboardButton(text='Ввести геолокацию функцией "Геолокация"'))
kb_location.row(types.KeyboardButton(text='Ввести адрес текстом'))
kb_location.row(types.KeyboardButton(text='Вернуться назад'))