from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb_soglasie = ReplyKeyboardBuilder()

kb_soglasie.row(types.KeyboardButton(text="Даю согласие"))