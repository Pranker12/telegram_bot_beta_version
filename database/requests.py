from sqlalchemy import select, delete, update, func

from database.models import UserInfo, UserPreInfo, async_session


async def get_all_data():
    async with async_session() as session:
       statement = select(UserInfo).where(UserInfo.fio != 'Не задано').where(UserInfo.approval == True)
       return (await session.execute(statement)).scalars().all()


async def get_user_data(user_id):
    async with async_session() as session:
       statement = select(UserInfo).where(UserInfo.user_id == f'tg://user?id={user_id}').where(UserInfo.fio != 'Не задано').where(UserInfo.approval == True)
       return (await session.execute(statement)).scalars().all()


async def get_user_data_by_id(user_id):
    async with async_session() as session:
        statement = select(UserInfo).where(UserInfo.user_id == f'tg://user?id={user_id}')
        return (await session.execute(statement)).scalars().first()


async def rework_user_name(name, id):
    async with async_session() as session:
        statement = update(UserInfo).where(UserInfo.user_id == f'tg://user?id={id}').values(fio = name)
        await session.execute(statement)
        await session.commit()



async def return_sqlite(user_id):
    async with async_session() as session:
        statement = select(UserPreInfo).where(UserPreInfo.user_id == user_id)
        user = (await session.execute(statement)).scalars().first()


    return f'<b>ФИО</b>: {user.fio} \n' \
                     f'<b>Фото</b>: {user.photo}\n'\
                     f'<b>Геопозиция/ адрес</b>: {user.geo_position}\n'\
                     f'<b>Согласие на обработку персональных данных</b>: {user.soglas}'


async def del_pers(user_id):
    async with async_session() as session:
        statement = delete(UserPreInfo).where(UserPreInfo.user_id == user_id)
        await session.execute(statement)
        await session.commit()


async def write_to_sqlite2(user_id):
    async with async_session() as session:
        user_info = UserPreInfo(user_id=user_id, fio='Не задано', photo='Не задано', geo_position='Не задано',soglas='Не задано',tg_data=user_id,photo_URL='Не задано')
        # user_info = UserPreInfo(user_id=user_id)
        session.add(user_info)
        await session.commit()


async def update_tg_data(user_id, tg_data):
    async with async_session() as session:
        statement = update(UserPreInfo).where(UserPreInfo.user_id == user_id).values(tg_data = tg_data)
        await session.execute(statement)
        await session.commit()


async def update_fio(user_id, fio):
    async with async_session() as session:
        statement = update(UserPreInfo).where(UserPreInfo.user_id == user_id).values(fio = fio)
        await session.execute(statement)
        await session.commit()


async def update_image(user_id, image):
    async with async_session() as session:
        statement = update(UserPreInfo).where(UserPreInfo.user_id == user_id).values(photo_URL = image).values(photo = 'Фото принято')
        await session.execute(statement)
        await session.commit()


async def update_geoposition(user_id, geo_position):
    async with async_session() as session:
        statement = update(UserPreInfo).where(UserPreInfo.user_id == user_id).values(geo_position = geo_position)
        await session.execute(statement)
        await session.commit()


async def update_soglasie(user_id, soglas):
    async with async_session() as session:
        statement = update(UserPreInfo).where(UserPreInfo.user_id == user_id).values(soglas = soglas)
        await session.execute(statement)
        await session.commit()


async def check_all_stack(user_id):
    async with async_session() as session:
        statement = select(UserPreInfo).where(UserPreInfo.user_id == user_id)
        user = (await session.execute(statement)).scalars().first()

        if user.fio != 'Не задано' and user.geo_position != 'Не задано' and user.photo != 'Не задано' and user.soglas != 'Не задано':
            return True
        else:
            return False


async def return_data_katy(user_id):
    async with async_session() as session:
        statement = select(UserInfo).where(UserInfo.user_id == user_id)
        user = (await session.execute(statement)).scalars().all()[-1]

        return f'Пришел новый пользователь:\n\n<b>ФИО</b>: {user.fio} \n' \
               f'<b>Геопозиция/ адрес</b>: {user.geo_position}\n' \
               f'<b>ID в базе</b>: {user.id}\n'


async def get_image(user_id):
    async with async_session() as session:
        statement = select(UserPreInfo).where(UserPreInfo.user_id == user_id)
        user = (await session.execute(statement)).scalars().first()
        return user.photo_URL


async def get_image_name(user_id):
    async with async_session() as session:
        statement = select(UserPreInfo).where(UserPreInfo.user_id == user_id)
        user = (await session.execute(statement)).scalars().first()
        return f'{user.fio}+{user.geo_position}'.replace('\\', '').replace(r'|', '').replace(r'/',
                                                                                                                  '').replace(
            r':', '').replace(r'*', '').replace(r'?', '').replace(r'"', '').replace(r"'", '').replace(r'<', '').replace(
            r'>', '').replace(r'.', '')


async def redirect(user_id):
    async with async_session() as session:
        statement = select(UserPreInfo).where(UserPreInfo.user_id == user_id)
        user = (await session.execute(statement)).scalars().first()

        user_info_3 = UserInfo(user_id= user.user_id,fio = user.fio,photo = user.photo ,geo_position = user.geo_position,soglas = user.soglas,tg_data = user.tg_data,photo_URL = user.photo_URL)
        session.add(user_info_3)
        await session.commit()


async def delete_semi_info(user_id):
    async with async_session() as session:
        statement = delete(UserPreInfo).where(UserPreInfo.user_id == user_id)
        await session.execute(statement)
        await session.commit()


async def count_data(user_id):
    async with async_session() as session:
        statement = select(UserInfo)
        return (await session.execute(statement)).scalars().all()


async def get_image_name_geoposition(user_name, geoposition):
    async with async_session() as session:
        statement = select(UserInfo).where(UserInfo.fio == user_name).where(UserInfo.geo_position==geoposition)
        user = (await session.execute(statement)).scalars().all()[-1]
        return f'{user.fio}+{user.geo_position}'.replace('\\', '').replace(r'|', '').replace(r'/',
                                                                                                                  '').replace(
            r':', '').replace(r'*', '').replace(r'?', '').replace(r'"', '').replace(r"'", '').replace(r'<', '').replace(
            r'>', '').replace(r'.', '')


async def approve_user(user_id, approve):
    async with async_session() as session:
        statement = update(UserInfo).where(UserInfo.id == user_id).values(approval=approve)
        await session.execute(statement)
        await session.commit()
