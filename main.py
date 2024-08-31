import asyncio
import logging
import os
import sys

from bot.bot import dp, bot
from database.models import async_main


async def main() -> None:
    if not os.path.exists('db'):
        os.mkdir('db')
    await async_main()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
