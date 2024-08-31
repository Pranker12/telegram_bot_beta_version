from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb_keyboard = ReplyKeyboardBuilder()

kb_keyboard.row(types.KeyboardButton(text="Добавить с компьютера"))
kb_keyboard.row(types.KeyboardButton(text="Добавить с телефона"))
kb_keyboard.row(types.KeyboardButton(text="Вернуться назад"))

