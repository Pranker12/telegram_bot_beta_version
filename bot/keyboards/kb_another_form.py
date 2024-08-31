from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb_another_form = ReplyKeyboardBuilder()

kb_another_form.row(types.KeyboardButton(text='Заполнить еще одну форму'))