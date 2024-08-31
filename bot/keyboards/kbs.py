from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb_client = ReplyKeyboardBuilder()

kb_client.row(types.KeyboardButton(text="Фамилия Имя Отчество"))
kb_client.row(types.KeyboardButton(text="Геопозиция"), types.KeyboardButton(text="Фото рекламы"))
kb_client.row(types.KeyboardButton(text="Согласие на обработку персональных данных"))
kb_client.row(types.KeyboardButton(text="Отправить анкету"))





