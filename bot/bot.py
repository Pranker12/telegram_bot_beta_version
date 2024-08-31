import os

from aiogram import Dispatcher, Bot, types, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode

from bot.keyboards import *
from config import TOKEN, USER
from database.requests import del_pers, write_to_sqlite2, update_tg_data, update_fio, \
    update_image, update_geoposition, update_soglasie, check_all_stack, return_data_katy, \
    get_image, get_image_name, delete_semi_info, redirect


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


class Form(StatesGroup):
    fio = State()
    photo = State()
    geolocation = State()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Приветствуем Вас. Спасибо что зашли в чат')
    await message.answer_sticker(
        sticker='CAACAgIAAxkBAAEC9zVlq7Y1WM55szHuqfxvcXb3d3Q6QQAC8kgAAulVBRgBMmSow_s7uzQE')
    await message.answer(
        'Давайте заполним анкету. \n\nЧтобы заполнить свои данные Вам необходимо нажимать на соответствующие клавиши вертуальной клавиатуры.'
        '\n\nЕсли после заполнения данных клавиатура не вернулась на место - Вы можете вызвать ее, '
        'нажав на <b>квадрат, рядом с символом записи голосовых сообщений</b>\n\n', reply_markup=kb_client.as_markup(resize_keyboard=True))
    tg_data = f'URL: {message.from_user.url}, Ссылка на пользователя: https://t.me/{message.from_user.username}'

    await del_pers(message.from_user.url)
    await write_to_sqlite2(message.from_user.url)
    await update_tg_data(message.from_user.url, tg_data)


@dp.message(F.text == 'Фамилия Имя Отчество')
async def fio(msg: types.Message, state: FSMContext) -> None:
    await bot.send_message(chat_id=msg.from_user.id, text='Укажите, пожалуйста, свое полное ФИО. ')
    await state.set_state(Form.fio)


@dp.message(Form.fio)  # Тут мы устанавливаем
async def fio_setter(msg: types.Message, state: FSMContext) -> None:
    await update_fio(msg.from_user.url, msg.text)
    await msg.answer(f'Приятно познакомиться. Можете переходить к следующему пункту заполнения анкеты. '
                     'Если хотите сменить свои данные – нажмите еще раз на эту кнопку.', reply_markup=kb_client.as_markup(resize_keyboard=True))
    await state.clear()


@dp.message(F.text == 'Фото рекламы')
async def image_handler(msg: types.Message) -> None:
    await bot.send_message(chat_id=msg.from_user.id,
                               text='Отправьте, пожалуйста <b><i>фотографию запрещенной рекламы</i></b>. Без загрузки фотографии Вы не сможете отправить нам анкету и функции бота будут заблокированы.', reply_markup=types.ReplyKeyboardRemove())
    await msg.answer(
            'Выберите с чего отправить фотографию.', reply_markup=kb_keyboard.as_markup(resize_keyboard=True))


@dp.message(F.text == 'Добавить с компьютера')
async def image_handler_comp(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(
            'Для того чтобы отправить нам фото, вы можете воспользоваться <i>«скрепкой»</i> (необходимо поставить галочку в пункте "Сжать изображение"). \n\nЛибо перенесите фото в раздел чата, в нижнюю половину с надписью «перетащите сюда фотографии для быстрой отправки»',
            reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.photo)


@dp.message(F.text == 'Добавить с телефона')
async def image_handler_phone(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(
        'Для того чтобы отправить нам фото с телефона,необходимо нажать на <i>«скрепку»</i> в правом нижнем углу и выбрать фотографию из галереи или сделать фото.',
        reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.photo)


@dp.message(Form.photo)
async def image_setter(msg: types.Message, state: FSMContext) -> None:
    if msg.photo:
        file_id = (msg.photo[-1].file_id)
        await update_image(msg.from_user.url, file_id)

        await msg.answer(
            '<b>Фото принято</b>. Можете переходить к следующему этапу. Если хотите сменить свои данные – нажмите еще раз на эту кнопку.',
            reply_markup=kb_client.as_markup(resize_keyboard=True))
        await state.clear()
    else:
        await msg.answer('Вы прислали не фото. Повторите, пожалуйста, попытку еще раз')


@dp.message(F.text == 'Вернуться назад')
async def mun_obr(msg: types.Message) -> None:
    await msg.answer('Возвращаемся к основной форме анкеты', reply_markup=kb_client.as_markup(resize_keyboard=True))


@dp.message(F.text == 'Геопозиция')
async def geoposition(msg: types.Message) -> None:
    await msg.answer(
        'В этом пункте Вам необходимо прислать <b><i>геопозицию места</i></b>, где расположена реклама запрещенных веществ.',
        reply_markup=types.ReplyKeyboardRemove())
    await msg.answer(
        ' Вы можете сделать это:\n - автоматически, с текущего места положения (только с телефона); \n - ввести самому с помощью встроенной функции геолокации; (только с телефона); \n - ввести самому адрес текстом (для пользователей с компьютера);',
        reply_markup=kb_location.as_markup(resize_keyboard=True))


@dp.message(F.location)
async def location_setter(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=f'<b>Данные приняты</b>. Ваша позиция: ',
                           reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(chat_id=message.from_user.id, text=f'Широта:{message.location.latitude}, '
                                                          f'Долгота: {message.location.longitude}', reply_markup=kb_client.as_markup(resize_keyboard=True))
    await update_geoposition(message.from_user.url, f'Широта:{message.location.latitude}, Долгота: {message.location.longitude}')


@dp.message(F.text == 'Ввести автоматически с текущего местоположения')
async def mun_obr(msg: types.Message) -> None:
    await msg.answer(
        'Возвращаемся к основной форме анкеты',
        reply_markup=kb_client.as_markup(resize_keyboard=True))


@dp.message(F.text == 'Ввести геолокацию функцией "Геолокация"')
async def mun_obr(msg: types.Message) -> None:
    await msg.answer(
        'Для того, чтобы прислать нам свою геолокацию необходимо нажать на <b>"скрепку"</b> в правом нижнем углу и вбрать вкладку "Геолокация, после чего отправить нам геолокацию выбранной фотографии')


@dp.message(F.text == 'Ввести адрес текстом')
async def mun_obr(msg: types.Message, state: FSMContext) -> None:
    await msg.answer('Напишите пожалуйста адрес, по которому размещена запрещенная реклама',
                     reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.geolocation)


@dp.message(Form.geolocation)
async def geolocation_setter(msg: types.Message, state: FSMContext) -> None:
    if msg.text:
        await update_geoposition(msg.from_user.url, msg.text.replace('\\','').replace(r'|','').replace(r'/','').replace(r':','').replace(r'*','').replace(r'?','').replace(r'"','').replace(r"'",'').replace(r'<','').replace(r'>',''))
        await msg.answer(
            'Ваш ответ <b>принят</b>, можете переходить к следующему этапу. Если хотите сменить свои данные – нажмите еще раз на эту кнопку.' , reply_markup=kb_client.as_markup(resize_keyboard=True))
        await state.clear()
    else:
        await msg.answer('Вы прислали не текст. Попробуйте еще раз')


@dp.message(F.text == 'Согласие на обработку персональных данных')
async def mun_obr(msg: types.Message) -> None:
    await msg.answer(
        '<b><i>Согласие</i></b> на осуществление Организатором любых законных действий в отношении полученных персональных данных, '
        'которые могут понадобиться для сбора, систематизации, хранения, уточнения (обновления, изменения), обработки, '
        'распространения и т.п. с учетом действующего законодательства Российской Федерации. ',
        reply_markup=types.ReplyKeyboardRemove())
    await msg.answer(
        'Согласие на обработку персональных данных дается без ограничения срока и может быть отозвано путем '
        'отправления заявления на официальную электронную почту.\nПредоставляя персональные данные, участник подтверждает, '
        'что ознакомлен с правами и обязанностями, предусмотренными Федеральным законом № 152-ФЗ от 27.07.2006 «О персональных данных». '
        '\n\nБез получения согласия Вы не сможете отправить нам анкету и функции бота будут заблокированы.',
        reply_markup=kb_soglasie.as_markup(resize_keyboard=True))


@dp.message(F.text == 'Даю согласие')
async def mun_obr(msg: types.Message) -> None:
    await update_soglasie(msg.from_user.url, 'Дано согласие' )
    await bot.send_message(chat_id=msg.from_user.id, text='Ваше согласие получено. Спасибо',reply_markup=kb_client.as_markup(resize_keyboard=True))


@dp.message(F.text == 'Отправить анкету')
async def mun_obr(msg: types.Message) -> None:
    try:
        if await check_all_stack(msg.from_user.url) == True:
            image_file_id = await get_image(msg.from_user.url)

            if not os.path.exists('static'):
                os.mkdir('static')

            image_name = await get_image_name(msg.from_user.url)
            await bot.download(
                image_file_id,
                destination=f"static/{image_name[:190]}.jpg"
            )
            await redirect(msg.from_user.url)
            await delete_semi_info(msg.from_user.url)
            await bot.send_photo(chat_id=USER, photo=image_file_id,
                                 caption=f'{await return_data_katy(msg.from_user.url)}')
            await msg.answer(
                '<b>Все данные зафиксированы</b>. \n\nБлагодарим за участие в конкурсе! Общими усилиями мы сделаем наш край лучше! ',
                reply_markup=kb_another_form.as_markup(resize_keyboard=True))
        else:
            await msg.answer('Форма еще не заполнена. Пока что мы не можем ее принять.'
                             '\n\nЕсли вы хотите стать участником конкурса - необходимо заполнить все поля.'
                             '\n\nЕсли вы хотите анонимно отправить информацию о нарушении, то необходимо заполнить поля (В данном случае вы не будете считаться участником Конкурса). '
                             '\n\nОтсмотреть статус заполненности своей анкеты можно при нажатии кнопки "Посмотреть анкету".')
    except:
        await msg.answer('Возникла ошибка: введите /start чтобы начать сначала')


@dp.message(F.text == 'Заполнить еще одну форму')
async def mun_obr(msg: types.Message) -> None:
    await msg.answer('Для того, чтобы заполнить форму еще раз - нажмите команду: /start')



@dp.message(F.text)
async def mun_obr(msg: types.Message) -> None:
    await msg.answer('Вы пока что просто отправили текст. '
                                                          'Чтобы направить нам свои данные воспользуйтесь встроенной '
                                                          'в бота клавиатурой')
